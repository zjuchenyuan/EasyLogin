#coding:utf-8
"""
使用fangcloud.py提供的download函数提供网页服务
Example:
https://api.chenyuan.me/fangcloud/448eb45f0d08cbf37c33f35419
"""

import http.server as BaseHTTPServer
from fangcloud import download

def APIhello(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write("hello world!".encode('ascii'))

def API302(self,url):
        self.wfile.write(("HTTP/1.1 302 Found\r\nLocation: "+url+"\r\n\r\n").encode('ascii'))

def APIfail(self,e):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(("Error:"+str(e)).encode('ascii'))
        
class APIHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("/")
        if path[1]=="fangcloud":
            try:
                url = download(path[2])
                return API302(self,url)
            except Exception as e:
                return APIfail(self,e)
        else:
            return APIhello(self)


if __name__=="__main__":
    port=8080
    print("Running on port %d"%port)
    server_address = ('127.0.0.1', port)
    httpd = BaseHTTPServer.HTTPServer(server_address, APIHandler)
    httpd.serve_forever()