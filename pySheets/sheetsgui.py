import tkinter as tk
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
        self.suggestion_box = None
        self.drag_origin = None
        self._build_grid()

    def _build_grid(self):
        for r in range(self.rows):
            row_entries = []
            for c in range(self.cols):
                entry = tk.Entry(self.root, width=12, justify="right")
                entry.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
                entry.bind("<FocusOut>", self.on_cell_focus_out(r, c))
                entry.bind("<F4>", self.on_f4)
                entry.bind("<Button-1>", self.start_drag)
                entry.bind("<ButtonRelease-1>", self.end_drag)
                entry.bind("<KeyRelease>", self.show_suggestions)
                row_entries.append(entry)
            self.entries.append(row_entries)
        for c in range(self.cols):
            self.root.grid_columnconfigure(c, weight=1)
        for r in range(self.rows):
            self.root.grid_rowconfigure(r, weight=1)

    def run(self):
        self.root.mainloop()

    def on_cell_focus_out(self, row, col):
        def handler(event):
            value = event.widget.get()
            self.core.set_cell(row, col, value)
            # If formula, evaluate and show result
            if value and (any(fn in value.upper() for fn in ["IF", "AND", "OR", "NOT"]) or re.search(r"[A-Z][0-9]+", value)):
                result = self.core.evaluate_formula(value, row, col)
                event.widget.delete(0, tk.END)
                event.widget.insert(0, str(result))
        return handler

    def on_f4(self, event):
        entry = event.widget
        text = entry.get()
        import re
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
        formula = origin_entry.get()
        target.delete(0, tk.END)
        target.insert(0, formula)
        self.core.set_cell(int(target_row), int(target_col), formula)
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
