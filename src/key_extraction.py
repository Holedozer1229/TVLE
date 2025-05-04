import numpy as np
from src.config import CONFIG, SEARCH_START, SEARCH_END
from src.utils import validate_key

class KeyExtractor:
    """Extracts Bitcoin private keys from the quantum state."""

    @staticmethod
    def extract(state, target_address, total_points, key_prediction_history):
        """
        Extract a private key from the quantum state.

        Args:
            state (QuantumState): The quantum state object
            target_address (str): Target Bitcoin address
            total_points (int): Total number of lattice points
            key_prediction_history (list): History of predicted keys

        Returns:
            tuple: (int, bool, str) - (key integer, success flag, WIF key if successful)
        """
        # Use magnitude and phase to generate bits
        state_magnitude = state.get_magnitude()
        state_phase = state.get_phase()
        # Project state along 6th dimension (w2, index 5) for demon observer
        state_6d = state.reshape_to_6d()
        demon_observation = np.sum(state_6d, axis=(0, 1, 2, 3, 4))  # Sum over all but 6th dimension
        demon_observation = demon_observation.flatten()  # Shape (3,)
        # Expand demon observation to full grid size by repeating
        demon_factor = np.tile(demon_observation, total_points // 3)[:total_points]
        # J-4 scalar longitudinal wave modulation along 6th dimension
        scalar_wave = CONFIG["j4_coupling"] * np.sin(state_phase)
        # Combine magnitude, phase, demon observation, and scalar wave
        combined = state_magnitude + 0.5 * (state_phase / np.pi) + 0.1 * demon_factor + 0.1 * scalar_wave
        # Sort combined values and split at the median
        indices = np.argsort(combined)
        key_bits = np.zeros_like(combined, dtype=int)
        key_bits[indices[total_points // 2:]] = 1
        key_int = 0
        for bit in key_bits[:256]:  # Extract 256 bits
            key_int = (key_int << 1) | bit
        # Ensure key_int is within SECP256k1 valid range (1 to n)
        if key_int == 0:
            key_bits = np.zeros(256, dtype=int)
            key_bits[np.random.choice(256, 128, replace=False)] = 1
            key_int = 0
            for bit in key_bits:
                key_int = (key_int << 1) | bit
        key_int = max(SEARCH_START, min(SEARCH_END, key_int))
        success, wif = validate_key(key_int, target_address)
        if success:
            key_prediction_history.append(key_int)
        return key_int, success, wif
