#base.py  
# Component base class

class Component:
    def __init__(self, name):
        self.name = name
        self.row = None
        self.col = None

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def simulate(self, t):
        # Override in subclasses
        return None

    def render(self, canvas, x, y, zoom):
        # Override in subclasses
        pass
