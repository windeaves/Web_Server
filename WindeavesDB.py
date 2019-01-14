import json

class WindeavesDatabase():
    '''
    status code:
    200 Already Exist (create repeating)
    404 Not Found/ Not exist
    '''

    def __init__(self, name='default'):
        self.name = name
        self.root = {}

    def __count(self, dic):
        r = 0
        for x in dic:
            r += 1
        return r

    def _query(self, path):
        cur = self.root
        for x in path:
            if x not in cur.keys():
                return (False, 404)
            else:
                cur =  cur[x]
        return (True, cur)


    def _create(self, path, obj):
        pass
    
    def _modify(self, path, value):
        pass

    def _insert(self, path, obj, value):
        ret, r = self._create(path, obj)
        if not ret:
            pass
        pass

    def _read(self, path):
        with open(path) as f:
            self.root = json.load(f)
        print(self.root)