# PTMP Auto-Channel Selection Simulator

A comprehensive Python simulator for benchmarking Automatic Channel Selection (ACS) algorithms in Point-to-Multipoint (PTMP) wireless networks.

## Overview

This simulator models a realistic PTMP wireless environment where an Access Point (AP) communicates with multiple client stations over multiple channels. Each station experiences heterogeneous channel conditions due to:

- **Distance from AP** (determines base rates)
- **Interference** (varies per channel and over time)
- **Multipath fading** (simulated via EWMA smoothing)

Six different ACS algorithms are implemented and compared based on their ability to balance:
- **Throughput** (aggregate data rate)
- **Fairness** (protection for worst-performing users)
- **Switching Stability** (minimizing channel oscillations)

---

## Architecture

### Core Components

```
ptmp_acs_simulator.py
├── SimulationConfig          # Configuration parameters
├── StationMetrics            # Per-station data
├── ChannelMetrics            # Per-channel performance metrics
├── PTMPEnvironment           # Wireless environment simulation
├── ACSAlgorithm              # Base algorithm class
│   ├── ThroughputMaximizer   # Algorithm 1
│   ├── MaxMinFairness        # Algorithm 2
│   ├── JainsFairnessAlgorithm # Algorithm 3
│   ├── WTFAlgorithm          # Algorithm 4
│   ├── HPFACSAlgorithm       # Algorithm 5
│   └── AdaptiveHPFACS        # Algorithm 6
├── PTMPSimulator             # Main simulator
└── SimulatorVisualizer       # Real-time visualization
```

### Data Flow

```
SimulationConfig
        ↓
   PTMPEnvironment (wireless medium simulation)
        ↓
   Get Channel Metrics
        ↓
   ACS Algorithms (decision making)
        ↓
   Record Metrics & History
        ↓
   SimulatorVisualizer (real-time display or PNG output)
```

---

## Configuration Parameters

### Basic Settings

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `n_stations` | int | 1-100 | 8 | Number of client stations |
| `n_channels` | int | 1-16 | 4 | Number of available channels |
| `n_time_steps` | int | 1-10000 | 200 | Simulation duration |

### Rate Parameters

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `min_rate` | float | 0-200 Mbps | 5.0 | Minimum achievable rate |
| `max_rate` | float | 0-200 Mbps | 100.0 | Maximum achievable rate |
| `fairness_param` | float | 0.0-1.0 | 0.5 | 0=random distribution, 1=uniform |

### Interference

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `base_interference` | list | 0.0-1.0 | [0.2,0.4,0.1,0.3] | Base interference per channel |
| `interference_noise_std_factor` | float | 0.0-1.0 | 0.1 | Noise = mean * this factor (AWGN) |

### Rate Smoothing (EWMA)

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `ewma_factor` | float | 0.0-1.0 | 0.3 | Alpha in: smoothed = α*new + (1-α)*old |

### Channel Switching

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `switch_threshold` | float | 0.0-1.0 | 0.08 | Utility improvement required (8%) |
| `min_dwell_time` | int | 0-100 | 10 | Minimum time steps before switching |

### Visualization

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `history_length` | int | 10-500 | 100 | Points to display in plots |

---

## Implemented Algorithms

### Algorithm 1: Throughput Maximizer
**Metric:** Highest aggregate throughput
```
Select channel = argmax(T_c)
where T_c = Σ R_{c,i}
```
**Pros:** Maximum system capacity
**Cons:** May starve users with poor channel quality

### Algorithm 2: Max-Min Fairness
**Metric:** Highest minimum rate (worst user)
```
Select channel = argmax(min_i(R_{c,i}))
```
**Pros:** Guarantees QoS for all users
**Cons:** May sacrifice total throughput

### Algorithm 3: Jain's Fairness Index
**Metric:** Highest Jain fairness index
```
JFI_c = [Σ R_{c,i}]² / [N · Σ R_{c,i}²]
Select channel = argmax(JFI_c)
```
**Pros:** Balanced fairness measure
**Cons:** Not directly optimizing throughput

### Algorithm 4: Weighted Throughput-Fairness (WTF)
**Metric:** Weighted combination (α=0.7, β=0.3)
```
U_c = 0.7 * E_c + 0.3 * (min_i(R_{c,i}) / R_max)
Select channel = argmax(U_c)
```
**Pros:** Balances throughput and fairness
**Cons:** Fixed weights may not adapt

### Algorithm 5: Hybrid Proportional Fair ACS (HPF-ACS)
**Metric:** Hybrid utility (α=0.5, β=0.3, γ=0.2)
```
E_c = T_c / (N * R_max)           [Normalized utilization]
U_c = 0.5*E_c + 0.3*(W_c/R_max) + 0.2*JFI_c
Select channel = argmax(U_c)
```
**Pros:** Combines throughput, fairness, and stability
**Cons:** Multiple parameters to tune

