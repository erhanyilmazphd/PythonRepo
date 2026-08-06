"""Statistical analysis and Monte Carlo framework for ACS Simulator"""

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass, field
import json


@dataclass
class AlgorithmStatistics:
    """Statistics for a single algorithm across multiple runs"""
    name: str
    n_runs: int = 0

    # Throughput statistics
    throughput_mean: float = 0.0
    throughput_std: float = 0.0
    throughput_min: float = 0.0
    throughput_max: float = 0.0
    throughput_p25: float = 0.0
    throughput_p75: float = 0.0

    # Fairness statistics
    fairness_mean: float = 0.0
    fairness_std: float = 0.0
    fairness_min: float = 0.0
    fairness_max: float = 0.0
    fairness_p25: float = 0.0
    fairness_p75: float = 0.0

    # Min rate statistics
    min_rate_mean: float = 0.0
    min_rate_std: float = 0.0
    min_rate_min: float = 0.0
    min_rate_max: float = 0.0

    # Switch statistics
    switches_mean: float = 0.0
    switches_std: float = 0.0
    switches_min: int = 0
    switches_max: int = 0

    # Composite metrics
    score_mean: float = 0.0  # Composite performance score
    score_std: float = 0.0

    # Time series (per-timestep means across runs)
    throughput_timeseries: List[float] = field(default_factory=list)
    fairness_timeseries: List[float] = field(default_factory=list)
    min_rate_timeseries: List[float] = field(default_factory=list)

    def to_dict(self):
        """Convert to dictionary for JSON export"""
        return {
            'name': self.name,
            'n_runs': self.n_runs,
            'throughput': {
                'mean': round(self.throughput_mean, 2),
                'std': round(self.throughput_std, 2),
                'min': round(self.throughput_min, 2),
                'max': round(self.throughput_max, 2),
                'p25': round(self.throughput_p25, 2),
                'p75': round(self.throughput_p75, 2),
            },
            'fairness': {
                'mean': round(self.fairness_mean, 4),
                'std': round(self.fairness_std, 4),
                'min': round(self.fairness_min, 4),
                'max': round(self.fairness_max, 4),
                'p25': round(self.fairness_p25, 4),
                'p75': round(self.fairness_p75, 4),
            },
            'min_rate': {
                'mean': round(self.min_rate_mean, 2),
                'std': round(self.min_rate_std, 2),
                'min': round(self.min_rate_min, 2),
                'max': round(self.min_rate_max, 2),
            },
            'switches': {
                'mean': round(self.switches_mean, 2),
                'std': round(self.switches_std, 2),
                'min': int(self.switches_min),
                'max': int(self.switches_max),
            },
            'score': {
                'mean': round(self.score_mean, 4),
                'std': round(self.score_std, 4),
            }
        }


class MonteCarloRunner:
    """Execute multiple independent simulator runs and collect statistics"""

    def __init__(self, config, n_runs: int = 10, seed: int = None):
        self.config = config
        self.n_runs = n_runs
        self.seed = seed or 42
        self.run_results = []

    def run(self, verbose: bool = True):
        """Execute N independent simulation runs"""
        from .simulator import PTMPSimulator

        results = []
        for run_idx in range(self.n_runs):
            if verbose:
                print(f"Run {run_idx+1}/{self.n_runs}...", end=' ', flush=True)

            # Seed for reproducibility
            np.random.seed(self.seed + run_idx)

            # Create and run simulator
            simulator = PTMPSimulator(self.config)
            simulator.run()

            # Extract per-algorithm results
            run_data = {}
            for algo_name, algo in simulator.algorithms.items():
                run_data[algo_name] = {
                    'metrics_history': algo.metrics_history,
                    'switch_history': algo.switch_history,
                }

            results.append(run_data)
            if verbose:
                print("✓")

        self.run_results = results
        return results

    def get_statistics(self) -> Dict[str, AlgorithmStatistics]:
        """Compute statistics from all runs"""
        if not self.run_results:
            raise ValueError("No runs completed yet. Call run() first.")

        stats = {}

        # Get all algorithm names from first run
        for algo_name in self.run_results[0].keys():
            stats[algo_name] = self._compute_algorithm_stats(algo_name)

        return stats

    def _compute_algorithm_stats(self, algo_name: str) -> AlgorithmStatistics:
        """Compute statistics for a single algorithm"""
        algo_stats = AlgorithmStatistics(name=algo_name, n_runs=len(self.run_results))

        throughputs = []
        fairnesses = []
        min_rates = []
        switches_list = []
        scores = []

        # Collect per-run metrics
        for run_data in self.run_results:
            algo_result = run_data[algo_name]
            metrics_history = algo_result['metrics_history']
            switch_history = algo_result['switch_history']

            # Average metrics across timesteps
            if metrics_history:
                avg_tp = np.mean([m.throughput for m in metrics_history])
                avg_fair = np.mean([m.fairness_index for m in metrics_history])
                avg_min_rate = np.mean([m.min_rate for m in metrics_history])
                n_switches = len(switch_history)

                throughputs.append(avg_tp)
                fairnesses.append(avg_fair)
                min_rates.append(avg_min_rate)
                switches_list.append(n_switches)

                # Composite score: normalized weighted combination
                score = 0.4 * (avg_tp / 400) + 0.4 * avg_fair + 0.2 * (avg_min_rate / 50)
                scores.append(score)

        # Compute statistics
        throughputs = np.array(throughputs)
        fairnesses = np.array(fairnesses)
        min_rates = np.array(min_rates)
        switches_list = np.array(switches_list)
        scores = np.array(scores)

        # Throughput statistics
        algo_stats.throughput_mean = float(np.mean(throughputs))
        algo_stats.throughput_std = float(np.std(throughputs))
        algo_stats.throughput_min = float(np.min(throughputs))
        algo_stats.throughput_max = float(np.max(throughputs))
        algo_stats.throughput_p25 = float(np.percentile(throughputs, 25))
        algo_stats.throughput_p75 = float(np.percentile(throughputs, 75))

        # Fairness statistics
        algo_stats.fairness_mean = float(np.mean(fairnesses))
        algo_stats.fairness_std = float(np.std(fairnesses))
        algo_stats.fairness_min = float(np.min(fairnesses))
        algo_stats.fairness_max = float(np.max(fairnesses))
        algo_stats.fairness_p25 = float(np.percentile(fairnesses, 25))
        algo_stats.fairness_p75 = float(np.percentile(fairnesses, 75))

        # Min rate statistics
        algo_stats.min_rate_mean = float(np.mean(min_rates))
        algo_stats.min_rate_std = float(np.std(min_rates))
        algo_stats.min_rate_min = float(np.min(min_rates))
        algo_stats.min_rate_max = float(np.max(min_rates))

        # Switch statistics
        algo_stats.switches_mean = float(np.mean(switches_list))
        algo_stats.switches_std = float(np.std(switches_list))
        algo_stats.switches_min = int(np.min(switches_list))
        algo_stats.switches_max = int(np.max(switches_list))

        # Score statistics
        algo_stats.score_mean = float(np.mean(scores))
        algo_stats.score_std = float(np.std(scores))

        # Compute time series (per-timestep means)
        n_timesteps = len(self.run_results[0][algo_name]['metrics_history'])
        for t in range(n_timesteps):
            tp_values = []
            fair_values = []
            min_rate_values = []

            for run_data in self.run_results:
                metrics = run_data[algo_name]['metrics_history']
                if t < len(metrics):
                    m = metrics[t]
                    tp_values.append(m.throughput)
                    fair_values.append(m.fairness_index)
                    min_rate_values.append(m.min_rate)

            algo_stats.throughput_timeseries.append(float(np.mean(tp_values)))
            algo_stats.fairness_timeseries.append(float(np.mean(fair_values)))
            algo_stats.min_rate_timeseries.append(float(np.mean(min_rate_values)))

        return algo_stats


