"""Main Tkinter window for ACS Simulator GUI"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import queue
import numpy as np

try:
    from .styles import COLORS, ALGORITHM_COLORS, FONTS, apply_matplotlib_style
except ImportError:
    from styles import COLORS, ALGORITHM_COLORS, FONTS, apply_matplotlib_style

try:
    from ..simulator import PTMPSimulator
    from ..config import SimulationConfig, config_balanced
except ImportError:
    from simulator import PTMPSimulator
    from config import SimulationConfig, config_balanced


class SimulatorGUI:
    """Main Tkinter GUI for ACS Simulator"""

    def __init__(self, config=None):
        self.config = config or config_balanced()
        self.simulator = None
        self.running = False
        self.paused = False
        self.current_step = 0
        self.speed = 50  # milliseconds per frame

        # Thread communication
        self.update_queue = queue.Queue()
        self.simulation_thread = None

        # Create main window
        self.root = tk.Tk()
        self.root.title("ACS Simulator - Tkinter GUI")
        self.root.geometry("1600x900")

        apply_matplotlib_style()

        self._setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _setup_ui(self):
        """Setup all UI components"""

        # Top control panel
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        ttk.Label(control_frame, text="Controls:", font=FONTS['subtitle']).pack(side=tk.LEFT, padx=5)

        self.play_btn = ttk.Button(control_frame, text="Play", command=self._on_play)
        self.play_btn.pack(side=tk.LEFT, padx=5)

        self.pause_btn = ttk.Button(control_frame, text="Pause", command=self._on_pause, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        self.step_btn = ttk.Button(control_frame, text="Step", command=self._on_step)
        self.step_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = ttk.Button(control_frame, text="Reset", command=self._on_reset)
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text="Speed:").pack(side=tk.LEFT, padx=(20, 5))
        self.speed_slider = ttk.Scale(control_frame, from_=1, to=100, orient=tk.HORIZONTAL,
                                     command=self._on_speed_change)
        self.speed_slider.set(self.speed)
        self.speed_slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True, ipadx=100)

        self.time_label = ttk.Label(control_frame, text="Time: 0/200", font=FONTS['normal'])
        self.time_label.pack(side=tk.RIGHT, padx=5)

        # Main content area (4 panels)
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create 2x2 grid
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Panel 1: Channel Rates Chart (top left)
        ttk.Label(left_frame, text="Channel Rates", font=FONTS['subtitle']).pack()
        self.fig1 = Figure(figsize=(6, 4), dpi=100)
        self.ax1 = self.fig1.add_subplot(111)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=left_frame)
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Panel 2: Metrics Display (top right)
        ttk.Label(right_frame, text="Metrics & Status", font=FONTS['subtitle']).pack()
        metrics_frame = ttk.Frame(right_frame)
        metrics_frame.pack(fill=tk.BOTH, expand=True)

        self.metrics_text = tk.Text(metrics_frame, height=12, width=50, font=FONTS['mono'])
        self.metrics_text.pack(fill=tk.BOTH, expand=True)

        # Panel 3: Algorithm Table (bottom left)
        ttk.Label(left_frame, text="Algorithm Comparison", font=FONTS['subtitle']).pack(pady=(10, 0))

        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        cols = ('Algorithm', 'Channel', 'TP', 'Fair', 'MinRate', 'Switches')
        self.tree = ttk.Treeview(tree_frame, columns=cols, height=8, show='headings')

        for col in cols:
            self.tree.column(col, width=75)
            self.tree.heading(col, text=col)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Panel 4: Channel Heatmap (bottom right)
        ttk.Label(right_frame, text="Station Rates Heatmap", font=FONTS['subtitle']).pack(pady=(10, 0))
        self.fig2 = Figure(figsize=(6, 4), dpi=100)
        self.ax2 = self.fig2.add_subplot(111)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=right_frame)
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _on_play(self):
        """Start simulation"""
        if not self.running:
            self.running = True
            self.paused = False
            self.play_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            self.step_btn.config(state=tk.DISABLED)

            # Create and start simulator thread
            self.simulator = PTMPSimulator(self.config)
            self.simulation_thread = threading.Thread(target=self._run_simulation, daemon=True)
            self.simulation_thread.start()

    def _on_pause(self):
        """Pause simulation"""
        self.paused = True
        self.pause_btn.config(state=tk.DISABLED)
        self.play_btn.config(state=tk.NORMAL)
        self.step_btn.config(state=tk.NORMAL)

    def _on_step(self):
        """Execute one timestep"""
        if not self.running:
            if not self.simulator:
                self.simulator = PTMPSimulator(self.config)

            self.simulator.environment.step()
            for algo in self.simulator.algorithms.values():
                algo.step(self.simulator.environment)

            self.current_step += 1
            self._update_display()

    def _on_reset(self):
        """Reset simulation"""
        self.running = False
        self.paused = False
        self.current_step = 0
        self.simulator = None
        self.play_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.step_btn.config(state=tk.NORMAL)
        self._clear_display()

    def _on_speed_change(self, value):
        """Update speed"""
        self.speed = int(100 - int(float(value)))  # Invert: higher slider = faster

    def _run_simulation(self):
        """Run simulation in background thread"""
        try:
            for step in range(self.config.n_time_steps):
                if not self.running:
                    break

                if not self.paused:
                    # Execute one timestep
                    self.simulator.environment.step()
                    for algo in self.simulator.algorithms.values():
                        algo.step(self.simulator.environment)

                    self.current_step = step + 1
                    self._update_display()

                    # Respect speed setting
                    import time
                    time.sleep(self.speed / 1000.0)
                else:
                    import time
                    time.sleep(0.1)

            self.running = False
            self.play_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Simulation error: {e}")
            self.running = False

    def _update_display(self):
        """Update all display panels"""
        try:
            # Update time label
            self.time_label.config(text=f"Time: {self.current_step}/{self.config.n_time_steps}")

            # Update channel rates chart
            self._update_channel_chart()

            # Update metrics
            self._update_metrics()

            # Update algorithm table
            self._update_algorithm_table()

            # Update heatmap
            self._update_heatmap()

            self.root.update_idletasks()
        except Exception as e:
            print(f"Display update error: {e}")

    def _update_channel_chart(self):
        """Update channel rates bar chart"""
        if not self.simulator:
            return

        self.ax1.clear()
        try:
            # Get channel metrics
            metrics = self.simulator.environment.get_channel_metrics_all()
            channels = list(range(self.config.n_channels))
            throughputs = [m.throughput for m in metrics]

            bars = self.ax1.bar(channels, throughputs, color=[ALGORITHM_COLORS.get(f'algo_{i}', '#2E86AB') for i in channels])

            # Highlight current channels
            for algo in self.simulator.algorithms.values():
                if algo.current_channel < len(bars):
                    bars[algo.current_channel].set_edgecolor('red')
                    bars[algo.current_channel].set_linewidth(2)

            self.ax1.set_xlabel('Channel')
            self.ax1.set_ylabel('Throughput (Mbps)')
            self.ax1.set_title('Channel Rates')
            self.ax1.set_xticks(channels)
            self.canvas1.draw_idle()
        except Exception as e:
            print(f"Chart update error: {e}")

    def _update_metrics(self):
        """Update metrics display"""
        if not self.simulator:
            return

        self.metrics_text.config(state=tk.NORMAL)
        self.metrics_text.delete('1.0', tk.END)

        try:
            summary = self.simulator.get_summary()

            text = "=== METRICS SUMMARY ===\n\n"
            for algo_name in sorted(summary.keys())[:3]:  # Show top 3
                stats = summary[algo_name]
                text += f"{algo_name}:\n"
                text += f"  TP: {stats['avg_throughput']:.1f} Mbps\n"
                text += f"  Fair: {stats['avg_fairness']:.4f}\n"
                text += f"  MinRate: {stats['avg_min_rate']:.1f}\n"
                text += f"  Switches: {stats['total_switches']}\n\n"

            self.metrics_text.insert('1.0', text)
            self.metrics_text.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Metrics update error: {e}")

    def _update_algorithm_table(self):
        """Update algorithm comparison table"""
        if not self.simulator:
            return

        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            rates = self.simulator.environment.get_client_rates()

            for algo_name in sorted(self.simulator.algorithms.keys()):
                algo = self.simulator.algorithms[algo_name]
                if algo.metrics_history:
                    m = algo.metrics_history[-1]
                    self.tree.insert('', tk.END, values=(
                        algo_name[:12],
                        str(m.current_channel),
                        f"{m.throughput:.0f}",
                        f"{m.fairness_index:.3f}",
                        f"{m.min_rate:.1f}",
                        str(len(algo.switch_history))
                    ))
        except Exception as e:
            print(f"Table update error: {e}")

    def _update_heatmap(self):
        """Update station rates heatmap"""
        if not self.simulator:
            return

        self.ax2.clear()
        try:
            rates = self.simulator.environment.get_client_rates()

            im = self.ax2.imshow(rates, cmap='RdYlGn', aspect='auto', vmin=0, vmax=self.config.max_rate)
            self.ax2.set_xlabel('Channel')
            self.ax2.set_ylabel('Station')
            self.ax2.set_title('Station Rates (Mbps)')

            plt.colorbar(im, ax=self.ax2, label='Rate')
            self.canvas2.draw_idle()
        except Exception as e:
            print(f"Heatmap update error: {e}")

    def _clear_display(self):
        """Clear all displays"""
        self.ax1.clear()
        self.ax2.clear()
        self.metrics_text.config(state=tk.NORMAL)
        self.metrics_text.delete('1.0', tk.END)
        self.metrics_text.config(state=tk.DISABLED)

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.time_label.config(text="Time: 0/200")
        self.canvas1.draw_idle()
        self.canvas2.draw_idle()

    def _on_closing(self):
        """Handle window closing"""
        self.running = False
        self.root.destroy()

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


if __name__ == '__main__':
    gui = SimulatorGUI()
    gui.run()
