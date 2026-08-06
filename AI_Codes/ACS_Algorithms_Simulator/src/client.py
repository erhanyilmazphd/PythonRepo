"""
Client class representing a user device in PTMP network
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class ClientMetrics:
    """Metrics for a single client"""
    client_id: int
    distance: float              # Normalized distance [0, 1]
    rates: np.ndarray            # Rate per channel (n_channels,)
    current_channel: int         # Channel currently on


class Client:
    """
    Represents a client device in the PTMP network.
    Characterized by distance from AP (affects base rate).
    """

    def __init__(self, client_id: int, distance: float, n_channels: int):
        self.client_id = client_id
        self.distance = np.clip(distance, 0, 1)  # Normalize to [0, 1]
        self.n_channels = n_channels

        # Rates per channel
        self.rates = np.zeros(n_channels)

    def set_rates(self, rates: np.ndarray):
        """Update rates for all channels"""
        assert len(rates) == self.n_channels, "Rates length mismatch"
        self.rates = np.array(rates)

    def get_rate(self, channel_id: int) -> float:
        """Get rate on specific channel"""
        return self.rates[channel_id]

    def get_metrics(self) -> ClientMetrics:
        """Return current metrics"""
        return ClientMetrics(
            client_id=self.client_id,
            distance=self.distance,
            rates=np.copy(self.rates),
            current_channel=-1,  # Set by AP when assigning channel
        )
