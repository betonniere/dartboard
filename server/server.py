#!/usr/bin/env python
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
import rich
import subprocess

import tornado.web as web
import tornado.websocket as websocket
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from serial_sniffer import SerialSniffer
from zeroconf import ZeroconfService
from cricket import Cricket

args     = None
game     = None
zeroconf = None
idle     = None
clients  = []


# ----------------------------------
class WebSocketHandler(websocket.WebSocketHandler):
    # ----
    def check_origin(self, origin):
        return True

    # ----
    def open(self):
        clients.append(self)

    # ----
    def on_message(self, message):
        global game

        message = json.loads(message)
        if args.verbose:
            rich.print(message)

        if 'name' in message:
            if message['name'] == 'HIT':
                on_sniffer_data(message)
            elif message['name'] == 'READY':
                if game is None:
                    game = Cricket()
                self.refresh(game.screenshot(), [self])
            elif game and game.on_message(message):
                self.refresh(game.screenshot(), clients)

    # ----
    def on_close(self):
        clients.remove(self)

    # ----
    def refresh(self, game_screenshot, sockets):
        if game:
            game_msg = '{"name": "GAME", "data": ' + game_screenshot + '}'
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
    def __init__(self):
        handlers = [(r'/',          IndexPageHandler),
                    (r'/(.*css)',   web.StaticFileHandler, {'path': '../webapp/css'}),
                    (r'/(.*png)',   web.StaticFileHandler, {'path': '../webapp/images'}),
                    (r'/(.*jpg)',   web.StaticFileHandler, {'path': '../webapp/images'}),
                    (r'/(.*svg)',   web.StaticFileHandler, {'path': '../webapp/images'}),
                    (r'/(.*ogg)',   web.StaticFileHandler, {'path': '../webapp/sounds'}),
                    (r'/(.*js)',    web.StaticFileHandler, {'path': '../webapp/js'}),
                    (r'/websocket', WebSocketHandler)]
        settings = {'template_path': '',
                    'debug':         True}

        web.Application.__init__(self, handlers, **settings)


# --------------------------------------------
def on_idle():
    message = {'name': 'IDLE'}
    for c in clients:
        c.write_message(message)


# --------------------------------------------
def on_sniffer_data(data, spawner=None):
    global idle

    if spawner:
        spawner.spawn_callback(on_sniffer_data, data, None)
        return

    if args.verbose:
        rich.print(data)

    if game:
        if idle:
            IOLoop.current().remove_timeout(idle)
            idle = None

        message = {'name': 'HIT', 'data': data}

        for c in clients:
            c.write_message(json.dumps(message))

        game.on_hit(message['data']['number'], message['data']['power'])
        idle = IOLoop.current().call_later(delay=3, callback=on_idle)

        game_screenshot = game.screenshot()
        for c in clients:
            c.refresh(game_screenshot, clients)


# -------------------------------------------------
def parse_args():
    global args

    parser = argparse.ArgumentParser(description='Dartboard web server')
    parser.add_argument('-f', '--fake',    action='store_true', help='Generate fake events')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')

    args = parser.parse_args()


# -------------------------------------------------
def fetch_upgrade():
    result = subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True)
    if result.stdout and result.stdout.startswith('https://'):
        result = subprocess.run(['git', 'pull'], capture_output=True, text=True)
        if args.verbose:
            rich.print(result.stdout)
            rich.print(result.stderr)


# --------------------------------------------
if __name__ == '__main__':
    parse_args()

    fetch_upgrade()

    app = Application()

    server = HTTPServer(app)
    server.listen(8080)

    zeroconf = ZeroconfService(name="Dartboard", port=8080)
    zeroconf.publish()

    main_loop = IOLoop.instance()
    sniffer   = SerialSniffer(on_sniffer_data, main_loop, args.fake)

    try:
        sniffer.start()
        main_loop.start()
    except KeyboardInterrupt:
        pass

    sniffer.stop()
    zeroconf.unpublish()

    for c in clients:
        c.write_message('{"name": "GOODBYE"}')
