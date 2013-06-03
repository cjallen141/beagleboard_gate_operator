import tornado.ioloop
import tornado.web
import gpio


pin38 = gpio.OutputGPIO("gpmc_ad6")

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