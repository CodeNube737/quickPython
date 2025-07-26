#circuit_grid.py 
# CircuitGrid class and dirty flag system

from components.ground import Ground

class CircuitGrid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.zoom_level = 1.0
        self.offset_x = 0
        self.offset_y = 0

    def place_component(self, row, col, component):
        if isinstance(component, Ground):
            if self.get_ground_node() is not None:
                raise ValueError("Ground already placed.")
        component.set_position(row, col)
        self.grid[row][col] = component
        self.dirty = True

    def get_ground_node(self):
        for row in range(self.rows):
            for col in range(self.cols):
                component = self.get_component(row, col)
                if isinstance(component, Ground):
                    return (row, col)
        return None

    def get_connected_neighbors(self, row, col): # maybe obsolete because of SignalEngine.et_adjacent_voltage(self, component)!!
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols:  # <- Fix here
                if self.get_component(r, c):
                    neighbors.append((r, c))
        return neighbors



    def remove_component(self, row, col):
        self.grid[row][col] = None

    def get_component(self, row, col):
        return self.grid[row][col]

    def zoom(self, factor):
        self.zoom_level *= factor

    def pan(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy

    def grid_to_screen(self, row, col):
        x = col * self.zoom_level + self.offset_x
        y = row * self.zoom_level + self.offset_y
        return (x, y)

    def screen_to_grid(self, x, y):
        col = int((x - self.offset_x) / self.zoom_level)
        row = int((y - self.offset_y) / self.zoom_level)
        return (row, col)
