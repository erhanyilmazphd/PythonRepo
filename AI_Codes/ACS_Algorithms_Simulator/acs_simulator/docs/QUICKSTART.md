# PTMP ACS Simulator - Quick Start Guide

## 5-Minute Setup

### Installation
```bash
# Requirements (Python 3.8+)
pip install numpy matplotlib
```

### Run Interactive Demo
```bash
python ptmp_acs_simulator.py
```

This will:
1. Configure a 8-station, 4-channel PTMP network
2. Simulate 200 time steps
3. Display real-time visualization showing:
   - Channel metrics over time
   - Algorithm performance comparison
   - Current network state

---

## 10-Minute Benchmark Suite

Run all 6 predefined experiments and generate reports:

```bash
python run_simulator_headless.py
```

Outputs:
- 6 visualization PNGs
- 6 statistics JSON files  
- 1 comparative summary

Check files:
```bash
ls -la results_exp*.png
ls -la stats_exp*.json
cat comparison_all_experiments.json
```

---

## Common Use Cases

### Use Case 1: Quick Performance Test
```python
from ptmp_acs_simulator import SimulationConfig, PTMPSimulator, SimulatorVisualizer

# Create config
config = SimulationConfig(
    n_stations=8,
    n_channels=4,
    n_time_steps=200,
)

# Run simulation
simulator = PTMPSimulator(config)
simulator.run()

# Display results
visualizer = SimulatorVisualizer(simulator)
visualizer.show()
```

### Use Case 2: Algorithm Comparison
```python
config = SimulationConfig(
    n_stations=10,
    n_channels=4,
    n_time_steps=500,
    fairness_param=0.3,  # Mixed distribution
)

simulator = PTMPSimulator(config)
simulator.run(verbose=True)

# Print comparison
stats = simulator.get_summary_stats()
for alg_name, stat in stats.items():
    print(f"{simulator.algorithms[alg_name].name}:")
    print(f"  Avg Throughput: {stat['avg_throughput']:.1f} Mbps")
    print(f"  Avg Fairness: {stat['avg_fairness']:.4f}")
    print(f"  Switches: {stat['switches']}")
```

### Use Case 3: Custom Scenario
```python
config = SimulationConfig(
    n_stations=12,
    n_channels=6,
    n_time_steps=300,
    min_rate=2.0,
    max_rate=150.0,
    fairness_param=0.2,  # Highly random
    base_interference=[0.3, 0.5, 0.2, 0.4, 0.6, 0.1],
    switch_threshold=0.10,  # 10% improvement required
    min_dwell_time=15,  # 15 time steps minimum
    ewma_factor=0.4,  # Medium smoothing
)

simulator = PTMPSimulator(config)
simulator.run()

stats = simulator.get_summary_stats()
# Analyze results...
```

---

## Simulation Parameters Explained

### Network Setup
- **n_stations**: Number of client devices (typically 2-50)
- **n_channels**: Number of available channels (typically 1-14 for WiFi)
- **n_time_steps**: How long to simulate (typically 100-1000)

### Wireless Conditions
- **min_rate/max_rate**: Rate range in Mbps
- **fairness_param**: 
  - `0.0` = Completely random station positions (low fairness)
  - `0.5` = Mixed distribution
  - `1.0` = All stations same distance (high fairness)
- **base_interference**: Initial interference per channel (0=none, 1=severe)

### Algorithm Behavior
- **switch_threshold**: Improvement % required to switch (8% typical)
- **min_dwell_time**: Minimum time steps before allowing switch (10-20 typical)
- **ewma_factor**: Rate smoothing (0.3 = fast response, 0.1 = stable)

---

## Understanding the Output

### Visualization Panels

**Top Left: Channel Throughput**
- Shows aggregate rate on each channel
- Higher is better
- Variability = channel quality changes

**Top Right: Minimum Rate (Worst User)**
- Critical for fairness
- Should be as high as possible
- Flat line = stable, poor user protection

**Middle Left: Fairness Index**
- Range 0 to 1 (1 = perfect fairness)
- Target typically ≥ 0.95
- Lower = some users disadvantaged

**Middle Right: Interference Levels**
- Shows channel noise variation
- Explains throughput changes
- Updates randomly (AWGN noise)

**Bottom Left: Algorithm Selection Heatmap**
- Which algorithm picked which channel
- Each row = one algorithm
- Color = channel ID

**Bottom Right: Station Rates**
- Individual bars for each station
- Shows rate disparity
- Wide variation = fairness challenge

### Statistics Table
Shows for each algorithm:
- **Current Ch**: Currently selected channel
- **Throughput**: Total rate in Mbps
- **Min Rate**: Worst user protection
- **Fairness**: Jain's index (0-1)
- **Switches**: Total channel switches made

---

## Interpreting Results

### Good Performance Indicators
✓ High throughput (>350 Mbps for 8 stations × 100 Mbps max)
✓ High fairness (>0.9 Jain index)
✓ Stable selection (few switches)
✓ Fair minimum rate (>50% of average)

