"""
Stage 1: Headless Simulator Example
Demonstrates core engine without GUI
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import SimulationConfig, config_balanced
from simulator import PTMPSimulator
import numpy as np


def main():
    print("\n" + "="*80)
    print("STAGE 1: PTMP ACS Simulator - Headless Engine".center(80))
    print("="*80)

    # Use balanced configuration
    config = config_balanced()

    print(f"\nConfiguration:")
    print(f"  Stations: {config.n_stations}")
    print(f"  Channels: {config.n_channels}")
    print(f"  Time Steps: {config.n_time_steps}")
    print(f"  Fairness Param: {config.fairness_param}")
    print(f"  Base Interference: {config.base_interference}")
    print(f"  EWMA Factor: {config.ewma_factor}")
    print(f"  Gauss-Markov ρ: {config.gauss_markov_rho}")
    print(f"  Switch Threshold: {config.switch_threshold*100:.1f}%")

    # Create and run simulator
    print(f"\nRunning simulation...")
    simulator = PTMPSimulator(config)
    simulator.run(verbose=True)

    # Print summary
    print("\n" + "="*80)
    print("SIMULATION COMPLETE".center(80))
    print("="*80)

    summary = simulator.get_summary()

    print(f"\nAlgorithm Performance Summary:")
    print("-" * 80)
    print(
        f"{'Algorithm':<25} | {'Avg TP':>10} | {'Avg Fair':>10} | "
        f"{'Avg MinRate':>11} | {'Switches':>8}"
    )
    print("-" * 80)

    for name, stats in sorted(summary.items()):
        print(
            f"{name:<25} | {stats['avg_throughput']:>10.1f} | "
            f"{stats['avg_fairness']:>10.4f} | {stats['avg_min_rate']:>11.1f} | "
            f"{stats['total_switches']:>8}"
        )

    print("-" * 80)

    # Sample metrics from key timesteps
    print(f"\nSample Metrics at Key Timesteps:")
    print("-" * 80)

    key_steps = [0, config.n_time_steps // 4, config.n_time_steps // 2,
                 3 * config.n_time_steps // 4, config.n_time_steps - 1]

    algo_name = "adaptive_hpf"  # Pick best algorithm
    algo = simulator.algorithms[algo_name]

    print(f"\nMetrics for '{algo_name}' algorithm:")
    print(f"{'Step':>5} | {'Channel':>7} | {'TP':>8} | {'Fair':>8} | {'MinRate':>8}")
    print("-" * 45)

    for step_idx in key_steps:
        if step_idx < len(algo.metrics_history):
            m = algo.metrics_history[step_idx]
            print(
                f"{m.timestep:>5} | {m.current_channel:>7} | "
                f"{m.throughput:>8.1f} | {m.fairness_index:>8.4f} | {m.min_rate:>8.1f}"
            )

    # Show interference progression
    print(f"\n\nInterference Levels Progression:")
    print("-" * 80)
    env = simulator.environment

    # Reconstruct interference history (only current state available)
    print("Final interference levels by channel:")
    final_interference = env.get_interference_levels()
    for ch, interference in enumerate(final_interference):
        print(f"  Channel {ch}: {interference:.4f}")

    print("\n" + "="*80)
    print("Stage 1 Complete!".center(80))
    print("="*80)
    print("\nNext steps:")
    print("  → Run Stage 2: python examples/stage2_algorithms.py")
    print("  → Run Stage 3: python main.py (GUI)")
    print("  → Run Stage 4: python run_monte_carlo.py (Statistics)")
    print()


if __name__ == '__main__':
    main()
