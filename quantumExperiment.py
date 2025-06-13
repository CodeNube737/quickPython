# quantumExperiment.py
# p9/68ieee80866_06_S

import numpy as np
import matplotlib.pyplot as plt
import random

class QuantumState:
    """Represents a quantum state with superposition and measurement visualization."""
    
    def __init__(self, state_0, state_1):
        self.state_0 = state_0
        self.state_1 = state_1
        self.coefficients = self.normalize([state_0, state_1])
    
    def normalize(self, states):
        """Ensures the quantum state is properly normalized."""
        norm = np.sqrt(sum(np.abs(s)**2 for s in states))
        return [s / norm for s in states]
    
    def measure(self):
        """Simulates quantum measurement, collapsing the state."""
        probabilities = [np.abs(c)**2 for c in self.coefficients]
        outcome = random.choices([0, 1], probabilities)[0]
        self.coefficients = [1 if outcome == i else 0 for i in range(2)]
        return outcome
    
    def visualize(self):
        """Displays the quantum state as a probability distribution."""
        probabilities = [np.abs(c)**2 for c in self.coefficients]
        labels = ['|0⟩', '|1⟩']
        
        plt.bar(labels, probabilities, color=['blue', 'red'])
        plt.ylabel('Probability')
        plt.title('Quantum State Probability Distribution')
        plt.show()

# Quantum Experimentation
def quantum_experiment():
    """Runs an interactive quantum experiment."""
    print("Initializing quantum state |ψ⟩ = α|0⟩ + β|1⟩")
    state = QuantumState(complex(1, 1), complex(1, -1))  # Example superposition
    
    print("Visualizing initial quantum state...")
    state.visualize()
    
    input("Press Enter to measure the quantum state...")
    result = state.measure()
    
    print(f"Measurement result: |{result}⟩")
    print("Visualizing collapsed state...")
    state.visualize()

# Run the quantum experiment
quantum_experiment()
