#-*- coding:utf-8 -*-
from http import server
import sys,os

class RequestHandler( server.BaseHTTPRequestHandler ):

    DefaultPage = '''\
    <html>
    <body>
    Hello World!
    </body>
    </html>
    '''.encode('utf-8')

    ErrorPage = '''{"status" : "Error","code" : 404,"msg": "{msg}"}'''  

    def do_GET(self):
        try:
            print(self.path)
            self.send_content(RequestHandler.DefaultPage)

        except Exception as msg:
            self.handle_error(msg)

    def send_content(self,page,status=200,type="text/html"):
        self.send_response(status)
        self.send_header("Content-Type", type)
        self.send_header("Content-Length",str(len(page)))
        self.end_headers()
        self.wfile.write(page)


    def handle_error(self, msg):
        content = self.ErrorPage.replace('{msg}', msg)
        self.send_content(content.encode('utf-8'),404)


if __name__ == '__main__':
    serverAddress = ('', 23333)
    WindeavesServer = server.HTTPServer(serverAddress, RequestHandler)
    WindeavesServer.serve_forever()