### Algorithm 6: Adaptive HPF-ACS
**Metric:** HPF-ACS with dynamic weights based on fairness
```
β = β_min + (β_max - β_min) * (1 - JFI_c)
α = α_max - (β - β_min)
γ = fixed

When fairness high: emphasize throughput
When fairness low: emphasize worst-case protection
```
**Pros:** Automatically adapts to network conditions
**Cons:** More complex

---

## Running the Simulator

### Option 1: Interactive Visualization
```bash
python ptmp_acs_simulator.py
```
Displays real-time interactive plots showing:
- Channel throughput and interference over time
- Fairness indices
- Current algorithm selections
- Station rate distributions
- Performance metrics comparison

### Option 2: Headless Mode (Generate Reports)
```bash
python run_simulator_headless.py
```
Runs 6 predefined experiments:
1. **Uniform Distribution** - All stations similar distance
2. **Random Distribution** - Stations spread out (low fairness)
3. **High Interference** - Challenging channel conditions
4. **Conservative Switching** - Minimal channel changes
5. **Aggressive Switching** - Rapid adaptation
6. **Many Stations** - Scale test with 16 stations

Outputs:
- PNG visualization for each experiment
- JSON statistics for analysis
- Comparative summary across all experiments

---

## Output Files

### Visualization Output
- `results_exp1_uniform.png` - Experiment visualization
- Similar files for each experiment

### Statistics Output
- `stats_exp1_uniform.json` - Performance metrics
- `comparison_all_experiments.json` - Comparative analysis

### JSON Structure
```json
{
  "Throughput Maximizer": {
    "avg_throughput": 394.14,
    "min_throughput": 105.13,
    "std_throughput": 32.38,
    "avg_min_rate": 4.44,
    "min_min_rate": 1.18,
    "avg_fairness": 0.7291,
    "switches": 1
  },
  ...
}
```

---

## Visualization Output

The simulator generates comprehensive visualizations with 8 subplots:

### Row 1
- **Channel Throughput** - Aggregate rate per channel over time
- **Minimum Rate** - Worst-user rate per channel over time

### Row 2
- **Fairness Index** - Jain's FI per channel (target: 0.95)
- **Interference Levels** - Channel interference variation

### Row 3
- **Channel Selection Heatmap** - Which algorithm selected which channel at each time

### Row 4
- **Algorithm Comparison Table** - Current metrics for all algorithms
- **Station Rates Heatmap** - Individual station rates per channel

---

## Creating Custom Scenarios

### Example 1: Stable Network
```python
config = SimulationConfig(
    n_stations=4,
    n_channels=3,
    fairness_param=0.9,  # Uniform distribution
    base_interference=[0.1, 0.15, 0.1],  # Low interference
    interference_noise_std_factor=0.05,  # Low variability
    switch_threshold=0.15,  # Conservative
    min_dwell_time=20,
)
simulator = PTMPSimulator(config)
simulator.run()
visualizer = SimulatorVisualizer(simulator)
visualizer.show()
```

### Example 2: Highly Dynamic Network
```python
config = SimulationConfig(
    n_stations=16,
    n_channels=6,
    fairness_param=0.2,  # Random distribution
    base_interference=[0.4, 0.6, 0.5, 0.7, 0.3, 0.5],  # High interference
    interference_noise_std_factor=0.3,  # High variability
    switch_threshold=0.05,  # Aggressive
    min_dwell_time=5,
    ewma_factor=0.5,  # Fast response
)
simulator = PTMPSimulator(config)
simulator.run()
visualizer = SimulatorVisualizer(simulator)
visualizer.show()
```

### Example 3: Performance Comparison
```python
config = SimulationConfig(
    n_stations=10,
    n_channels=4,
    n_time_steps=500,
    fairness_param=0.3,
)
simulator = PTMPSimulator(config)
simulator.run(verbose=True)
stats = simulator.get_summary_stats()

# Analyze which algorithm performs best
for alg_name, stat in stats.items():
    print(f"{alg_name}: Throughput={stat['avg_throughput']:.1f}, "
          f"Fairness={stat['avg_fairness']:.3f}, "
          f"Switches={stat['switches']}")
```

---

## Performance Metrics

### Key Metrics Calculated

1. **Throughput (T_c)**
   - Sum of achievable rates: T_c = Σ R_{c,i}
   - Units: Megabits/second

2. **Minimum Rate (W_c)**
   - Worst-user protection: W_c = min_i(R_{c,i})
   - Indicates fairness for slowest station

