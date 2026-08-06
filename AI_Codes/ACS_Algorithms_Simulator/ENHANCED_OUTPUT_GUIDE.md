# Enhanced ACS Simulator - Interactive Output & Visualization Guide

**Date**: August 6, 2026  
**Version**: 2.0 - Enhanced Outputs  
**Status**: ✅ Production Ready

---

## 📋 Overview

The ACS simulator has been refactored with **professional-grade interactive outputs** inspired by the USE_CASES.md decision analysis format. All outputs are now clean, tabular, and designed for quick decision analysis.

---

## 🎯 Key Features

### 1. **Clean Decision Tables** (Text Output)
Formatted tables showing all channel metrics at each time step:
- Channel ID
- Sum Rate (Throughput)
- Min Rate (Fairness measure)
- Mean Rate  
- Variance
- Utility Score
- Interference Level
- Status (CURRENT, BEST)

**Example Output:**
```
 Ch | Sum Rate | Min Rate | Mean Rate | Variance | Utility | Interference | Status
====================================================================
  0 |   364.0  |    5.0   |    45.5   |   24.75  |  180.1  |     0.15     | CURRENT ✓
  1 |   340.0  |    3.2   |    42.5   |   28.90  |  162.3  |     0.35     |
  2 |   355.0  |    4.8   |    44.4   |   25.20  |  175.8  |     0.25     |
  3 |   345.0  |    4.0   |    43.1   |   27.50  |  168.5  |     0.10     |
  4 |   350.0  |    4.5   |    43.8   |   26.80  |  171.9  |     0.40     |
```

### 2. **Station Rate Matrices** (Text Output)
Shows achievable rates for each station on each channel:
- Rows: Stations (Sta-0 through Sta-N)
- Columns: Channels (Ch-0 through Ch-F)
- Values: Achievable rate in Mbps
- Mean column: Average rate across channels

**Example Output:**
```
Station | Ch-0 | Ch-1 | Ch-2 | Ch-3 | Ch-4 | Mean
====================================================
Sta-0   |  5.0 |  5.0 |  5.0 |  5.0 |  5.0 |  5.0
Sta-1   | 22.7 | 22.7 | 22.7 | 22.7 | 22.7 | 22.7
Sta-2   | 74.1 | 74.1 | 74.1 | 74.1 | 74.1 | 74.1
Sta-3   | 48.8 | 48.8 | 48.8 | 48.8 | 48.8 | 48.8
Sta-4   | 82.6 | 82.6 | 82.6 | 82.6 | 82.6 | 82.6
====================================================
Average | 45.5 | 45.5 | 45.5 | 45.5 | 45.5
```

### 3. **Algorithm Comparison Tables** (Text Output)
Compares all 6 algorithms at each time step:
- Algorithm name
- Current channel selected
- Throughput
- Minimum rate (worst user)
- Fairness index
- Total channel switches

**Example Output:**
```
Algorithm              | Channel | Throughput | Min Rate | Fairness | Switches
================================================================================
Throughput Maximizer   |    0    |   364.0    |   5.0    |  0.7717  |    0
Max-Min Fairness       |    0    |   364.0    |   5.0    |  0.7717  |    0
Jain's Fairness        |    0    |   364.0    |   5.0    |  0.7717  |    0
WTF (α=0.7, β=0.3)    |    0    |   364.0    |   5.0    |  0.7717  |    0
HPF-ACS                |    0    |   364.0    |   5.0    |  0.7717  |    0
Adaptive HPF-ACS       |    0    |   364.0    |   5.0    |  0.7717  |    0
```

### 4. **Waterfall Summary** (Text Output)
Shows algorithm progression over time windows:
- Divides simulation into equal windows (e.g., 50 time steps each)
- Shows average and standard deviation for each metric
- Helps identify performance trends

