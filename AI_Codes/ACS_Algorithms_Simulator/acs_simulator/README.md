# PTMP Auto-Channel Selection (ACS) Simulator

A complete, production-ready Python simulator for benchmarking Auto-Channel Selection algorithms in Point-to-Multipoint (PTMP) wireless networks.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run interactive demo (real-time visualization)
python src/ptmp_acs_simulator.py

# Run full benchmark suite (headless mode)
python src/run_simulator_headless.py
```

## What's Included

### Core Components
- **ptmp_acs_simulator.py** (900+ lines): Main simulator with 6 ACS algorithms
- **run_simulator_headless.py** (400+ lines): Batch experiment runner

### 6 Implemented Algorithms
1. Throughput Maximizer - Focus on maximum aggregate rate
2. Max-Min Fairness - Protect worst-case user
3. Jain's Fairness Index - Balanced fairness metric
4. WTF (Weighted Throughput-Fairness) - 70% throughput, 30% fairness
5. HPF-ACS (Hybrid Proportional Fair) - Comprehensive approach
6. Adaptive HPF-ACS - Auto-tuning based on conditions

### Documentation
- **docs/00_START_HERE.txt** - Entry point (start here!)
- **docs/QUICKSTART.md** - 5-15 minute getting started guide
- **docs/SIMULATOR_README.md** - Complete reference manual
- **docs/ARCHITECTURE.md** - System design and implementation details
- **docs/INDEX.md** - Master documentation index
- **docs/DELIVERABLES_SUMMARY.md** - Overview of what was built

## Output

### Interactive Mode
- Real-time visualization with 8 subplots
- Algorithm comparison dashboard
- Station rate distribution analysis

### Headless Mode (Batch)
- 6 PNG visualizations (results_exp*.png)
- 6 JSON statistics files (stats_exp*.json)
- Comprehensive comparison summary

## Features

✓ Realistic PTMP wireless environment simulation  
✓ 6 ACS algorithms ready to benchmark  
✓ Real-time interactive visualization  
✓ Batch experiment runner with 6 predefined scenarios  
✓ Comprehensive performance metrics  
✓ Production-quality, well-documented code  
✓ Easily extensible for custom algorithms  

## Getting Help

1. **For Quick Start**: Read `docs/QUICKSTART.md` (5 minutes)
2. **For Full Reference**: Read `docs/SIMULATOR_README.md` (30 minutes)
3. **For System Design**: Read `docs/ARCHITECTURE.md` (20 minutes)
4. **For Everything**: Start with `docs/00_START_HERE.txt`

## Key Metrics

- **Throughput** (Mbps) - Sum of achievable rates across all stations
- **Minimum Rate** (Mbps) - Rate of worst-performing user
- **Fairness Index** (0-1) - 1.0 = perfectly fair, <0.8 = unfair
- **Channel Switches** - Stability vs adaptivity tradeoff

## Configuration

Customize simulation parameters:

```python
from src.ptmp_acs_simulator import SimulationConfig, PTMPSimulator

config = SimulationConfig(
    n_stations=8,              # Number of clients
    n_channels=4,              # Number of channels
    n_time_steps=200,          # Simulation duration
    min_rate=5.0,              # Minimum rate (Mbps)
    max_rate=100.0,            # Maximum rate (Mbps)
    fairness_param=0.5,        # 0=random, 1=deterministic positions
    base_interference=[0.2, 0.4, 0.1, 0.3],  # Per-channel interference
)

sim = PTMPSimulator(config)
sim.run()
stats = sim.get_summary_stats()
```

## Requirements

- Python 3.8+
- numpy >= 1.19.0
- matplotlib >= 3.3.0

## Quick Links

| Want to... | Read... |
|-----------|---------|
| Get started quickly | docs/QUICKSTART.md |
| Understand all algorithms | docs/SIMULATOR_README.md |
| See the architecture | docs/ARCHITECTURE.md |
| Navigate all docs | docs/INDEX.md |
| Get immediate help | docs/00_START_HERE.txt |

## Next Steps

1. Read `docs/00_START_HERE.txt` for comprehensive overview
2. Run `python src/ptmp_acs_simulator.py` for interactive demo
3. Run `python src/run_simulator_headless.py` for full benchmark
4. Check generated PNG and JSON files in `output/`
5. Customize scenarios as needed

---

**Status**: Production-Ready | **Created**: August 2026 | **Python**: 3.8+ required
