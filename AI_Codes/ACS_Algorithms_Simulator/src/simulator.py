"""
Headless PTMP ACS Simulator
Orchestrates environment and algorithms without GUI
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional
from abc import ABC, abstractmethod

try:
    from .config import SimulationConfig
    from .environment import WirelessEnvironment, EnvironmentState
except ImportError:
    from config import SimulationConfig
    from environment import WirelessEnvironment, EnvironmentState


@dataclass
class Metrics:
    """Per-timestep metrics for an algorithm"""
    timestep: int
    throughput: float
    min_rate: float
    max_rate: float
    mean_rate: float
    fairness_index: float
    current_channel: int


class ACSAlgorithm(ABC):
    """
    Abstract base class for ACS algorithms.
    Each algorithm decides channel selection based on metrics.
    """

    def __init__(self, name: str, config: SimulationConfig):
        self.name = name
        self.config = config
        self.current_channel = 0
        self.switch_history: List[tuple] = []  # [(timestep, new_channel), ...]
        self.metrics_history: List[Metrics] = []
        self.last_switch_time = -config.min_dwell_time  # Allow switch at t=0

    @abstractmethod
    def compute_utility(self, metrics: List) -> List[float]:
        """
        Compute utility for each channel.
        Args: metrics - list of APMetrics for each channel
        Returns: list of utility scores
        """
        pass

    def decide_channel(self, environment: WirelessEnvironment) -> int:
        """
        Make channel decision with hysteresis.
        - Check minimum dwell time
        - Compute utility for all channels
        - Switch if improvement exceeds threshold
        """
        env_state = environment.get_state()
        metrics = env_state.channel_metrics

        # Check dwell time constraint
        if env_state.timestep - self.last_switch_time < self.config.min_dwell_time:
            return self.current_channel

        # Compute utilities
        utilities = self.compute_utility(metrics)

        # Find best channel
        best_channel = np.argmax(utilities)
        current_utility = utilities[self.current_channel]
        best_utility = utilities[best_channel]

        # Apply hysteresis threshold
        if best_channel != self.current_channel:
            improvement = (best_utility - current_utility) / (abs(current_utility) + 1e-6)
            if improvement > self.config.switch_threshold:
                self.current_channel = best_channel
                self.last_switch_time = env_state.timestep
                self.switch_history.append((env_state.timestep, best_channel))

        return self.current_channel

    def step(self, environment: WirelessEnvironment):
        """Execute one timestep: decide and record metrics"""
        # Make channel decision
        channel = self.decide_channel(environment)
        environment.set_channel(channel)

        # Record metrics
        current_metrics = environment.get_current_metrics()
        self.metrics_history.append(
            Metrics(
                timestep=environment.timestep,
                throughput=current_metrics.throughput,
                min_rate=current_metrics.min_rate,
                max_rate=current_metrics.max_rate,
                mean_rate=current_metrics.mean_rate,
                fairness_index=current_metrics.fairness_index,
                current_channel=current_metrics.current_channel,
            )
        )


# Concrete ACS Algorithm Implementations

class ThroughputMaximizer(ACSAlgorithm):
    """Maximize total throughput (sum of rates)"""

    def __init__(self, config: SimulationConfig):
        super().__init__("Throughput Maximizer", config)

    def compute_utility(self, metrics: List) -> List[float]:
        return [m.throughput for m in metrics]


class ProportionalFair(ACSAlgorithm):
    """Pure proportional fairness (sum of logarithms)"""

    def __init__(self, config: SimulationConfig):
        super().__init__("Proportional Fair", config)

    def compute_utility(self, metrics: List) -> List[float]:
        return [np.log(m.throughput + 1.0) for m in metrics]


class MaxMinFairness(ACSAlgorithm):
    """Maximize minimum rate (protect worst user)"""

    def __init__(self, config: SimulationConfig):
        super().__init__("Max-Min Fairness", config)

    def compute_utility(self, metrics: List) -> List[float]:
        return [m.min_rate for m in metrics]


class JainsFairnessAlgorithm(ACSAlgorithm):
    """Maximize Jain's fairness index"""

    def __init__(self, config: SimulationConfig):
        super().__init__("Jain's Fairness", config)

    def compute_utility(self, metrics: List) -> List[float]:
        return [m.fairness_index for m in metrics]


