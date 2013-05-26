import tornado.ioloop
import tornado.web
import gpio


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

		
application = tornado.web.Application([
	(r"/", MainHandler),
])

if __name__ == "__main__":
	pin38 = gpio.GPIO("gpmc_ad6",7,"out")
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
	