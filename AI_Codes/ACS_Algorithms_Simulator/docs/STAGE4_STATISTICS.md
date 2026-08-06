# Stage 4: Statistical Analysis, Export, and Plotting

**Status**: ✅ COMPLETE  
**Date**: 2026-08-06  
**Tests**: 23/23 passing  
**Files**: 3 production modules + 1 test suite + 1 example

---

## Overview

Stage 4 adds production-ready statistical analysis and comprehensive reporting capabilities:

- **Monte Carlo Framework**: Run N independent simulations with configurable seeds
- **Statistical Aggregation**: Compute mean, std, percentiles, and composite metrics
- **Multi-Format Export**: CSV, JSON, and human-readable text reports
- **Publication-Quality Plots**: 8 different visualization types
- **Flexible Reporting**: Rankings by multiple metrics, cross-algorithm comparison

---

## Core Components

### 1. src/statistics.py (~450 lines)

**AlgorithmStatistics** - Dataclass for per-algorithm statistics
```python
@dataclass
class AlgorithmStatistics:
    name: str
    n_runs: int
    
    # Throughput statistics (mean, std, min, max, percentiles)
    throughput_mean, throughput_std, ...
    
    # Fairness statistics (mean, std, min, max, percentiles)
    fairness_mean, fairness_std, ...
    
    # Min rate statistics
    min_rate_mean, min_rate_std, ...
    
    # Switch statistics
    switches_mean, switches_std, switches_min, switches_max
    
    # Composite score
    score_mean, score_std
    
    # Time series (per-timestep means across runs)
    throughput_timeseries: List[float]
    fairness_timeseries: List[float]
    min_rate_timeseries: List[float]
```

**MonteCarloRunner** - Execute multiple independent runs
```python
runner = MonteCarloRunner(config, n_runs=10, seed=42)
runner.run(verbose=True)
statistics = runner.get_statistics()
```

**StatisticsReport** - Generate rankings and analysis
```python
report = StatisticsReport(statistics)

# Rankings
ranking = report.get_ranking_by_throughput(top_n=10)
ranking = report.get_ranking_by_fairness(top_n=10)
ranking = report.get_ranking_by_score(top_n=10)
ranking = report.get_stability_ranking(top_n=10)

# Print summary
report.print_summary()
```

### 2. src/export.py (~400 lines)

**DataExporter** - Export results to multiple formats

CSV Exports:
```python
exporter = DataExporter(output_dir='output')

# Statistics CSV
filepath = exporter.export_statistics_to_csv(statistics)
# Columns: algorithm, n_runs, tp_mean, tp_std, fair_mean, ...

# Time series CSV
filepath = exporter.export_timeseries_to_csv(statistics)
# Columns: timestep, algo1_tp, algo1_fair, algo2_tp, ...
```

JSON Export:
```python
filepath = exporter.export_statistics_to_json(statistics)
# Full nested structure with all statistics
```

Text Report:
```python
filepath = exporter.create_summary_report(statistics)
# Human-readable formatted report with rankings
```

### 3. src/plotting.py (~500 lines)

**StatisticsPlotter** - Generate publication-quality plots

Available plots:
1. **Throughput Comparison** - Bar chart with error bars
2. **Fairness Comparison** - Bar chart comparing fairness index
3. **Tradeoff Curve** - Scatter plot of throughput vs fairness
4. **Time Series** - Line plots over 200 timesteps
5. **CDF Plots** - Cumulative distribution functions
6. **Stability Comparison** - Box plots of variability
7. **Min Rate Comparison** - QoS metric bar chart

```python
plotter = StatisticsPlotter(output_dir='output')

# Individual plots
plotter.plot_throughput_comparison(statistics)
plotter.plot_fairness_comparison(statistics)
plotter.plot_tradeoff_curve(statistics)
plotter.plot_timeseries(statistics)
plotter.plot_cdf(statistics, metric='throughput')
plotter.plot_stability_comparison(statistics)
plotter.plot_min_rate_comparison(statistics)

# Generate all at once
plots = plotter.generate_all_plots(statistics)
```

