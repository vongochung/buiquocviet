import pickle
class MultiCookie():
    def __init__(self,cookie=None,values=None):
        if cookie != None:
            try:
                self.values = pickle.loads(cookie)
            except:
                # assume that it used to just hold a string value
                self.values = cookie
        elif values != None:
            self.values = values
        else:
            self.values = None

    def __str__(self):
        return pickle.dumps(self.values)