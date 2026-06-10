# Copyright (C) Yannick Le Roux.
# This file is part of Dartboard.
#
#   Dartboard is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Dartboard is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Dartboard.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import json
import logging
import subprocess

from rich.logging import RichHandler

import tornado
import tornado.web as web
import tornado.process
import tornado.websocket as websocket
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from network_status import NetworkStatus
from serial_sniffer import SerialSniffer
from cricket import Cricket

logger = logging.getLogger('dartboard.server')


# ----------------------------------
class WebSocketHandler(websocket.WebSocketHandler):
    # ----
    def check_origin(self, origin):
        return True

    # ----
    def open(self):
        self.application.on_client(self)

    # ----
    async def on_message(self, message):
        app = self.application
        try:
            message_data = json.loads(message)
        except json.JSONDecodeError:
            return

        logger.info(message_data)

        name = message_data.get('name', None)
        data = message_data.get('data', None)
        if name:
            if name == 'HIT':
                app.on_sniffer_data(message_data)
            elif name == 'READY':
                if app.game is None:
                    app.game = Cricket()
                self.refresh()
            elif name == 'SET_WIFI' and data:
                ssid = data.get('ssid', None)
                password = data.get('password', None)

                if not ssid or not password:
                    return

                cmd = [
                    'sudo',
                    'nmcli',
                    'con',
                    'modify',
                    'WifiClient',
                    '802-11-wireless.ssid',
                    ssid,
                    '802-11-wireless-security.psk',
                    password,
                ]
                proc = tornado.process.Subprocess(cmd)
                await proc.wait_for_exit()

                cmd = ['sudo', 'nmcli', 'con', 'up', 'WifiClient']
                proc = tornado.process.Subprocess(cmd)
                await proc.wait_for_exit()
            elif app.game and app.game.on_message(message_data):
                for client in app.clients:
                    client.refresh()

    # ----
    def on_close(self):
        self.application.clients.remove(self)

    # ----
    def refresh(self):
        if self.application.game:
            game_msg = json.dumps(
                {
                    'name': 'GAME',
                    'data': json.loads(self.application.game.screenshot()),
                }
            )
            self.write_message(game_msg)


# ----------------------------------
class IndexPageHandler(web.RequestHandler):
    # ----
    def get(self):
        self.render('../webapp/index.html')


# ----------------------------------
class Application(web.Application):
    # ----
    def __init__(self, args):
        self.args = args
        self.game = None
        self.idle = None
        self.network_status = None
        self.clients = []

        handlers = [
            (r'/', IndexPageHandler),
            (r'/(.*css)', web.StaticFileHandler, {'path': '../webapp/css'}),
            (r'/(.*png)', web.StaticFileHandler, {'path': '../webapp/images'}),
            (r'/(.*jpg)', web.StaticFileHandler, {'path': '../webapp/images'}),
            (r'/(.*svg)', web.StaticFileHandler, {'path': '../webapp/images'}),
            (r'/(.*ogg)', web.StaticFileHandler, {'path': '../webapp/sounds'}),
            (r'/(.*js)', web.StaticFileHandler, {'path': '../webapp/js'}),
            (r'/websocket', WebSocketHandler),
        ]
        settings = {'template_path': '', 'debug': True}
        super().__init__(handlers, **settings)

    # ----
    def on_client(self, client):
        self.clients.append(client)

        if self.network_status:
            self.send_network_status(client)

    # ----
    def on_idle(self):
        message = json.dumps({'name': 'IDLE'})
        for client in self.clients:
            client.write_message(message)

    # ----
    def send_network_status(self, client):
        message = json.dumps(
            {
                'name': 'NETWORK_STATUS',
                'data': {'connection': self.network_status},
            }
        )

        client.write_message(message)

    # ----
    def on_network_status(self, status, spawner=None):
        if spawner:
            spawner.spawn_callback(self.on_network_status, status, None)
            return

        if status != self.network_status:
            logger.info(f'Active connections: {status}')

            self.network_status = status
            for client in self.clients:
                self.send_network_status(client)

    # ----
    def on_sniffer_data(self, data, spawner=None):
        if spawner:
            spawner.spawn_callback(self.on_sniffer_data, data, None)
            return

        logger.info(data)

        if self.game:
            if self.idle:
                IOLoop.current().remove_timeout(self.idle)
                self.idle = None

            if 'number' in data:
                message = {'name': 'HIT', 'data': data}
                for client in self.clients:
                    client.write_message(json.dumps(message))
                self.game.on_hit(
                    message['data']['number'], message['data']['power']
                )
            elif 'function' in data:
                self.game.on_function(data['function'])

            for client in self.clients:
                client.refresh()

            self.idle = IOLoop.current().call_later(
                delay=3, callback=self.on_idle
            )


# -------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(description='Dartboard web server')
    parser.add_argument(
        '-u',
        '--usb',
        action='store_true',
        help='Read the hits from USB connector.',
    )
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')
    return parser.parse_args()


# -------------------------------------------------
def fetch_upgrade():
    result = subprocess.run(
        ['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True
    )
    if result.stdout and result.stdout.startswith('https://'):
        result = subprocess.run(['git', 'pull'], capture_output=True, text=True)

        logger.info(result.stdout)
        logger.info(result.stderr)


# -------------------------------------------------
def main():
    args = parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(message)s',
        datefmt='[%X]',
        handlers=[RichHandler(rich_tracebacks=True, show_time=False)],
    )

    logger.info('Démarrage du serveur Dartboard sur le port 8080...')

    fetch_upgrade()

    app = Application(args)
    server = HTTPServer(app)
    server.listen(8080)

    main_loop = IOLoop.current()

    device = 'ttyACM0' if args.usb else 'ttyS0'
    sniffer = SerialSniffer(app.on_sniffer_data, main_loop, device)

    networkStatus = NetworkStatus(app.on_network_status, main_loop)

    try:
        sniffer.start()
        networkStatus.start()

        main_loop.start()
    except KeyboardInterrupt:
        pass
    finally:
        sniffer.stop()
        networkStatus.stop()

        goodbye_msg = json.dumps({'name': 'GOODBYE'})
        for client in app.clients:
            client.write_message(goodbye_msg)


# --------------------------------------------
if __name__ == '__main__':
    main()
