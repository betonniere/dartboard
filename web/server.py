import time
import tornado.web       as web
import tornado.websocket as websocket
from tornado.httpserver import HTTPServer
from tornado.ioloop     import IOLoop
from tornado.ioloop     import PeriodicCallback


from serial_sniffer import SerialSniffer

clients = []

# --------------------------------------------
class WebSocketHandler (websocket.WebSocketHandler):
    def check_origin (self, origin):
        return True

    def open (self):
        clients.append (self)

    def on_message (self, message):
        print 'on_message'
        pass

    def on_close (self):
        clients.remove (self)

# --------------------------------------------
class IndexPageHandler (web.RequestHandler):
    def get (self):
        self.render ("index.html")

# --------------------------------------------
class Application (web.Application):
    def __init__ (self):
        handlers = [(r'/',           IndexPageHandler),
                    (r'/js/(.*)',    web.StaticFileHandler, {'path': "js"}),
                    (r'/websocket',  WebSocketHandler)]
        settings = {'template_path': '',
                    'debug':         True}

        web.Application.__init__ (self, handlers, **settings)

# --------------------------------------------
def on_sniffer_data (data):
    for c in clients:
        c.write_message (data)

# --------------------------------------------
if __name__ == '__main__':
    app = Application ()

    server = HTTPServer (app)
    server.listen (8080)

    main_loop = IOLoop.instance ()
    sniffer   = SerialSniffer (main_loop, on_sniffer_data)

    try:
        sniffer.start ()
        main_loop.start ()
    except KeyboardInterrupt:
        pass

    sniffer.stop ()