### Algorithm Comparison Matrix
```
           Throughput  Fairness  Stability  Switches
Throughput Max    ✓✓✓      ✓      ✓✓✓        ✗
MaxMin             ✓       ✓✓✓     ✓✓✓        ✓
Jain's             ✓✓      ✓✓✓     ✓          ✓
WTF                ✓✓✓     ✓✓      ✓✓         ✓
HPF-ACS            ✓✓✓     ✓✓✓     ✓✓         ✓
Adaptive HPF       ✓✓✓     ✓✓✓     ✓✓✓        ✓
```

---

## Experiments to Try

### Experiment 1: Impact of Fairness Parameter
```python
for fairness in [0.1, 0.3, 0.5, 0.7, 0.9]:
    config = SimulationConfig(fairness_param=fairness)
    # Run and compare
```
**Expected:** Higher fairness_param → higher Jain index

### Experiment 2: Algorithm Stability
```python
# Conservative
config = SimulationConfig(
    switch_threshold=0.20,
    min_dwell_time=30,
)

# Aggressive
config = SimulationConfig(
    switch_threshold=0.05,
    min_dwell_time=5,
)
# Compare switches count and utility variance
```
**Expected:** Conservative = fewer switches, Aggressive = more switches

### Experiment 3: Scale Test
```python
for n_stations in [4, 8, 16, 32]:
    config = SimulationConfig(n_stations=n_stations)
    # Run and compare metrics
```
**Expected:** Fairness typically decreases as stations increase

### Experiment 4: Channel Count Impact
```python
for n_channels in [2, 4, 6, 8]:
    config = SimulationConfig(n_channels=n_channels)
    # Run and compare
```
**Expected:** More channels → better optimization opportunity

---

## Tips & Tricks

### For Research Papers
1. Run multiple trials with different random seeds
2. Average results across trials
3. Report: mean ± standard deviation
4. Save JSON output for statistical analysis

### For Presentations
1. Use conservative parameters (few switches, stable)
2. Reduce n_time_steps for demo (100-150)
3. Export PNG visualizations with `matplotlib.savefig()`

### For Troubleshooting
1. Check if one channel dominates:
   ```python
   metrics = simulator.environment.get_all_metrics()
   for m in metrics:
       print(f"Ch{m.channel_id}: T={m.throughput:.1f}, "
             f"F={m.min_rate:.1f}, JFI={m.fairness_index:.3f}")
   ```

2. Monitor switching behavior:
   ```python
   for alg_name, alg in simulator.algorithms.items():
       print(f"{alg_name}: {len(alg.switch_history)} switches")
   ```

3. Analyze rate distribution:
   ```python
   rates = simulator.environment.smoothed_rates[:, current_ch]
   print(f"Mean: {np.mean(rates):.2f}, Std: {np.std(rates):.2f}")
   ```

---

## Performance Tips

### For Large Simulations (n_time_steps > 1000)
- Use headless mode: `run_simulator_headless.py`
- Reduce `history_length` to save memory
- Run in background: `nohup python script.py &`

### For Real-Time Visualization
- Use small n_time_steps (100-200)
- Set `interval=200` in animation (slower update)
- Close other applications

### For Statistical Analysis
- Export to JSON format
- Use pandas for analysis: `pd.read_json('stats.json')`
- matplotlib for custom plots

---

## File Structure

```
ptmp_acs_simulator/
├── ptmp_acs_simulator.py           # Main simulator
├── run_simulator_headless.py       # Batch runner
├── SIMULATOR_README.md             # Full documentation
├── QUICKSTART.md                   # This file
└── results/
    ├── results_exp*.png            # Output visualizations
    ├── stats_exp*.json             # Output statistics
    └── comparison_all_experiments.json
```

---

## Next Steps

1. **Run the quick demo:** `python ptmp_acs_simulator.py`
2. **Run benchmarks:** `python run_simulator_headless.py`
3. **Read full docs:** `SIMULATOR_README.md`
4. **Customize scenarios:** Edit `SimulationConfig` parameters
5. **Add new algorithms:** Extend `ACSAlgorithm` base class

---

## FAQ

**Q: Why do algorithms select different channels?**
A: They optimize different objectives (throughput vs fairness vs stability).

**Q: Why so many switches?**
A: Channels are changing dynamically. Use higher `switch_threshold` to reduce.

**Q: Is this realistic?**
A: Simplified PTMP model. Real systems have more complex propagation, handovers, etc.

**Q: Can I use this for production?**
A: Research tool only. Adapt algorithms as needed for your hardware.

**Q: What if I want to add interference traces?**
A: Load real interference data and replace the AWGN simulation in `PTMPEnvironment.step()`.

---

**Ready to run?** Start with:
```bash
python ptmp_acs_simulator.py
```

Enjoy the simulator! 🚀
