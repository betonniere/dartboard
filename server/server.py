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

import tornado.web       as web
import tornado.websocket as websocket
from tornado.httpserver import HTTPServer
from tornado.ioloop     import IOLoop

from serial_sniffer import SerialSniffer
from zeroconf       import ZeroconfService
from cricket        import Cricket

args     = None
game     = None
zeroconf = None
clients  = []

# --------------------------------------------
class WebSocketHandler (websocket.WebSocketHandler):
    def check_origin (self, origin):
        return True

    def open (self):
        clients.append (self)

    def on_message (self, message):
        json_msg = json.loads (message)
        if 'msg' in json_msg:
            if json_msg['msg'] == 'HIT':
                on_sniffer_data ('"number": ' + str (json_msg['number']) + ', "power": 1')
            elif json_msg['msg'] == 'READY':
                if game:
                    self.refresh (game.screenShot ())

    def on_close (self):
        clients.remove (self)

    def refresh (self, game_screenshot):
        if game:
            game_msg = '{"msg": "GAME",' + game_screenshot + '}'
            self.write_message (game_msg);


# --------------------------------------------
class IndexPageHandler (web.RequestHandler):
    def get (self):
        global game

        self.render ('../webapp/index.html')

        if game is None:
            game = Cricket ()

# --------------------------------------------
class Application (web.Application):
    def __init__ (self):
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

        web.Application.__init__ (self, handlers, **settings)

# --------------------------------------------
def on_sniffer_data (data):
    if args.verbose:
        print data

    if game:
        msg      = '{"msg": "HIT",' + data + '}'
        json_msg = json.loads (msg)

        for c in clients:
            c.write_message (msg)

        game.onHit (json_msg['number'], json_msg['power'])

        game_screenshot = game.screenShot ();
        for c in clients:
            c.refresh (game_screenshot)

# -------------------------------------------------
def parse_args ():
  global args

  parser = argparse.ArgumentParser (description='Dartboard web server')
  parser.add_argument ('-f', '--fake',    action='store_true', help='Generate fake events')
  parser.add_argument ('-v', '--verbose', action='store_true', help='Verbose')

  args = parser.parse_args ()

# --------------------------------------------
if __name__ == '__main__':
    parse_args ()

    app = Application ()

    server = HTTPServer (app)
    server.listen (8080)

    zeroconf = ZeroconfService (name="Dartboard", port=8080)
    zeroconf.publish ()

    main_loop = IOLoop.instance ()
    sniffer   = SerialSniffer (main_loop, on_sniffer_data, args.fake)

    try:
        sniffer.start ()
        main_loop.start ()
    except KeyboardInterrupt:
        pass

    sniffer.stop ()
    zeroconf.unpublish ()

    for c in clients:
        c.write_message ('{"msg": "GOODBYE"}')
