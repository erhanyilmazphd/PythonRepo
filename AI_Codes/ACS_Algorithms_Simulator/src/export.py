"""Export simulation data to various formats (CSV, JSON)"""

import csv
import json
from pathlib import Path
from typing import Dict
from datetime import datetime


class DataExporter:
    """Export simulator results to different formats"""

    def __init__(self, output_dir: str = 'output'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def export_run_to_csv(self, simulator, filename: str = None) -> str:
        """Export single run to CSV (per-timestep data)"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'simulation_run_{timestamp}.csv'

        filepath = self.output_dir / filename

        # Collect all data
        rows = []
        n_timesteps = len(list(simulator.algorithms.values())[0].metrics_history)

        for t in range(n_timesteps):
            for algo_name, algo in simulator.algorithms.items():
                if t < len(algo.metrics_history):
                    m = algo.metrics_history[t]
                    row = {
                        'timestep': t,
                        'algorithm': algo_name,
                        'channel': m.current_channel,
                        'throughput_mbps': round(m.throughput, 2),
                        'fairness_index': round(m.fairness_index, 4),
                        'min_rate': round(m.min_rate, 2),
                        'total_switches': len(algo.switch_history),
                    }
                    rows.append(row)

        # Write CSV
        if rows:
            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

        return str(filepath)

    def export_statistics_to_csv(self, statistics: Dict, filename: str = None) -> str:
        """Export Monte Carlo statistics to CSV"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'statistics_{timestamp}.csv'

        filepath = self.output_dir / filename

        rows = []
        for algo_name, stats in statistics.items():
            row = {
                'algorithm': algo_name,
                'n_runs': stats.n_runs,
                'throughput_mean': round(stats.throughput_mean, 2),
                'throughput_std': round(stats.throughput_std, 2),
                'throughput_min': round(stats.throughput_min, 2),
                'throughput_max': round(stats.throughput_max, 2),
                'fairness_mean': round(stats.fairness_mean, 4),
                'fairness_std': round(stats.fairness_std, 4),
                'fairness_min': round(stats.fairness_min, 4),
                'fairness_max': round(stats.fairness_max, 4),
                'min_rate_mean': round(stats.min_rate_mean, 2),
                'min_rate_std': round(stats.min_rate_std, 2),
                'switches_mean': round(stats.switches_mean, 2),
                'switches_std': round(stats.switches_std, 2),
                'score_mean': round(stats.score_mean, 4),
                'score_std': round(stats.score_std, 4),
            }
            rows.append(row)

        # Write CSV
        if rows:
            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

        return str(filepath)

    def export_statistics_to_json(self, statistics: Dict, filename: str = None) -> str:
        """Export Monte Carlo statistics to JSON"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'statistics_{timestamp}.json'

        filepath = self.output_dir / filename

        # Convert to dict format
        data = {
            'timestamp': datetime.now().isoformat(),
            'algorithms': {
                name: stats.to_dict()
                for name, stats in statistics.items()
            }
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        return str(filepath)

    def export_timeseries_to_csv(self, statistics: Dict, filename: str = None) -> str:
        """Export time series (per-timestep means) to CSV"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'timeseries_{timestamp}.csv'

        filepath = self.output_dir / filename

        # Find max timesteps
        max_t = max(len(stats.throughput_timeseries) for stats in statistics.values())

        rows = []
        for t in range(max_t):
            row = {'timestep': t}
            for algo_name, stats in statistics.items():
                if t < len(stats.throughput_timeseries):
                    row[f'{algo_name}_tp'] = round(stats.throughput_timeseries[t], 2)
                    row[f'{algo_name}_fair'] = round(stats.fairness_timeseries[t], 4)
                    row[f'{algo_name}_minrate'] = round(stats.min_rate_timeseries[t], 2)

            rows.append(row)

        # Write CSV
        if rows:
            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

        return str(filepath)

    def create_summary_report(self, statistics: Dict, filename: str = None) -> str:
        """Create human-readable text report"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'report_{timestamp}.txt'

        filepath = self.output_dir / filename

        with open(filepath, 'w') as f:
            f.write("ACS SIMULATOR - MONTE CARLO RESULTS REPORT\n")
            f.write("="*80 + "\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"Algorithms Tested: {len(statistics)}\n")

            # Get first stats to find n_runs
            first_stats = next(iter(statistics.values()))
            f.write(f"Monte Carlo Runs: {first_stats.n_runs}\n")
            f.write("="*80 + "\n\n")

            # Throughput ranking
            f.write("THROUGHPUT RANKING (Mean ± Std, Mbps)\n")
            f.write("-"*80 + "\n")
            ranked = sorted(
                statistics.items(),
                key=lambda x: x[1].throughput_mean,
                reverse=True
            )
            for i, (name, stats) in enumerate(ranked, 1):
                f.write(f"{i:2d}. {name:30s} {stats.throughput_mean:7.1f} ± {stats.throughput_std:5.1f}\n")

            # Fairness ranking
            f.write("\n\nFAIRNESS RANKING (Mean ± Std)\n")
            f.write("-"*80 + "\n")
            ranked = sorted(
                statistics.items(),
                key=lambda x: x[1].fairness_mean,
                reverse=True
            )
            for i, (name, stats) in enumerate(ranked, 1):
                f.write(f"{i:2d}. {name:30s} {stats.fairness_mean:.4f} ± {stats.fairness_std:.4f}\n")

            # Stability ranking
            f.write("\n\nSTABILITY RANKING (Coefficient of Variation)\n")
            f.write("-"*80 + "\n")
            rankings = []
            for name, stats in statistics.items():
                if stats.throughput_mean > 0:
                    cv = stats.throughput_std / stats.throughput_mean
                    rankings.append((name, cv, stats))

            for i, (name, cv, stats) in enumerate(sorted(rankings, key=lambda x: x[1])[:10], 1):
                f.write(f"{i:2d}. {name:30s} CV={cv:.4f}\n")

            # Min rate ranking
            f.write("\n\nMINIMUM RATE RANKING (Mean ± Std, Mbps)\n")
            f.write("-"*80 + "\n")
            ranked = sorted(
                statistics.items(),
                key=lambda x: x[1].min_rate_mean,
                reverse=True
            )
            for i, (name, stats) in enumerate(ranked[:10], 1):
                f.write(f"{i:2d}. {name:30s} {stats.min_rate_mean:7.1f} ± {stats.min_rate_std:5.1f}\n")

            # Summary statistics
            f.write("\n\nSUMMARY STATISTICS BY ALGORITHM\n")
            f.write("="*80 + "\n")
            for name, stats in sorted(statistics.items()):
                f.write(f"\n{name}\n")
                f.write("-"*80 + "\n")
                f.write(f"  Throughput:  {stats.throughput_mean:7.1f} ± {stats.throughput_std:5.1f} " +
                       f"[{stats.throughput_min:5.1f}, {stats.throughput_max:5.1f}] Mbps\n")
                f.write(f"  Fairness:    {stats.fairness_mean:.4f} ± {stats.fairness_std:.4f} " +
                       f"[{stats.fairness_min:.4f}, {stats.fairness_max:.4f}]\n")
                f.write(f"  Min Rate:    {stats.min_rate_mean:7.1f} ± {stats.min_rate_std:5.1f} " +
                       f"[{stats.min_rate_min:5.1f}, {stats.min_rate_max:5.1f}] Mbps\n")
                f.write(f"  Switches:    {stats.switches_mean:5.1f} ± {stats.switches_std:4.1f} " +
                       f"[{stats.switches_min}, {stats.switches_max}]\n")
                f.write(f"  Stability (CV): {stats.throughput_std / stats.throughput_mean:.4f}\n")

        return str(filepath)
