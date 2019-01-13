#-*- coding:utf-8 -*-
from http import server
import sys,os
from windeaves_api import *

class RequestHandler( server.BaseHTTPRequestHandler ):

    DefaultPage = '''\
    <html>
    <body>
    Hello World!
    </body>
    </html>
    '''.encode('utf-8')

    ErrorPage = '''{"status" : "Error","code" : 404,"msg": "{msg}"}'''

    apis = [Api()] 

    def do_GET(self):
        try:
            print(self.path)
            path = self.path.split('/')
            print(path)
            if(path[0]==''):
                path.pop(0)
            if(path[0] == 'api'):
                print('api: '+path[1])
                for api in RequestHandler.apis:
                    if(api.id(path[1])):
                        api.setPara(path[2])
                        send = api.send()
                        if(send[0] == 200):
                            self.send_content(send[1])
                        else:
                            self.handle_error(send[1])
                        return
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
        content = self.ErrorPage.replace('{msg}', str(msg))
        self.send_content(content.encode('utf-8'),404)


if __name__ == '__main__':
    serverAddress = ('', 23333)
    WindeavesServer = server.HTTPServer(serverAddress, RequestHandler)
    WindeavesServer.serve_forever()
