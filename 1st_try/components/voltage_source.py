#voltage_source.py

import numexpr as ne
from components.base import Component

class VoltageSource(Component):
    def __init__(self, equation_str):
        super().__init__('VoltageSource')
        self.equation_str = equation_str

    def simulate(self, t):
        try:
            result = ne.evaluate(self.equation_str, local_dict={"t": t})
            return float(result)
        except Exception as e:
            print(f"Simulation error in VoltageSource: {e}")
            return 0.0

    def render(self, canvas, x, y, zoom):
        # Example using tkinter-style canvas
        canvas.create_oval(x, y, x+zoom, y+zoom, outline="blue", width=2)
        canvas.create_text(x+zoom/2, y+zoom/2, text="V", fill="blue")

    def is_safe_equation(eq):
        safe_chars = set("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+-*/(). _")
        return all(char in safe_chars for char in eq)
