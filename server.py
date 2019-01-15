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

    apis = [ RegisterGetSaltApi('regsNaNO3'), Api()] 

    def do_GET(self):
        try:
            print(self.path)
            path = self.path.split('/')
            print(path)
            if(path[0]==''):
                path.pop(0)
            if(path[0] == 'api'):
                for api in RequestHandler.apis:
                    if(api.id(path[1].split('?')[0])):
                        print('api: '+api.name)
                        api.setPara(path[1].split('?')[1])
                        send = api.send()
                        if(send[0] == 200):
                            self.send_content(send[1],status=200, type=api.type)
                        else:
                            self.handle_error(send[1])
                        return
            else:
                if(path[0] == 'favicon.ico'):
                    print("send favicon.ico")
                    with open('./favicon.ico', 'rb') as f:
                        self.send_content(f.read(), 200, "image/x-icon")

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