**Example Output:**
```
Window: Steps 0-50
──────────────────────────────────────────────────────────────────────
  Throughput Maximizer:
    Throughput   339.6 ± 47.8 | Fairness  0.783 ± 0.000 | MinRate    4.0 ±  0.6

Window: Steps 50-100
──────────────────────────────────────────────────────────────────────
  Throughput Maximizer:
    Throughput   356.7 ± 2.0  | Fairness  0.783 ± 0.000 | MinRate    4.2 ±  0.0
```

---

## 📊 Visualization Outputs

### 1. **Waterfall Dashboard** (`waterfall_dashboard.png`)
**Comprehensive 4-panel visualization showing algorithm performance progression:**

**Panel 1 (Top Left): Throughput Waterfall**
- Line plot showing throughput over time for each algorithm
- Each algorithm has a distinct color
- Shows trends: whether throughput is improving, stable, or degrading

**Panel 2 (Top Right): Fairness Index Progression**
- Jain's fairness index (0-1) over time
- Higher = more fair distribution
- Each algorithm tracked separately

**Panel 3 (Middle Left): Min Rate Waterfall**
- Minimum achievable rate (worst user) over time
- Critical for QoS guarantees
- Indicates how well the algorithm protects edge users

**Panel 4 (Middle Right): Channel Selection Heatmap**
- Y-axis: Algorithm names
- X-axis: Time steps
- Colors: Channel selected (0-4)
- Shows which algorithms switch channels and when

**Panel 5 (Bottom): Summary Statistics Table**
- Comparative metrics for all algorithms:
  - Avg Throughput ± Std Dev
  - Avg Fairness ± Std Dev
  - Avg Min Rate ± Std Dev
  - Total Switches
  - Max/Min Throughput

### 2. **Decision Tree Visualization** (`decision_tree_final.png`)
**Shows the decision-making process at final time step:**

**Top Left: Station Rates Heatmap**
- Color-coded matrix showing current rates for each station on each channel
- Green = high rate, Red = low rate
- Numbers show exact Mbps values
- Easy to spot outliers and imbalances

**Top Right: Channel Utility Comparison**
- Bar chart comparing utility score for each channel
- Green bar = selected (best) channel
- Light blue = other channels
- Values shown above each bar for easy comparison

**Bottom Left: Algorithm Selections Table**
- What each algorithm selected at this time step
- Shows: Algorithm name, Selected Channel, Sum Rate, Min Rate

**Bottom Right: Simulation Details**
- Configuration parameters
- Current environment status
- Thresholds and settings

### 3. **Comparative Summary** (`comparative_summary.png`)
**Final algorithm comparison with three metrics:**

**Top Panel: Normalized Performance Comparison**
- Bars comparing:
  - Throughput (normalized to max)
  - Fairness (normalized to max)
  - Min Rate (normalized to max)
  - Stability (100 - normalized switches)

**Bottom Left: Efficiency Score**
- Combined Throughput + Fairness / 2
- Horizontal bar chart
- Shows balanced performance

**Bottom Right: Stability Score**
- 100 - (switches / max_switches)
- Higher = fewer switches = more stable
- Shows number of switches in parentheses

---

## 🔧 Usage Examples

### Run Full Interactive Dashboard

```bash
python3 examples/interactive_dashboard.py
```

**Outputs:**
- Console: Decision tables, station matrices, comparisons, waterfall summary
- Files:
  - `output/waterfall_dashboard.png` - Waterfall visualization
  - `output/decision_tree_final.png` - Decision process at final step
  - `output/comparative_summary.png` - Algorithm comparison
  - `output/interactive_results.json` - Detailed metrics in JSON

### Run With Custom Configuration

