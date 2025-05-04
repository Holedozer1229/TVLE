import numpy as np
from src.config import CONFIG, G, m_n, e, epsilon_0, v_higgs, INV_LAMBDA_SQ, TEMPORAL_CONSTANT, hbar

class Hamiltonian:
    """Defines the Hamiltonian for the 6D TOE simulation."""

    def __init__(self, grid_size, dx, V, wormhole_state, logger):
        self.grid_size = grid_size
        self.total_points = np.prod(grid_size)
        self.dx = dx
        self.V = V
        self.wormhole_state = wormhole_state
        self.logger = logger

    def __call__(self, t, y, state_history, temporal_entanglement):
        """
        Compute the time derivative of the quantum state.

        Args:
            t (float): Current time
            y (np.ndarray): Current quantum state
            state_history (list): History of quantum states for CTC feedback
            temporal_entanglement (np.ndarray): Temporal entanglement vector

        Returns:
            np.ndarray: Derivative of the quantum state
        """
        # Reshape state to 6D for computation
        y_grid = y.reshape(self.grid_size)
        laplacian = np.zeros_like(y_grid, dtype=np.complex128)
        entanglement_term = np.zeros_like(y_grid, dtype=np.complex128)
        # Compute 6D discrete Laplacian and entanglement term
        for axis in range(6):
            # Laplacian for kinetic term
            laplacian += (np.roll(y_grid, 1, axis=axis) + 
                          np.roll(y_grid, -1, axis=axis) - 2 * y_grid) / (self.dx**2)
            # Entanglement term: couple neighboring grid points with time-dependent coupling
            shift_plus = np.roll(y_grid, 1, axis=axis)
            shift_minus = np.roll(y_grid, -1, axis=axis)
            coupling = CONFIG["entanglement_coupling"] * (1 + np.sin(t))
            entanglement_term += coupling * (shift_plus - y_grid) * np.conj(shift_minus - y_grid)
        laplacian = laplacian.flatten()
        entanglement_term = entanglement_term.flatten()
        # Kinetic term: -hbar^2 / (2m) * Laplacian
        kinetic_scale = 1e30  # Adjusted scaling for balance
        kinetic = -hbar**2 / (2 * m_n) * kinetic_scale * laplacian
        # Potential term with time-dependent perturbation
        potential = self.V * y * (1 + 2.0 * np.sin(t))
        # Entanglement term
        entanglement = entanglement_term
        # Hamiltonian applied to state: Hψ = kinetic + potential + entanglement
        H_psi = kinetic + potential + entanglement
        H_psi = -1j * H_psi / hbar
        # Wormhole term with time-dependent phase for quantum tunneling (3rd to 5th dimension)
        phase_factor = np.exp(1j * 2 * t)
        wormhole_term = CONFIG["wormhole_coupling"] * phase_factor * (self.wormhole_state.conj().dot(y)) * self.wormhole_state
        # CTC spin network feedback along 4th dimension (time)
        ctc_term = np.zeros_like(y, dtype=np.complex128)
        if len(state_history) > 0:
            past_state = state_history[-1]
            phase_diff = np.angle(y) - np.angle(past_state)
            # Maxwell's Demon sorting via temporal constant
            demon_sorting = TEMPORAL_CONSTANT * np.tanh(phase_diff)
            ctc_term = CONFIG["ctc_feedback_factor"] * np.exp(1j * demon_sorting) * np.abs(y)
        total_deriv = H_psi + wormhole_term + ctc_term
        total_deriv = np.clip(total_deriv, -CONFIG["field_clamp_max"], CONFIG["field_clamp_max"])
        return total_deriv
