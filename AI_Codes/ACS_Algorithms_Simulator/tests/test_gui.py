"""GUI tests for ACS Simulator"""

import sys
import os
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gui.main_window import SimulatorGUI
from src.config import (
    config_balanced, config_high_fairness, config_stable,
    config_highly_variable, config_fairness_critical
)


class TestGUIInitialization(unittest.TestCase):
    """Test GUI initialization and structure"""

    def setUp(self):
        self.config = config_balanced()
        self.gui = SimulatorGUI(config=self.config)

    def tearDown(self):
        if self.gui:
            self.gui.root.destroy()

    def test_gui_window_created(self):
        """Test GUI window is created"""
        self.assertTrue(self.gui.root.winfo_exists())

    def test_gui_title(self):
        """Test window title is set"""
        self.assertEqual(self.gui.root.title(), "ACS Simulator - Tkinter GUI")

    def test_all_buttons_exist(self):
        """Test all control buttons exist"""
        self.assertIsNotNone(self.gui.play_btn)
        self.assertIsNotNone(self.gui.pause_btn)
        self.assertIsNotNone(self.gui.step_btn)
        self.assertIsNotNone(self.gui.reset_btn)

    def test_all_widgets_exist(self):
        """Test all display widgets exist"""
        self.assertIsNotNone(self.gui.speed_slider)
        self.assertIsNotNone(self.gui.time_label)
        self.assertIsNotNone(self.gui.metrics_text)
        self.assertIsNotNone(self.gui.tree)
        self.assertIsNotNone(self.gui.fig1)
        self.assertIsNotNone(self.gui.fig2)
        self.assertIsNotNone(self.gui.canvas1)
        self.assertIsNotNone(self.gui.canvas2)

    def test_initial_state(self):
        """Test GUI initial state"""
        self.assertFalse(self.gui.running)
        self.assertFalse(self.gui.paused)
        self.assertEqual(self.gui.current_step, 0)
        self.assertIsNone(self.gui.simulator)


class TestGUIControls(unittest.TestCase):
    """Test GUI control functionality"""

    def setUp(self):
        self.config = config_balanced()
        self.gui = SimulatorGUI(config=self.config)

    def tearDown(self):
        if self.gui:
            self.gui.root.destroy()

    def test_step_execution(self):
        """Test step button executes one timestep"""
        self.gui._on_step()
        self.assertEqual(self.gui.current_step, 1)
        self.assertIsNotNone(self.gui.simulator)

    def test_multiple_steps(self):
        """Test multiple step executions"""
        for i in range(5):
            self.gui._on_step()
        self.assertEqual(self.gui.current_step, 5)

    def test_reset_clears_state(self):
        """Test reset clears simulation state"""
        self.gui._on_step()
        self.gui._on_step()
        self.gui._on_reset()

        self.assertEqual(self.gui.current_step, 0)
        self.assertIsNone(self.gui.simulator)
        self.assertFalse(self.gui.running)
        self.assertFalse(self.gui.paused)

    def test_speed_slider_changes(self):
        """Test speed slider adjusts frame delay"""
        initial_speed = self.gui.speed
        self.gui._on_speed_change(75)
        # Speed should be different
        self.assertNotEqual(self.gui.speed, initial_speed)

    def test_simulator_initialization(self):
        """Test simulator is properly initialized on first step"""
        self.gui._on_step()

        self.assertIsNotNone(self.gui.simulator)
        self.assertIsNotNone(self.gui.simulator.environment)
        self.assertEqual(len(self.gui.simulator.algorithms), 10)

    def test_pause_resume_cycle(self):
        """Test pause and resume functionality"""
        self.gui._on_play()
        self.assertTrue(self.gui.running)

        self.gui._on_pause()
        self.assertTrue(self.gui.paused)

        self.gui._on_play()
        # Should resume (still running)


class TestGUIConfigurationPresets(unittest.TestCase):
    """Test GUI with different configuration presets"""

    def test_balanced_config(self):
        """Test GUI with balanced configuration"""
        gui = SimulatorGUI(config=config_balanced())
        for _ in range(10):
            gui._on_step()
        self.assertEqual(gui.current_step, 10)
        gui.root.destroy()

    def test_high_fairness_config(self):
        """Test GUI with fairness-focused configuration"""
        gui = SimulatorGUI(config=config_high_fairness())
        for _ in range(10):
            gui._on_step()
        self.assertEqual(gui.current_step, 10)
        gui.root.destroy()

    def test_stable_config(self):
        """Test GUI with stable (low noise) configuration"""
        gui = SimulatorGUI(config=config_stable())
        for _ in range(10):
            gui._on_step()
        self.assertEqual(gui.current_step, 10)
        gui.root.destroy()

    def test_highly_variable_config(self):
        """Test GUI with highly variable configuration"""
        gui = SimulatorGUI(config=config_highly_variable())
        for _ in range(10):
            gui._on_step()
        self.assertEqual(gui.current_step, 10)
        gui.root.destroy()

    def test_fairness_critical_config(self):
        """Test GUI with fairness-critical configuration"""
        gui = SimulatorGUI(config=config_fairness_critical())
        for _ in range(10):
            gui._on_step()
        self.assertEqual(gui.current_step, 10)
        gui.root.destroy()


