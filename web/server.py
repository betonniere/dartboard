import time
import tornado.web       as web
import tornado.websocket as websocket
from tornado.queues     import Queue
from tornado.httpserver import HTTPServer
from tornado.ioloop     import IOLoop
from tornado.ioloop     import PeriodicCallback

# --------------------------------------------
class WebSocketHandler (websocket.WebSocketHandler):
    def check_origin (self, origin):
        return True

    def open (self):
        self.sector   = 0
        self.power    = 0
        self.callback = PeriodicCallback (self.on_timeout, 1000)
        self.callback.start ()

    def on_message (self, message):
        self.write_message (u"Your message was: " + message)

    def on_close (self):
        self.callback.stop ()

    def on_timeout (self):
        self.write_message (str (self.sector + 1) + '.' + str (self.power + 1))
        self.sector += 1
        self.sector = self.sector%20
        self.power  += 1
        self.power  = self.power%3

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
if __name__ == '__main__':
    app = Application ()

    server = HTTPServer (app)
    server.listen (8080)

    IOLoop.instance().start ()
