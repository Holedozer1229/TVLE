import numpy as np
from scipy.integrate import solve_ivp
from src.config import CONFIG, hbar, m_n, INV_LAMBDA_SQ, TEMPORAL_CONSTANT

class QuantumState:
    """Handles the quantum state and its evolution in the 6D grid."""

    def __init__(self, grid_size, logger):
        self.grid_size = grid_size
        self.total_points = np.prod(grid_size)
        self.logger = logger
        # Initialize quantum state with random phases
        phases = np.random.uniform(0, 2 * np.pi, self.total_points)
        self.state = np.exp(1j * phases) / np.sqrt(self.total_points)
        self.temporal_entanglement = np.zeros(self.total_points, dtype=np.complex128)
        self.state_history = []

    def evolve(self, dt, rtol, atol, hamiltonian):
        """
        Evolve the quantum state using the Schrödinger equation.

        Args:
            dt (float): Time step
            rtol (float): Relative tolerance for ODE solver
            atol (float): Absolute tolerance for ODE solver
            hamiltonian (callable): Hamiltonian function for evolution
        """
        state_flat = self.state.copy()
        # Debug: Confirm CONFIG["entanglement_factor"]
        self.logger.debug(f"CONFIG['entanglement_factor'] = {CONFIG['entanglement_factor']}")
        sol = solve_ivp(
            hamiltonian,
            [0, dt],
            state_flat,
            method='RK45',
            rtol=rtol,
            atol=atol
        )
        if not sol.success:
            self.logger.error("Quantum state evolution failed")
            raise RuntimeError("ODE solver failed")
        self.state = sol.y[:, -1]
        norm = np.linalg.norm(self.state)
        if norm > 0:
            self.state /= norm
        else:
            self.logger.warning("Quantum state norm is zero; resetting")
            phases = np.random.uniform(0, 2 * np.pi, self.total_points)
            self.state = np.exp(1j * phases) / np.sqrt(self.total_points)
        self.state_history.append(self.state.copy())
        # Keep only the last state for CTC feedback
        if len(self.state_history) > 1:
            self.state_history = self.state_history[-1:]
        self.temporal_entanglement = self.state.conj() * CONFIG["entanglement_factor"]

    def get_magnitude(self):
        """Return the magnitude of the quantum state."""
        return np.abs(self.state)

    def get_phase(self):
        """Return the phase of the quantum state."""
        return np.angle(self.state)

    def reshape_to_6d(self):
        """Reshape the state to 6D grid."""
        return self.state.reshape(self.grid_size)
