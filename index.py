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

class dockerps(tornado.web.RequestHandler):
    def get(self):
        print "Requested docker ps"
        log=""
        p=subprocess.Popen("docker ps -a".split(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        log+=p.stdout.read().strip()
        self.write(log)

class ifconfig(tornado.web.RequestHandler):
    def get(self):
        print "Requested Ifconfig"
        log=""
        p=subprocess.Popen("ifconfig".split(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        log+=p.stdout.read().strip()
        self.write(log)

class networktest(tornado.web.RequestHandler):
    def get(self):
        print "Requested network test"
        log=""
        #p=subprocess.Popen("ifconfig".split(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #log+=p.stdout.read().strip()
        p=subprocess.Popen(["bash","-c","echo default gateway $(route -n | grep -E \"^0.0.0.0\" | awk '{ print $2}')"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        log+=p.stdout.read().strip()+'\n'

        p=subprocess.Popen(["bash","-c","echo Ping default gateway;ping -c 4 $(route -n | grep -E \"^0.0.0.0\" | awk '{ print $2}')"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        log+=p.stdout.read().strip()+'\n'

        p=subprocess.Popen(["bash","-c","echo Pinging google DNS server;ping -c 4 8.8.8.8"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        log+=p.stdout.read().strip()+'\n'

        p=subprocess.Popen(["bash","-c","echo Testing DNS resolution;nslookup github.com"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        log+=p.stdout.read().strip()

        self.write(log)

application = tornado.web.Application([
    (r"/df", df),
    (r"/ifconfig", ifconfig),
    (r"/dockerps", dockerps),
    (r"/networktest", networktest),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": ".","default_filename": "index.html"}),
])

if __name__ == "__main__":
    application.listen(8080,"0.0.0.0")
    tornado.ioloop.IOLoop.instance().start()
