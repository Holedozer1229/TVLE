import logging
from src.simulation import Unified6DTOE

# Configure logging
logging.basicConfig(
    filename='toe_6d_simulation.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("TOE6D_Simulation")

if __name__ == "__main__":
    # Test Simulation
    print("Running Test Simulation...")
    test_sim = Unified6DTOE(
        target_address="1TestAddress",
        target_pubkey=(0x123456789, None),
        logger=logger
    )
    test_sim.start()
    test_sim.shutdown()

    # Full Simulation (Bitcoin Puzzle #135)
    print("\nRunning Full Simulation for Bitcoin Puzzle #135...")
    full_sim = Unified6DTOE(
        target_address="16RGFo6hjq9ym6Pj7N5H7L1NR1rVPJyw2v",
        target_pubkey=(int("02145d2611c823a396ef6712ce0f712f09b9b4f3135e3e0aa3230fb9b6d08d1e16", 16), None),
        logger=logger
    )
    full_sim.start()
    full_sim.shutdown()

    print("Simulation complete. Check 'toe_6d_simulation.log' for details.")
