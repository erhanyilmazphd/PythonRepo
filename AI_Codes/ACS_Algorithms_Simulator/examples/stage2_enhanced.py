"""
Stage 2 Enhanced: Comprehensive Algorithm Comparison & Analysis
Demonstrates all 10 algorithms with detailed comparison framework
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import SimulationConfig, config_balanced
from simulator import PTMPSimulator


def analyze_fairness_throughput_tradeoff(simulator):
    """Analyze fairness-throughput tradeoff for all algorithms"""

    print("\n" + "="*120)
    print("FAIRNESS-THROUGHPUT TRADEOFF ANALYSIS".center(120))
    print("="*120)

    summary = simulator.get_summary()

    # Normalize metrics for comparison
    all_tp = [summary[a]['avg_throughput'] for a in summary]
    all_fair = [summary[a]['avg_fairness'] for a in summary]

    max_tp = max(all_tp)
    max_fair = max(all_fair)

    print("\n{:<30} | {:<15} | {:<15} | {:<20} | {:<15}".format(
        "Algorithm", "Throughput", "Fairness", "Tradeoff Score", "Switch Count"
    ))
    print("-" * 100)

    # Calculate tradeoff scores
    for algo_name in sorted(summary.keys()):
        stats = summary[algo_name]
        tp_norm = stats['avg_throughput'] / max_tp
        fair_norm = stats['avg_fairness'] / max_fair

        # Tradeoff score: balanced if both are high
        tradeoff_score = (tp_norm + fair_norm) / 2.0

        print("{:<30} | {:<15.1f} | {:<15.4f} | {:<20.3f} | {:<15}".format(
            algo_name,
            stats['avg_throughput'],
            stats['avg_fairness'],
            tradeoff_score,
            stats['total_switches']
        ))

    print("-" * 100)


def analyze_algorithm_profiles(simulator):
    """Characterize algorithm behavior profiles"""

    print("\n" + "="*120)
    print("ALGORITHM PROFILES & CHARACTERISTICS".center(120))
    print("="*120)

    summary = simulator.get_summary()

    profiles = {
        "Throughput Focus": {"tp_coeff": 0.7, "fair_coeff": 0.3},
        "Fairness Focus": {"tp_coeff": 0.3, "fair_coeff": 0.7},
        "Balanced": {"tp_coeff": 0.5, "fair_coeff": 0.5},
        "Stability Focus": {"tp_coeff": 0.4, "fair_coeff": 0.4, "switch_coeff": -0.2},
    }

    all_tp = [summary[a]['avg_throughput'] for a in summary]
    all_fair = [summary[a]['avg_fairness'] for a in summary]
    all_switches = [summary[a]['total_switches'] for a in summary]

    max_tp = max(all_tp)
    max_fair = max(all_fair)
    max_switches = max(all_switches) if max(all_switches) > 0 else 1

    print("\nAlgorithm Profiles:")
    print("-" * 120)

    for algo_name in sorted(summary.keys()):
        stats = summary[algo_name]

        tp_norm = stats['avg_throughput'] / max_tp
        fair_norm = stats['avg_fairness'] / max_fair
        switch_norm = 1 - (stats['total_switches'] / max_switches)

        # Determine profile
        if tp_norm > 0.9 and fair_norm < 0.8:
            profile = "⚡ Throughput Focus"
        elif fair_norm > 0.95 and tp_norm < 0.9:
            profile = "⚖️  Fairness Focus"
        elif abs(tp_norm - fair_norm) < 0.1:
            profile = "⚔️  Balanced"
        elif stats['total_switches'] < 3:
            profile = "🛡️  Stability Focus"
        else:
            profile = "🎯 Adaptive"

        print("{:<30} | Profile: {:<20} | TP: {:.2f}, Fair: {:.4f}, Stable: {:.2f}".format(
            algo_name, profile, tp_norm, fair_norm, switch_norm
        ))

    print("-" * 120)


def analyze_decision_distribution(simulator):
    """Analyze how often each algorithm selects each channel"""

    print("\n" + "="*120)
    print("CHANNEL SELECTION DISTRIBUTION".center(120))
    print("="*120)

    # Track channel selections for each algorithm
    channel_counts = {}
    for algo_name, algo in simulator.algorithms.items():
        channel_counts[algo_name] = {}
        for ch in range(simulator.config.n_channels):
            channel_counts[algo_name][ch] = 0

        for metric in algo.metrics_history:
            channel_counts[algo_name][metric.current_channel] += 1

    # Display distribution
    print("\nHow algorithms distribute selections across channels:")
    print("-" * 120)

    for algo_name in sorted(channel_counts.keys()):
        counts = channel_counts[algo_name]
        total = sum(counts.values())

        percentages = {ch: (count / total * 100) for ch, count in counts.items()}

        dist_str = " | ".join([f"Ch{ch}: {pct:5.1f}%" for ch, pct in sorted(percentages.items())])
        print("{:<30} | {}".format(algo_name, dist_str))

    print("-" * 120)


def analyze_convergence_speed(simulator):
    """Analyze how quickly algorithms stabilize"""

    print("\n" + "="*120)
    print("CONVERGENCE SPEED ANALYSIS".center(120))
    print("="*120)

    print("\nHow quickly metrics stabilize (std_dev ratio: early/late):")
    print("-" * 120)
    print("{:<30} | {:<20} | {:<20} | {:<15}".format(
        "Algorithm", "Early Period Std", "Late Period Std", "Convergence Ratio"
    ))
    print("-" * 120)

    for algo_name, algo in simulator.algorithms.items():
        if not algo.metrics_history:
            continue

        metrics = algo.metrics_history

        # Split into quarters
        quarter = len(metrics) // 4

        early_tp = [m.throughput for m in metrics[:quarter]]
        late_tp = [m.throughput for m in metrics[-quarter:]]

        early_std = np.std(early_tp)
        late_std = np.std(late_tp)
        ratio = late_std / (early_std + 1e-6)

        convergence = "✓ Fast" if ratio < 0.5 else "◐ Moderate" if ratio < 0.8 else "✗ Slow"

        print("{:<30} | {:<20.2f} | {:<20.2f} | {:<15}".format(
            algo_name, early_std, late_std, f"{ratio:.3f} ({convergence})"
        ))

    print("-" * 120)


def analyze_robustness(simulator):
    """Analyze algorithm robustness to interference"""

    print("\n" + "="*120)
    print("ROBUSTNESS ANALYSIS".center(120))
    print("="*120)

    print("\nPerformance consistency (lower std = more robust):")
    print("-" * 120)
    print("{:<30} | {:<20} | {:<20} | {:<15}".format(
        "Algorithm", "Throughput CV%", "Fairness CV%", "Robustness"
    ))
    print("-" * 120)

    for algo_name, algo in simulator.algorithms.items():
        if not algo.metrics_history:
            continue

        metrics = algo.metrics_history

        tp_mean = np.mean([m.throughput for m in metrics])
        tp_std = np.std([m.throughput for m in metrics])
        tp_cv = (tp_std / tp_mean * 100) if tp_mean > 0 else 0

        fair_mean = np.mean([m.fairness_index for m in metrics])
        fair_std = np.std([m.fairness_index for m in metrics])
        fair_cv = (fair_std / fair_mean * 100) if fair_mean > 0 else 0

        # Robustness score (lower CV = more robust)
        robustness = "Excellent" if (tp_cv + fair_cv) / 2 < 5 else \
                     "Good" if (tp_cv + fair_cv) / 2 < 10 else \
                     "Fair" if (tp_cv + fair_cv) / 2 < 15 else "Poor"

        print("{:<30} | {:<20.2f}% | {:<20.2f}% | {:<15}".format(
            algo_name, tp_cv, fair_cv, robustness
        ))

    print("-" * 120)


def main():
    print("\n" + "="*120)
    print("STAGE 2 ENHANCED: COMPREHENSIVE ALGORITHM COMPARISON".center(120))
    print("="*120)

    config = config_balanced()

    print(f"\nConfiguration:")
    print(f"  Stations: {config.n_stations}")
    print(f"  Channels: {config.n_channels}")
    print(f"  Time Steps: {config.n_time_steps}")
    print(f"  Algorithms: 10 (6 original + 4 new)")

    print(f"\nRunning simulation with all algorithms...")
    simulator = PTMPSimulator(config)
    simulator.run(verbose=True)

    # Run all analysis functions
    analyze_fairness_throughput_tradeoff(simulator)
    analyze_algorithm_profiles(simulator)
    analyze_decision_distribution(simulator)
    analyze_convergence_speed(simulator)
    analyze_robustness(simulator)

    # Final summary
    print("\n" + "="*120)
    print("KEY INSIGHTS".center(120))
    print("="*120)

    summary = simulator.get_summary()

    # Find best by different metrics
    best_tp = max(summary.items(), key=lambda x: x[1]['avg_throughput'])[0]
    best_fair = max(summary.items(), key=lambda x: x[1]['avg_fairness'])[0]
    best_minrate = max(summary.items(), key=lambda x: x[1]['avg_min_rate'])[0]
    least_switches = min(summary.items(), key=lambda x: x[1]['total_switches'])[0]

    print(f"\n✓ Best Throughput: {best_tp} ({summary[best_tp]['avg_throughput']:.1f} Mbps)")
    print(f"✓ Best Fairness: {best_fair} ({summary[best_fair]['avg_fairness']:.4f})")
    print(f"✓ Best Min Rate: {best_minrate} ({summary[best_minrate]['avg_min_rate']:.1f} Mbps)")
    print(f"✓ Most Stable: {least_switches} ({summary[least_switches]['total_switches']} switches)")

    print("\nNew Algorithms Performance:")
    print(f"  • Weighted TF: prioritizes configurable TP-fairness tradeoff")
    print(f"  • HPF+Cost: penalizes frequent switching for stability")
    print(f"  • Adaptive Threshold: adjusts switching aggressiveness dynamically")
    print(f"  • Channel Predictor: looks ahead for better decisions")

    print("\n" + "="*120)
    print("Stage 2 Enhanced Complete!".center(120))
    print("="*120 + "\n")


if __name__ == '__main__':
    main()
