import unittest
import logging
from src.simulation import Unified6DTOE

class TestSimulation(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("TestLogger")
        self.logger.addHandler(logging.NullHandler())

    def test_simulation_initialization(self):
        sim = Unified6DTOE(
            target_address="1TestAddress",
            target_pubkey=(0x123456789, None),
            logger=self.logger
        )
        self.assertEqual(sim.target_address, "1TestAddress")
        self.assertEqual(sim.total_points, 5625)

    def test_run_simulation(self):
        sim = Unified6DTOE(
            target_address="1TestAddress",
            target_pubkey=(0x123456789, None),
            logger=self.logger
        )
        sim.run_simulation(iterations=10)
        self.assertFalse(sim.key_found.is_set())

if __name__ == "__main__":
    unittest.main()
