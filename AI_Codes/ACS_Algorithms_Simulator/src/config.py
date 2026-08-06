"""
Configuration module for PTMP ACS Simulator
Centralized parameters for simulation, environment, and algorithms
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SimulationConfig:
    """Central configuration for simulation parameters"""

    # Network topology
    n_stations: int = 8
    n_channels: int = 5
    n_time_steps: int = 200

    # Channel model parameters
    min_rate: float = 5.0              # Mbps at max distance
    max_rate: float = 100.0            # Mbps at zero distance
    max_distance: float = 1.0          # Normalized distance [0, 1]

    # Interference model (Gauss-Markov)
    base_interference: Optional[List[float]] = None  # Per-channel mean interference
    interference_mean: float = 0.2                   # Global mean if not per-channel
    interference_std_factor: float = 0.1             # std = factor * mean
    gauss_markov_rho: float = 0.7                    # Temporal correlation [0, 1]

    # EWMA filtering
    ewma_factor: float = 0.3           # Weight for new samples [0, 1]

    # Algorithm switching
    switch_threshold: float = 0.08     # % improvement needed to switch
    min_dwell_time: int = 10           # Min timesteps before next switch

    # Fairness/utility weighting
    fairness_param: float = 0.5        # Position distribution fairness [0, 1]

    # Random seed
    seed: Optional[int] = None         # For reproducibility

    def __post_init__(self):
        """Validate and initialize parameters"""
        # Initialize per-channel interference if not provided
        if self.base_interference is None:
            self.base_interference = [self.interference_mean] * self.n_channels

        # Ensure lists are correct size
        assert len(self.base_interference) == self.n_channels, \
            f"base_interference length ({len(self.base_interference)}) must match n_channels ({self.n_channels})"

        # Validate parameter ranges
        assert 0 < self.ewma_factor <= 1, "ewma_factor must be in (0, 1]"
        assert 0 <= self.gauss_markov_rho < 1, "gauss_markov_rho must be in [0, 1)"
        assert 0 < self.switch_threshold < 1, "switch_threshold must be in (0, 1)"
        assert self.min_dwell_time >= 0, "min_dwell_time must be >= 0"
        assert 0 <= self.fairness_param <= 1, "fairness_param must be in [0, 1]"


# Preset configurations for common scenarios

def config_balanced() -> SimulationConfig:
    """Balanced configuration: moderate interference, fairness-aware"""
    return SimulationConfig(
        n_stations=8,
        n_channels=5,
        n_time_steps=200,
        base_interference=[0.15, 0.35, 0.25, 0.10, 0.40],
        switch_threshold=0.08,
        min_dwell_time=10,
        ewma_factor=0.3,
        fairness_param=0.5,
    )


def config_high_fairness() -> SimulationConfig:
    """High fairness: uniform station distribution, low interference"""
    return SimulationConfig(
        n_stations=12,
        n_channels=6,
        n_time_steps=300,
        base_interference=[0.10] * 6,
        switch_threshold=0.05,
        min_dwell_time=15,
        ewma_factor=0.2,
        fairness_param=1.0,
    )


def config_high_dynamics() -> SimulationConfig:
    """High dynamics: varying interference, aggressive switching"""
    return SimulationConfig(
        n_stations=6,
        n_channels=4,
        n_time_steps=250,
        base_interference=[0.30, 0.50, 0.20, 0.60],
        switch_threshold=0.02,
        min_dwell_time=5,
        ewma_factor=0.4,
        fairness_param=0.3,
        gauss_markov_rho=0.9,
    )


def config_stable() -> SimulationConfig:
    """Stable environment: low interference variance, conservative switching"""
    return SimulationConfig(
        n_stations=10,
        n_channels=5,
        n_time_steps=500,
        base_interference=[0.15] * 5,
        interference_std_factor=0.05,
        switch_threshold=0.15,
        min_dwell_time=30,
        ewma_factor=0.1,
        fairness_param=0.8,
        gauss_markov_rho=0.95,
    )


def config_highly_variable() -> SimulationConfig:
    """Highly variable interference: tests adaptation capability"""
    return SimulationConfig(
        n_stations=8,
        n_channels=5,
        n_time_steps=300,
        base_interference=[0.20, 0.60, 0.15, 0.50, 0.35],
        interference_std_factor=0.3,      # High noise
        switch_threshold=0.03,             # Aggressive
        min_dwell_time=3,
        ewma_factor=0.4,
        fairness_param=0.5,
        gauss_markov_rho=0.4,             # Low correlation (jittery)
    )


def config_fairness_critical() -> SimulationConfig:
    """Fairness-critical: uniform positions, require high fairness"""
    return SimulationConfig(
        n_stations=12,
        n_channels=6,
        n_time_steps=250,
        base_interference=[0.12] * 6,
        interference_std_factor=0.08,
        switch_threshold=0.10,
        min_dwell_time=12,
        ewma_factor=0.25,
        fairness_param=1.0,               # Uniform positions
        gauss_markov_rho=0.85,
    )


def config_throughput_critical() -> SimulationConfig:
    """Throughput-critical: maximize capacity with some fairness"""
    return SimulationConfig(
        n_stations=6,
        n_channels=4,
        n_time_steps=200,
        base_interference=[0.10, 0.25, 0.15, 0.30],
        interference_std_factor=0.12,
        switch_threshold=0.05,
        min_dwell_time=5,
        ewma_factor=0.35,
        fairness_param=0.2,               # Random positions
        gauss_markov_rho=0.6,
    )