```python
from src.ptmp_acs_simulator import SimulationConfig, PTMPSimulator
from src.acs_output_formatter import ACSOutputFormatter
from src.enhanced_visualizer import EnhancedACSVisualizer

# Configure
config = SimulationConfig(
    n_stations=12,
    n_channels=6,
    n_time_steps=300,
    fairness_param=0.3,
)

# Run simulation
sim = PTMPSimulator(config)
sim.run()

# Create formatter
formatter = ACSOutputFormatter(config, sim)

# Print reports
formatter.print_summary_report()

# At specific time step
print(formatter.generate_decision_table("throughput", time_step=50))
print(formatter.generate_station_rates_table("throughput", time_step=50))
print(formatter.generate_algorithm_comparison(time_step=50))

# Generate visualizations
visualizer = EnhancedACSVisualizer(sim, formatter)
visualizer.create_waterfall_dashboard(filename="my_waterfall.png")
visualizer.create_comparative_summary(filename="my_summary.png")
```

---

## 📁 Output Files

### Console Output (Text)
Generated when running the dashboard:

1. **Configuration Summary**
   - Number of stations, channels, time steps
   - Fairness parameter
   - Base interference levels

2. **Summary Statistics**
   - Final metrics for each algorithm
   - Throughput, fairness, min rate comparisons

3. **Sample Decision Tables**
   - At key time steps (0, 1/4, 1/2, 3/4, final)
   - Complete channel analysis for each

4. **Waterfall Summary**
   - Performance progression over time windows
   - Trends and stability metrics

### Image Files (PNG)
High-resolution professional visualizations:

- `waterfall_dashboard.png` (222 KB)
  - 4-panel comprehensive analysis
  - 150 DPI, suitable for publications

- `decision_tree_final.png` (162 KB)
  - Decision process visualization
  - Final time step analysis

- `comparative_summary.png` (114 KB)
  - Algorithm comparison charts
  - Efficiency and stability scores

### Data Files (JSON)
Exportable data for external analysis:

- `interactive_results.json` (100 KB)
  - All metrics for each algorithm
  - Channel selection history
  - Switch events
  - Aggregated statistics

---

## 🎓 Understanding the Metrics

### Throughput (Mbps)
- **Definition**: Sum of all achievable rates across all stations on a channel
- **Formula**: Σ R_{c,i} for all stations i on channel c
- **Higher is better**: More total capacity available
- **Tradeoff**: May sacrifice fairness for throughput

### Min Rate (Worst User) (Mbps)
- **Definition**: Minimum achievable rate among all stations
- **Formula**: min(R_{c,i}) for all stations on channel c
- **Higher is better**: Guarantees QoS to all users
- **Use**: Fairness measure - protects edge users

### Fairness Index (0-1)
- **Definition**: Jain's fairness index
- **Formula**: [Σ R_{c,i}]² / (N × Σ R²_{c,i})
- **Range**: 0 (completely unfair) to 1 (perfectly fair)
- **Interpretation**:
  - 0.9+ = Good fairness
  - 0.8-0.9 = Acceptable
  - <0.8 = Unfair distribution

### Utility Score
- **Definition**: Weighted combination of throughput, fairness, and variance
- **Formula**: 0.5 × Sum Rate + 0.35 × Min Rate - 0.15 × Variance
- **Use**: Decision metric for channel selection

### Channel Switches
- **Definition**: Number of times algorithm changed channels
- **Lower is better**: Fewer switches = more stable
- **Tradeoff**: Stability vs. adaptivity

---

## 💡 Interpreting the Output

### When All Algorithms Are Identical
If all algorithms select the same channel throughout:
- **Reason**: Uniform environment with one dominant channel
- **Interpretation**: Current conditions don't require sophisticated ACS
- **Action**: Introduce interference variability to see algorithm differences

### When Algorithms Diverge
If algorithms select different channels:
- **Reason**: Different optimization objectives (throughput vs. fairness)
- **Interpretation**: Good testbed for algorithm comparison
- **Analysis**: Check waterfall - does one consistently outperform?

### Channel Switching Patterns
If an algorithm switches frequently:
- **High switches (>5)**: Aggressive adaptation, may cause latency issues
- **Low switches (0-2)**: Conservative approach, stable but may miss opportunities
- **Hysteresis**: Look for minimum dwell time in switch events

