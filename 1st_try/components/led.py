#led.py

from components.base import Component
class LED(Component):
    def __init__(self, threshold=2.0):
        super().__init__('LED')
        self.threshold = threshold
        self.lit = False

    def simulate(self, t, voltage_in):
        self.lit = voltage_in >= self.threshold
        return self.lit

    def render(self, canvas, x, y, zoom):
        color = "red" if self.lit else "black"
        canvas.create_oval(x, y, x+zoom, y+zoom, fill=color)
