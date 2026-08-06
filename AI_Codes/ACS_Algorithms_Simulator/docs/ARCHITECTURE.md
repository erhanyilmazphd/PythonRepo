# PTMP ACS Simulator - Architecture & Design

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PTMP ACS SIMULATOR ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────────────────────┘

                                 ┌──────────────────┐
                                 │  USER INTERFACE  │
                                 ├──────────────────┤
                                 │ Configuration    │
                                 │ Parameters       │
                                 └────────┬─────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
         ┌──────────▼──────────┐  ┌──────▼──────────┐  ┌──────▼──────────┐
         │   Interactive Mode  │  │  Batch Mode    │  │  Custom Scripts  │
         │   (Real-time viz)   │  │  (Headless)    │  │  (Research)      │
         │                     │  │                │  │                  │
         │ ptmp_acs_          │  │ run_simulator_ │  │ Your Python      │
         │ simulator.py        │  │ headless.py    │  │ code             │
         └──────────┬──────────┘  └──────┬─────────┘  └──────┬──────────┘
                    │                    │                   │
                    └────────────────────┼───────────────────┘
                                         │
                    ┌────────────────────▼───────────────────┐
                    │                                        │
              ┌─────▼────────────────────────────────────────▼──────┐
              │                                                      │
              │        CORE SIMULATOR (ptmp_acs_simulator.py)       │
              │                                                      │
              ├──────────────────────────────────────────────────────┤
              │                                                      │
              │  ┌────────────────────────────────────────────────┐  │
              │  │  SimulationConfig (Dataclass)                 │  │
              │  ├────────────────────────────────────────────────┤  │
              │  │ • n_stations, n_channels, n_time_steps        │  │
              │  │ • min_rate, max_rate                          │  │
              │  │ • fairness_param                              │  │
              │  │ • base_interference (per channel)             │  │
              │  │ • interference_noise_std_factor               │  │
              │  │ • ewma_factor                                 │  │
              │  │ • switch_threshold, min_dwell_time           │  │
              │  │ • history_length                              │  │
              │  └────────────────────────────────────────────────┘  │
              │                                                      │
              │  ┌────────────────────────────────────────────────┐  │
              │  │  PTMPEnvironment                              │  │
              │  ├────────────────────────────────────────────────┤  │
              │  │ State:                                         │  │
              │  │ • client_distances (position model)           │  │
              │  │ • base_rates (distance-based)                 │  │
              │  │ • current_interference (dynamic)              │  │
              │  │ • current_rates (base * (1-int))              │  │
              │  │ • smoothed_rates (EWMA filtered)              │  │
              │  │                                               │  │
              │  │ Methods:                                      │  │
              │  │ • step() - advance one time step              │  │
              │  │ • get_channel_metrics() - calc metrics        │  │
              │  │ • get_all_metrics() - for all channels        │  │
              │  └────────────────────────────────────────────────┘  │
              │                                                      │
              │  ┌────────────────────────────────────────────────┐  │
              │  │  ACSAlgorithm (Abstract Base Class)           │  │
              │  ├────────────────────────────────────────────────┤  │
              │  │ State:                                         │  │
              │  │ • current_channel                             │  │
              │  │ • time_on_channel                             │  │
              │  │ • last_switch_time                            │  │
              │  │ • switch_history                              │  │
              │  │                                               │  │
              │  │ Methods:                                      │  │
              │  │ • select_channel() - abstract                 │  │
              │  │ • step() - execute one step                   │  │
              │  │ • _should_switch() - hysteresis logic         │  │
              │  │                                               │  │
              │  │ ┌─ Concrete Implementations ─────────────┐   │  │
              │  │ │                                        │   │  │
              │  │ │ 1. ThroughputMaximizer                │   │  │
              │  │ │    argmax(T_c)                        │   │  │
              │  │ │                                        │   │  │
              │  │ │ 2. MaxMinFairness                     │   │  │
              │  │ │    argmax(min_i(R_{c,i}))            │   │  │
              │  │ │                                        │   │  │
              │  │ │ 3. JainsFairnessAlgorithm             │   │  │
              │  │ │    argmax(JFI_c)                      │   │  │
              │  │ │                                        │   │  │
              │  │ │ 4. WTFAlgorithm                       │   │  │
              │  │ │    argmax(0.7*E_c + 0.3*W/R_max)     │   │  │
              │  │ │                                        │   │  │
              │  │ │ 5. HPFACSAlgorithm                    │   │  │
              │  │ │    argmax(0.5*E_c + 0.3*W + 0.2*JFI)│   │  │
              │  │ │                                        │   │  │
              │  │ │ 6. AdaptiveHPFACS                     │   │  │
              │  │ │    Dynamic weights based on JFI      │   │  │
              │  │ │                                        │   │  │
              │  │ └────────────────────────────────────────┘   │  │
              │  └────────────────────────────────────────────────┘  │
              │                                                      │
              │  ┌────────────────────────────────────────────────┐  │
              │  │  PTMPSimulator (Orchestrator)                 │  │
              │  ├────────────────────────────────────────────────┤  │
              │  │ State:                                         │  │
              │  │ • environment (PTMPEnvironment)                │  │
              │  │ • algorithms (Dict[name, Algorithm])           │  │
              │  │ • history (metrics per time step)              │  │
              │  │ • current_metrics (latest metrics)             │  │
              │  │                                               │  │
              │  │ Methods:                                      │  │
              │  │ • step() - advance one time step              │  │
              │  │ • run() - run full simulation                 │  │
              │  │ • get_summary_stats() - aggregate results     │  │
              │  └────────────────────────────────────────────────┘  │
              │                                                      │
              └──────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
         ┌──────────▼─────────┐ ┌──▼─────────────┐ ┌▼──────────────┐
         │ SimulatorVisualizer│ │ Data Export    │ │ Custom Analysis
         ├────────────────────┤ ├────────────────┤ ├────────────────┤
         │ Real-time display  │ │ JSON output    │ │ Direct access  │
         │ 8 subplots         │ │ PNG export     │ │ to history/    │
         │ Live heatmap       │ │ Statistics     │ │ metrics        │
         │ Animation support  │ │ Comparisons    │ │                │
         └────────────────────┘ └────────────────┘ └────────────────┘
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          SIMULATION FLOW                            │
└─────────────────────────────────────────────────────────────────────┘

    START
      │
      │ Initialize SimulationConfig
      ▼
    ┌─────────────────────────────┐
    │ PTMPEnvironment.__init__()  │
    ├─────────────────────────────┤
    │ • Initialize positions      │
    │ • Calculate base rates      │
    │ • Set interference levels   │
    │ • Initialize EWMA smoothing │
    └────────┬────────────────────┘
             │
             ▼
    ┌─────────────────────────────────────┐
    │ Create PTMPSimulator & Algorithms   │
    ├─────────────────────────────────────┤
    │ • Instantiate all 6 algorithms      │
    │ • Initialize history storage        │
    │ • Set current_channel = 0           │
    └────────┬────────────────────────────┘
             │
             │ ┌──── FOR each time step ─────┐
             │ │                              │
             ▼ ▼                              │
    ┌─────────────────────────────────┐      │
    │ PTMPEnvironment.step()          │      │
    ├─────────────────────────────────┤      │
    │ 1. Update interference (AWGN)   │      │
    │    interference = mean + N(0,σ) │      │
    │                                 │      │
    │ 2. Update rates                 │      │
    │    rate = base * (1 - int)      │      │
    │                                 │      │
    │ 3. Apply EWMA smoothing         │      │
    │    smooth = α*new + (1-α)*old  │      │
    └────────┬────────────────────────┘      │
             │                               │
             ▼                               │
    ┌──────────────────────────────────┐     │
    │ Get metrics for all channels     │     │
    ├──────────────────────────────────┤     │
    │ For each channel c:              │     │
    │  • T(c) = Σ R_{c,i}             │     │
    │  • W(c) = min_i(R_{c,i})        │     │
    │  • JFI(c) = [T]²/[N·Σ R²]       │     │
    │  • E(c) = T/(N·R_max)            │     │
    │  • U_wtf, U_hpf, U_mmf          │     │
    └────────┬─────────────────────────┘     │
             │                               │
             ▼                               │
    ┌──────────────────────────────────┐     │
    │ For each algorithm:              │     │
    │ algorithm.step(metrics)          │     │
    ├──────────────────────────────────┤     │
    │ 1. Select best channel           │     │
    │    c_best = select_channel(...)  │     │
    │                                  │     │
    │ 2. Check switching conditions    │     │
    │    - Dwell time elapsed?         │     │
    │    - Utility gain >= threshold?  │     │
    │                                  │     │
    │ 3. Update current_channel        │     │
    │ 4. Record in switch_history      │     │
    └────────┬────────────────────────┘      │
             │                               │
             ▼                               │
    ┌──────────────────────────────────┐     │
    │ Record metrics to history        │     │
    ├──────────────────────────────────┤     │
    │ • time_step                      │     │
    │ • interference[c]                │     │
    │ • throughput[c]                  │     │
    │ • min_rate[c]                    │     │
    │ • fairness[c]                    │     │
    │ • selected_channel[alg]          │     │
    │ • current_metrics[alg]           │     │
    └────────┬────────────────────────┘      │
             │                               │
             │ ◄──────────────────────────────┤
             │ More steps?                   │
             │ NO                            │
             ▼
    ┌──────────────────────────────────┐
    │ Simulation Complete              │
    ├──────────────────────────────────┤
    │ • Generate summary statistics    │
    │ • Create visualization           │
    │ • Export results (PNG, JSON)     │
    └──────────────┬───────────────────┘
                   │
                   ▼
                 END