---

## 🔍 Advanced Analysis

### Using the JSON Export

```python
import json

# Load results
with open('output/interactive_results.json', 'r') as f:
    results = json.load(f)

# Access algorithm performance
for algo_name, metrics in results['algorithms'].items():
    print(f"{algo_name}:")
    print(f"  Avg Throughput: {metrics['avg_throughput']:.1f} Mbps")
    print(f"  Avg Fairness: {metrics['avg_fairness']:.3f}")
    print(f"  Switch Events: {len(metrics['switch_events'])}")
```

### Plotting Custom Analysis

```python
import matplotlib.pyplot as plt

# Plot fairness over time for a specific algorithm
fairness_data = results['algorithms']['throughput']['fairness_indices']
plt.plot(fairness_data, label='Throughput Maximizer')
plt.xlabel('Time Step')
plt.ylabel('Fairness Index')
plt.title('Fairness Evolution')
plt.show()
```

---

## 📈 Performance Interpretation

### Ideal Scenario
- **Throughput**: High (close to maximum achievable)
- **Fairness**: >0.85 (all users get reasonable rates)
- **Min Rate**: >20 Mbps (edge users protected)
- **Switches**: <5 (stable, not oscillating)

### Throughput-Focused
- **Throughput**: Highest among algorithms
- **Fairness**: May be lower (<0.75)
- **Use case**: Web services where average user experience matters

### Fairness-Focused
- **Throughput**: May sacrifice some capacity
- **Fairness**: >0.9 (excellent fairness)
- **Min Rate**: High
- **Use case**: Critical services (healthcare, emergency)

### Balanced
- **Throughput**: Good
- **Fairness**: Good (0.8-0.9)
- **Min Rate**: Acceptable
- **Switches**: Low (stable)
- **Use case**: General purpose networks

---

## 🎯 Troubleshooting

### No Channel Switches Detected
- **Cause**: Environment is uniform or algorithms find optimal channel immediately
- **Solution**: 
  - Increase interference variability
  - Reduce switch threshold in config
  - Check if multiple channels are actually different

### All Algorithms Identical
- **Cause**: Metrics weighted equally lead to same selection
- **Solution**:
  - Adjust utility function weights
  - Introduce realistic interference levels
  - Check if environment has true channel diversity

### Unexpected Fairness Values
- **Cause**: Fairness index calculation or data interpretation
- **Check**:
  - Verify min rate values
  - Check station rate distribution
  - Look at variance scores

---

## 📝 Files Modified/Added

### New Files
- `src/acs_output_formatter.py` - Clean output formatting
- `src/enhanced_visualizer.py` - Waterfall and decision visualizations
- `examples/interactive_dashboard.py` - Complete demo script

### Output Directory
- `output/waterfall_dashboard.png` - Main visualization
- `output/decision_tree_final.png` - Decision analysis
- `output/comparative_summary.png` - Algorithm comparison
- `output/interactive_results.json` - Detailed metrics

---

## 🚀 Next Steps

1. **Explore outputs**: Run `python3 examples/interactive_dashboard.py`
2. **Examine visualizations**: Open PNG files to study patterns
3. **Analyze JSON**: Load `interactive_results.json` for custom analysis
4. **Customize**: Modify config and rerun with your parameters
5. **Extend**: Add custom algorithms or metrics as needed

---

## ✅ Summary

The enhanced ACS simulator now provides:

✓ **Clean, professional text output** - Decision tables and comparisons  
✓ **Waterfall visualizations** - Algorithm progression over time  
✓ **Decision analysis** - Shows reasoning behind channel selection  
✓ **Comparative metrics** - Algorithm benchmarking  
✓ **JSON export** - Data for external analysis  
✓ **Production-ready** - Professional quality outputs  

**All inspired by the USE_CASES.md decision analysis format for clear, interpretable results.**

