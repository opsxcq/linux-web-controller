import tornado.ioloop
import tornado.web
import subprocess

class df(tornado.web.RequestHandler):
    def get(self):
        print "Requested disk usage information"
        log=""
        p=subprocess.Popen("df -h".split(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        log+=p.stdout.read().strip()
        self.write(log)

class ifconfig(tornado.web.RequestHandler):
    def get(self):
        print "Ifconfig"
        log=""
        p=subprocess.Popen("ifconfig".split(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        log+=p.stdout.read().strip()
        self.write(log)

application = tornado.web.Application([
    (r"/df", df),
    (r"/ifconfig", ifconfig),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": ".","default_filename": "index.html"}),
])

if __name__ == "__main__":
    application.listen(8080,"0.0.0.0")
    tornado.ioloop.IOLoop.instance().start()
