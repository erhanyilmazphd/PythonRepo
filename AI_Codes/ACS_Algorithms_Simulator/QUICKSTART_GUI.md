# Quick Start: GUI Launch & Usage

## 30-Second Launch

```bash
cd /path/to/ACS_Algorithms_Simulator
python3 main.py
```

Done! The GUI window opens with interactive simulation.

---

## Controls

| Control | Action |
|---------|--------|
| **Play** | Start continuous simulation |
| **Pause** | Pause ongoing simulation |
| **Step** | Execute one timestep (debug mode) |
| **Reset** | Restart simulation to beginning |
| **Speed** | Adjust frame rate (1-100 FPS) |

---

## 4-Panel Display

**Top Left**: Channel rates bar chart  
**Top Right**: Metrics display (top 3 algorithms)  
**Bottom Left**: Algorithm comparison table (all 10 algorithms)  
**Bottom Right**: Station rates heatmap (2D color map)

---

## Common Workflows

### Workflow 1: Full Run
```
1. Click "Play"
2. Watch simulation run for 200 timesteps
3. Observe metrics updating in real-time
4. Click "Pause" to stop anytime
5. Click "Reset" to restart
```

### Workflow 2: Single Step Debugging
```
1. Click "Step" once
2. Observe display update
3. Click "Step" again for next timestep
4. Perfect for investigating algorithm decisions
```

### Workflow 3: Pause and Resume
```
1. Click "Play"
2. Simulation runs...
3. Click "Pause" to freeze
4. Examine metrics in detail
5. Click "Play" to resume
```

### Workflow 4: Adjust Speed
```
1. Click "Play"
2. Drag Speed slider left (slower) or right (faster)
3. Animation adjusts instantly
4. Find sweet spot for visualization
```

---

## Configuration Options

### Launch with Different Config

```python
from src.gui.main_window import SimulatorGUI
from src.config import config_stable

gui = SimulatorGUI(config=config_stable())
gui.run()
```

**Available configs:**
- `config_balanced()` - Default balanced scenario
- `config_high_fairness()` - Fairness-focused
- `config_high_dynamics()` - Aggressive interference
- `config_stable()` - Low noise (best for visualization)
- `config_highly_variable()` - Jittery interference
- `config_fairness_critical()` - QoS guarantee
- `config_throughput_critical()` - Capacity focused

### Recommendation
Start with `config_balanced()` (default in main.py) for best visual experience.

---

## Understanding the Display

### Channel Rates Chart
- **X-axis**: Channel numbers (0-4)
- **Y-axis**: Throughput in Mbps
- **Height**: Bar height = channel quality
- Shows which channels are best right now

### Metrics Display
- **TP**: Average throughput (Mbps)
- **Fair**: Fairness index (0-1, higher is better)
- **MinRate**: Minimum client rate
- **Switches**: Number of channel switches

### Algorithm Table
- **Algorithm**: Algorithm name
- **Channel**: Currently selected channel
- **TP**: Current throughput
- **Fair**: Fairness metric
- **MinRate**: Minimum rate
- **Switches**: Total switches to date

### Heatmap
- **Green**: Good performance on that channel
- **Yellow**: Medium performance
- **Red**: Poor performance
- Shows how algorithms balance channels across stations

---

## Troubleshooting

### GUI doesn't open
```bash
# Check dependencies
python3 -c "import tkinter; print('OK')"
python3 -c "import matplotlib; print('OK')"

# Try demo script
python3 examples/gui_demo.py
```

### Display updates too slow
- Drag Speed slider right to increase frame rate
- GUI targets 20 FPS by default (50ms per frame)

### Display updates too fast
- Drag Speed slider left to decrease frame rate
- Can slow to 1 FPS for detailed inspection

### Metrics show zeros
- This is normal at the start
- Wait for simulation to stabilize (5-10 timesteps)
- Metrics accumulate as simulation progresses

---

## Tips for Best Experience

1. **Start Simple**: Use `config_balanced()` to get familiar with GUI
2. **Adjust Speed**: Find frame rate that lets you see patterns clearly
3. **Watch Metrics**: The "Metrics & Status" panel shows algorithm performance
4. **Check Heatmap**: Helps visualize fairness across stations
5. **Use Step Mode**: Click "Step" to inspect individual timestep decisions

---

## Features Ready in Stage 3

✅ Real-time interactive simulation  
✅ 4-panel live visualization  
✅ All 10 algorithms supported  
✅ All 7 configuration presets  
✅ Play/Pause/Step/Reset controls  
✅ Speed adjustment slider  
✅ Background threading (non-blocking UI)  

---

## Next: Stage 4 (Coming Soon)

- Monte Carlo statistical runs
- CSV/JSON export
- Advanced visualization plots
- Algorithm ranking system
- Performance statistics

---

**Ready?** Run `python3 main.py` now!
