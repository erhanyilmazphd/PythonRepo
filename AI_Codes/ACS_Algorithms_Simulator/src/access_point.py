"""
Access Point managing clients and channel selection
"""

import numpy as np
from dataclasses import dataclass
from typing import List

try:
    from .client import Client
except ImportError:
    from client import Client


@dataclass
class APMetrics:
    """Metrics for AP's current channel"""
    current_channel: int
    throughput: float              # Sum of all client rates
    min_rate: float                # Worst user rate
    max_rate: float                # Best user rate
    mean_rate: float               # Average rate
    fairness_index: float          # Jain's fairness index


class AccessPoint:
    """
    Access Point managing one or more clients.
    Handles channel selection and aggregates client metrics.
    """

    def __init__(self, ap_id: int, clients: List[Client], n_channels: int):
        self.ap_id = ap_id
        self.clients = clients
        self.n_channels = n_channels
        self.current_channel = 0  # Start on channel 0

    def set_channel(self, channel_id: int):
        """Switch to specified channel"""
        assert 0 <= channel_id < self.n_channels, f"Invalid channel {channel_id}"
        self.current_channel = channel_id

    def compute_metrics(self) -> APMetrics:
        """Compute aggregate metrics for current channel"""
        rates = np.array([c.get_rate(self.current_channel) for c in self.clients])

        throughput = np.sum(rates)
        min_rate = np.min(rates)
        max_rate = np.max(rates)
        mean_rate = np.mean(rates)

        # Jain's Fairness Index
        if np.sum(rates) > 0:
            fairness = (np.sum(rates) ** 2) / (len(rates) * np.sum(rates ** 2))
        else:
            fairness = 0.0

        return APMetrics(
            current_channel=self.current_channel,
            throughput=throughput,
            min_rate=min_rate,
            max_rate=max_rate,
            mean_rate=mean_rate,
            fairness_index=fairness,
        )

    def get_all_channel_metrics(self) -> List[APMetrics]:
        """Compute metrics for all channels (for decision making)"""
        metrics = []
        for ch in range(self.n_channels):
            # Temporarily switch to compute metrics
            old_ch = self.current_channel
            self.current_channel = ch
            metrics.append(self.compute_metrics())
            self.current_channel = old_ch
        return metrics