3. **Jain's Fairness Index (JFI_c)**
   - Range: 0 (unfair) to 1 (perfect fairness)
   - Formula: JFI_c = [Σ R_{c,i}]² / [N · Σ R_{c,i}²]

4. **Utilization (E_c)**
   - Normalized by channel capacity
   - E_c = T_c / (N · R_max)

5. **Utility Functions**
   - WTF: 0.7*E_c + 0.3*(W_c/R_max)
   - HPF: 0.5*E_c + 0.3*(W_c/R_max) + 0.2*JFI_c
   - MMF: W_c + 0.05*(T_c/T_total)

---

## Advanced Features

### Rate Measurement Simulation
- **PHY Layer Metrics:** Base rates calculated from distance
- **Interference:** AWGN noise applied per channel
- **EWMA Smoothing:** Simulates rate estimation convergence

### Channel Switching Logic
```python
IF utility_new >= (1 + threshold) * utility_current:
    IF time_since_last_switch >= min_dwell_time:
        SWITCH to new channel
    ENDIF
ENDIF
```

### History Storage
- Efficient deque-based storage (FIFO)
- Configurable history length
- Real-time metric calculation

---

## Performance Tuning

### For Throughput-Focused Deployment
```python
# Use Algorithm 1 or 4
config.switch_threshold = 0.05  # Aggressive switching
config.min_dwell_time = 5
config.ewma_factor = 0.5  # Fast response
```

### For Fairness-Focused Deployment
```python
# Use Algorithm 2, 3, or 6
config.switch_threshold = 0.15  # Conservative
config.min_dwell_time = 20
config.ewma_factor = 0.2  # Stable estimate
```

### For Stable Environments
```python
# Reduce responsiveness
config.switch_threshold = 0.20
config.min_dwell_time = 30
config.ewma_factor = 0.1
```

### For Dynamic Environments
```python
# Increase responsiveness
config.switch_threshold = 0.05
config.min_dwell_time = 5
config.ewma_factor = 0.7
```

---

## Troubleshooting

### Issue: All algorithms select same channel
- **Cause:** One channel dominates in all metrics
- **Solution:** Increase interference variability or channel count

### Issue: Too many switches
- **Cause:** Threshold too low or min_dwell_time too short
- **Solution:** Increase `switch_threshold` or `min_dwell_time`

### Issue: Low fairness
- **Cause:** High distance variation or heterogeneous interference
- **Solution:** Increase `fairness_param` or use fairness-focused algorithm

### Issue: Visualization not displaying
- **Cause:** Display server not available (headless environment)
- **Solution:** Use `run_simulator_headless.py` to generate PNGs

---

## Extension Points

### Adding New Algorithms
```python
class MyCustomAlgorithm(ACSAlgorithm):
    def __init__(self, config: SimulationConfig):
        super().__init__(config, "My Algorithm Name")

    def select_channel(self, metrics: List[ChannelMetrics], 
                      current_channel: int) -> int:
        # Your custom logic here
        utilities = [...]
        return int(np.argmax(utilities))

# Register in PTMPSimulator
simulator.algorithms['custom'] = MyCustomAlgorithm(config)
```

### Adding New Metrics
```python
def get_custom_metric(self, channel_id: int) -> float:
    # Add to ChannelMetrics calculation
    rates = self.smoothed_rates[:, channel_id]
    custom_metric = your_calculation(rates)
    return custom_metric
```

### Custom Visualization
```python
def plot_custom_analysis(simulator):
    plt.figure(figsize=(12, 6))
    
    for alg_name, metrics_list in simulator.history['metrics'].items():
        values = [your_extraction(m) for m in metrics_list]
        plt.plot(values, label=alg_name)
    
    plt.show()
```

---

## References

1. **Jain's Fairness Index:** R. K. Jain, D. M. Chiu, W. R. Hawe, "A quantitative measure of fairness and discrimination for resource allocation in shared computer system", 1984

2. **Proportional Fairness:** F. P. Kelly, A. K. Maulloo, D. K. Tan, "Rate control for communication networks: shadow prices, proportional fairness and stability", 1998

3. **802.11 ACS:** Cisco White Papers, Aruba Networks Technical Guides

---

## License & Citation

This simulator is provided for research and educational purposes.

**Citation:**
```
@software{ptmp_acs_simulator_2026,
  title={PTMP Auto-Channel Selection Simulator},
  author={Auto-Channel Selection Research},
  year={2026},
  url={...}
}
```

---

## Support & Feedback

For issues, feature requests, or extensions, please refer to the code comments and docstrings throughout the simulator.

**Last Updated:** August 2026
