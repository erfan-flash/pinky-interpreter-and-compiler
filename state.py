class Environment:
    def __init__(self , parent = None):
        self.values = {}
        self.parent = parent
    def set_variable(self , name, value):
        self.values.update({name : value})
    def get_variable(self, name):
        if name in self.values:
            return self.values[name]
        if self.parent is not None:
            return self.parent.get_variable(name)
        return None
    def new_environment(self ):
        return Environment(parent = self)