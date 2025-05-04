CONFIG = {
    "grid_size": (5, 5, 5, 5, 3, 3),  # 6D grid: (x, y, z, t, w1, w2)
    "max_iterations": 10000,          # For extensive key space exploration
    "dt": 1e-12,                      # Time step (seconds)
    "dx": 1e-15,                      # Spatial step (meters)
    "ctc_feedback_factor": 0.5,       # Strength of CTC retrocausal feedback
    "wormhole_coupling": 5000.0,      # Strong influence for quantum tunneling
    "entanglement_coupling": 2.0,     # Coupling strength for entanglement
    "charge": 1.60217662e-19,         # Electron charge (Coulombs)
    "em_strength": 3.0,               # Electromagnetic coupling strength
    "flux_coupling": 1e-3,            # Quantum flux coupling
    "field_clamp_max": 1e6,           # Maximum field magnitude clamp
    "rtol": 1e-6,                     # Relative tolerance for ODE solver
    "atol": 1e-9,                     # Absolute tolerance for ODE solver
    "anisotropic_weights": [1.0, 1.0, 1.0, 0.1, 0.1, 0.1],  # Weights for 6D distance
    "hopping_strength": 1e-1,         # Hopping strength for kinetic term
    "scalar_coupling": 1e-2,          # Coupling constant for scalar field
    "j4_coupling": 1.0,               # Coupling for J-4 scalar longitudinal waves
    "entanglement_factor": 0.2,       # Factor for temporal entanglement
}

# Physical Constants
G = 6.67430e-11          # Gravitational constant (m^3 kg^-1 s^-2)
c = 2.99792458e8         # Speed of light (m/s)
hbar = 1.0545718e-34     # Reduced Planck constant (J·s)
e = 1.60217662e-19       # Elementary charge (C)
epsilon_0 = 8.854187817e-12  # Vacuum permittivity (F/m)
m_n = 1.67e-27           # Neutron mass (kg)
v_higgs = 246e9 * e / c**2  # Higgs vacuum expectation value (kg)
kappa = 1e-8             # Curvature coupling constant
l_p = np.sqrt(hbar * G / c**3)  # Planck length (m)
t_p = np.sqrt(hbar * G / c**5)  # Planck time (s)
LAMBDA = 1.1e-52         # Cosmological constant (m^-2)
INV_LAMBDA_SQ = 1 / (LAMBDA ** 2)  # Inverse square of Lambda for gravitational entropy

# Temporal constant for Maxwell's Demon (scaled by dt)
TEMPORAL_CONSTANT = t_p / CONFIG["dt"]

# Bitcoin SECP256k1 Curve Constants
SECP256k1_CURVE = ecdsa.SECP256k1
SECP256k1_P = SECP256k1_CURVE.curve.p()  # Field prime
SECP256k1_N = SECP256k1_CURVE.order  # Curve order
SEARCH_START = 1  # Minimum valid value
SEARCH_END = SECP256k1_N