```

---

## Metrics Calculation Flow

```
┌────────────────────────────────────────────────────────────────┐
│              CHANNEL METRICS CALCULATION                       │
└────────────────────────────────────────────────────────────────┘

INPUT: smoothed_rates[:, channel_id]  (rates for all stations)

STEP 1: Aggregation
┌─────────────────────────┐
│ T(c) = Σ R_{c,i}       │  Total throughput
│ M(c) = Σ R_{c,i} / N   │  Mean rate
│ W(c) = min(R_{c,i})    │  Worst rate
│ B(c) = max(R_{c,i})    │  Best rate
└─────────────────────────┘

STEP 2: Fairness Index
┌──────────────────────────────────────────┐
│ Jain FI = [Σ R_{c,i}]² / [N·Σ R²_{c,i}] │
│         = T(c)² / [N·Σ R²_{c,i}]        │
│ Range: 0 (unfair) to 1.0 (fair)        │
└──────────────────────────────────────────┘

STEP 3: Utilization
┌──────────────────────────────────────────┐
│ E(c) = T(c) / (N·R_max)                 │
│      = [Σ R_{c,i}] / [N·100]            │
│ Normalized by channel capacity          │
└──────────────────────────────────────────┘

STEP 4: Utility Functions

┌─────────────────────────────────┐
│ WTF (Weighted TF)               │
│ U_wtf = 0.7·E(c) + 0.3·W/R_max │
│                                 │
│ Balanced: 70% throughput focus  │
│           30% fairness focus    │
└─────────────────────────────────┘