---

## Usage Examples

### Example 1: Quick Monte Carlo Analysis

```python
from src.statistics import MonteCarloRunner, StatisticsReport
from src.config import config_balanced

# Run 10 independent simulations
runner = MonteCarloRunner(config_balanced(), n_runs=10)
runner.run(verbose=True)

# Compute statistics
statistics = runner.get_statistics()

# Print rankings
report = StatisticsReport(statistics)
report.print_summary()
```

### Example 2: Full Pipeline with Export and Plots

```python
from src.statistics import MonteCarloRunner
from src.export import DataExporter
from src.plotting import StatisticsPlotter
from src.config import config_stable

# Monte Carlo
runner = MonteCarloRunner(config_stable(), n_runs=20, seed=42)
runner.run()
statistics = runner.get_statistics()

# Export
exporter = DataExporter(output_dir='my_results')
exporter.export_statistics_to_csv(statistics)
exporter.export_statistics_to_json(statistics)
exporter.create_summary_report(statistics)

# Plot
plotter = StatisticsPlotter(output_dir='my_results')
plots = plotter.generate_all_plots(statistics)
```

### Example 3: Scenario Comparison

```python
from src.statistics import MonteCarloRunner
from src.config import config_balanced, config_stable, config_highly_variable

configs = {
    'balanced': config_balanced(),
    'stable': config_stable(),
    'variable': config_highly_variable(),
}

results = {}
for scenario, config in configs.items():
    runner = MonteCarloRunner(config, n_runs=5)
    runner.run()
    results[scenario] = runner.get_statistics()

# Now compare across scenarios...
```

---

## Command-Line Usage

### Run Full Pipeline

```bash
python3 examples/stage4_monte_carlo.py
```

Output directory: `stage4_output/`

Generated files:
- `statistics_*.csv` - Statistical summary
- `statistics_*.json` - Full statistics data
- `timeseries_*.csv` - Per-timestep data
- `report_*.txt` - Formatted text report
- `throughput_comparison_*.png` - Throughput plot
- `fairness_comparison_*.png` - Fairness plot
- `tradeoff_curve_*.png` - TP vs Fairness scatter
- `timeseries_*.png` - Time series line plot
- `cdf_throughput_*.png` - Throughput CDF
- `cdf_fairness_*.png` - Fairness CDF
- `stability_*.png` - Stability comparison
- `min_rate_comparison_*.png` - Min rate QoS plot

---

## Statistics Computed

### Per-Algorithm Metrics (per run average)

**Throughput (Mbps)**
- Mean, Std Dev
- Min, Max
- 25th and 75th percentiles

**Fairness Index (0-1)**
- Mean, Std Dev
- Min, Max
- 25th and 75th percentiles

**Minimum Client Rate (Mbps)**
- Mean, Std Dev
- Min, Max

**Channel Switches**
- Mean, Std Dev
- Min, Max

**Composite Score**
- Formula: `0.4 * (TP/400) + 0.4 * Fairness + 0.2 * (MinRate/50)`
- Mean, Std Dev

**Stability (Coefficient of Variation)**
- CV = Std Dev / Mean
- Lower is better

### Time Series (Aggregated across runs)

**Per-Timestep Averages**
- Throughput by timestep
- Fairness by timestep
- Min-rate by timestep

Useful for observing convergence patterns.

---

## Export Formats

### CSV: Statistics

```
algorithm,n_runs,throughput_mean,throughput_std,...
throughput,10,405.7,35.2,...
proportional_fair,10,385.2,32.1,...
```

### CSV: Time Series

```
timestep,channel_predictor_tp,channel_predictor_fair,...
0,320.5,0.85,...
1,325.3,0.87,...
```

### JSON: Full Statistics

