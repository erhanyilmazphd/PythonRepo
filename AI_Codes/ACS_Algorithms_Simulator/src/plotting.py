"""Plotting and visualization for statistics and analysis"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class StatisticsPlotter:
    """Generate publication-quality plots from simulation statistics"""

    def __init__(self, output_dir: str = 'output', dpi: int = 100):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.dpi = dpi
        plt.style.use('seaborn-v0_8-darkgrid')

    def plot_throughput_comparison(self, statistics: Dict, filename: str = None, top_n: int = 10):
        """Bar chart comparing algorithm throughputs"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'throughput_comparison_{timestamp}.png'

        # Sort by throughput
        ranked = sorted(
            statistics.items(),
            key=lambda x: x[1].throughput_mean,
            reverse=True
        )[:top_n]

        names = [name for name, _ in ranked]
        means = [stats.throughput_mean for _, stats in ranked]
        stds = [stats.throughput_std for _, stats in ranked]

        fig, ax = plt.subplots(figsize=(12, 6))
        x = np.arange(len(names))
        bars = ax.bar(x, means, yerr=stds, capsize=5, alpha=0.7, color='steelblue', edgecolor='black')

        ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
        ax.set_ylabel('Throughput (Mbps)', fontsize=12, fontweight='bold')
        ax.set_title('Algorithm Throughput Comparison (Mean ± Std)', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=self.dpi)
        plt.close()
        return str(self.output_dir / filename)

    def plot_fairness_comparison(self, statistics: Dict, filename: str = None, top_n: int = 10):
        """Bar chart comparing algorithm fairness"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'fairness_comparison_{timestamp}.png'

        ranked = sorted(
            statistics.items(),
            key=lambda x: x[1].fairness_mean,
            reverse=True
        )[:top_n]

        names = [name for name, _ in ranked]
        means = [stats.fairness_mean for _, stats in ranked]
        stds = [stats.fairness_std for _, stats in ranked]

        fig, ax = plt.subplots(figsize=(12, 6))
        x = np.arange(len(names))
        bars = ax.bar(x, means, yerr=stds, capsize=5, alpha=0.7, color='seagreen', edgecolor='black')

        ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
        ax.set_ylabel('Fairness Index', fontsize=12, fontweight='bold')
        ax.set_title('Algorithm Fairness Comparison (Mean ± Std)', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha='right')
        ax.set_ylim([0, 1.05])
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=self.dpi)
        plt.close()
        return str(self.output_dir / filename)

    def plot_tradeoff_curve(self, statistics: Dict, filename: str = None):
        """Scatter plot showing throughput vs fairness tradeoff"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'tradeoff_curve_{timestamp}.png'

        fig, ax = plt.subplots(figsize=(10, 8))

        # Plot each algorithm
        colors = plt.cm.tab10(np.linspace(0, 1, len(statistics)))
        for (name, stats), color in zip(sorted(statistics.items()), colors):
            ax.scatter(
                stats.fairness_mean,
                stats.throughput_mean,
                s=200,
                alpha=0.6,
                color=color,
                edgecolors='black',
                linewidth=1.5,
                label=name
            )
            # Add error bars
            ax.errorbar(
                stats.fairness_mean,
                stats.throughput_mean,
                xerr=stats.fairness_std,
                yerr=stats.throughput_std,
                fmt='none',
                color=color,
                alpha=0.3,
                linewidth=1
            )

        ax.set_xlabel('Fairness Index', fontsize=12, fontweight='bold')
        ax.set_ylabel('Throughput (Mbps)', fontsize=12, fontweight='bold')
        ax.set_title('Throughput vs Fairness Tradeoff', fontsize=14, fontweight='bold')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        return str(self.output_dir / filename)

    def plot_timeseries(self, statistics: Dict, filename: str = None, max_algos: int = 5):
        """Line plot showing time series of throughput/fairness/min-rate"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'timeseries_{timestamp}.png'

        # Select top algorithms by throughput
        ranked = sorted(
            statistics.items(),
            key=lambda x: x[1].throughput_mean,
            reverse=True
        )[:max_algos]

        fig, axes = plt.subplots(3, 1, figsize=(14, 10))

        colors = plt.cm.tab10(np.linspace(0, 1, len(ranked)))

        for (name, stats), color in zip(ranked, colors):
            # Throughput
            axes[0].plot(stats.throughput_timeseries, label=name, color=color, linewidth=2)

            # Fairness
            axes[1].plot(stats.fairness_timeseries, label=name, color=color, linewidth=2)

            # Min rate
            axes[2].plot(stats.min_rate_timeseries, label=name, color=color, linewidth=2)

        axes[0].set_ylabel('Throughput (Mbps)', fontsize=11, fontweight='bold')
        axes[0].set_title('Algorithm Performance Over Time', fontsize=12, fontweight='bold')
        axes[0].legend(loc='best', fontsize=9)
        axes[0].grid(True, alpha=0.3)

        axes[1].set_ylabel('Fairness Index', fontsize=11, fontweight='bold')
        axes[1].legend(loc='best', fontsize=9)
        axes[1].grid(True, alpha=0.3)
        axes[1].set_ylim([0, 1.05])

        axes[2].set_xlabel('Timestep', fontsize=11, fontweight='bold')
        axes[2].set_ylabel('Min Rate (Mbps)', fontsize=11, fontweight='bold')
        axes[2].legend(loc='best', fontsize=9)
        axes[2].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=self.dpi)
        plt.close()
        return str(self.output_dir / filename)

    def plot_cdf(self, statistics: Dict, metric: str = 'throughput', filename: str = None):
        """CDF plot comparing algorithm distributions"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'cdf_{metric}_{timestamp}.png'

        fig, ax = plt.subplots(figsize=(12, 7))

        colors = plt.cm.tab10(np.linspace(0, 1, len(statistics)))

        for (name, stats), color in zip(sorted(statistics.items()), colors):
            # Get timeseries for metric
            if metric == 'throughput':
                data = stats.throughput_timeseries
                xlabel = 'Throughput (Mbps)'
            elif metric == 'fairness':
                data = stats.fairness_timeseries
                xlabel = 'Fairness Index'
            else:
                data = stats.min_rate_timeseries
                xlabel = 'Min Rate (Mbps)'

            # Compute CDF
            sorted_data = np.sort(data)
            cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)

            ax.plot(sorted_data, cdf, label=name, color=color, linewidth=2, marker='o', markersize=3)

        ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
        ax.set_ylabel('CDF (Probability)', fontsize=12, fontweight='bold')
        ax.set_title(f'Cumulative Distribution Function - {metric.capitalize()}', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, 1.05])

        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=self.dpi)
        plt.close()
        return str(self.output_dir / filename)

    def plot_stability_comparison(self, statistics: Dict, filename: str = None):
        """Box plot showing stability (throughput std) comparison"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'stability_{timestamp}.png'

        # Sort by stability (low std is good)
        ranked = sorted(
            statistics.items(),
            key=lambda x: x[1].throughput_std
        )

        names = [name for name, _ in ranked]
        stds = [stats.throughput_std for _, stats in ranked]
        cvs = [stats.throughput_std / stats.throughput_mean if stats.throughput_mean > 0 else 0
               for _, stats in ranked]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Absolute std
        x = np.arange(len(names))
        ax1.bar(x, stds, alpha=0.7, color='coral', edgecolor='black')
        ax1.set_xlabel('Algorithm', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Std Dev of Throughput (Mbps)', fontsize=11, fontweight='bold')
        ax1.set_title('Throughput Variability (Absolute)', fontsize=12, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(names, rotation=45, ha='right')
        ax1.grid(axis='y', alpha=0.3)

        # Coefficient of variation
        ax2.bar(x, cvs, alpha=0.7, color='lightblue', edgecolor='black')
        ax2.set_xlabel('Algorithm', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Coefficient of Variation', fontsize=11, fontweight='bold')
        ax2.set_title('Throughput Variability (Relative)', fontsize=12, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(names, rotation=45, ha='right')
        ax2.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=self.dpi)
        plt.close()
        return str(self.output_dir / filename)

    def plot_min_rate_comparison(self, statistics: Dict, filename: str = None, top_n: int = 10):
        """Bar chart comparing minimum rates (QoS metric)"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'min_rate_comparison_{timestamp}.png'

        ranked = sorted(
            statistics.items(),
            key=lambda x: x[1].min_rate_mean,
            reverse=True
        )[:top_n]

        names = [name for name, _ in ranked]
        means = [stats.min_rate_mean for _, stats in ranked]
        stds = [stats.min_rate_std for _, stats in ranked]

        fig, ax = plt.subplots(figsize=(12, 6))
        x = np.arange(len(names))
        bars = ax.bar(x, means, yerr=stds, capsize=5, alpha=0.7, color='mediumpurple', edgecolor='black')

        ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
        ax.set_ylabel('Minimum Client Rate (Mbps)', fontsize=12, fontweight='bold')
        ax.set_title('QoS: Minimum Rate Guarantee Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=self.dpi)
        plt.close()
        return str(self.output_dir / filename)

    def generate_all_plots(self, statistics: Dict) -> List[str]:
        """Generate all standard plots"""
        plots = []
        print("Generating plots...")
        print("  • Throughput comparison...", end=' ')
        plots.append(self.plot_throughput_comparison(statistics))
        print("✓")
        print("  • Fairness comparison...", end=' ')
        plots.append(self.plot_fairness_comparison(statistics))
        print("✓")
        print("  • Tradeoff curve...", end=' ')
        plots.append(self.plot_tradeoff_curve(statistics))
        print("✓")
        print("  • Time series...", end=' ')
        plots.append(self.plot_timeseries(statistics))
        print("✓")
        print("  • CDF (throughput)...", end=' ')
        plots.append(self.plot_cdf(statistics, metric='throughput'))
        print("✓")
        print("  • CDF (fairness)...", end=' ')
        plots.append(self.plot_cdf(statistics, metric='fairness'))
        print("✓")
        print("  • Stability comparison...", end=' ')
        plots.append(self.plot_stability_comparison(statistics))
        print("✓")
        print("  • Min rate comparison...", end=' ')
        plots.append(self.plot_min_rate_comparison(statistics))
        print("✓")

        return plots
