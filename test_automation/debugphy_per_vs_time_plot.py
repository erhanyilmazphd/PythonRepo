#!/usr/bin/env python3
"""
Script to parse WiFi log file and plot Time vs PER (Packet Error Rate)
Extracts timestamp and PER% from log entries
"""

import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np


def parse_log_file(filename):
    """
    Parse the log file to extract timestamp and PER data

    Expected format after PER% header:
    MAC_ADDRESS TIMESTAMP TYPE |TxMbps TxPkts Rate BW MCS Pow PER% ...
    """
    timestamps = []
    per_values = []

    with open(filename, 'r') as f:
        lines = f.readlines()

    # Find lines that contain actual data (MAC address at start)
    mac_pattern = re.compile(
        r'^([0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2})\s+(\d+)\s+\w+\s*\|')

    first_timestamp = None

    for line in lines:
        match = mac_pattern.match(line)
        if match:
            mac = match.group(1)
            timestamp = int(match.group(2))

            # Store first timestamp as reference
            if first_timestamp is None:
                first_timestamp = timestamp

            # Split the line to extract PER value
            # Format: MAC TSTAMP TYPE |TxMbps TxPkts Rate BW MCS Pow PER% ...
            parts = line.split('|')
            if len(parts) > 1:
                tx_stats = parts[1].split()
                if len(tx_stats) >= 7:
                    try:
                        per = float(tx_stats[6])  # PER% is the 7th field

                        # Convert to relative time in seconds from first timestamp
                        relative_time = timestamp - first_timestamp

                        timestamps.append(relative_time)
                        per_values.append(per)
                    except (ValueError, IndexError):
                        continue

    return timestamps, per_values, first_timestamp


def plot_per_vs_time(timestamps, per_values, first_timestamp, output_file='per_vs_time_plot.png'):
    """
    Create a plot of PER vs Time
    timestamps: relative time in seconds from start
    """
    fig, ax = plt.subplots(figsize=(14, 7))

    # Convert timestamps to minutes for better readability
    time_minutes = [t / 60.0 for t in timestamps]

    # Plot the data
    ax.plot(time_minutes, per_values, marker='o', markersize=2, linestyle='-',
            linewidth=0.8, color='#2E86AB', alpha=0.6, label='PER%')

    # Add rolling average for better trend visualization
    if len(per_values) > 50:
        window_size = min(50, len(per_values) // 20)
        rolling_avg = np.convolve(per_values, np.ones(window_size) / window_size, mode='valid')
        rolling_time = time_minutes[window_size - 1:]
        ax.plot(rolling_time, rolling_avg, color='#A23B72', linewidth=2.5,
                label=f'Moving Average (window={window_size})', alpha=0.8)

    # Formatting
    ax.set_xlabel('Time (minutes)', fontsize=12, fontweight='bold')
    ax.set_ylabel('PER (%)', fontsize=12, fontweight='bold')
    ax.set_title('Packet Error Rate (PER) vs Time', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper right', fontsize=10)

    # Set y-axis limits with some padding
    if per_values:
        y_min = min(per_values)
        y_max = max(per_values)
        y_range = y_max - y_min if y_max > y_min else 1
        ax.set_ylim(max(0, y_min - 0.1 * y_range), y_max + 0.1 * y_range)

    # Add info text
    duration_sec = timestamps[-1] if timestamps else 0
    duration_str = f"{int(duration_sec // 3600)}h {int((duration_sec % 3600) // 60)}m {int(duration_sec % 60)}s"
    info_text = f"Duration: {duration_str} | Samples: {len(timestamps)}"
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
            fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()

    # Save the plot
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Plot saved to: {output_file}")

    return fig, ax


def print_statistics(per_values):
    """
    Print basic statistics about the PER data
    """
    if not per_values:
        print("No PER data found!")
        return

    print("\n" + "=" * 60)
    print("PER STATISTICS")
    print("=" * 60)
    print(f"Total samples:     {len(per_values)}")
    print(f"Mean PER:          {np.mean(per_values):.3f}%")
    print(f"Median PER:        {np.median(per_values):.3f}%")
    print(f"Std Dev:           {np.std(per_values):.3f}%")
    print(f"Min PER:           {np.min(per_values):.3f}%")
    print(f"Max PER:           {np.max(per_values):.3f}%")
    print(
        f"PER = 0:           {sum(1 for p in per_values if p == 0)} samples ({100 * sum(1 for p in per_values if p == 0) / len(per_values):.1f}%)")
    print(
        f"PER > 0:           {sum(1 for p in per_values if p > 0)} samples ({100 * sum(1 for p in per_values if p > 0) / len(per_values):.1f}%)")
    print(
        f"PER > 1:           {sum(1 for p in per_values if p > 1)} samples ({100 * sum(1 for p in per_values if p > 1) / len(per_values):.1f}%)")
    print(
        f"PER > 5:           {sum(1 for p in per_values if p > 5)} samples ({100 * sum(1 for p in per_values if p > 5) / len(per_values):.1f}%)")
    print("=" * 60 + "\n")


def main():
    # Input file
    input_file = 'test_automation/loga6_1202.txt'
    output_file = 'test_automation/per_vs_time_plot.png'

    print("Parsing log file...")
    timestamps, per_values, first_timestamp = parse_log_file(input_file)

    if not timestamps:
        print("Error: No PER data found in the log file!")
        return

    print(f"Found {len(timestamps)} data points")
    duration_sec = timestamps[-1] if timestamps else 0
    duration_str = f"{int(duration_sec // 3600)}h {int((duration_sec % 3600) // 60)}m {int(duration_sec % 60)}s"
    print(f"Time range: 0s to {timestamps[-1]}s (Duration: {duration_str})")
    print(f"First timestamp value: {first_timestamp}")

    # Print statistics
    print_statistics(per_values)

    # Create plot
    print("Creating plot...")
    plot_per_vs_time(timestamps, per_values, first_timestamp, output_file)

    print("\nDone!")


if __name__ == "__main__":
    main()