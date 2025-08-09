import re
from functions import IF, AND, OR, NOT

class SheetCore:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = [['' for _ in range(cols)] for _ in range(rows)]

    def set_cell(self, row, col, value):
        self.cells[row][col] = value

    def get_cell(self, row, col):
        return self.cells[row][col]

    def evaluate_formula(self, formula, cur_row=None, cur_col=None):
        # Replace absolute references
        formula = formula.replace('$', '')
        # Replace cell references with their values
        def cell_ref(match):
            ref = match.group(0)
            col = ord(ref[0].upper()) - 65
            row = int(ref[1:]) - 1
            if 0 <= row < self.rows and 0 <= col < self.cols:
                val = self.get_cell(row, col)
                try:
                    return str(float(val))
                except ValueError:
                    return str(val)
            return "0"
        formula = re.sub(r"[A-Z][0-9]+", cell_ref, formula)
        try:
            # Only allow our functions, no builtins
            result = eval(formula, {"__builtins__": None}, {"IF": IF, "AND": AND, "OR": OR, "NOT": NOT})
        except Exception as e:
            return f"#ERR"
        return result