┌──────────────────────────────────────────┐
│ HPF-ACS (Hybrid Proportional Fair)       │
│ U_hpf = 0.5·E(c) +                      │
│         0.3·(W(c)/R_max) +              │
│         0.2·JFI(c)                      │
│                                          │
│ Hybrid: 50% utilization                 │
│         30% fairness guarantee          │
│         20% proportional fairness       │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ MMF (Max-Min Fairness)                   │
│ U_mmf = W(c) + 0.05·(T(c)/T_max)       │
│                                          │
│ Primary: Maximize minimum rate          │
│ Secondary: Throughput tie-breaker       │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ Adaptive Weights (for Adaptive HPF-ACS)  │
│                                          │
│ β = β_min + (β_max - β_min)·(1 - JFI)  │
│ α = α_max - (β - β_min)                │
│ γ = constant (0.2)                      │
│                                          │
│ Effect: When fairness low → protect     │
│         When fairness high → throughput │
└──────────────────────────────────────────┘

OUTPUT: ChannelMetrics object
├── throughput (Mbps)
├── min_rate (Mbps)
├── max_rate (Mbps)
├── fairness_index (0-1)
├── utilization (0-1)
├── utility_wtf (scalar)
├── utility_hpf (scalar)
└── utility_mmf (scalar)
```

---

## Class Hierarchy

```
┌───────────────────────────────┐
│      ACSAlgorithm             │
│     (Abstract Base)           │
├───────────────────────────────┤
│ + select_channel()  [abstract]│
│ + step()                      │
│ + _should_switch()            │
│ - switch_threshold            │
│ - min_dwell_time              │
│ - current_channel             │
│ - switch_history              │
└───────────┬───────────────────┘
            │
     ┌──────┴──────────┐
     │                 │
     │    ┌────────────┴─────────────┬─────────────┬─────────────┐
     │    │                          │             │             │
     ▼    ▼                          ▼             ▼             ▼
    ThroughputMaximizer   MaxMinFairness   JainsFairnessAlgorithm
    (argmax throughput)   (argmax min)     (argmax JFI)
    
    WTFAlgorithm          HPFACSAlgorithm  AdaptiveHPFACS
    (weighted combo)      (hybrid 3-way)   (dynamic weights)