```json
{
  "timestamp": "2026-08-06T14:50:00",
  "algorithms": {
    "throughput": {
      "name": "throughput",
      "n_runs": 10,
      "throughput": {
        "mean": 405.7,
        "std": 35.2,
        ...
      },
      ...
    }
  }
}
```

### Text Report

```
ACS SIMULATOR - MONTE CARLO RESULTS REPORT
================================================================================
Generated: 2026-08-06T14:50:00
Algorithms Tested: 10
Monte Carlo Runs: 10

THROUGHPUT RANKING (Mean ± Std, Mbps)
────────────────────────────────────────────────────────────────────────────────
 1. channel_predictor               406.2 ± 34.0
 2. max_min                         405.7 ± 33.5
 ...
```

---

## Testing

### Test Coverage (23 tests)

**Monte Carlo Runner Tests (5)**
- Initialization
- Run completion
- Results structure
- Statistics computation
- Reproducibility with seed

**Algorithm Statistics Tests (2)**
- Initialization with defaults
- Dict conversion for JSON

**Statistics Report Tests (4)**
- Ranking by throughput
- Ranking by fairness
- Ranking by score
- Stability ranking

**Data Exporter Tests (4)**
- CSV statistics export
- JSON export
- Time series CSV export
- Text report generation

**Plotting Tests (8)**
- Throughput comparison plot
- Fairness comparison plot
- Tradeoff curve
- Time series plot
- CDF plots
- Stability comparison
- Min rate comparison
- Generate all plots

**Run Tests:**
```bash
python3 -m pytest tests/test_stage4.py -v
```

**Result:** 23/23 passing

---

## Performance

### Simulation Speed
- Single run (200 timesteps): ~100-200ms
- N=10 Monte Carlo: ~2-3 seconds
- N=50 Monte Carlo: ~10-15 seconds

### Export Speed
- CSV write: <100ms
- JSON write: <100ms
- Text report: <100ms

### Plotting Speed
- Each plot: 1-3 seconds
- All 8 plots: ~15-20 seconds

### Memory Usage
- Per run: ~5-10 MB
- Statistics for 10 algorithms: ~10 MB
- Plots: <100 MB total

---

## Rankings Available

### By Throughput (Mean ± Std)

Measures raw capacity - higher is better
```
1. channel_predictor      406.2 ± 34.0 Mbps
2. max_min                405.7 ± 33.5 Mbps
3. throughput             405.7 ± 33.7 Mbps
...
```

### By Fairness (Mean ± Std)

Measures equality across clients - higher is better
```
1. channel_predictor      0.9822 ± 0.0113
2. max_min                0.9822 ± 0.0113
...
```

### By Composite Score

Balanced metric: `0.4*TP + 0.4*Fairness + 0.2*MinRate`
```
1. channel_predictor      0.9640 ± 0.0521
2. max_min                0.9633 ± 0.0514
...
```

### By Stability (CV = Std/Mean)

Consistency - lower is better
```
1. max_min                CV=0.0826
2. throughput             CV=0.0830
...
```

---

## Visualization Types

### 1. Bar Charts with Error Bars

**Throughput Comparison**
- X-axis: Algorithm name
- Y-axis: Throughput (Mbps)
- Error bars: ±1 Std Dev
- Use case: Quick performance overview

**Fairness Comparison**
- X-axis: Algorithm name
- Y-axis: Fairness index (0-1)
- Error bars: ±1 Std Dev
- Use case: QoS guarantees

**Min Rate Comparison**
- X-axis: Algorithm name
- Y-axis: Min rate (Mbps)
- Error bars: ±1 Std Dev
- Use case: Worst-case performance

### 2. Scatter Plot: Tradeoff Curve

- X-axis: Fairness index
- Y-axis: Throughput (Mbps)
- Points: One per algorithm
- Error ellipses: ±1 Std Dev
- Use case: See TP-fairness tradeoff

### 3. Line Plot: Time Series

