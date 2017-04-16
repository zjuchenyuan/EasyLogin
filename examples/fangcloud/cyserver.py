import http.server as BaseHTTPServer

class CYServer():
    class APIHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        def _hello(self):
            self.server_write_html("hello world!")

        def _302(self,url):
            self.wfile.write(("HTTP/1.1 302 Found\r\nLocation: "+url+"\r\n\r\n").encode('ascii'))

        def _fail(self,e):
            self.server_write_html("Error: "+str(e),content_type="text/plain")

        def server_write_html(self,html,content_type="text/html"):
            data=bytes(str(html),encoding="utf-8")
            self.server_write_bytes(data,content_type=content_type)

        def server_write_bytes(self,data,content_type="image/gif"):
            content=bytes("HTTP/1.0 200 OK\r\nContent-Type: {type}; charset=utf-8\r\nContent-Length: {size}\r\nServer: CYServer\r\n\r\n".format(type=content_type,size=len(data)),encoding="utf-8")+data
            self.wfile.write(content)
    
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