```

---

## State Machines

### Algorithm State Machine

```
                ┌─────────────────────────────┐
                │   WAITING ON CHANNEL        │
                │ current_channel = c         │
                │ time_on_channel++           │
                └────┬────────────┬────────────┘
                     │            │
              [candidate better?] │
              [& dwell expired?]  │
                     │ YES        │ NO
                     │            │
                     ▼            ▼
            ┌──────────────┐   STAY
            │ SWITCH CHECK │   (no change)
            │              │
            └──────┬───────┘
                   │
          [utility gain
           >= threshold?]
                   │
            ┌──────┴──────┐
            │ YES   │ NO  │
            ▼       ▼     │
        SWITCH    STAY────┘
          │
          ▼
    ┌──────────────────┐
    │ SWITCH EXECUTED  │
    │ current_ch = c'  │
    │ time_on_ch = 0   │
    │ record switch    │
    └────────┬─────────┘
             │
             ▼
    WAITING ON NEW CHANNEL
```

### Environment State Machine

```
    ┌──────────────────────────┐
    │  TIME STEP t             │
    ├──────────────────────────┤
    │ 1. Update interference   │
    │    int[c] = base[c] +    │
    │             N(0, σ)      │
    │                          │
    │ 2. Update rates          │
    │    rate[i,c] =           │
    │    base[i,c] *           │
    │    (1 - int[c])          │
    │                          │
    │ 3. Apply EWMA            │
    │    smooth = α*new +      │
    │              (1-α)*old   │
    │                          │
    │ 4. time_step++           │
    └──────────────────────────┘
             │
             ▼
    ┌──────────────────────────┐
    │  TIME STEP t+1           │
    └──────────────────────────┘
```

---

## Visualization Coordinate System

```
┌────────────────────────────────────────────────────────────┐
│              VISUALIZATION LAYOUT (8 SUBPLOTS)            │
└────────────────────────────────────────────────────────────┘

┌─────────────────────────────┬──────────────────────────────┐
│  [0,0] Throughput           │  [0,1] Min Rate              │
│  ████ Ch0                   │  ████ Ch0                    │
│  ████ Ch1                   │  ████ Ch1                    │
│  ████ Ch2                   │  ████ Ch2                    │
│  ████ Ch3                   │  ████ Ch3                    │
└─────────────────────────────┴──────────────────────────────┘

┌─────────────────────────────┬──────────────────────────────┐
│  [1,0] Fairness             │  [1,1] Interference          │
│  ████ Ch0                   │  ════ Ch0                    │
│  ████ Ch1                   │  ════ Ch1                    │
│  ════ Target (0.95)         │  ════ Ch2                    │
│                              │  ════ Ch3                    │
└─────────────────────────────┴──────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  [2,0:3] Heatmap: Channel Selection by Algorithm           │
│  ┌─────────────────────────────────────────────────────────┐
│  │ Alg1  ▒ ▒ ░ ░ ░ ░ ░ ░ ▒ ▒ ...                         │
│  │ Alg2  ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ...                         │
│  │ Alg3  ▓ ▓ ▓ ▒ ▒ ▓ ▓ ▓ ▓ ▓ ...                         │
│  │ Alg4  ░ ░ ▒ ▒ ▒ ░ ░ ░ ▒ ▒ ...                         │
│  │ Alg5  ▒ ▒ ▒ ░ ░ ░ ▒ ▒ ▒ ▒ ...                         │
│  │ Alg6  ░ ░ ░ ▓ ▓ ▓ ░ ░ ░ ░ ...                         │
│  └─────────────────────────────────────────────────────────┘
│  Color: Channel ID (0=white, 1=light, 2=dark, 3=black)     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────┬──────────────────────────────┐
│  [3,0:1] Metrics Table      │  [3,2:3] Station Rates       │
│  ┌──────────────────────────┤  ────────────────────────────┤
│  │ Algorithm | Ch | T  │ F  │  █ St0                      │
│  │ Alg1      │ 2  │345│0.92│  █ St1                      │
│  │ Alg2      │ 1  │320│0.95│  █ St2                      │
│  │ Alg3      │ 3  │335│0.88│  █ St3                      │
│  │ Alg4      │ 0  │360│0.91│  █ St4                      │
│  │ Alg5      │ 1  │355│0.93│  █ St5                      │
│  │ Alg6      │ 2  │350│0.94│  █ St6                      │
│  └──────────────────────────┤  █ St7                      │
│                              └──────────────────────────────┘
└─────────────────────────────┴──────────────────────────────┘