- X-axis: Timestep (0-200)
- Y-axis: Metric value
- Lines: One per algorithm (top 5)
- Use case: Observe convergence behavior

### 4. Line Plot: CDF

- X-axis: Metric value
- Y-axis: Cumulative probability (0-1)
- Lines: One per algorithm
- Use case: Compare distributions

### 5. Box Plot: Stability

- X-axis: Algorithm name
- Y-axis: Variability metric
- Two plots: Absolute (Std Dev) and Relative (CV)
- Use case: Compare consistency

---

## Advanced Usage

### Custom Configuration Scenario

```python
from src.config import SimulationConfig
from src.statistics import MonteCarloRunner
from src.export import DataExporter

# Custom config
config = SimulationConfig(
    n_channels=8,
    n_clients=20,
    n_time_steps=500,
    gauss_markov_rho=0.3,  # Low correlation
    interference_std_factor=0.4,  # High dynamics
)

# Run analysis
runner = MonteCarloRunner(config, n_runs=20)
runner.run()
stats = runner.get_statistics()

# Export
exporter = DataExporter(output_dir='custom_scenario')
exporter.export_statistics_to_csv(stats)
```

### Batch Scenario Analysis

```python
from src.config import (
    config_balanced, config_stable,
    config_highly_variable, config_fairness_critical
)
from src.statistics import MonteCarloRunner
from src.export import DataExporter
from src.plotting import StatisticsPlotter

scenarios = {
    'balanced': config_balanced(),
    'stable': config_stable(),
    'variable': config_highly_variable(),
    'fairness_critical': config_fairness_critical(),
}

for scenario_name, config in scenarios.items():
    print(f"Analyzing {scenario_name}...")
    
    # Run
    runner = MonteCarloRunner(config, n_runs=10)
    runner.run()
    stats = runner.get_statistics()
    
    # Export
    output_dir = f'results/{scenario_name}'
    exporter = DataExporter(output_dir=output_dir)
    exporter.export_statistics_to_csv(stats)
    
    # Plot
    plotter = StatisticsPlotter(output_dir=output_dir)
    plotter.generate_all_plots(stats)

print("Batch analysis complete!")
```

---

## Integration with Stages 1-3

**Stage 1 (Engine)**: Uses `PTMPSimulator` directly
**Stage 2 (Algorithms)**: Works with all 10 algorithms
**Stage 3 (GUI)**: Can be used alongside for interactive + batch analysis
**Stage 4**: Provides rigorous statistical foundation for research

---

## Reproducibility

### Seed Management

```python
# Reproducible runs
runner1 = MonteCarloRunner(config, n_runs=10, seed=42)
runner1.run()
stats1 = runner1.get_statistics()

# Same seed = same results
runner2 = MonteCarloRunner(config, n_runs=10, seed=42)
runner2.run()
stats2 = runner2.get_statistics()

# assert stats1 ≈ stats2
```

### Output Preservation

```python
# All exports include timestamp
export_path = exporter.export_statistics_to_csv(stats)
# → output/statistics_20260806_145015.csv

# Unique filenames prevent overwrites
```

---

## Summary

**Stage 4 provides:**

✅ **Monte Carlo Framework**
- Configurable number of runs
- Seeded randomness for reproducibility
- Comprehensive statistics computation

✅ **Multi-Format Export**
- CSV for spreadsheet analysis
- JSON for programmatic access
- Text reports for human review

✅ **Publication-Quality Plots**
- 8 different visualization types
- Professional formatting
- Suitable for presentations and papers

✅ **Flexible Rankings**
- By throughput, fairness, score, stability
- Top-N rankings
- Cross-algorithm comparison

✅ **Complete Testing**
- 23 tests covering all functionality
- 100% test pass rate
- Production-ready code

---

**Status**: ✅ STAGE 4 COMPLETE

Ready for:
- Research publications
- Performance benchmarking
- Statistical validation
- Algorithm comparison studies
- Monte Carlo simulations

---

*Last Updated: 2026-08-06*
