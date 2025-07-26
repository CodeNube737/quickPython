#ground.py

from components.base import Component
class Ground(Component):
    def __init__(self):
        super().__init__('Ground')
        self.is_reference = True  # Flag for engine to recognize this as 0V

    def simulate(self, t):
        return 0.0  # Ground is always 0 volts

    def render(self, canvas, x, y, zoom):
        canvas.create_rectangle(x, y, x+zoom, y+zoom, outline="black", width=2)
        canvas.create_text(x+zoom/2, y+zoom/2, text="GND", fill="black")
