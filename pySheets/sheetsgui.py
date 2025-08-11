import tkinter as tk
import re
from sheetscore import SheetCore
from utils import cell_address, toggle_reference

class SheetGUI:
    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        self.root = tk.Tk()
        self.root.title("pySheets")
        self.entries = []
        self.core = SheetCore(rows, cols)
        self.cell_formulas = [['' for _ in range(cols)] for _ in range(rows)]  # Store raw formulas
        self.cell_editing = [[False for _ in range(cols)] for _ in range(rows)] # Track editing state
        self.suggestion_box = None
        self.drag_origin = None
        self._build_grid()

    def _build_grid(self):
        # Column labels (A, B, C, ...)
        for c in range(self.cols):
            label = tk.Label(self.root, text=chr(c + 65), width=12, bg="#e0e0e0", relief="ridge")
            label.grid(row=0, column=c+1, sticky="nsew")

        # Row labels (1, 2, 3, ...)
        for r in range(self.rows):
            label = tk.Label(self.root, text=str(r + 1), width=4, bg="#e0e0e0", relief="ridge")
            label.grid(row=r+1, column=0, sticky="nsew")

        # Data entries
        for r in range(self.rows):
            row_entries = []
            for c in range(self.cols):
                entry = tk.Entry(self.root, width=12, justify="right")
                entry.grid(row=r+1, column=c+1, sticky="nsew", padx=1, pady=1)
                entry.bind("<FocusOut>", self.on_cell_focus_out(r, c))
                entry.bind("<FocusIn>", self.on_cell_focus_in(r, c))
                entry.bind("<F4>", self.on_f4)
                entry.bind("<Button-1>", self.start_drag)
                entry.bind("<ButtonRelease-1>", self.end_drag)
                entry.bind("<KeyRelease>", self.show_suggestions)
                row_entries.append(entry)
            self.entries.append(row_entries)

        for c in range(self.cols + 1):
            self.root.grid_columnconfigure(c, weight=1)
        for r in range(self.rows + 1):
            self.root.grid_rowconfigure(r, weight=1)

    def run(self):
        # Initial display: show evaluated values for all cells
        self.refresh_display()
        self.root.mainloop()

    def refresh_display(self):
        # For all cells, show evaluated value unless actively being edited
        for r in range(self.rows):
            for c in range(self.cols):
                entry = self.entries[r][c]
                if self.cell_editing[r][c]:
                    # Show formula while editing
                    entry.delete(0, tk.END)
                    entry.insert(0, self.cell_formulas[r][c])
                else:
                    formula = self.cell_formulas[r][c]
                    if formula.startswith("="):
                        result = self.core.evaluate_formula(formula[1:], r, c)
                        entry.delete(0, tk.END)
                        entry.insert(0, str(result))
                    else:
                        entry.delete(0, tk.END)
                        entry.insert(0, formula)

    def on_cell_focus_in(self, row, col):
        def handler(event):
            self.cell_editing[row][col] = True
            # Show the raw formula in the entry
            entry = self.entries[row][col]
            entry.delete(0, tk.END)
            entry.insert(0, self.cell_formulas[row][col])
        return handler

    def on_cell_focus_out(self, row, col):
        def handler(event):
            self.cell_editing[row][col] = False
            value = event.widget.get()
            self.cell_formulas[row][col] = value  # Always store the raw formula
            self.core.set_cell(row, col, value)   # Set in core for dependency
            # If formula, evaluate and show result
            if value.startswith("="):
                result = self.core.evaluate_formula(value[1:], row, col)
                event.widget.delete(0, tk.END)
                event.widget.insert(0, str(result))
            else:
                event.widget.delete(0, tk.END)
                event.widget.insert(0, value)
        return handler

    def on_f4(self, event):
        entry = event.widget
        text = entry.get()
        def toggle_ref(match):
            return toggle_reference(match.group(0))
        new_text = re.sub(r"(\$?[A-Z]\$?[0-9]+)", toggle_ref, text)
        entry.delete(0, tk.END)
        entry.insert(0, new_text)

    def start_drag(self, event):
        self.drag_origin = (event.widget, event.widget.grid_info()["row"], event.widget.grid_info()["column"])

    def end_drag(self, event):
        if not self.drag_origin:
            return
        origin_entry, origin_row, origin_col = self.drag_origin
        target = event.widget
        target_row = target.grid_info()["row"]
        target_col = target.grid_info()["column"]
        # Adjust for label row/col (grid row/col +1; so subtract 1)
        r_src = int(origin_row) - 1
        c_src = int(origin_col) - 1
        r_tgt = int(target_row) - 1
        c_tgt = int(target_col) - 1
        if 0 <= r_src < self.rows and 0 <= c_src < self.cols and 0 <= r_tgt < self.rows and 0 <= c_tgt < self.cols:
            formula = self.cell_formulas[r_src][c_src]
            self.cell_formulas[r_tgt][c_tgt] = formula
            self.core.set_cell(r_tgt, c_tgt, formula)
            self.refresh_display()
        self.drag_origin = None

    def show_suggestions(self, event):
        entry = event.widget
        text = entry.get()
        functions = ["IF", "AND", "OR", "NOT"]
        matches = [fn for fn in functions if fn.startswith(text.upper())]
        if self.suggestion_box:
            self.suggestion_box.destroy()
            self.suggestion_box = None
        if matches and text:
            self.suggestion_box = tk.Listbox(self.root, height=len(matches))
            for fn in matches:
                self.suggestion_box.insert(tk.END, fn)
            x = entry.winfo_rootx() - self.root.winfo_rootx()
            y = entry.winfo_rooty() - self.root.winfo_rooty() + entry.winfo_height()
            self.suggestion_box.place(x=x, y=y)
            self.suggestion_box.bind("<<ListboxSelect>>", lambda e: self.insert_suggestion(entry))
        else:
            if self.suggestion_box:
                self.suggestion_box.destroy()
                self.suggestion_box = None

    def insert_suggestion(self, entry):
        if self.suggestion_box:
            selection = self.suggestion_box.curselection()
            if selection:
                value = self.suggestion_box.get(selection[0])
                entry.delete(0, tk.END)
                entry.insert(0, value)
            self.suggestion_box.destroy()
            self.suggestion_box = None