class HybridHPF(ACSAlgorithm):
    """
    Hybrid proportional fairness.
    Utility = α*efficiency + β*fairness + γ*min_rate
    """

    def __init__(self, config: SimulationConfig, alpha=0.5, beta=0.3, gamma=0.2):
        super().__init__("Hybrid HPF", config)
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def compute_utility(self, metrics: List) -> List[float]:
        utilities = []
        for m in metrics:
            # Normalize components
            efficiency = m.throughput / (self.config.max_rate * self.config.n_stations + 1e-6)
            fairness = m.fairness_index  # Already in [0, 1]
            min_rate_norm = m.min_rate / (self.config.max_rate + 1e-6)

            utility = (
                self.alpha * efficiency
                + self.beta * fairness
                + self.gamma * min_rate_norm
            )
            utilities.append(utility)
        return utilities


class AdaptiveHPF(ACSAlgorithm):
    """
    Adaptive hybrid proportional fairness.
    Adjusts weights based on fairness trend.
    """

    def __init__(self, config: SimulationConfig):
        super().__init__("Adaptive HPF", config)
        self.fairness_history: List[float] = []
        self.alpha = 0.5
        self.beta = 0.3
        self.gamma = 0.2

    def update_weights(self):
        """Adjust weights based on recent fairness trend"""
        if len(self.fairness_history) < 10:
            return

        recent_fairness = self.fairness_history[-10:]
        trend = recent_fairness[-1] - recent_fairness[0]

        # If fairness declining, increase fairness weight
        if trend < 0:
            self.beta = min(0.7, self.beta + 0.05)
            self.alpha = max(0.1, self.alpha - 0.03)
        # If fairness good, can prioritize efficiency
        elif trend > 0.02:
            self.alpha = min(0.7, self.alpha + 0.05)
            self.beta = max(0.1, self.beta - 0.03)

    def compute_utility(self, metrics: List) -> List[float]:
        self.update_weights()

        utilities = []
        for m in metrics:
            efficiency = m.throughput / (self.config.max_rate * self.config.n_stations + 1e-6)
            fairness = m.fairness_index
            min_rate_norm = m.min_rate / (self.config.max_rate + 1e-6)

            utility = (
                self.alpha * efficiency
                + self.beta * fairness
                + self.gamma * min_rate_norm
            )
            utilities.append(utility)
            self.fairness_history.append(fairness)

        return utilities


class PTMPSimulator:
    """
    Main headless simulator orchestrating environment and algorithms.
    """

    def __init__(self, config: SimulationConfig):
        self.config = config
        self.environment = WirelessEnvironment(config)

        # Initialize all algorithms
        self.algorithms: Dict[str, ACSAlgorithm] = {
            "throughput": ThroughputMaximizer(config),
            "proportional_fair": ProportionalFair(config),
            "max_min": MaxMinFairness(config),
            "jain": JainsFairnessAlgorithm(config),
            "hpf": HybridHPF(config),
            "adaptive_hpf": AdaptiveHPF(config),
        }

    def run(self, verbose: bool = False):
        """Run simulation for n_time_steps"""
        for step in range(self.config.n_time_steps):
            # Environment step
            self.environment.step()

            # Each algorithm makes decision
            for algo in self.algorithms.values():
                algo.step(self.environment)

            if verbose and (step + 1) % 50 == 0:
                print(f"Timestep {step + 1}/{self.config.n_time_steps}")

    def get_summary(self) -> Dict:
        """Return summary statistics for all algorithms"""
        summary = {}
        for name, algo in self.algorithms.items():
            if not algo.metrics_history:
                continue

            metrics = algo.metrics_history
            throughputs = [m.throughput for m in metrics]
            fairness = [m.fairness_index for m in metrics]
            min_rates = [m.min_rate for m in metrics]

            summary[name] = {
                "avg_throughput": float(np.mean(throughputs)),
                "std_throughput": float(np.std(throughputs)),
                "avg_fairness": float(np.mean(fairness)),
                "std_fairness": float(np.std(fairness)),
                "avg_min_rate": float(np.mean(min_rates)),
                "std_min_rate": float(np.std(min_rates)),
                "total_switches": len(algo.switch_history),
            }

        return summary