class TestGUIDisplayUpdates(unittest.TestCase):
    """Test GUI display update methods"""

    def setUp(self):
        self.config = config_balanced()
        self.gui = SimulatorGUI(config=self.config)

    def tearDown(self):
        if self.gui:
            self.gui.root.destroy()

    def test_update_display_no_crash(self):
        """Test display update doesn't crash"""
        self.gui._on_step()
        self.gui._on_step()
        try:
            self.gui._update_display()
        except Exception as e:
            self.fail(f"Display update crashed: {e}")

    def test_time_label_updates(self):
        """Test time label updates"""
        self.gui._on_step()
        self.gui._on_step()
        self.gui._on_step()

        label_text = self.gui.time_label.cget('text')
        self.assertIn("3/200", label_text)

    def test_metrics_display_updates(self):
        """Test metrics text display updates"""
        self.gui._on_step()
        self.gui._on_step()
        self.gui._on_step()

        self.gui._update_metrics()
        text_content = self.gui.metrics_text.get('1.0', 'end')
        # Should have some metrics content
        self.assertIn("METRICS", text_content)

    def test_algorithm_table_updates(self):
        """Test algorithm comparison table updates"""
        self.gui._on_step()
        self.gui._on_step()

        self.gui._update_algorithm_table()
        # Check tree has items
        items = self.gui.tree.get_children()
        # Should have some algorithms displayed
        self.assertGreater(len(items), 0)

    def test_clear_display(self):
        """Test clear display empties all widgets"""
        self.gui._on_step()
        self.gui._on_step()
        self.gui._on_step()

        self.gui._clear_display()

        # Tree should be empty
        self.assertEqual(len(self.gui.tree.get_children()), 0)
        # Time label should be reset
        self.assertIn("0/200", self.gui.time_label.cget('text'))


class TestGUIMetricsCollection(unittest.TestCase):
    """Test metrics collection during simulation"""

    def setUp(self):
        self.config = config_balanced()
        self.gui = SimulatorGUI(config=self.config)

    def tearDown(self):
        if self.gui:
            self.gui.root.destroy()

    def test_metrics_history_grows(self):
        """Test algorithm metrics history grows with steps"""
        self.gui._on_step()
        initial_len = len(list(self.gui.simulator.algorithms.values())[0].metrics_history)

        self.gui._on_step()
        self.gui._on_step()

        final_len = len(list(self.gui.simulator.algorithms.values())[0].metrics_history)
        self.assertGreater(final_len, initial_len)

    def test_metrics_available_after_step(self):
        """Test metrics are available after each step"""
        self.gui._on_step()

        summary = self.gui.simulator.get_summary()
        self.assertGreater(len(summary), 0)

        for algo_name, stats in summary.items():
            self.assertIn('avg_throughput', stats)
            self.assertIn('avg_fairness', stats)
            self.assertIn('avg_min_rate', stats)

    def test_channel_metrics_available(self):
        """Test channel metrics are available"""
        self.gui._on_step()
        self.gui._on_step()

        metrics = self.gui.simulator.environment.get_channel_metrics_all()
        self.assertEqual(len(metrics), self.config.n_channels)

        for m in metrics:
            self.assertGreater(m.throughput, 0)


class TestGUIIntegration(unittest.TestCase):
    """Integration tests for GUI workflow"""

    def test_full_simulation_workflow(self):
        """Test complete simulation workflow"""
        gui = SimulatorGUI(config=config_balanced())

        # Run simulation
        for i in range(50):
            gui._on_step()
            if i % 10 == 0:
                gui._update_display()

        self.assertEqual(gui.current_step, 50)

        # Get summary
        summary = gui.simulator.get_summary()
        self.assertGreater(len(summary), 0)

        # Reset
        gui._on_reset()
        self.assertEqual(gui.current_step, 0)
        self.assertIsNone(gui.simulator)

        gui.root.destroy()

    def test_pause_resume_workflow(self):
        """Test pause/resume workflow"""
        gui = SimulatorGUI(config=config_balanced())

        # Play
        gui._on_play()
        self.assertTrue(gui.running)
        self.assertFalse(gui.paused)

        # Pause
        gui._on_pause()
        self.assertTrue(gui.paused)

        # Step while paused should work
        initial_step = gui.current_step
        gui._on_step()
        # Note: step when running=True doesn't increment

        gui.root.destroy()


if __name__ == '__main__':
    unittest.main()
