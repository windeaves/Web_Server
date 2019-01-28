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
            return (200, json.dumps({"status": "Normal", "code": 200, "content": {"salt" : self.generateSalt(), "tel": self.para["tel"]}}))
    
    def setPara(self, path):
        super().setPara(path)
        if "tel" in self.para.keys():
            self.para["tel"] = str(self.para["tel"])

    def send(self):
        code, content = self.run()
        content = content.encode()
        return (code, content)

    def generateSalt(self):
        salt = ''.join(sample(digits+ascii_letters, 16))
        with open('./data/registerSalt.json', "r+") as f:
            ary = json.load(f)
            flag = True
        with open('./data/registerSalt.json','w+') as f:
            for x in ary:
                if(x["tel"] == self.para["tel"]):
                    x["salt"] = salt
                    flag = False
                    break
            if(flag):
                ary.append({"tel":self.para["tel"], "salt": salt})
            json.dump(ary,f)
            return salt
            
class Register(Api):
    # tel, mail, 
    template = {"status": "Normal", "code": 200, "content": None}

    def __init__(self, name='regs'):
        super().__init__(name=name)
        self.type = "application/json"

    def run(self):
        with open('./data/userInfo.json','r+') as f:
            ary = json.load(f)
            ary.append(self.para)
        with open('./data/userInfo.json','w+') as f:
            json.dump(ary,f)
        b = Register.template
        b["content"] = {"tel":self.para["tel"]}
        return (200, str(b))


    def setPara(self, path):
        super().setPara(path)
        if "tel" in self.para.keys():
            self.para["tel"] = str(self.para["tel"])
        
    def send(self):
        code, content = self.run()
        content = content.encode()
        return (code, content)