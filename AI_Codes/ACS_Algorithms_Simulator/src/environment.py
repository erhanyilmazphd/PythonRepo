"""
PTMP Wireless Environment
Orchestrates channels, clients, and interference
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Optional

try:
    from .channel import Channel
    from .client import Client
    from .access_point import AccessPoint, APMetrics
except ImportError:
    from channel import Channel
    from client import Client
    from access_point import AccessPoint, APMetrics


@dataclass
class EnvironmentState:
    """Current state of the environment"""
    timestep: int
    interference_levels: List[float]
    channel_metrics: List[APMetrics]  # Metrics for all channels
    client_rates: np.ndarray           # Shape: (n_clients, n_channels)


class WirelessEnvironment:
    """
    Simulates PTMP (Point-to-Multipoint) wireless environment.
    - Multiple channels with independent Gauss-Markov interference
    - Clients with distance-based rate degradation
    - Single AP managing all clients
    """

    def __init__(self, config):
        self.config = config
        self.timestep = 0

        # Initialize random seed if provided
        if config.seed is not None:
            np.random.seed(config.seed)

        # Create channels
        self.channels: List[Channel] = [
            Channel(ch_id, config) for ch_id in range(config.n_channels)
        ]

        # Create clients with random distances
        # Fairness param controls distribution: 0=random, 1=uniform
        if config.fairness_param == 1.0:
            # Uniform distribution
            distances = np.linspace(0, config.max_distance, config.n_stations)
        else:
            # Random distribution with fairness weighting
            distances = np.random.uniform(0, config.max_distance, config.n_stations)

        self.clients: List[Client] = [
            Client(i, distances[i], config.n_channels) for i in range(config.n_stations)
        ]

        # Create AP managing all clients
        self.access_point = AccessPoint(0, self.clients, config.n_channels)

    def step(self):
        """
        Execute one timestep of environment simulation:
        1. Update channel interference (Gauss-Markov)
        2. Compute client rates based on distance and interference
        3. Apply EWMA smoothing
        4. Log state
        """
        self.timestep += 1

        # Update interference on each channel
        for channel in self.channels:
            channel.step()

        # Compute rates for all clients on all channels
        client_rates = np.zeros((len(self.clients), self.config.n_channels))

        for client_idx, client in enumerate(self.clients):
            for ch_idx, channel in enumerate(self.channels):
                # Get base rate (distance-based)
                base_rate = channel.get_base_rate(client.distance)

                # Apply interference
                effective_rate = channel.apply_interference(base_rate)

                # Update EWMA smoothing
                channel.update_smoothed_rate(effective_rate)

                # Store rate
                client_rates[client_idx, ch_idx] = channel.smoothed_rate

        # Update client rates
        for client_idx, client in enumerate(self.clients):
            client.set_rates(client_rates[client_idx, :])

    def get_state(self) -> EnvironmentState:
        """Return current environment state"""
        interference = [ch.current_interference for ch in self.channels]
        metrics = self.access_point.get_all_channel_metrics()

        client_rates = np.array([c.rates for c in self.clients])

        return EnvironmentState(
            timestep=self.timestep,
            interference_levels=interference,
            channel_metrics=metrics,
            client_rates=client_rates,
        )

    def get_interference_levels(self) -> List[float]:
        """Get current interference on each channel"""
        return [ch.current_interference for ch in self.channels]

    def get_client_rates(self) -> np.ndarray:
        """Get rates for all clients on all channels"""
        return np.array([c.rates for c in self.clients])

    def get_channel_metrics_all(self) -> List[APMetrics]:
        """Get metrics for all channels"""
        return self.access_point.get_all_channel_metrics()

    def set_channel(self, channel_id: int):
        """Set AP to specific channel"""
        self.access_point.set_channel(channel_id)

    def get_current_metrics(self) -> APMetrics:
        """Get metrics for current channel"""
        return self.access_point.compute_metrics()
