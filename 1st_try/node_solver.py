# node_solver.py

from components import Ground, VoltageSource, LED, Resistor
import numpy as np

class NodeSolver:
    def __init__(self, circuit_grid, signal_engine):
        self.grid = circuit_grid
        self.engine = signal_engine
        self.node_ids = {}
        self.ground_node_id = None
        self.next_node_id = 0

    def assign_nodes(self):
        self.node_ids.clear()
        self.next_node_id = 0
        print("📌 Node Mapping:\n--------------------------")
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                comp = self.grid.get_component(row, col)
                if comp:
                    pos = (row, col)
                    if isinstance(comp, Ground):
                        self.ground_node_id = self.next_node_id
                    self.node_ids[pos] = self.next_node_id
                    comp.node_id = self.next_node_id
                    print(f"Node {self.next_node_id} @ {pos} -> {type(comp).__name__}")
                    self.next_node_id += 1
        print("--------------------------\n")

    def assemble_system(self, t):
        if self.grid.get_ground_node() is None:
            raise RuntimeError("Simulation requires a ground reference.")

        self.assign_nodes()
        n = self.next_node_id
        G = np.zeros((n, n))
        I = np.zeros(n)

        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                comp = self.grid.get_component(row, col)
                if not comp:
                    continue
                node = comp.node_id

                if isinstance(comp, VoltageSource):
                    G[node, node] = 1.0
                    I[node] = comp.simulate(t)

                elif isinstance(comp, Resistor):
                    voltage_in = self.engine.get_adjacent_voltage(comp)
                    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    for dr, dc in neighbors:
                        r, c = row + dr, col + dc
                        if 0 <= r < self.grid.rows and 0 <= c < self.grid.cols:
                            nbr = self.grid.get_component(r, c)
                            if nbr and hasattr(nbr, "node_id"):
                                ni = node
                                nj = nbr.node_id
                                g = 1.0 / comp.resistance
                                G[ni, ni] += g
                                G[nj, nj] += g
                                G[ni, nj] -= g
                                G[nj, ni] -= g

                elif isinstance(comp, Ground):
                    G[node] = 0
                    G[node, node] = 1.0
                    I[node] = 0.0

        return G, I

    def solve(self, t):
        G, I = self.assemble_system(t)
        try:
            V = np.linalg.solve(G, I)
            return V
        except np.linalg.LinAlgError as e:
            print(f"Solver error: {e}")
            return np.zeros_like(I)
