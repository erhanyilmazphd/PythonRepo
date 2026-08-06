"""
Channel model with Gauss-Markov interference process
Implements realistic temporal correlation in interference
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class ChannelState:
    """State of a single channel at a timestep"""
    channel_id: int
    base_rate: float           # Rate at zero interference
    current_interference: float  # Current interference level
    effective_rate: float      # base_rate * (1 - interference)


class Channel:
    """
    Models a wireless channel with:
    - Distance-based rate degradation
    - Gauss-Markov interference process (temporally correlated)
    - EWMA filtering of rates
    """

    def __init__(self, channel_id: int, config):
        self.channel_id = channel_id
        self.config = config

        # Interference state (Gauss-Markov)
        self.current_interference = config.base_interference[channel_id]
        self.mean_interference = config.base_interference[channel_id]
        self.rho = config.gauss_markov_rho  # Correlation coefficient [0, 1)

        # EWMA state for rate smoothing
        self.smoothed_rate = config.max_rate
        self.ewma_factor = config.ewma_factor

    def get_base_rate(self, distance: float) -> float:
        """
        Compute base rate from distance (no interference).
        Formula: R_i = R_max - (R_max - R_min) * d_i
        where d_i in [0, 1] is normalized distance.
        """
        return self.config.max_rate - (
            self.config.max_rate - self.config.min_rate
        ) * distance

    def apply_interference(self, base_rate: float) -> float:
        """Apply current interference to base rate.
        Formula: R = R_base * (1 - I) where I is interference level.
        """
        return base_rate * (1.0 - self.current_interference)

    def step(self):
        """
        Update channel state for next timestep.
        Implements Gauss-Markov process for interference:
        I(t+1) = ρ*I(t) + (1-ρ)*μ + w(t)
        where w(t) ~ N(0, σ²) with σ = std_factor * μ
        """
        # Gaussian noise
        sigma = self.config.interference_std_factor * self.mean_interference
        noise = np.random.normal(0, sigma)

        # Gauss-Markov update
        self.current_interference = (
            self.rho * self.current_interference
            + (1 - self.rho) * self.mean_interference
            + noise
        )

        # Clamp to valid range [0, 1]
        self.current_interference = np.clip(self.current_interference, 0, 1)

    def get_state(self) -> ChannelState:
        """Return current channel state"""
        return ChannelState(
            channel_id=self.channel_id,
            base_rate=self.smoothed_rate,
            current_interference=self.current_interference,
            effective_rate=self.smoothed_rate * (1.0 - self.current_interference),
        )

    def update_smoothed_rate(self, instantaneous_rate: float):
        """Apply EWMA smoothing to rate.
        Formula: R_new = α*R_inst + (1-α)*R_old
        """
        self.smoothed_rate = (
            self.ewma_factor * instantaneous_rate
            + (1 - self.ewma_factor) * self.smoothed_rate
        )
