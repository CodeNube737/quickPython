#main.py
# Entry point: initializes app and simulation loop
# a test, half-way through architecture setup to see if these modules can solve a simple circuit
# should return "V1 ≈ 0.4794 and V2 ≈ 0.3196"


from circuit_grid import CircuitGrid
from node_solver import NodeSolver
from signal_engine import SignalEngine
from components.voltage_source import VoltageSource
from components.resistor import Resistor
from components.ground import Ground
import math

# Initialize grid (3x3 for simplicity)
grid = CircuitGrid(rows=3, cols=6)

# Place components
#grid.place_component(0, 0, Ground())                    # Node 0: Ground ##NOT SUPPOSED TO BE PLACED HERE!
grid.place_component(0, 1, VoltageSource("sin(t)"))     # Node 1: Source
grid.place_component(0, 2, Resistor(1000))              # Node 2: R1
grid.place_component(0, 3, Resistor(2000))              # R2 to ground
grid.place_component(0, 4, Ground())          	     		# Ground

# Wire connections could be implicit by grid adjacency for now

# Run simulation
engine = SignalEngine(grid)
solver = NodeSolver(grid, engine)
t = 0.5
V = solver.solve(t)

print(f"Simulated Voltages at t = {t:.2f}:")
for i, v in enumerate(V):
    print(f"V[{i}] = {v:.4f}")