(T = Throughput, F = Fairness, numbers scaled)
```

---

## Configuration Parameter Impact

```
Parameter               │ Impact on Simulation
───────────────────────┼──────────────────────────────────────
n_stations              │ More stations → more complex metrics
                        │ Fairness typically decreases
n_channels              │ More options → algorithms select more
                        │ Higher potential throughput
fairness_param          │ 0=random (unfair) → 1=uniform (fair)
                        │ Controls station distance variation
base_interference       │ Higher → lower rates, better channel
                        │ differentiation
interference_noise_     │ Higher → more volatile rates,
std_factor              │ more switching decisions
ewma_factor             │ Higher → faster response, noisier
                        │ Lower → stable, delayed
switch_threshold        │ Higher → fewer switches, suboptimal
                        │ Lower → many switches, adaptive
min_dwell_time          │ Higher → stable, less responsive
                        │ Lower → adaptive, volatile
n_time_steps            │ More steps → convergence, better stats
                        │ Visualization more meaningful
history_length          │ Memory usage vs visualization detail
```

---

## Performance Characteristics

```
Computational Complexity

Algorithm Selection:
  Time: O(F·N)  where F=channels, N=stations
  Space: O(F·N) for rates matrix
  
  Typical: F=4, N=8 → 32 operations per step
  Full sim: 200 steps → 6,400 ops (< 1ms)

Metric Calculation:
  Time: O(F·N)  per step
  Space: O(F) for metric storage

History Storage:
  Time: O(1) append to deque
  Space: O(F·N·H) where H=history_length
  Typical: 4·8·100 = 3,200 floats per algorithm

Visualization:
  Time: O(T·F) to redraw, T=time steps
  Space: ~500KB for PNG output

Total Simulation Runtime (8 stations, 4 channels, 200 steps):
  Pure computation: ~10ms
  With visualization: ~500ms
  Headless output: ~100ms per experiment
```

---

## Extension Points

```
1. Add New Algorithm
   ├── Inherit from ACSAlgorithm
   ├── Implement select_channel()
   ├── Register in PTMPSimulator.algorithms
   └── Runs automatically in comparisons

2. Add New Metric
   ├── Extend ChannelMetrics dataclass
   ├── Calculate in get_channel_metrics()
   ├── Visualize in SimulatorVisualizer
   └── Export to JSON

3. Add New Scenario
   ├── Create SimulationConfig instance
   ├── Adjust parameters for scenario
   ├── Run simulator
   └── Analyze results

4. Custom Interference Model
   ├── Override PTMPEnvironment.step()
   ├── Replace AWGN with your model
   └── Current rates update automatically

5. Custom Visualization
   ├── Access simulator.history directly
   ├── Create custom matplotlib plots
   ├── Or extend SimulatorVisualizer
   └── Export to PNG/PDF
```

---

## Summary

- **Modular Design**: Each component has single responsibility
- **Extensible**: Easy to add algorithms, metrics, scenarios
- **Efficient**: O(F·N) per step, suitable for large simulations
- **Comprehensive**: 6 algorithms, full metrics, detailed visualization
- **Well-Documented**: Code comments, docstrings, external docs
- **Production-Ready**: Type hints, error handling, clean code