class StatisticsReport:
    """Generate comprehensive statistics reports"""

    def __init__(self, statistics: Dict[str, AlgorithmStatistics]):
        self.stats = statistics

    def get_ranking_by_throughput(self, top_n: int = 10) -> List[Tuple[str, float]]:
        """Rank algorithms by average throughput"""
        ranked = sorted(
            self.stats.items(),
            key=lambda x: x[1].throughput_mean,
            reverse=True
        )
        return [(name, stats.throughput_mean) for name, stats in ranked[:top_n]]

    def get_ranking_by_fairness(self, top_n: int = 10) -> List[Tuple[str, float]]:
        """Rank algorithms by average fairness"""
        ranked = sorted(
            self.stats.items(),
            key=lambda x: x[1].fairness_mean,
            reverse=True
        )
        return [(name, stats.fairness_mean) for name, stats in ranked[:top_n]]

    def get_ranking_by_score(self, top_n: int = 10) -> List[Tuple[str, float]]:
        """Rank algorithms by composite score"""
        ranked = sorted(
            self.stats.items(),
            key=lambda x: x[1].score_mean,
            reverse=True
        )
        return [(name, stats.score_mean) for name, stats in ranked[:top_n]]

    def get_stability_ranking(self, top_n: int = 10) -> List[Tuple[str, float]]:
        """Rank by consistency (low coefficient of variation)"""
        rankings = []
        for name, stats in self.stats.items():
            if stats.throughput_mean > 0:
                cv = stats.throughput_std / stats.throughput_mean
                rankings.append((name, cv))

        rankings = sorted(rankings, key=lambda x: x[1])
        return rankings[:top_n]

    def print_summary(self):
        """Print formatted statistics summary"""
        print("\n" + "="*80)
        print("MONTE CARLO STATISTICS REPORT")
        print("="*80)

        print("\n📊 THROUGHPUT RANKING (mean ± std)")
        for i, (name, stats) in enumerate(sorted(
            self.stats.items(),
            key=lambda x: x[1].throughput_mean,
            reverse=True
        )[:10], 1):
            print(f"  {i:2d}. {name:25s} {stats.throughput_mean:7.1f} ± {stats.throughput_std:5.1f} Mbps")

        print("\n⚖️  FAIRNESS RANKING (mean ± std)")
        for i, (name, stats) in enumerate(sorted(
            self.stats.items(),
            key=lambda x: x[1].fairness_mean,
            reverse=True
        )[:10], 1):
            print(f"  {i:2d}. {name:25s} {stats.fairness_mean:.4f} ± {stats.fairness_std:.4f}")

        print("\n🎯 COMPOSITE SCORE RANKING")
        for i, (name, stats) in enumerate(sorted(
            self.stats.items(),
            key=lambda x: x[1].score_mean,
            reverse=True
        )[:10], 1):
            print(f"  {i:2d}. {name:25s} {stats.score_mean:.4f} ± {stats.score_std:.4f}")

        print("\n⏱️  STABILITY RANKING (coefficient of variation, lower is better)")
        for i, (name, cv) in enumerate(self.get_stability_ranking(10), 1):
            stats = self.stats[name]
            print(f"  {i:2d}. {name:25s} CV={cv:.4f} ({stats.throughput_std:.1f}/{stats.throughput_mean:.1f})")

        print("\n" + "="*80)
