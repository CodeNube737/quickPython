#resistor.py

from components.base import Component
class Resistor(Component):
    def __init__(self, resistance=1000):
        super().__init__('Resistor')
        self.resistance = resistance

    def simulate(self, t, voltage_in):
        return voltage_in / self.resistance  # Ohm's law (simplified)

    def render(self, canvas, x, y, zoom):
        canvas.create_rectangle(x, y, x+zoom, y+zoom, outline="brown", width=2)
