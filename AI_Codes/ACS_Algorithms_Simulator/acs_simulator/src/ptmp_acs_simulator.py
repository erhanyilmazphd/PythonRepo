"""
PTMP Auto-Channel Selection (ACS) Simulator
============================================
Simulates a Point-to-Multipoint wireless network with multiple channels
and benchmarks different ACS algorithms.

Author: Auto-Channel Selection Research
Date: 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from abc import ABC, abstractmethod
from collections import deque
import warnings
warnings.filterwarnings('ignore')


# ============================================================================
# CONFIGURATION AND DATA STRUCTURES
# ============================================================================

@dataclass
class SimulationConfig:
    """Configuration parameters for the simulator"""
    n_stations: int = 8
    n_channels: int = 4
    n_time_steps: int = 200

    # Rate parameters (Mbps)
    min_rate: float = 5.0
    max_rate: float = 100.0

    # Fairness and distribution
    fairness_param: float = 0.5  # 0: random, 1: deterministic (all same distance)

    # Interference parameters [0, 1] per channel
    base_interference: List[float] = field(default_factory=lambda: [0.2, 0.4, 0.1, 0.3])
    interference_noise_std_factor: float = 0.1  # std = mean * this factor

    # Rate smoothing (EWMA)
    ewma_factor: float = 0.3  # 1-α where α is forgetting factor

    # Channel switching hysteresis
    switch_threshold: float = 0.08  # 8% improvement required
    min_dwell_time: int = 10  # minimum time steps on a channel

    # Visualization
    history_length: int = 100  # points to display in plots


@dataclass
class StationMetrics:
    """Per-station performance metrics"""
    station_id: int
    channel_rates: Dict[int, float] = field(default_factory=dict)  # c -> rate
    smoothed_rates: Dict[int, float] = field(default_factory=dict)  # EWMA filtered


@dataclass
class ChannelMetrics:
    """Per-channel performance metrics"""
    channel_id: int
    throughput: float = 0.0  # sum of all rates
    min_rate: float = 0.0  # worst user
    max_rate: float = 0.0  # best user
    fairness_index: float = 0.0  # Jain's FI
    utilization: float = 0.0  # normalized by R_max
    utility_wtf: float = 0.0  # Weighted Throughput-Fairness
    utility_hpf: float = 0.0  # Hybrid Proportional Fair
    utility_mmf: float = 0.0  # Max-Min Fairness


# ============================================================================
# PTMP ENVIRONMENT
# ============================================================================

class PTMPEnvironment:
    """
    Simulates a PTMP wireless environment with multiple channels and stations.
    """

    def __init__(self, config: SimulationConfig):
        self.config = config
        self.time_step = 0

        # Initialize client positions (distance proxy [0, 1])
        self._initialize_client_positions()

        # Initialize base rates for each station on each channel
        self.base_rates = np.zeros((config.n_stations, config.n_channels))
        self._initialize_base_rates()

        # Current interference levels per channel
        self.current_interference = np.array(config.base_interference, dtype=float)

        # Current achievable rates (base * (1 - interference))
        self.current_rates = np.zeros((config.n_stations, config.n_channels))

        # EWMA smoothed rates
        self.smoothed_rates = np.zeros((config.n_stations, config.n_channels))

        # Update rates
        self._update_rates()

    def _initialize_client_positions(self):
        """
        Initialize client positions based on fairness parameter.

        fairness_param = 0: fully random positions
        fairness_param = 1: all at same distance (deterministic)
        """
        if self.config.fairness_param >= 0.99:
            # Deterministic: all stations at same distance
            self.client_distances = np.ones(self.config.n_stations) * 0.5
        else:
            # Random with fairness parameter controlling spread
            # Lower fairness_param → higher variance
            random_component = np.random.uniform(0, 1, self.config.n_stations)
            mean_distance = 0.5
            variance = (1 - self.config.fairness_param) * 0.25
            self.client_distances = np.clip(
                np.random.normal(mean_distance, np.sqrt(variance), self.config.n_stations),
                0, 1
            )

    def _initialize_base_rates(self):
        """
        Initialize base rates for each station on each channel.
        Rates depend on distance to AP: closer → higher rate.

        Rate = max_rate * (1 - distance) + min_rate * distance
        """
        for i in range(self.config.n_stations):
            for c in range(self.config.n_channels):
                # Distance-based rate: closer stations get higher rates
                distance_factor = self.client_distances[i]
                base_rate = (self.config.max_rate * (1 - distance_factor) +
                            self.config.min_rate * distance_factor)
                self.base_rates[i, c] = base_rate

    def _update_rates(self):
        """
        Update current rates based on interference.
        Rate = base_rate * (1 - interference)
        """
        for c in range(self.config.n_channels):
            interference = self.current_interference[c]
            self.current_rates[:, c] = self.base_rates[:, c] * (1 - interference)

    def step(self):
        """
        Advance simulation by one time step.
        - Update interference with AWGN noise
        - Update rates based on new interference
        - Apply EWMA smoothing
        """
        self.time_step += 1

        # Update interference: AWGN with mean = base, std = base * factor
        for c in range(self.config.n_channels):
            base = self.config.base_interference[c]
            std = base * self.config.interference_noise_std_factor
            noise = np.random.normal(0, std)
            self.current_interference[c] = np.clip(base + noise, 0, 1)

        # Update rates based on new interference
        self._update_rates()

        # Apply EWMA smoothing: smoothed = α * current + (1-α) * prev
        alpha = self.config.ewma_factor
        self.smoothed_rates = (alpha * self.current_rates +
                               (1 - alpha) * self.smoothed_rates)

    def get_channel_metrics(self, channel_id: int, use_smoothed: bool = True) -> ChannelMetrics:
        """
        Calculate performance metrics for a specific channel.
        """
        rates = self.smoothed_rates[:, channel_id] if use_smoothed else self.current_rates[:, channel_id]

        throughput = np.sum(rates)
        min_rate = np.min(rates)
        max_rate = np.max(rates)

        # Jain's Fairness Index
        sum_rates = np.sum(rates)
        sum_sq_rates = np.sum(rates ** 2)
        if sum_sq_rates > 0:
            jain_fi = (sum_rates ** 2) / (self.config.n_stations * sum_sq_rates)
        else:
            jain_fi = 0.0

        # Utilization (normalized by channel capacity)
        utilization = throughput / (self.config.n_stations * self.config.max_rate)

        # Calculate utilities
        alpha, beta, gamma = 0.5, 0.3, 0.2  # Weights

        # Normalized utilization
        E_c = throughput / (self.config.n_stations * self.config.max_rate)

        # Weighted Throughput-Fairness (WTF)
        utility_wtf = 0.7 * E_c + 0.3 * (min_rate / self.config.max_rate)

        # HPF-ACS utility
        utility_hpf = (alpha * E_c +
                      beta * (min_rate / self.config.max_rate) +
                      gamma * jain_fi)

        # Max-Min Fairness (MMF)
        utility_mmf = min_rate + 0.05 * (throughput / np.sum(self.base_rates))

        return ChannelMetrics(
            channel_id=channel_id,
            throughput=throughput,
            min_rate=min_rate,
            max_rate=max_rate,
            fairness_index=jain_fi,
            utilization=utilization,
            utility_wtf=utility_wtf,
            utility_hpf=utility_hpf,
            utility_mmf=utility_mmf
        )

    def get_all_metrics(self) -> List[ChannelMetrics]:
        """Get metrics for all channels"""
        return [self.get_channel_metrics(c) for c in range(self.config.n_channels)]


# ============================================================================
# ACS ALGORITHMS
# ============================================================================

class ACSAlgorithm(ABC):
    """Base class for ACS algorithms"""

    def __init__(self, config: SimulationConfig, name: str):
        self.config = config
        self.name = name
        self.current_channel = 0
        self.time_on_channel = 0
        self.last_switch_time = 0
        self.switch_history = []

    @abstractmethod
    def select_channel(self, metrics: List[ChannelMetrics], current_channel: int) -> int:
        """
        Select best channel based on metrics.

        Args:
            metrics: List of ChannelMetrics for all channels
            current_channel: Currently active channel

        Returns:
            Selected channel ID
        """
        pass

    def step(self, metrics: List[ChannelMetrics], time_step: int) -> int:
        """
        Execute one step of the algorithm.
        """
        # Select best channel
        best_channel = self.select_channel(metrics, self.current_channel)

        # Decide whether to switch
        if best_channel != self.current_channel:
            # Apply hysteresis and dwell time constraints
            if self._should_switch(metrics, best_channel, time_step):
                self.current_channel = best_channel
                self.time_on_channel = 0
                self.last_switch_time = time_step
                self.switch_history.append((time_step, best_channel))

        self.time_on_channel += 1
        return self.current_channel

    def _should_switch(self, metrics: List[ChannelMetrics],
                      candidate: int, time_step: int) -> bool:
        """Check if switching criteria are met"""
        # Check minimum dwell time
        if time_step - self.last_switch_time < self.config.min_dwell_time:
            return False

        # Check utility improvement threshold (8%)
        current_metric = metrics[self.current_channel]
        candidate_metric = metrics[candidate]

        switch_threshold = 1 + self.config.switch_threshold

        # Use HPF utility for switching decision
        if candidate_metric.utility_hpf >= switch_threshold * current_metric.utility_hpf:
            return True

        return False


class ThroughputMaximizer(ACSAlgorithm):
    """Algorithm 1: Simple throughput maximization"""

    def __init__(self, config: SimulationConfig):
        super().__init__(config, "Throughput Maximizer")

    def select_channel(self, metrics: List[ChannelMetrics], current_channel: int) -> int:
        """Select channel with highest aggregate throughput"""
        throughputs = [m.throughput for m in metrics]
        return int(np.argmax(throughputs))


class MaxMinFairness(ACSAlgorithm):
    """Algorithm 2: Max-min fairness (protect worst user)"""

    def __init__(self, config: SimulationConfig):
        super().__init__(config, "Max-Min Fairness")

    def select_channel(self, metrics: List[ChannelMetrics], current_channel: int) -> int:
        """Select channel with highest minimum rate"""
        min_rates = [m.min_rate for m in metrics]
        return int(np.argmax(min_rates))


class JainsFairnessAlgorithm(ACSAlgorithm):
    """Algorithm 3: Jain's fairness index"""

    def __init__(self, config: SimulationConfig):
        super().__init__(config, "Jain's Fairness")

    def select_channel(self, metrics: List[ChannelMetrics], current_channel: int) -> int:
        """Select channel with highest Jain's fairness index"""
        jain_indices = [m.fairness_index for m in metrics]
        return int(np.argmax(jain_indices))


