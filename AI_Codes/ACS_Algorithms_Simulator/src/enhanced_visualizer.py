"""
Enhanced ACS Simulator Visualizer with Waterfall Charts
Provides clean, professional visualization inspired by USE_CASES.md
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')


class EnhancedACSVisualizer:
    """Enhanced visualization with waterfall charts and clean dashboards"""

    def __init__(self, simulator, output_formatter=None):
        self.simulator = simulator
        self.formatter = output_formatter
        self.config = simulator.config

    def create_waterfall_dashboard(self, filename: str = None):
        """
        Create waterfall visualization showing algorithm performance over time
        Inspired by USE_CASES.md decision progression
        """
        fig = plt.figure(figsize=(20, 14))
        fig.suptitle('ACS Simulator - Waterfall Performance Analysis',
                    fontsize=18, fontweight='bold', y=0.995)

        gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)

        history = self.simulator.history['metrics']
        algorithms = sorted(self.simulator.algorithms.keys())
        n_steps = len(next(iter(history.values())))

        # Color palette
        colors = plt.cm.Set3(np.linspace(0, 1, len(algorithms)))
        algo_colors = {algo: colors[i] for i, algo in enumerate(algorithms)}

        # 1. Throughput Waterfall
        ax1 = fig.add_subplot(gs[0, :2])
        for algo, color in algo_colors.items():
            throughputs = [m.throughput for m in history[algo]]
            ax1.plot(range(n_steps), throughputs, label=algo, color=color, linewidth=2, alpha=0.8)
        ax1.set_title('Throughput Progression', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Throughput (Mbps)', fontsize=10)
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='best', fontsize=8)

        # 2. Fairness Waterfall
        ax2 = fig.add_subplot(gs[0, 2])
        for algo, color in algo_colors.items():
            fairness = [m.fairness_index for m in history[algo]]
            ax2.plot(range(n_steps), fairness, label=algo, color=color, linewidth=2, alpha=0.8)
        ax2.set_title('Fairness Index Progression', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Jain FI', fontsize=10)
        ax2.set_ylim([0, 1.05])
        ax2.grid(True, alpha=0.3)

        # 3. Min Rate Waterfall
        ax3 = fig.add_subplot(gs[1, 0])
        for algo, color in algo_colors.items():
            min_rates = [m.min_rate for m in history[algo]]
            ax3.plot(range(n_steps), min_rates, label=algo, color=color, linewidth=2, alpha=0.8)
        ax3.set_title('Min Rate (Worst User)', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Min Rate (Mbps)', fontsize=10)
        ax3.grid(True, alpha=0.3)

        # 4. Channel Selection Heatmap - reconstruct from switch history
        ax4 = fig.add_subplot(gs[1, 1:])
        channel_data = np.zeros((len(algorithms), n_steps))

        for i, algo in enumerate(algorithms):
            alg_obj = self.simulator.algorithms[algo]
            current_ch = 0  # Start channel

            for step in range(n_steps):
                # Check if there was a switch at this step
                for switch_step, new_ch in alg_obj.switch_history:
                    if switch_step == step:
                        current_ch = new_ch
                        break
                channel_data[i, step] = current_ch

        im = ax4.imshow(channel_data, aspect='auto', cmap='tab10',
                       vmin=0, vmax=self.config.n_channels-1, interpolation='nearest')
        ax4.set_title('Channel Selection Over Time', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Algorithm', fontsize=10)
        ax4.set_xlabel('Time Step', fontsize=10)
        ax4.set_yticks(range(len(algorithms)))
        ax4.set_yticklabels(algorithms, fontsize=8)
        plt.colorbar(im, ax=ax4, label='Channel #')

        # 5. Summary Statistics Table
        ax5 = fig.add_subplot(gs[2, :])
        ax5.axis('off')

        # Create summary data
        summary_data = []
        for algo in algorithms:
            metrics = history[algo]
            throughputs = [m.throughput for m in metrics]
            fairness = [m.fairness_index for m in metrics]
            min_rates = [m.min_rate for m in metrics]
            switches = len(self.simulator.algorithms[algo].switch_history)

            summary_data.append([
                algo,
                f"{np.mean(throughputs):.1f} ± {np.std(throughputs):.1f}",
                f"{np.mean(fairness):.3f} ± {np.std(fairness):.3f}",
                f"{np.mean(min_rates):.1f} ± {np.std(min_rates):.1f}",
                f"{switches}",
                f"{np.max(throughputs):.1f}",
                f"{np.min(throughputs):.1f}",
            ])

        columns = ['Algorithm', 'Avg Throughput', 'Avg Fairness', 'Avg Min Rate',
                  'Switches', 'Max TP', 'Min TP']

        table = ax5.table(cellText=summary_data, colLabels=columns,
                         cellLoc='center', loc='center',
                         bbox=[0, 0, 1, 1])
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)

        # Color header
        for i in range(len(columns)):
            table[(0, i)].set_facecolor('#40466e')
            table[(0, i)].set_text_props(weight='bold', color='white')

        # Alternate row colors
        for i in range(1, len(summary_data) + 1):
            color = '#f0f0f0' if i % 2 == 0 else 'white'
            for j in range(len(columns)):
                table[(i, j)].set_facecolor(color)

        if filename:
            plt.savefig(filename, dpi=150, bbox_inches='tight')

        return fig

    def create_decision_tree_visualization(self, time_step: int, filename: str = None):
        """
        Create visualization showing decision-making process at a specific time step
        """
        fig = plt.figure(figsize=(18, 12))
        fig.suptitle(f'ACS Decision Process - Time Step {time_step}',
                    fontsize=16, fontweight='bold')

        gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

        # Get current rates
        rates = self.simulator.environment.base_rates

        # Left: Station rates heatmap
        ax1 = fig.add_subplot(gs[0, 0])
        im1 = ax1.imshow(rates, cmap='RdYlGn', aspect='auto', vmin=0, vmax=self.config.max_rate)
        ax1.set_title('Current Station Rates (Mbps)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Station', fontsize=10)
        ax1.set_xlabel('Channel', fontsize=10)
        ax1.set_xticks(range(self.config.n_channels))
        ax1.set_yticks(range(self.config.n_stations))
        plt.colorbar(im1, ax=ax1, label='Rate (Mbps)')

        # Add text annotations
        for i in range(self.config.n_stations):
            for c in range(self.config.n_channels):
                ax1.text(c, i, f'{rates[i, c]:.0f}', ha='center', va='center',
                        fontsize=8, color='black', weight='bold')

        # Right: Channel utility comparison
        ax2 = fig.add_subplot(gs[0, 1])

        utilities = []
        channels = []
        interference = self.simulator.environment.current_interference

        for c in range(self.config.n_channels):
            channel_rates = rates[:, c]
            sum_rate = np.sum(channel_rates)
            min_rate = np.min(channel_rates)
            variance = np.std(channel_rates)
            utility = 0.5 * sum_rate + 0.35 * min_rate - 0.15 * variance
            utilities.append(utility)
            channels.append(f'Ch-{c}')

        best_ch = np.argmax(utilities)
        colors_util = ['green' if i == best_ch else 'lightblue' for i in range(len(utilities))]

        bars = ax2.bar(channels, utilities, color=colors_util, edgecolor='black', linewidth=2)
        ax2.set_title('Channel Utility Comparison', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Utility Score', fontsize=10)
        ax2.grid(True, alpha=0.3, axis='y')

        # Add value labels on bars
        for bar, util in zip(bars, utilities):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{util:.1f}', ha='center', va='bottom', fontsize=9, weight='bold')

        # Bottom left: Algorithm selections
        ax3 = fig.add_subplot(gs[1, 0])
        ax3.axis('off')

        selections = []
        y_pos = 0.95
        for algo_name in sorted(self.simulator.algorithms.keys()):
            alg = self.simulator.algorithms[algo_name]
            current_ch = alg.current_channel
            channel_rates = rates[:, current_ch]

            selections.append([
                algo_name,
                f"Ch-{current_ch}",
                f"{np.sum(channel_rates):.1f}",
                f"{np.min(channel_rates):.1f}",
            ])

        # Create table
        table_ax = ax3
        table_ax.axis('off')

        col_labels = ['Algorithm', 'Selected Ch', 'Sum Rate', 'Min Rate']
        table = table_ax.table(cellText=selections, colLabels=col_labels,
                              cellLoc='center', loc='center',
                              bbox=[0, 0, 1, 1])
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)

        for i in range(len(col_labels)):
            table[(0, i)].set_facecolor('#40466e')
            table[(0, i)].set_text_props(weight='bold', color='white')

        for i in range(1, len(selections) + 1):
            color = '#f0f0f0' if i % 2 == 0 else 'white'
            for j in range(len(col_labels)):
                table[(i, j)].set_facecolor(color)

        # Bottom right: Metrics detail
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.axis('off')

        info_text = f"""
        SIMULATION DETAILS (Time Step {time_step})

        Configuration:
        • Stations: {self.config.n_stations}
        • Channels: {self.config.n_channels}
        • Fairness Parameter: {self.config.fairness_param}

        Current Environment:
        • Interference Levels: {[f'{i:.2f}' for i in interference]}
        • Best Channel: Ch-{best_ch} (Utility: {utilities[best_ch]:.1f})

        Thresholds:
        • Switch Threshold: {self.config.switch_threshold*100:.1f}%
        • Min Dwell Time: {self.config.min_dwell_time} steps
        • EWMA Factor: {self.config.ewma_factor}
        """

        ax4.text(0.05, 0.95, info_text, transform=ax4.transAxes,
                fontsize=9, verticalalignment='top', family='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        if filename:
            plt.savefig(filename, dpi=150, bbox_inches='tight')

        return fig

    def create_comparative_summary(self, filename: str = None):
        """Create final comparative summary visualization"""
        fig = plt.figure(figsize=(16, 10))
        fig.suptitle('ACS Algorithms - Final Comparative Summary',
                    fontsize=16, fontweight='bold')

        gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

        history = self.simulator.history['metrics']
        algorithms = sorted(self.simulator.algorithms.keys())

        # 1. Average Metrics Comparison
        ax1 = fig.add_subplot(gs[0, :])

        metrics_names = ['Avg Throughput', 'Avg Fairness', 'Avg Min Rate', 'Total Switches']
        x_pos = np.arange(len(algorithms))
        width = 0.2

        avg_throughput = [np.mean([m.throughput for m in history[a]]) for a in algorithms]
        avg_fairness = [np.mean([m.fairness_index for m in history[a]]) for a in algorithms]
        avg_min_rate = [np.mean([m.min_rate for m in history[a]]) for a in algorithms]
        total_switches = [len(self.simulator.algorithms[a].switch_history) for a in algorithms]

        # Normalize for visualization
        max_tp = max(avg_throughput)
        max_fair = max(avg_fairness) if max(avg_fairness) > 0 else 1
        max_min = max(avg_min_rate)
        max_sw = max(total_switches) if max(total_switches) > 0 else 1

        norm_throughput = [x / max_tp * 100 for x in avg_throughput]
        norm_fairness = [x / max_fair * 100 for x in avg_fairness]
        norm_min_rate = [x / max_min * 100 for x in avg_min_rate]
        norm_switches = [100 - (x / max_sw * 100) for x in total_switches]  # Inverse for stability

        ax1.bar(x_pos - 1.5*width, norm_throughput, width, label='Throughput', alpha=0.8)
        ax1.bar(x_pos - 0.5*width, norm_fairness, width, label='Fairness', alpha=0.8)
        ax1.bar(x_pos + 0.5*width, norm_min_rate, width, label='Min Rate', alpha=0.8)
        ax1.bar(x_pos + 1.5*width, norm_switches, width, label='Stability', alpha=0.8)

        ax1.set_ylabel('Normalized Score (%)', fontsize=10)
        ax1.set_title('Algorithm Performance Comparison (Normalized)', fontsize=12, fontweight='bold')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(algorithms, fontsize=9)
        ax1.legend(loc='best', fontsize=9)
        ax1.grid(True, alpha=0.3, axis='y')
        ax1.set_ylim([0, 120])

        # 2. Efficiency Score (Throughput vs Fairness Tradeoff)
        ax2 = fig.add_subplot(gs[1, 0])

        efficiency_scores = [(tp + fair) / 2 for tp, fair in zip(norm_throughput, norm_fairness)]
        colors = plt.cm.Set3(np.linspace(0, 1, len(algorithms)))

        bars = ax2.barh(algorithms, efficiency_scores, color=colors, edgecolor='black', linewidth=2)
        ax2.set_xlabel('Efficiency Score (%)', fontsize=10)
        ax2.set_title('Efficiency (Throughput + Fairness)', fontsize=12, fontweight='bold')
        ax2.set_xlim([0, 120])

        for bar, score in zip(bars, efficiency_scores):
            width_bar = bar.get_width()
            ax2.text(width_bar + 2, bar.get_y() + bar.get_height()/2.,
                    f'{score:.0f}%', va='center', fontsize=9, weight='bold')

        # 3. Stability Score (fewer switches)
        ax3 = fig.add_subplot(gs[1, 1])

        stability_scores = [100 - (s / max_sw * 100) if max_sw > 0 else 100 for s in total_switches]
        bars = ax3.barh(algorithms, stability_scores, color=colors, edgecolor='black', linewidth=2)
        ax3.set_xlabel('Stability Score (%)', fontsize=10)
        ax3.set_title('Stability (Lower Switches)', fontsize=12, fontweight='bold')
        ax3.set_xlim([0, 120])

        for bar, score, switches in zip(bars, stability_scores, total_switches):
            width_bar = bar.get_width()
            ax3.text(width_bar + 2, bar.get_y() + bar.get_height()/2.,
                    f'{score:.0f}% ({switches})', va='center', fontsize=9, weight='bold')

        if filename:
            plt.savefig(filename, dpi=150, bbox_inches='tight')

        return fig
