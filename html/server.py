import os
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop

# --------------------------------------------
class WebSocketHandler (tornado.websocket.WebSocketHandler):
    def check_origin (self, origin):
        return True

    def open (self):
        self.write_message (u"13")
        pass

    def on_message (self, message):
        self.write_message (u"Your message was: " + message)

    def on_close (self):
        pass

# --------------------------------------------
class IndexPageHandler (tornado.web.RequestHandler):
    def get (self):
        self.render ("index.html")

# --------------------------------------------
class Application (tornado.web.Application):
    def __init__ (self):
        handlers = [(r'/',           IndexPageHandler),
                    (r'/js/(.*)',    tornado.web.StaticFileHandler, {'path': "js"}),
                    (r'/websocket',  WebSocketHandler)]
        settings = {'template_path': '',
                    'debug':         True}

        tornado.web.Application.__init__ (self, handlers, **settings)

# --------------------------------------------
if __name__ == '__main__':
    app = Application ()

    server = tornado.httpserver.HTTPServer (app)
    server.listen (8080)

    tornado.ioloop.IOLoop.instance ().start ()
