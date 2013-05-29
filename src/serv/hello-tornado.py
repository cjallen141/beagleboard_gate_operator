import tornado.ioloop
import tornado.web
import gpio


pin38 = gpio.GPIO("gpmc_ad6",7,"out")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
        pin38.writeVal()

		
application = tornado.web.Application([
	(r"/", MainHandler),
])

if __name__ == "__main__":
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()