class WTFAlgorithm(ACSAlgorithm):
    """Algorithm 4: Weighted Throughput-Fairness"""

    def __init__(self, config: SimulationConfig):
        super().__init__(config, "WTF (α=0.7, β=0.3)")

    def select_channel(self, metrics: List[ChannelMetrics], current_channel: int) -> int:
        """Select channel with highest WTF utility"""
        utilities = [m.utility_wtf for m in metrics]
        return int(np.argmax(utilities))


class HPFACSAlgorithm(ACSAlgorithm):
    """Algorithm 5: Hybrid Proportional Fair ACS (HPF-ACS)"""

    def __init__(self, config: SimulationConfig):
        super().__init__(config, "HPF-ACS (Proposed)")

    def select_channel(self, metrics: List[ChannelMetrics], current_channel: int) -> int:
        """Select channel with highest HPF utility"""
        utilities = [m.utility_hpf for m in metrics]
        return int(np.argmax(utilities))


class AdaptiveHPFACS(ACSAlgorithm):
    """Algorithm 6: Adaptive HPF-ACS with dynamic weights"""

    def __init__(self, config: SimulationConfig):
        super().__init__(config, "Adaptive HPF-ACS")
        self.alpha_max = 0.6
        self.beta_min = 0.2
        self.beta_max = 0.5
        self.gamma = 0.2

    def select_channel(self, metrics: List[ChannelMetrics], current_channel: int) -> int:
        """Select channel using adaptive weighted utility"""
        utilities = []

        for metric in metrics:
            # Adaptive weights based on fairness
            J_c = metric.fairness_index
            beta = self.beta_min + (self.beta_max - self.beta_min) * (1 - J_c)
            alpha = self.alpha_max - (beta - self.beta_min)
            gamma = self.gamma

            # Calculate adaptive utility
            E_c = metric.utilization
            utility = (alpha * E_c +
                      beta * (metric.min_rate / self.config.max_rate) +
                      gamma * J_c)
            utilities.append(utility)

        return int(np.argmax(utilities))


