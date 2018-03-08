import time
import argparse

import tornado.web       as web
import tornado.websocket as websocket
from tornado.httpserver import HTTPServer
from tornado.ioloop     import IOLoop

from serial_sniffer import SerialSniffer

args    = None
clients = []

# --------------------------------------------
class WebSocketHandler (websocket.WebSocketHandler):
    def check_origin (self, origin):
        return True

    def open (self):
        clients.append (self)
        self.write_message ("HELLO")

    def on_message (self, message):
        print 'on_message'
        pass

    def on_close (self):
        clients.remove (self)

# --------------------------------------------
class IndexPageHandler (web.RequestHandler):
    def get (self):
        self.render (args.home_page)

# --------------------------------------------
class Application (web.Application):
    def __init__ (self):
        handlers = [(r'/',             IndexPageHandler),
                    (r'/scripts/(.*)', web.StaticFileHandler, {'path': "scripts"}),
                    (r'/(.*py)',       web.StaticFileHandler, {'path': "scripts"}),
                    (r'/(.*png)',      web.StaticFileHandler, {'path': "png"}),
                    (r'/(.*ogg)',      web.StaticFileHandler, {'path': "sounds"}),
                    (r'/js/(.*)',      web.StaticFileHandler, {'path': "js"}),
                    (r'/websocket',    WebSocketHandler)]
        settings = {'template_path': '',
                    'debug':         True}

        web.Application.__init__ (self, handlers, **settings)

# --------------------------------------------
def on_sniffer_data (data):
    for c in clients:
        print data
        c.write_message (data)

# -------------------------------------------------
def parse_args ():
  global args

  parser = argparse.ArgumentParser (description="Dartboard web server")
  parser.add_argument ('-f', '--fake',  action='store_true',                                         help='Generate fake events')
  parser.add_argument ('-i', '--index', action='store',      dest='home_page', default='index.html', help="Home page")

  args = parser.parse_args ()

# --------------------------------------------
if __name__ == '__main__':
    parse_args ()

    app = Application ()

    server = HTTPServer (app)
    server.listen (8080)

    main_loop = IOLoop.instance ()
    sniffer   = SerialSniffer (main_loop, on_sniffer_data, args.fake)

    try:
        sniffer.start ()
        main_loop.start ()
    except KeyboardInterrupt:
        pass

    sniffer.stop ()

    for c in clients:
        c.write_message ("GOODBYE")
