"""
Temporal Vector Lattice Entanglement (TVLE) Simulation Package

This package implements the Unified6DTOE simulation to demonstrate TVLE for predicting
Bitcoin private keys in a 6D spacetime grid. It includes modules for configuration,
quantum state management, Hamiltonian definition, key extraction, and simulation.

Author: Travis Jones
Version: 1.0.0
"""

__version__ = "1.0.0"

# Expose key modules and classes for import
from .config import CONFIG, G, c, hbar, e, epsilon_0, m_n, v_higgs, kappa, l_p, t_p, LAMBDA, INV_LAMBDA_SQ, TEMPORAL_CONSTANT, SECP256k1_CURVE, SECP256k1_P, SECP256k1_N, SEARCH_START, SEARCH_END
from .quantum_state import QuantumState
from .hamiltonian import Hamiltonian
from .key_extraction import KeyExtractor
from .simulation import Unified6DTOE
from .utils import validate_key