# ============================================================================
# SIMULATOR
# ============================================================================

class PTMPSimulator:
    """Main simulator orchestrating environment and algorithms"""

    def __init__(self, config: SimulationConfig):
        self.config = config
        self.environment = PTMPEnvironment(config)

        # Initialize algorithms
        self.algorithms = {
            'throughput': ThroughputMaximizer(config),
            'mmf': MaxMinFairness(config),
            'jain': JainsFairnessAlgorithm(config),
            'wtf': WTFAlgorithm(config),
            'hpf': HPFACSAlgorithm(config),
            'adaptive_hpf': AdaptiveHPFACS(config),
        }

        # History storage
        self.history = {
            'time': [],
            'interference': {c: deque(maxlen=config.history_length) for c in range(config.n_channels)},
            'throughput': {c: deque(maxlen=config.history_length) for c in range(config.n_channels)},
            'min_rate': {c: deque(maxlen=config.history_length) for c in range(config.n_channels)},
            'fairness': {c: deque(maxlen=config.history_length) for c in range(config.n_channels)},
            'selected_channel': {alg: deque(maxlen=config.history_length) for alg in self.algorithms},
            'metrics': {alg: [] for alg in self.algorithms},
        }

        self.current_metrics = None

    def step(self):
        """Execute one simulation step"""
        # Advance environment
        self.environment.step()

        # Get current metrics for all channels
        self.current_metrics = self.environment.get_all_metrics()

        # Record interference and channel metrics
        self.history['time'].append(self.environment.time_step)

        for c in range(self.config.n_channels):
            self.history['interference'][c].append(self.environment.current_interference[c])
            self.history['throughput'][c].append(self.current_metrics[c].throughput)
            self.history['min_rate'][c].append(self.current_metrics[c].min_rate)
            self.history['fairness'][c].append(self.current_metrics[c].fairness_index)

        # Run each algorithm and record selections
        for alg_name, algorithm in self.algorithms.items():
            channel = algorithm.step(self.current_metrics, self.environment.time_step)
            self.history['selected_channel'][alg_name].append(channel)
            self.history['metrics'][alg_name].append(self.current_metrics[channel])

    def run(self, verbose=False):
        """Run entire simulation"""
        for step in range(self.config.n_time_steps):
            self.step()
            if verbose and step % 20 == 0:
                print(f"Step {step}/{self.config.n_time_steps}")

    def get_summary_stats(self) -> Dict[str, Dict[str, float]]:
        """Calculate summary statistics for each algorithm"""
        stats = {}

        for alg_name in self.algorithms:
            metrics_list = self.history['metrics'][alg_name]

            throughputs = [m.throughput for m in metrics_list]
            min_rates = [m.min_rate for m in metrics_list]
            fairness = [m.fairness_index for m in metrics_list]

            stats[alg_name] = {
                'avg_throughput': np.mean(throughputs),
                'min_throughput': np.min(throughputs),
                'std_throughput': np.std(throughputs),
                'avg_min_rate': np.mean(min_rates),
                'min_min_rate': np.min(min_rates),
                'avg_fairness': np.mean(fairness),
                'switches': len(self.algorithms[alg_name].switch_history),
            }

        return stats


