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
    def init(self, name=""):
        self.name = name

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
        else:
            raise Exception("Wrong Para!")
        
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
    
    def judgeId(self, name):
        if(name == 'regsNaNO3'):
            return True
        else:
            return False
    
    def run(self):
        if('tel' not in self.para.keys()):
            return (400, "para incorrect!")
        else:
            return 

    def send(self):
        content = self.run()
        if(content[0] == 400):
            return content