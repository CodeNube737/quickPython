#signal_engine.py
# Signal simulation and math evaluation

from components import VoltageSource, Resistor, LED

class SignalEngine:
    def __init__(self, circuit_grid):
        self.grid = circuit_grid
        self.time = 0.0
        self.dt = 0.01  # Time step
        self.signal_data = []

    def update(self):
        self.time += self.dt
        voltages = []

        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                component = self.grid.get_component(row, col)
                if component:
                    voltage = self.simulate_component(component)
                    voltages.append(voltage)

        self.signal_data.append((self.time, voltages))

    def simulate_component(self, component):
        if isinstance(component, VoltageSource):
            return component.simulate(self.time)
        elif isinstance(component, Resistor):
            voltage_in = self.get_adjacent_voltage(component)
            return component.simulate(self.time, voltage_in)
        elif isinstance(component, LED):
            voltage_in = self.get_adjacent_voltage(component)
            component.simulate(self.time, voltage_in)
            return voltage_in if component.lit else 0.0
        return 0.0

    def get_adjacent_voltage(self, component):
        row, col = component.row, component.col
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in neighbors:
            r, c = row + dr, col + dc
            if 0 <= r < self.grid.rows and 0 <= c < self.grid.cols:
                neighbor = self.grid.get_component(r, c)
                if isinstance(neighbor, VoltageSource):
                    return neighbor.simulate(self.time)
        return 0.0

    def get_latest_signals(self):
        return self.signal_data[-1] if self.signal_data else (0.0, [])
