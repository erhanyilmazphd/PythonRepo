"""
Scenario Comparison: Test all algorithms across different scenarios
Demonstrates algorithm robustness and applicability to different use cases
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import (
    SimulationConfig,
    config_balanced,
    config_high_fairness,
    config_highly_variable,
    config_fairness_critical,
    config_throughput_critical,
)
from simulator import PTMPSimulator


def compare_algorithms_on_scenario(scenario_name, config):
    """Run all algorithms on a single scenario and compare"""

    print(f"\n{'='*120}")
    print(f"SCENARIO: {scenario_name}".center(120))
    print(f"{'='*120}")

    print(f"\nEnvironment Setup:")
    print(f"  Stations: {config.n_stations}, Channels: {config.n_channels}, Steps: {config.n_time_steps}")
    print(f"  Fairness Param: {config.fairness_param:.2f} (0=random, 1=uniform)")
    print(f"  Base Interference: {config.base_interference}")
    print(f"  Gauss-Markov ρ: {config.gauss_markov_rho:.2f} (correlation)")

    simulator = PTMPSimulator(config)
    simulator.run(verbose=False)

    summary = simulator.get_summary()

    # Rank algorithms by different metrics
    ranked_by_throughput = sorted(
        summary.items(),
        key=lambda x: x[1]['avg_throughput'],
        reverse=True
    )

    ranked_by_fairness = sorted(
        summary.items(),
        key=lambda x: x[1]['avg_fairness'],
        reverse=True
    )

    ranked_by_minrate = sorted(
        summary.items(),
        key=lambda x: x[1]['avg_min_rate'],
        reverse=True
    )

    ranked_by_stability = sorted(
        summary.items(),
        key=lambda x: x[1]['total_switches']
    )

    # Display results
    print(f"\n{'Rank':<6} | {'Throughput':<30} | {'Fairness':<30} | {'Min Rate':<30} | {'Stability':<30}")
    print("-" * 130)

    for rank in range(min(5, len(summary))):
        tp_algo, tp_stats = ranked_by_throughput[rank]
        fair_algo, fair_stats = ranked_by_fairness[rank]
        minr_algo, minr_stats = ranked_by_minrate[rank]
        stab_algo, stab_stats = ranked_by_stability[rank]

        print(
            f"{rank+1:<6} | {tp_algo:<30} | {fair_algo:<30} | {minr_algo:<30} | {stab_algo:<30}"
        )

    print("-" * 130)

    # Statistics
    print(f"\nScenario Statistics:")
    print(f"  Avg Algorithm Throughput: {np.mean([s['avg_throughput'] for s in summary.values()]):.1f} Mbps")
    print(f"  Avg Algorithm Fairness: {np.mean([s['avg_fairness'] for s in summary.values()]):.4f}")
    print(f"  Avg Algorithm Min Rate: {np.mean([s['avg_min_rate'] for s in summary.values()]):.1f} Mbps")
    print(f"  Avg Algorithm Switches: {np.mean([s['total_switches'] for s in summary.values()]):.1f}")

    # Identify best overall algorithm for this scenario
    scores = {}
    for algo_name, stats in summary.items():
        # Normalized composite score
        tp_score = stats['avg_throughput'] / (config.max_rate * config.n_stations)
        fair_score = stats['avg_fairness']
        minr_score = stats['avg_min_rate'] / config.max_rate
        stab_score = 1 - (stats['total_switches'] / (config.n_time_steps / 10))

        # Balanced scoring
        composite = (tp_score * 0.3 + fair_score * 0.3 + minr_score * 0.2 + stab_score * 0.2)
        scores[algo_name] = composite

    best_algo = max(scores.items(), key=lambda x: x[1])[0]
    print(f"\n  🏆 Best Overall for this Scenario: {best_algo}")

    return summary


def main():
    print("\n" + "="*120)
    print("SCENARIO COMPARISON: 10 ALGORITHMS × 5 SCENARIOS".center(120))
    print("="*120)

    # Define scenarios
    scenarios = [
        ("Balanced (Default)", config_balanced()),
        ("High Fairness", config_high_fairness()),
        ("Highly Variable Interference", config_highly_variable()),
        ("Fairness Critical", config_fairness_critical()),
        ("Throughput Critical", config_throughput_critical()),
    ]

    results = {}

    # Run all scenarios
    for scenario_name, config in scenarios:
        results[scenario_name] = compare_algorithms_on_scenario(scenario_name, config)

    # Cross-scenario analysis
    print("\n" + "="*120)
    print("CROSS-SCENARIO ANALYSIS".center(120))
    print("="*120)

    print("\nAlgorithm Consistency Across Scenarios:")
    print("-" * 120)

    all_algorithms = set()
    for scenario_results in results.values():
        all_algorithms.update(scenario_results.keys())

    print(f"{'Algorithm':<30} | {'Avg TP':<15} | {'Avg Fair':<15} | {'Consistency':<20}")
    print("-" * 120)

    for algo_name in sorted(all_algorithms):
        throughputs = []
        fairnesses = []

        for scenario_results in results.values():
            if algo_name in scenario_results:
                throughputs.append(scenario_results[algo_name]['avg_throughput'])
                fairnesses.append(scenario_results[algo_name]['avg_fairness'])

        if throughputs:
            avg_tp = np.mean(throughputs)
            avg_fair = np.mean(fairnesses)
            consistency = 1 - (np.std(throughputs) / (avg_tp + 1e-6))  # Higher = more consistent

            consistency_label = "Excellent" if consistency > 0.9 else \
                               "Good" if consistency > 0.8 else \
                               "Fair" if consistency > 0.7 else "Variable"

            print(f"{algo_name:<30} | {avg_tp:<15.1f} | {avg_fair:<15.4f} | {consistency_label:<20}")

    print("-" * 120)

    # Recommendations
    print("\n" + "="*120)
    print("ALGORITHM RECOMMENDATIONS BY USE CASE".center(120))
    print("="*120)

    recommendations = {
        "Balanced": "adaptive_hpf, channel_predictor",
        "High Fairness": "max_min, jain, channel_predictor",
        "Variable Interference": "adaptive_threshold, adaptive_hpf, channel_predictor",
        "Fairness Critical": "max_min, jain, hpf_switch_cost",
        "Throughput Critical": "throughput, channel_predictor, weighted_tf",
        "Stability Focused": "hpf_switch_cost, proportional_fair",
        "General Purpose": "adaptive_hpf, channel_predictor",
    }

    for use_case, algos in recommendations.items():
        print(f"\n  {use_case:.<30} {algos}")

    print("\n" + "="*120)
    print("Scenario Comparison Complete!".center(120))
    print("="*120 + "\n")


if __name__ == '__main__':
    main()
