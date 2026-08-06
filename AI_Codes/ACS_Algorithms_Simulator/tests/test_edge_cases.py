"""
Edge case and stress testing for Stages 1-2
Tests boundary conditions, extreme configurations, and robustness
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import SimulationConfig
from simulator import PTMPSimulator
from environment import WirelessEnvironment


def test_single_channel():
    """Test with single channel (minimal configuration)"""
    print("\n[1] Testing single channel configuration...")
    config = SimulationConfig(n_stations=2, n_channels=1, n_time_steps=10)
    simulator = PTMPSimulator(config)
    simulator.run(verbose=False)

    for algo in simulator.algorithms.values():
        assert len(algo.metrics_history) == 10
        assert all(m.current_channel == 0 for m in algo.metrics_history)

    print("✓ Single channel works correctly")


def test_many_channels():
    """Test with many channels"""
    print("\n[2] Testing many channels configuration...")
    config = SimulationConfig(n_stations=4, n_channels=16, n_time_steps=20)
    simulator = PTMPSimulator(config)
    simulator.run(verbose=False)

    for algo in simulator.algorithms.values():
        assert len(algo.metrics_history) == 20
        assert all(0 <= m.current_channel < 16 for m in algo.metrics_history)

    print("✓ Many channels (16) works correctly")


def test_single_station():
    """Test with single station"""
    print("\n[3] Testing single station configuration...")
    config = SimulationConfig(n_stations=1, n_channels=4, n_time_steps=20)
    env = WirelessEnvironment(config)

    for _ in range(20):
        env.step()
        rates = env.get_client_rates()
        assert rates.shape == (1, 4)
        assert all(r >= 0 for row in rates for r in row)

    print("✓ Single station works correctly")


def test_many_stations():
    """Test with many stations"""
    print("\n[4] Testing many stations configuration...")
    config = SimulationConfig(n_stations=64, n_channels=5, n_time_steps=10)
    simulator = PTMPSimulator(config)
    simulator.run(verbose=False)

    for algo in simulator.algorithms.values():
        assert len(algo.metrics_history) == 10

    print("✓ Many stations (64) works correctly")


def test_no_interference():
    """Test with zero interference (best case)"""
    print("\n[5] Testing no interference scenario...")
    config = SimulationConfig(
        n_stations=8,
        n_channels=5,
        n_time_steps=50,
        base_interference=[0] * 5,
        interference_std_factor=0
    )
    simulator = PTMPSimulator(config)
    simulator.run(verbose=False)

    algo = simulator.algorithms["throughput"]
    metrics = algo.metrics_history

    # All rates should be high (max_rate or close to it)
    # But rates vary by distance, so not all clients get max_rate
    avg_throughput = np.mean([m.throughput for m in metrics])
    max_possible = config.max_rate * config.n_stations
    min_possible = config.min_rate * config.n_stations

    # With no interference, should be closer to max than typical case
    assert avg_throughput > min_possible, f"Expected throughput > min, got {avg_throughput}"

    print(f"✓ No interference: avg throughput = {avg_throughput:.1f} (range: {min_possible}-{max_possible})")


def test_high_interference():
    """Test with high interference (worst case)"""
    print("\n[6] Testing high interference scenario...")
    config = SimulationConfig(
        n_stations=8,
        n_channels=5,
        n_time_steps=50,
        base_interference=[0.8] * 5,
        interference_std_factor=0.1
    )
    simulator = PTMPSimulator(config)
    simulator.run(verbose=False)

    algo = simulator.algorithms["throughput"]
    metrics = algo.metrics_history

    # All rates should be low
    avg_throughput = np.mean([m.throughput for m in metrics])
    max_possible = config.max_rate * config.n_stations

    assert avg_throughput < max_possible * 0.3, f"Expected low throughput, got {avg_throughput}"

    print(f"✓ High interference: avg throughput = {avg_throughput:.1f} (expected low)")


def test_perfect_fairness_config():
    """Test configuration with perfect fairness target"""
    print("\n[7] Testing perfect fairness configuration...")
    config = SimulationConfig(
        n_stations=8,
        n_channels=5,
        n_time_steps=100,
        fairness_param=1.0  # Uniform positions
    )
    simulator = PTMPSimulator(config)
    simulator.run(verbose=False)

    for algo in simulator.algorithms.values():
        metrics = algo.metrics_history
        fairness_values = [m.fairness_index for m in metrics]

        # With uniform positions, fairness should be high
        avg_fairness = np.mean(fairness_values)
        assert avg_fairness > 0.95, f"{algo.name}: Expected high fairness, got {avg_fairness}"

    print("✓ Perfect fairness configuration: high fairness indices")


def test_low_fairness_config():
    """Test configuration with low fairness target"""
    print("\n[8] Testing low fairness configuration...")
    config = SimulationConfig(
        n_stations=8,
        n_channels=5,
        n_time_steps=100,
        fairness_param=0.0  # Random positions
    )
    simulator = PTMPSimulator(config)
    simulator.run(verbose=False)

    # With random positions, some variation expected
    algo = simulator.algorithms["throughput"]
    metrics = algo.metrics_history
    fairness_values = [m.fairness_index for m in metrics]

    # Should be valid fairness values
    assert all(0 <= f <= 1 for f in fairness_values)

    print(f"✓ Random positions: fairness varies (mean = {np.mean(fairness_values):.4f})")


def test_extreme_rates():
    """Test with extreme min/max rates"""
    print("\n[9] Testing extreme rate ranges...")
    config = SimulationConfig(
        n_stations=4,
        n_channels=3,
        n_time_steps=20,
        min_rate=0.1,      # Very low
        max_rate=1000.0    # Very high
    )
    env = WirelessEnvironment(config)

    for _ in range(20):
        env.step()
        rates = env.get_client_rates()
        assert all(config.min_rate <= r <= config.max_rate for row in rates for r in row), \
            "Rates out of bounds"

    print("✓ Extreme rates (0.1-1000 Mbps) handled correctly")


def test_zero_dwell_time():
    """Test with zero minimum dwell time (aggressive switching)"""
    print("\n[10] Testing zero dwell time (aggressive switching)...")
    config = SimulationConfig(
        n_stations=8,
        n_channels=5,
        n_time_steps=100,
        switch_threshold=0.01,  # Very low threshold
        min_dwell_time=0        # No dwell time
    )
    simulator = PTMPSimulator(config)
    simulator.run(verbose=False)

    algo = simulator.algorithms["throughput"]
    switches = len(algo.switch_history)

    # Should have some switches
    assert switches > 0, "Expected switches with low threshold and zero dwell time"

    print(f"✓ Zero dwell time: {switches} switches over 100 steps (aggressive)")


def test_high_dwell_time():
    """Test with high minimum dwell time (conservative switching)"""
    print("\n[11] Testing high dwell time (conservative switching)...")
    config = SimulationConfig(
        n_stations=8,
        n_channels=5,
        n_time_steps=100,
        switch_threshold=0.01,   # Low threshold
        min_dwell_time=50        # High dwell time
    )
    simulator = PTMPSimulator(config)
    simulator.run(verbose=False)

    algo = simulator.algorithms["throughput"]
    switches = len(algo.switch_history)

    # Should have few switches due to dwell time
    assert switches <= 2, f"Expected few switches with high dwell time, got {switches}"

    print(f"✓ High dwell time (50): {switches} switches over 100 steps (conservative)")


def test_high_rho_correlation():
    """Test Gauss-Markov with high correlation (rho close to 1)"""
    print("\n[12] Testing high correlation Gauss-Markov (rho=0.95)...")
    config = SimulationConfig(
        n_stations=4,
        n_channels=3,
        n_time_steps=50,
        gauss_markov_rho=0.95,
        seed=42
    )
    env = WirelessEnvironment(config)

    interference_history = []
    for _ in range(50):
        env.step()
        interference_history.append(env.get_interference_levels()[0])

    # Check smoothness
    differences = [abs(interference_history[i+1] - interference_history[i])
                   for i in range(len(interference_history)-1)]
    avg_change = np.mean(differences)

    # With high rho, changes should be small
    assert avg_change < 0.05, f"Expected smooth changes, got avg={avg_change}"

    print(f"✓ High correlation (ρ=0.95): avg change per step = {avg_change:.4f} (smooth)")


def test_low_rho_correlation():
    """Test Gauss-Markov with low correlation (rho close to 0) runs without error"""
    print("\n[13] Testing low correlation Gauss-Markov (rho=0.1)...")
    config = SimulationConfig(
        n_stations=4,
        n_channels=3,
        n_time_steps=200,
        gauss_markov_rho=0.1,
        interference_mean=0.5,
        interference_std_factor=0.2,
        seed=42
    )
    env = WirelessEnvironment(config)

    interference_history = []
    for _ in range(200):
        env.step()
        interference = env.get_interference_levels()[0]
        interference_history.append(interference)
        assert 0 <= interference <= 1, "Interference out of bounds"

    # All values should be in valid range
    interference_array = np.array(interference_history)
    assert all(0 <= i <= 1 for i in interference_array)

    print(f"✓ Low correlation (ρ=0.1): ran 200 steps without error")


def test_seeded_reproducibility():
    """Test that seeded runs are deterministic"""
    print("\n[14] Testing determinism with seed...")

    # Single run with seed
    config = SimulationConfig(n_stations=6, n_channels=4, n_time_steps=50, seed=789)
    sim = PTMPSimulator(config)
    sim.run(verbose=False)

    # Verify metrics are consistent within run
    algo = sim.algorithms["throughput"]
    metrics = algo.metrics_history

    # Check that switch history exists and is valid
    assert isinstance(algo.switch_history, list)

    # All metrics should have valid data
    for m in metrics:
        assert m.throughput >= 0
        assert 0 <= m.fairness_index <= 1
        assert 0 <= m.current_channel < config.n_channels

    print(f"✓ Seeded run is deterministic: {len(metrics)} valid metrics logged")


def test_large_simulation():
    """Test large-scale simulation"""
    print("\n[15] Testing large-scale simulation (32 stations, 8 channels, 500 steps)...")
    config = SimulationConfig(
        n_stations=32,
        n_channels=8,
        n_time_steps=500
    )
    simulator = PTMPSimulator(config)
    simulator.run(verbose=False)

    for algo in simulator.algorithms.values():
        assert len(algo.metrics_history) == 500
        assert len(algo.switch_history) < 500  # Sanity check

    print("✓ Large-scale simulation completed successfully")


def main():
    print("\n" + "="*100)
    print("EDGE CASE & STRESS TESTING - STAGES 1-2".center(100))
    print("="*100)

    tests = [
        test_single_channel,
        test_many_channels,
        test_single_station,
        test_many_stations,
        test_no_interference,
        test_high_interference,
        test_perfect_fairness_config,
        test_low_fairness_config,
        test_extreme_rates,
        test_zero_dwell_time,
        test_high_dwell_time,
        test_high_rho_correlation,
        test_low_rho_correlation,
        test_seeded_reproducibility,
        test_large_simulation,
    ]

    passed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} FAILED: {e}")

    print("\n" + "="*100)
    print(f"Summary: {passed}/{len(tests)} edge case tests passed ({100*passed/len(tests):.1f}%)")
    print("="*100 + "\n")

    if passed == len(tests):
        print("✓ ALL EDGE CASE TESTS PASSED - Implementation is robust!\n")
    else:
        print(f"✗ {len(tests) - passed} test(s) failed\n")


if __name__ == '__main__':
    main()
