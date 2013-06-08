import tornado.ioloop
import tornado.web
import tornado.template
import gpio


pin38 = gpio.OutputGPIO("gpmc_ad6")

class MainHandler(tornado.web.RequestHandler):
    t = tornado.template.Loader("html")
    def get(self):

        #load the template file
        
        self.write( self.t.load("template.html").generate() )
        #self.write("Hello, world")
        #pin38.writeVal()


    def post(self):
        pin38.writeVal()
        self.write(self.t.load("template.html").generate())
		
application = tornado.web.Application([
	(r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(80)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt: #catch when stop the webserver
        # I need to clean up all the gpio that are used
        gpio.GPIO.close_all()
