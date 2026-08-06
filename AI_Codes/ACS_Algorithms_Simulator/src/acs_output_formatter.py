"""
ACS Simulator Output Formatter
Provides clean, interactive output inspired by USE_CASES.md decision tables
"""

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
import json


@dataclass
class ChannelDecision:
    """Decision analysis for a single time step"""
    time_step: int
    algorithm: str
    current_channel: int
    best_channel: int
    channels_data: Dict[int, Dict]  # channel_id -> {throughput, min_rate, fairness, variance, utility}
    switched: bool
    reason: str
    improvement: float


class ACSOutputFormatter:
    """Format ACS simulation output for clean, interpretable analysis"""

    def __init__(self, config, simulator):
        self.config = config
        self.simulator = simulator

    def generate_decision_table(self, algorithm_name: str, time_step: int) -> str:
        """
        Generate a formatted decision table for a single time step
        Inspired by USE_CASES.md format
        """
        sim = self.simulator
        alg = sim.algorithms[algorithm_name]

        # Get rates for current time step
        rates = sim.environment.base_rates  # N_stations x N_channels
        interference = sim.environment.current_interference

        # Compute metrics for all channels
        channels_data = {}
        for c in range(self.config.n_channels):
            channel_rates = rates[:, c]
            sum_rate = np.sum(channel_rates)
            min_rate = np.min(channel_rates)
            mean_rate = np.mean(channel_rates)
            variance = np.std(channel_rates)

            # Simple utility (can be enhanced)
            utility = 0.5 * sum_rate + 0.35 * min_rate - 0.15 * variance

            channels_data[c] = {
                'throughput': sum_rate,
                'min_rate': min_rate,
                'mean_rate': mean_rate,
                'variance': variance,
                'utility': utility,
                'interference': interference[c],
            }

        # Generate table
        output = []
        output.append(f"\n{'='*100}")
        output.append(f"DECISION TABLE: {algorithm_name} at Time Step {time_step}")
        output.append(f"{'='*100}\n")

        # Create header
        output.append(
            f"{'Ch':>3} | {'Sum Rate':>10} | {'Min Rate':>10} | {'Mean Rate':>10} | "
            f"{'Variance':>10} | {'Utility':>10} | {'Interference':>12} | {'Status':>20}"
        )
        output.append("-" * 115)

        # Get current and best channels
        current_ch = alg.current_channel
        best_ch = max(channels_data.keys(), key=lambda c: channels_data[c]['utility'])

        # Print each channel
        for c in range(self.config.n_channels):
            data = channels_data[c]
            status = ""
            if c == current_ch:
                status = "CURRENT ✓"
            if c == best_ch and c != current_ch:
                status = "BEST ✓"

            output.append(
                f"{c:>3} | {data['throughput']:>10.1f} | {data['min_rate']:>10.1f} | "
                f"{data['mean_rate']:>10.1f} | {data['variance']:>10.2f} | "
                f"{data['utility']:>10.1f} | {data['interference']:>12.2f} | {status:>20}"
            )

        output.append("-" * 115)

        # Analysis
        if best_ch != current_ch:
            current_util = channels_data[current_ch]['utility']
            best_util = channels_data[best_ch]['utility']
            improvement = (best_util - current_util) / current_util * 100
            output.append(
                f"\nAnalysis: Ch-{best_ch} (Utility: {best_util:.1f}) "
                f"vs Current Ch-{current_ch} (Utility: {current_util:.1f})"
            )
            output.append(f"Improvement: {improvement:.1f}%")
            if improvement > self.config.switch_threshold * 100:
                output.append(f"✓ SWITCH RECOMMENDED (>{self.config.switch_threshold * 100}%)")
            else:
                output.append(f"✗ STAY (improvement {improvement:.1f}% < {self.config.switch_threshold * 100}%)")
        else:
            output.append(f"\n✓ Current channel Ch-{current_ch} is optimal (Utility: {channels_data[current_ch]['utility']:.1f})")

        output.append(f"{'='*100}\n")

        return "\n".join(output)

    def generate_station_rates_table(self, algorithm_name: str, time_step: int) -> str:
        """Generate station-by-channel rates matrix"""
        sim = self.simulator
        rates = sim.environment.base_rates  # N_stations x N_channels

        output = []
        output.append(f"\n{'='*100}")
        output.append(f"STATION RATES MATRIX: {algorithm_name} at Time Step {time_step}")
        output.append(f"{'='*100}\n")

        # Header
        header = "Station"
        for c in range(self.config.n_channels):
            header += f" | Ch-{c}"
        header += " | Mean"
        output.append(header)
        output.append("-" * len(header))

        # Rows
        for i in range(self.config.n_stations):
            row = f"Sta-{i}"
            for c in range(self.config.n_channels):
                row += f" | {rates[i, c]:>6.1f}"
            row += f" | {np.mean(rates[i, :]):>6.1f}"
            output.append(row)

        output.append("-" * len(header))
        output.append("Average" + "".join([f" | {np.mean(rates[:, c]):>6.1f}" for c in range(self.config.n_channels)]))

        output.append(f"{'='*100}\n")

        return "\n".join(output)

    def generate_algorithm_comparison(self, time_step: int) -> str:
        """Compare all algorithms at current time step"""
        output = []
        output.append(f"\n{'='*100}")
        output.append(f"ALGORITHM COMPARISON at Time Step {time_step}")
        output.append(f"{'='*100}\n")

        # Header
        output.append(
            f"{'Algorithm':<30} | {'Channel':>8} | {'Throughput':>12} | "
            f"{'Min Rate':>10} | {'Fairness':>10} | {'Switches':>8}"
        )
        output.append("-" * 95)

        # Data for each algorithm
        rates = self.simulator.environment.base_rates
        for alg_name in sorted(self.simulator.algorithms.keys()):
            alg = self.simulator.algorithms[alg_name]
            current_ch = alg.current_channel
            channel_rates = rates[:, current_ch]

            throughput = np.sum(channel_rates)
            min_rate = np.min(channel_rates)
            fairness = self._compute_jain_fairness(channel_rates)
            switches = len(alg.switch_history)

            output.append(
                f"{alg_name:<30} | {current_ch:>8} | {throughput:>12.1f} | "
                f"{min_rate:>10.1f} | {fairness:>10.4f} | {switches:>8}"
            )

        output.append("-" * 95)
        output.append(f"{'='*100}\n")

        return "\n".join(output)

    def generate_waterfall_summary(self, window_size: int = 50) -> str:
        """Generate waterfall chart summary over time windows"""
        output = []
        output.append(f"\n{'='*100}")
        output.append(f"WATERFALL SUMMARY - Algorithm Performance Progression")
        output.append(f"{'='*100}\n")

        history = self.simulator.history['metrics']
        n_steps = len(next(iter(history.values())))

        # Generate windows
        for window_start in range(0, n_steps, window_size):
            window_end = min(window_start + window_size, n_steps)
            output.append(f"\nWindow: Steps {window_start}-{window_end}")
            output.append("-" * 80)

            # Aggregate metrics for this window
            for alg_name in sorted(self.simulator.algorithms.keys()):
                metrics_window = history[alg_name][window_start:window_end]
                if not metrics_window:
                    continue

                throughputs = [m.throughput for m in metrics_window]
                fairnesses = [m.fairness_index for m in metrics_window]
                min_rates = [m.min_rate for m in metrics_window]

                output.append(
                    f"  {alg_name:<28}: "
                    f"Throughput {np.mean(throughputs):>7.1f}±{np.std(throughputs):>5.1f} | "
                    f"Fairness {np.mean(fairnesses):>6.3f}±{np.std(fairnesses):>5.3f} | "
                    f"MinRate {np.mean(min_rates):>6.1f}±{np.std(min_rates):>5.1f}"
                )

        output.append(f"\n{'='*100}\n")
        return "\n".join(output)

    def generate_interactive_dashboard(self, time_step: int) -> str:
        """Generate complete interactive dashboard for a time step"""
        dashboard = []

        # Title
        dashboard.append("\n" + "="*100)
        dashboard.append("PTMP ACS SIMULATOR - INTERACTIVE DASHBOARD".center(100))
        dashboard.append("="*100)

        # Overall status
        dashboard.append(f"\nSimulation Progress: Time Step {time_step}/{self.config.n_time_steps}")
        dashboard.append(f"Stations: {self.config.n_stations}, Channels: {self.config.n_channels}")
        dashboard.append(f"Configuration: Fairness={self.config.fairness_param}, "
                        f"Switch Threshold={self.config.switch_threshold*100}%")

        # Algorithm comparison
        dashboard.append("\n" + self.generate_algorithm_comparison(time_step))

        # Current station rates
        best_alg = max(self.simulator.algorithms.keys(),
                      key=lambda a: np.sum(self.simulator.environment.base_rates[
                          :, self.simulator.algorithms[a].current_channel
                      ]))
        dashboard.append(self.generate_station_rates_table(best_alg, time_step))

        # Decision table for best algorithm
        dashboard.append(self.generate_decision_table(best_alg, time_step))

        return "\n".join(dashboard)

    @staticmethod
    def _compute_jain_fairness(rates: np.ndarray) -> float:
        """Compute Jain's fairness index"""
        if len(rates) == 0 or np.sum(rates) == 0:
            return 0.0
        numerator = np.sum(rates) ** 2
        denominator = len(rates) * np.sum(rates ** 2)
        return numerator / denominator if denominator > 0 else 0.0

    def export_to_json(self, filename: str) -> None:
        """Export detailed results to JSON"""
        data = {
            'config': {
                'n_stations': self.config.n_stations,
                'n_channels': self.config.n_channels,
                'n_time_steps': self.config.n_time_steps,
                'fairness_param': self.config.fairness_param,
            },
            'algorithms': {}
        }

        history = self.simulator.history['metrics']

        for alg_name in self.simulator.algorithms.keys():
            alg = self.simulator.algorithms[alg_name]
            metrics_list = history[alg_name]

            data['algorithms'][alg_name] = {
                'name': alg.name,
                'throughputs': [float(m.throughput) for m in metrics_list],
                'min_rates': [float(m.min_rate) for m in metrics_list],
                'fairness_indices': [float(m.fairness_index) for m in metrics_list],
                'switch_events': [(int(step), int(ch)) for step, ch in alg.switch_history],
                'total_switches': len(alg.switch_history),
                'avg_throughput': float(np.mean([m.throughput for m in metrics_list])),
                'avg_fairness': float(np.mean([m.fairness_index for m in metrics_list])),
                'avg_min_rate': float(np.mean([m.min_rate for m in metrics_list])),
            }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def print_summary_report(self) -> None:
        """Print comprehensive summary report"""
        print("\n" + "="*100)
        print("PTMP ACS SIMULATOR - FINAL SUMMARY REPORT".center(100))
        print("="*100)

        history = self.simulator.history['metrics']

        print(f"\nConfiguration:")
        print(f"  Stations: {self.config.n_stations}")
        print(f"  Channels: {self.config.n_channels}")
        print(f"  Time Steps: {self.config.n_time_steps}")
        print(f"  Fairness Parameter: {self.config.fairness_param}")
        print(f"  Switch Threshold: {self.config.switch_threshold*100}%")

        print(f"\nAlgorithm Performance Summary:")
        print("-" * 100)
        print(
            f"{'Algorithm':<30} | {'Avg Throughput':>15} | {'Avg Fairness':>13} | "
            f"{'Avg Min Rate':>12} | {'Total Switches':>14}"
        )
        print("-" * 100)

        for alg_name in sorted(self.simulator.algorithms.keys()):
            alg = self.simulator.algorithms[alg_name]
            metrics_list = history[alg_name]

            throughputs = [m.throughput for m in metrics_list]
            fairness = [m.fairness_index for m in metrics_list]
            min_rates = [m.min_rate for m in metrics_list]

            print(
                f"{alg_name:<30} | {np.mean(throughputs):>15.1f} | {np.mean(fairness):>13.4f} | "
                f"{np.mean(min_rates):>12.1f} | {len(alg.switch_history):>14}"
            )

        print("-" * 100)
        print("="*100 + "\n")
