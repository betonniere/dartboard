#!/usr/bin/env python
# Copyright (C) Yannick Le Roux.
# This file is part of Dartboard.
# [...] (Mentions de licence conservées)

import argparse
import json
import logging
import subprocess

from rich.logging import RichHandler  # <--- À ajouter dans vos imports

import tornado.web as web
import tornado.websocket as websocket
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from serial_sniffer import SerialSniffer
from zeroconf import ZeroconfService
from cricket import Cricket

logger = logging.getLogger('dartboard.server')


# ----------------------------------
class WebSocketHandler(websocket.WebSocketHandler):
    # ----
    def check_origin(self, origin):
        return True

    # ----
    def open(self):
        self.application.clients.append(self)

    # ----
    def on_message(self, message):
        app = self.application
        try:
            message_data = json.loads(message)
        except json.JSONDecodeError:
            return

        logger.info(message_data)

        if 'name' in message_data:
            if message_data['name'] == 'HIT':
                app.on_sniffer_data(message_data)
            elif message_data['name'] == 'READY':
                if app.game is None:
                    app.game = Cricket()
                self.refresh(app.game.screenshot(), [self])
            elif app.game and app.game.on_message(message_data):
                self.refresh(app.game.screenshot(), app.clients)

    # ----
    def on_close(self):
        self.application.clients.remove(self)

    # ----
    def refresh(self, game_screenshot, sockets):
        if self.application.game:
            game_msg = json.dumps(
                {'name': 'GAME', 'data': json.loads(game_screenshot)}
            )
            for s in sockets:
                s.write_message(game_msg)


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
    def on_idle(self):
        message = json.dumps({'name': 'IDLE'})
        for c in self.clients:
            c.write_message(message)

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
                for c in self.clients:
                    c.write_message(json.dumps(message))
                self.game.on_hit(
                    message['data']['number'], message['data']['power']
                )
            elif 'function' in data:
                self.game.on_function(data['function'])

            game_screenshot = self.game.screenshot()
            for c in self.clients:
                c.refresh(game_screenshot, self.clients)

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


# --------------------------------------------
def log_active_connections():
    cmd = ['nmcli', '-g', 'NAME', 'connection', 'show', '--active']
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        active_connections = result.stdout.strip().split()
        if active_connections:
            logger.info(f'Active connections: {active_connections[0]}')


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

    zeroconf = ZeroconfService(name='Dartboard', port=8080)
    zeroconf.publish()

    log_active_connections()

    main_loop = IOLoop.current()
    device = 'ttyACM0' if args.usb else 'ttyS0'
    sniffer = SerialSniffer(app.on_sniffer_data, main_loop, device)

    try:
        sniffer.start()
        main_loop.start()
    except KeyboardInterrupt:
        pass
    finally:
        sniffer.stop()
        zeroconf.unpublish()
        goodbye_msg = json.dumps({'name': 'GOODBYE'})
        for c in app.clients:
            c.write_message(goodbye_msg)


# --------------------------------------------
if __name__ == '__main__':
    main()
