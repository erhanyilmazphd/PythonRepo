"""
Stage 2: ACS Algorithms Analysis
Demonstrates all 6 algorithms and their decision-making process
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import SimulationConfig, config_balanced
from simulator import PTMPSimulator


def print_algorithm_decisions(simulator, timesteps=[0, 50, 100, 150, 199]):
    """Print detailed decision analysis for each algorithm at key timesteps"""

    print("\n" + "="*120)
    print("ALGORITHM DECISION ANALYSIS".center(120))
    print("="*120)

    for step in timesteps:
        if step >= len(next(iter(simulator.algorithms.values())).metrics_history):
            continue

        print(f"\n{'─'*120}")
        print(f"Timestep {step}".ljust(120))
        print(f"{'─'*120}\n")

        # Get environment state at this step
        env_state = None
        interference = None

        # Display environment state
        print("CHANNEL INTERFERENCE LEVELS:")
        print("─" * 120)
        for ch_id in range(simulator.config.n_channels):
            print(f"  Channel {ch_id}: interference varies (Gauss-Markov process)")
        print()

        # Display each algorithm's decision
        print("ALGORITHM DECISIONS & METRICS:")
        print("-" * 120)
        print(
            f"{'Algorithm':<30} | {'Channel':>8} | {'Utility':>12} | "
            f"{'Throughput':>12} | {'Fairness':>10} | {'Min Rate':>10}"
        )
        print("-" * 120)

        for algo_name in sorted(simulator.algorithms.keys()):
            algo = simulator.algorithms[algo_name]
            if step < len(algo.metrics_history):
                m = algo.metrics_history[step]
                # Get utilities at this step (reconstruct from decision logic)
                env = simulator.environment
                metrics_list = env.access_point.get_all_channel_metrics()
                utilities = algo.compute_utility(metrics_list)
                best_util = max(utilities)

                print(
                    f"{algo_name:<30} | {m.current_channel:>8} | "
                    f"{best_util:>12.2f} | {m.throughput:>12.1f} | "
                    f"{m.fairness_index:>10.4f} | {m.min_rate:>10.1f}"
                )

        print("-" * 120)


def analyze_algorithm_convergence(simulator):
    """Analyze convergence and stability of algorithms"""

    print("\n" + "="*120)
    print("ALGORITHM CONVERGENCE ANALYSIS".center(120))
    print("="*120)

    print("\nMetric Stability (Standard Deviation over time):")
    print("-" * 120)
    print(
        f"{'Algorithm':<30} | {'TP Std':>10} | {'Fair Std':>10} | "
        f"{'MinRate Std':>12} | {'Convergence':>20}"
    )
    print("-" * 120)

    for algo_name in sorted(simulator.algorithms.keys()):
        algo = simulator.algorithms[algo_name]
        metrics = algo.metrics_history

        if not metrics:
            continue

        throughputs = [m.throughput for m in metrics]
        fairness = [m.fairness_index for m in metrics]
        min_rates = [m.min_rate for m in metrics]

        tp_std = np.std(throughputs)
        fair_std = np.std(fairness)
        minrate_std = np.std(min_rates)

        # Convergence: if last 50 timesteps have lower std than first 50
        first_50_tp = np.std(throughputs[:50])
        last_50_tp = np.std(throughputs[-50:]) if len(throughputs) > 50 else 0
        convergence = "CONVERGED" if last_50_tp < first_50_tp * 0.8 else "STABLE"

        print(
            f"{algo_name:<30} | {tp_std:>10.2f} | {fair_std:>10.4f} | "
            f"{minrate_std:>12.2f} | {convergence:>20}"
        )

    print("-" * 120)


def analyze_algorithm_switching(simulator):
    """Analyze switching behavior of algorithms"""

    print("\n" + "="*120)
    print("ALGORITHM SWITCHING ANALYSIS".center(120))
    print("="*120)

    print("\nChannel Switches & Stability:")
    print("-" * 120)
    print(
        f"{'Algorithm':<30} | {'Total Switches':>15} | {'Avg Switch Interval':>20} | "
        f"{'Stability Score':>15}"
    )
    print("-" * 120)

    for algo_name in sorted(simulator.algorithms.keys()):
        algo = simulator.algorithms[algo_name]
        total_switches = len(algo.switch_history)

        if total_switches > 0:
            # Compute average interval between switches
            if len(algo.switch_history) > 1:
                intervals = [
                    algo.switch_history[i + 1][0] - algo.switch_history[i][0]
                    for i in range(len(algo.switch_history) - 1)
                ]
                avg_interval = np.mean(intervals)
            else:
                avg_interval = simulator.config.n_time_steps
        else:
            avg_interval = simulator.config.n_time_steps

        # Stability score: 100 = no switches, lower = more switches
        stability = 100 - (total_switches / (simulator.config.n_time_steps / 10))
        stability = max(0, min(100, stability))

        print(
            f"{algo_name:<30} | {total_switches:>15} | {avg_interval:>20.1f} | "
            f"{stability:>15.1f}%"
        )

    print("-" * 120)


def main():
    print("\n" + "="*120)
    print("STAGE 2: ACS ALGORITHMS - DETAILED ANALYSIS".center(120))
    print("="*120)

    # Use balanced configuration
    config = config_balanced()

    print(f"\nConfiguration:")
    print(f"  Stations: {config.n_stations}")
    print(f"  Channels: {config.n_channels}")
    print(f"  Time Steps: {config.n_time_steps}")
    print(f"  Switch Threshold: {config.switch_threshold*100:.1f}%")
    print(f"  Min Dwell Time: {config.min_dwell_time} steps")

    # Create and run simulator
    print(f"\nRunning simulation with all algorithms...")
    simulator = PTMPSimulator(config)
    simulator.run(verbose=False)

    # Print algorithm decision analysis
    print_algorithm_decisions(simulator)

    # Analyze convergence
    analyze_algorithm_convergence(simulator)

    # Analyze switching
    analyze_algorithm_switching(simulator)

    # Final summary
    print("\n" + "="*120)
    print("STAGE 2 SUMMARY".center(120))
    print("="*120)

    summary = simulator.get_summary()
    print("\nFinal Performance Metrics:")
    print("-" * 120)
    print(
        f"{'Algorithm':<30} | {'Avg Throughput':>15} | {'Avg Fairness':>15} | "
        f"{'Avg Min Rate':>15} | {'Switches':>10}"
    )
    print("-" * 120)

    for name in sorted(summary.keys()):
        stats = summary[name]
        print(
            f"{name:<30} | {stats['avg_throughput']:>15.1f} | "
            f"{stats['avg_fairness']:>15.4f} | {stats['avg_min_rate']:>15.1f} | "
            f"{stats['total_switches']:>10}"
        )

    print("-" * 120)

    print("\nObservations:")
    print("  • Algorithms with similar objectives (e.g., Throughput & Max-Min) may produce similar decisions")
    print("  • Fairness-focused algorithms (Jain, HPF) prioritize edge users (min rate)")
    print("  • Adaptive algorithms adjust weights based on recent fairness trends")
    print("  • Switch threshold prevents oscillation but may delay adaptation")

    print("\n" + "="*120)
    print("Stage 2 Complete!".center(120))
    print("="*120)
    print("\nNext steps:")
    print("  → Run Stage 3: python main.py (Tkinter GUI with live animation)")
    print("  → Run Stage 4: python run_monte_carlo.py (Monte Carlo statistics)")
    print()


if __name__ == '__main__':
    main()