# ============================================================================
# VISUALIZATION
# ============================================================================

class SimulatorVisualizer:
    """Real-time visualization of simulation"""

    def __init__(self, simulator: PTMPSimulator):
        self.simulator = simulator
        self.fig = None
        self.axes = {}

    def create_figure(self):
        """Create visualization figure with multiple subplots"""
        self.fig = plt.figure(figsize=(20, 14))
        self.fig.suptitle('PTMP Auto-Channel Selection Simulator', fontsize=16, fontweight='bold')

        gs = GridSpec(4, 4, figure=self.fig, hspace=0.35, wspace=0.3)

        # Channel throughput over time
        self.axes['throughput'] = self.fig.add_subplot(gs[0, 0:2])
        self.axes['throughput'].set_title('Channel Throughput Over Time')
        self.axes['throughput'].set_xlabel('Time Step')
        self.axes['throughput'].set_ylabel('Throughput (Mbps)')
        self.axes['throughput'].grid(True, alpha=0.3)

        # Minimum rate over time
        self.axes['min_rate'] = self.fig.add_subplot(gs[0, 2:4])
        self.axes['min_rate'].set_title('Minimum Rate (Worst User) Over Time')
        self.axes['min_rate'].set_xlabel('Time Step')
        self.axes['min_rate'].set_ylabel('Min Rate (Mbps)')
        self.axes['min_rate'].grid(True, alpha=0.3)

        # Fairness over time
        self.axes['fairness'] = self.fig.add_subplot(gs[1, 0:2])
        self.axes['fairness'].set_title('Fairness Index Over Time')
        self.axes['fairness'].set_xlabel('Time Step')
        self.axes['fairness'].set_ylabel('Jain FI')
        self.axes['fairness'].set_ylim([0, 1.05])
        self.axes['fairness'].grid(True, alpha=0.3)

        # Interference levels
        self.axes['interference'] = self.fig.add_subplot(gs[1, 2:4])
        self.axes['interference'].set_title('Channel Interference Levels')
        self.axes['interference'].set_xlabel('Time Step')
        self.axes['interference'].set_ylabel('Interference Level')
        self.axes['interference'].set_ylim([0, 1.0])
        self.axes['interference'].grid(True, alpha=0.3)

        # Channel selection heatmap (algorithms x time)
        self.axes['heatmap'] = self.fig.add_subplot(gs[2, :])
        self.axes['heatmap'].set_title('Channel Selection by Algorithm Over Time')
        self.axes['heatmap'].set_xlabel('Time Step')
        self.axes['heatmap'].set_ylabel('Algorithm')

        # Current metrics table
        self.axes['metrics_table'] = self.fig.add_subplot(gs[3, :2])
        self.axes['metrics_table'].axis('off')

        # Station rates comparison
        self.axes['station_rates'] = self.fig.add_subplot(gs[3, 2:])
        self.axes['station_rates'].set_title('Current Station Rates on All Channels')
        self.axes['station_rates'].set_xlabel('Channel')
        self.axes['station_rates'].set_ylabel('Rate (Mbps)')
        self.axes['station_rates'].grid(True, alpha=0.3, axis='y')

    def update(self):
        """Update all plots"""
        self._update_throughput()
        self._update_min_rate()
        self._update_fairness()
        self._update_interference()
        self._update_heatmap()
        self._update_metrics_table()
        self._update_station_rates()

    def _update_throughput(self):
        """Update throughput plot"""
        ax = self.axes['throughput']
        ax.clear()

        for c in range(self.simulator.config.n_channels):
            times = list(range(len(self.simulator.history['throughput'][c])))
            throughputs = list(self.simulator.history['throughput'][c])
            ax.plot(times, throughputs, label=f'Ch {c}', linewidth=2, alpha=0.7)

        ax.set_title('Channel Throughput Over Time')
        ax.set_xlabel('Time Step')
        ax.set_ylabel('Throughput (Mbps)')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)

    def _update_min_rate(self):
        """Update minimum rate plot"""
        ax = self.axes['min_rate']
        ax.clear()

        for c in range(self.simulator.config.n_channels):
            times = list(range(len(self.simulator.history['min_rate'][c])))
            min_rates = list(self.simulator.history['min_rate'][c])
            ax.plot(times, min_rates, label=f'Ch {c}', linewidth=2, alpha=0.7)

        ax.set_title('Minimum Rate (Worst User) Over Time')
        ax.set_xlabel('Time Step')
        ax.set_ylabel('Min Rate (Mbps)')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)

    def _update_fairness(self):
        """Update fairness plot"""
        ax = self.axes['fairness']
        ax.clear()

        for c in range(self.simulator.config.n_channels):
            times = list(range(len(self.simulator.history['fairness'][c])))
            fairness = list(self.simulator.history['fairness'][c])
            ax.plot(times, fairness, label=f'Ch {c}', linewidth=2, alpha=0.7)

        ax.axhline(y=0.95, color='r', linestyle='--', alpha=0.3, label='Target (0.95)')
        ax.set_title('Fairness Index Over Time')
        ax.set_xlabel('Time Step')
        ax.set_ylabel('Jain FI')
        ax.set_ylim([0, 1.05])
        ax.legend(loc='lower right')
        ax.grid(True, alpha=0.3)

    def _update_interference(self):
        """Update interference plot"""
        ax = self.axes['interference']
        ax.clear()

        for c in range(self.simulator.config.n_channels):
            times = list(range(len(self.simulator.history['interference'][c])))
            interference = list(self.simulator.history['interference'][c])
            ax.plot(times, interference, label=f'Ch {c}', linewidth=2, alpha=0.7)

        ax.set_title('Channel Interference Levels')
        ax.set_xlabel('Time Step')
        ax.set_ylabel('Interference Level')
        ax.set_ylim([0, 1.0])
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)

    def _update_heatmap(self):
        """Update channel selection heatmap"""
        ax = self.axes['heatmap']
        ax.clear()

        # Create matrix of selections (algorithms x time)
        alg_names = list(self.simulator.algorithms.keys())
        n_steps = min(self.simulator.config.history_length,
                     len(list(self.simulator.history['selected_channel'].values())[0]))

        heatmap_data = np.zeros((len(alg_names), n_steps))

        for i, alg_name in enumerate(alg_names):
            selections = list(self.simulator.history['selected_channel'][alg_name])[-n_steps:]
            heatmap_data[i, :] = selections

        im = ax.imshow(heatmap_data, aspect='auto', cmap='tab10', vmin=0,
                      vmax=self.simulator.config.n_channels-1)
        ax.set_yticks(range(len(alg_names)))
        ax.set_yticklabels([self.simulator.algorithms[a].name for a in alg_names], fontsize=9)
        ax.set_xlabel('Time Step')
        ax.set_ylabel('Algorithm')
        ax.set_title('Channel Selection by Algorithm Over Time')
        plt.colorbar(im, ax=ax, label='Channel ID')

    def _update_metrics_table(self):
        """Update metrics comparison table"""
        ax = self.axes['metrics_table']
        ax.clear()
        ax.axis('off')

        if self.simulator.current_metrics is None:
            return

        # Prepare table data
        columns = ['Algorithm', 'Current Ch', 'Throughput', 'Min Rate', 'Fairness', 'Switches']
        table_data = []

        for alg_name, algorithm in self.simulator.algorithms.items():
            current_ch = algorithm.current_channel
            metric = self.simulator.current_metrics[current_ch]
            switches = len(algorithm.switch_history)

            table_data.append([
                algorithm.name[:20],
                f'Ch{current_ch}',
                f'{metric.throughput:.1f}',
                f'{metric.min_rate:.1f}',
                f'{metric.fairness_index:.3f}',
                f'{switches}'
            ])

        table = ax.table(cellText=table_data, colLabels=columns,
                        cellLoc='center', loc='center',
                        bbox=[0, 0, 1, 1])
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)

        # Color header
        for i in range(len(columns)):
            table[(0, i)].set_facecolor('#40466e')
            table[(0, i)].set_text_props(weight='bold', color='white')

    def _update_station_rates(self):
        """Update station rates bar chart"""
        ax = self.axes['station_rates']
        ax.clear()

        if self.simulator.current_metrics is None:
            return

        # Get rates for all stations on all channels
        rates = self.simulator.environment.smoothed_rates

        x = np.arange(self.simulator.config.n_channels)
        width = 0.08

        for i in range(self.simulator.config.n_stations):
            offset = (i - self.simulator.config.n_stations/2) * width
            ax.bar(x + offset, rates[i, :], width, label=f'St{i}', alpha=0.7)

        ax.set_xlabel('Channel')
        ax.set_ylabel('Smoothed Rate (Mbps)')
        ax.set_title('Current Station Rates on All Channels')
        ax.set_xticks(x)
        ax.set_xticklabels([f'Ch{c}' for c in range(self.simulator.config.n_channels)])
        ax.legend(loc='upper right', ncol=4, fontsize=8)
        ax.grid(True, alpha=0.3, axis='y')

    def show(self):
        """Display the visualization"""
        self.create_figure()
        self.update()
        plt.tight_layout()
        plt.show()

    def animate(self, interval=100):
        """Create animation of simulation"""
        self.create_figure()

        def animate_step(frame):
            self.update()
            if frame < self.simulator.config.n_time_steps - 1:
                self.simulator.step()

        anim = animation.FuncAnimation(
            self.fig, animate_step, frames=self.simulator.config.n_time_steps,
            interval=interval, repeat=True
        )

        plt.tight_layout()
        plt.show()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution script"""
    print("=" * 80)
    print("PTMP Auto-Channel Selection Simulator")
    print("=" * 80)

    # Configuration
    config = SimulationConfig(
        n_stations=8,
        n_channels=4,
        n_time_steps=200,
        min_rate=5.0,
        max_rate=100.0,
        fairness_param=0.3,  # 0: random, 1: deterministic
        base_interference=[0.2, 0.4, 0.1, 0.3],
        switch_threshold=0.08,
        ewma_factor=0.3,
        min_dwell_time=10,
    )

    print(f"\nConfiguration:")
    print(f"  Stations: {config.n_stations}")
    print(f"  Channels: {config.n_channels}")
    print(f"  Time steps: {config.n_time_steps}")
    print(f"  Rate range: {config.min_rate}-{config.max_rate} Mbps")
    print(f"  Fairness param: {config.fairness_param}")
    print(f"  Base interference: {config.base_interference}")
    print(f"  Switch threshold: {config.switch_threshold * 100}%")
    print(f"  EWMA factor: {config.ewma_factor}")

    # Create and run simulator
    print("\nRunning simulation...")
    simulator = PTMPSimulator(config)
    simulator.run(verbose=True)

    # Print statistics
    print("\nSimulation Results:")
    print("-" * 80)
    stats = simulator.get_summary_stats()

    for alg_name, stat in stats.items():
        print(f"\n{simulator.algorithms[alg_name].name}:")
        print(f"  Avg Throughput: {stat['avg_throughput']:.2f} Mbps")
        print(f"  Min Throughput: {stat['min_throughput']:.2f} Mbps")
        print(f"  Throughput Std Dev: {stat['std_throughput']:.2f} Mbps")
        print(f"  Avg Min Rate: {stat['avg_min_rate']:.2f} Mbps")
        print(f"  Worst Min Rate: {stat['min_min_rate']:.2f} Mbps")
        print(f"  Avg Fairness: {stat['avg_fairness']:.4f}")
        print(f"  Channel Switches: {stat['switches']}")

    # Visualize
    print("\nGenerating visualization...")
    visualizer = SimulatorVisualizer(simulator)
    visualizer.show()


if __name__ == "__main__":
    main()
