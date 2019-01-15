import json
from string import digits, ascii_letters
from random import sample

def trs_native(x):
    try:
        int(x)
        x = int(x)
        return x
    except ValueError:
        try:
            float(x)
            x = float(x)
            return x
        except ValueError:
            return x            

class Api():
    def __init__(self, name=""):
        self.name = name
        self.api = "application/json"

    def judgeId(self):
        raise NotImplementedError("JudgeId Not Implemented: No Name")

    def id(self, name):
        try:
            x = self.judgeId()
            return x
        except NotImplementedError:
            return (self.name == name)

    def setPara(self,path):
        if(path[0]=='?'):
            path = path[1:]
        #else:
        #    raise Exception("Wrong Para!")
        
        para = path.split('&')
        self.para = {}
        for pa in para:
            pa = pa.split('=')
            self.para[pa[0]] = trs_native(pa[1])
        
    def run(self):
        page = "<html><body><h1>Hello World!</h1><h1>test api para</h1>{content}</body></html>"
        return page.format(content=str(self.para))

    def send(self):
        return (200, self.run().encode('utf-8'))


class RegisterGetSaltApi(Api):

    template = {"status": "Normal", "code": 200, "content": {"salt" : None}}

    def __init__(self, name=''):
        super().__init__()
        self.type = "application/json"
    
    def judgeId(self, name):
        if(name == 'regsNaNO3'):
            return True
        else:
            return False

    def id(self, name):
        return self.judgeId(name)
    
    def run(self):
        if('tel' not in self.para.keys()):
            return (400, "para incorrect!")
        else:
            return (200, json.dumps({"status": "Normal", "code": 200, "content": {"salt" : self.generateSalt()}}))
    
    def setPara(self, path):
        return super().setPara(path)

    def send(self):
        code, content = self.run()
        content = content.encode()
        return (code, content)

    def generateSalt(self):
        salt = ''.join(sample(digits+ascii_letters, 16))
