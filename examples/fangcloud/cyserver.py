import http.server as BaseHTTPServer

class CYServer():
    class APIHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        def _hello(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write("hello world!".encode('ascii'))

        def _302(self,url):
            self.wfile.write(("HTTP/1.1 302 Found\r\nLocation: "+url+"\r\n\r\n").encode('ascii'))

        def _404(self):
            self.wfile.write("Not Found")

        def _fail(self,e):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(("Error:"+str(e)).encode('ascii'))

    def __init__(self, port, do_GET, do_POST=None, do_HEAD=None, bind_address="0.0.0.0"):
        self.port=port
        self.do_GET=do_GET
        self.do_POST = do_POST
        self.do_HEAD = do_HEAD
        self.bind_address = bind_address

    def run(self):
        for i in ["GET","POST","HEAD"]:
            script = """
if callable(self.do_{}):
    self.APIHandler.do_{} = self.do_{}
else:
    self.APIHandler.do_{} = self.APIHandler._hello
""".format(i,i,i,i)
            exec(script,globals(),locals())
        print("Running on {}:{}".format(self.bind_address,self.port))
        httpd = BaseHTTPServer.HTTPServer((self.bind_address,self.port), self.APIHandler)
        httpd.serve_forever()