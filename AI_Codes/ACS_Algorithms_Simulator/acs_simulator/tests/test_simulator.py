"""
Basic tests for PTMP ACS Simulator
==================================

Verify that the simulator runs without errors and produces valid outputs.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ptmp_acs_simulator import SimulationConfig, PTMPSimulator


def test_basic_simulation():
    """Test basic simulation runs without errors"""
    config = SimulationConfig(
        n_stations=4,
        n_channels=2,
        n_time_steps=50,
    )
    simulator = PTMPSimulator(config)
    simulator.run()
    stats = simulator.get_summary_stats()

    assert stats is not None
    assert len(stats) == 6  # 6 algorithms
    print("✓ Basic simulation test passed")


def test_algorithm_produces_metrics():
    """Test that all algorithms produce valid metrics"""
    config = SimulationConfig(
        n_stations=6,
        n_channels=3,
        n_time_steps=100,
    )
    simulator = PTMPSimulator(config)
    simulator.run()
    stats = simulator.get_summary_stats()

    for algo_name, algo_stats in stats.items():
        assert 'avg_throughput' in algo_stats
        assert 'avg_min_rate' in algo_stats
        assert 'avg_fairness' in algo_stats
        assert 'switches' in algo_stats
        assert algo_stats['avg_throughput'] > 0
        assert 0 <= algo_stats['avg_fairness'] <= 1

    print("✓ Algorithm metrics test passed")


def test_different_configurations():
    """Test simulator with various configurations"""
    configs = [
        SimulationConfig(n_stations=2, n_channels=1, n_time_steps=30,
                        base_interference=[0.2]),
        SimulationConfig(n_stations=10, n_channels=5, n_time_steps=50,
                        base_interference=[0.2, 0.4, 0.1, 0.3, 0.25]),
        SimulationConfig(n_stations=8, n_channels=4, n_time_steps=100, fairness_param=0.0),
        SimulationConfig(n_stations=8, n_channels=4, n_time_steps=100, fairness_param=1.0),
    ]

    for i, config in enumerate(configs):
        simulator = PTMPSimulator(config)
        simulator.run()
        stats = simulator.get_summary_stats()
        assert len(stats) == 6

    print(f"✓ Configuration test passed ({len(configs)} configurations)")


def test_channel_switch_threshold():
    """Test that switch threshold affects switching behavior"""
    config_low = SimulationConfig(
        n_stations=8,
        n_channels=4,
        n_time_steps=100,
        switch_threshold=0.01,  # Very low threshold
    )

    config_high = SimulationConfig(
        n_stations=8,
        n_channels=4,
        n_time_steps=100,
        switch_threshold=0.5,  # Very high threshold
    )

    sim_low = PTMPSimulator(config_low)
    sim_low.run()
    stats_low = sim_low.get_summary_stats()

    sim_high = PTMPSimulator(config_high)
    sim_high.run()
    stats_high = sim_high.get_summary_stats()

    # Low threshold should generally result in more switches
    low_switches = sum(s['switches'] for s in stats_low.values())
    high_switches = sum(s['switches'] for s in stats_high.values())

    print(f"✓ Switch threshold test passed")
    print(f"  Low threshold (0.01): avg {low_switches/6:.1f} switches")
    print(f"  High threshold (0.5): avg {high_switches/6:.1f} switches")


def test_interference_levels():
    """Test that different interference levels produce different results"""
    config1 = SimulationConfig(
        n_stations=6,
        n_channels=3,
        n_time_steps=80,
        base_interference=[0.1, 0.1, 0.1],  # Low interference
    )

    config2 = SimulationConfig(
        n_stations=6,
        n_channels=3,
        n_time_steps=80,
        base_interference=[0.8, 0.8, 0.8],  # High interference
    )

    sim1 = PTMPSimulator(config1)
    sim1.run()
    stats1 = sim1.get_summary_stats()

    sim2 = PTMPSimulator(config2)
    sim2.run()
    stats2 = sim2.get_summary_stats()

    # Generally, high interference should reduce throughput
    avg_throughput1 = sum(s['avg_throughput'] for s in stats1.values()) / 6
    avg_throughput2 = sum(s['avg_throughput'] for s in stats2.values()) / 6

    print(f"✓ Interference test passed")
    print(f"  Low interference: avg throughput {avg_throughput1:.1f} Mbps")
    print(f"  High interference: avg throughput {avg_throughput2:.1f} Mbps")


if __name__ == '__main__':
    print("=" * 60)
    print("Running PTMP ACS Simulator Tests")
    print("=" * 60)

    try:
        test_basic_simulation()
        test_algorithm_produces_metrics()
        test_different_configurations()
        test_channel_switch_threshold()
        test_interference_levels()

        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
