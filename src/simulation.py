from src.quantum_state import QuantumState
from src.hamiltonian import Hamiltonian
from src.key_extraction import KeyExtractor
from src.config import CONFIG
from tqdm import tqdm

class Unified6DTOE:
    """
    A unified 6D Theory of Everything simulation for TVLE-based key prediction.
    """

    def __init__(self, target_address, target_pubkey, logger):
        self.target_address = target_address
        self.target_pubkey = target_pubkey
        self.logger = logger
        self.grid_size = CONFIG["grid_size"]
        self.total_points = np.prod(self.grid_size)
        self.dx = CONFIG["dx"]
        self.dt = CONFIG["dt"]
        self.running = True
        self.key_found = threading.Event()
        self.key_prediction_history = []
        self.predicted_key = None
        self.quantum_state = QuantumState(self.grid_size, logger)
        self.wormhole_state = None
        self.V = None
        self.send_pubkey_through_wormhole()

    def send_pubkey_through_wormhole(self):
        """
        Inject the target public key into the quantum state via a distributed wormhole.
        """
        if not self.target_pubkey or not isinstance(self.target_pubkey[0], int):
            raise ValueError("Invalid target public key")
        # Convert public key to binary string (256 bits)
        pubkey_binary = bin(self.target_pubkey[0])[2:].zfill(256)
        pubkey_bits = [int(bit) for bit in pubkey_binary]
        # Initialize scalar field based on public key
        N = self.total_points
        self.scalar_field = np.zeros(N)
        for i in range(N):
            self.scalar_field[i] = pubkey_bits[i % 256]  # Repeat 256-bit pattern across grid
        # Compute potential energy vector
        ranges = [np.linspace(0, (gs-1)*self.dx, gs) for gs in self.grid_size]
        coords = np.meshgrid(*ranges, indexing='ij')
        weights = CONFIG["anisotropic_weights"]
        r_6d_sq = sum(w * c**2 for w, c in zip(weights, coords))
        r_6d = np.sqrt(r_6d_sq) + 1e-10  # Avoid division by zero
        V_grav = -G * m_n / (r_6d**4) * INV_LAMBDA_SQ
        V_em = CONFIG["em_strength"] * e**2 / (4 * np.pi * epsilon_0 * r_6d**4)
        V_higgs = v_higgs * CONFIG["flux_coupling"] / r_6d
        phi_6d = self.scalar_field.reshape(self.grid_size)
        V_phi = CONFIG["scalar_coupling"] * phi_6d
        self.V = (V_grav + V_em + V_higgs + V_phi).flatten()
        # Compute distributed wormhole state
        center = [gs // 2 * self.dx for gs in self.grid_size]  # Center of the grid
        r_6d = np.sqrt(sum((c - cent)**2 for c, cent in zip(coords, center)))
        z_to_w1_weight = 1.0 + 2.0 * (coords[2] - center[2]) * (coords[4] - center[4])
        sigma = self.dx * 5  # Spread over several grid points
        psi_wormhole = np.exp(-r_6d**2 / (2 * sigma**2)) * z_to_w1_weight
        for i in range(len(psi_wormhole.flat)):
            psi_wormhole.flat[i] *= pubkey_bits[i % 256]
        self.wormhole_state = psi_wormhole.flatten()
        norm = np.linalg.norm(self.wormhole_state)
        if norm > 0:
            self.wormhole_state /= norm
        self.logger.info("Public key injected via distributed wormhole")

    def start(self):
        """
        Start the simulation by running it for the specified number of iterations.
        """
        self.run_simulation(CONFIG["max_iterations"])

    def run_simulation(self, iterations):
        """
        Run the 6D TOE simulation for a specified number of iterations.

        Args:
            iterations (int): Number of iterations to run
        """
        self.logger.info(f"Starting 6D TOE simulation for {iterations} iterations")
        hamiltonian = Hamiltonian(self.grid_size, self.dx, self.V, self.wormhole_state, self.logger)
        for i in tqdm(range(iterations), desc="Simulation Progress"):
            if not self.running or self.key_found.is_set():
                self.logger.info(f"Simulation stopped at iteration {i}")
                break
            try:
                self.quantum_state.evolve(
                    self.dt,
                    CONFIG["rtol"],
                    CONFIG["atol"],
                    lambda t, y: hamiltonian(t, y, self.quantum_state.state_history, self.quantum_state.temporal_entanglement)
                )
                key_int, success, wif = KeyExtractor.extract(
                    self.quantum_state,
                    self.target_address,
                    self.total_points,
                    self.key_prediction_history
                )
                if success:
                    self.predicted_key = wif
                    self.key_found.set()
                    self.logger.info(f"Simulation succeeded at iteration {i}")
                    break
                if i % 10 == 0:  # Log every 10 iterations
                    self.logger.info(f"Iteration {i}: Predicted Key = {hex(key_int)}")
            except Exception as e:
                self.logger.error(f"Error at iteration {i}: {e}")
                self.running = False
                break
        if not self.key_found.is_set():
            self.logger.info("Simulation completed without finding the key")

    def shutdown(self):
        """Gracefully shut down the simulation."""
        self.running = False
        self.key_found.set()
        self.logger.info("Simulation shutdown initiated")
