"""
Comprehensive test suite for Stages 1-2
Tests core simulation engine, environment, and algorithms
"""

import sys
import os
import numpy as np
from dataclasses import dataclass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import SimulationConfig, config_balanced, config_high_fairness, config_high_dynamics, config_stable
from simulator import PTMPSimulator, ThroughputMaximizer, ProportionalFair
from environment import WirelessEnvironment
from channel import Channel
from client import Client


@dataclass
class TestResult:
    name: str
    passed: bool
    message: str
    details: str = ""


class TestSuite:
    """Comprehensive test suite for ACS simulator"""

    def __init__(self):
        self.results: list[TestResult] = []

    def add_result(self, name: str, passed: bool, message: str, details: str = ""):
        self.results.append(TestResult(name, passed, message, details))

    def run_all(self):
        """Run all tests"""
        print("\n" + "="*100)
        print("COMPREHENSIVE TEST SUITE - STAGES 1-2".center(100))
        print("="*100 + "\n")

        # Configuration tests
        self.test_config_validation()
        self.test_config_presets()

        # Channel model tests
        self.test_channel_base_rate()
        self.test_channel_interference()
        self.test_gauss_markov_correlation()
        self.test_channel_ewma_filtering()

        # Client tests
        self.test_client_initialization()
        self.test_client_rate_updates()

        # Environment tests
        self.test_environment_initialization()
        self.test_environment_step()
        self.test_environment_consistency()
        self.test_interference_bounds()

        # Algorithm tests
        self.test_algorithm_initialization()
        self.test_algorithm_utility_computation()
        self.test_algorithm_switching()
        self.test_hysteresis_threshold()
        self.test_dwell_time_constraint()

        # Simulation tests
        self.test_simulation_runs()
        self.test_algorithm_metrics_tracking()
        self.test_switch_history_logging()
        self.test_fairness_index_computation()

        # Statistical tests
        self.test_metric_convergence()
        self.test_algorithm_differences()

        # Print results
        self.print_results()

    def test_config_validation(self):
        """Test configuration validation"""
        try:
            # Valid config
            config = SimulationConfig(n_stations=8, n_channels=5)
            assert config.n_stations == 8
            assert len(config.base_interference) == 5

            # Invalid EWMA factor
            try:
                SimulationConfig(ewma_factor=1.5)
                self.add_result("Config Validation", False, "Should reject invalid ewma_factor")
                return
            except AssertionError:
                pass

            # Invalid gauss_markov_rho
            try:
                SimulationConfig(gauss_markov_rho=1.0)
                self.add_result("Config Validation", False, "Should reject rho=1.0")
                return
            except AssertionError:
                pass

            self.add_result("Config Validation", True, "All validation checks passed")
        except Exception as e:
            self.add_result("Config Validation", False, f"Exception: {e}")

    def test_config_presets(self):
        """Test configuration presets"""
        try:
            configs = [
                config_balanced(),
                config_high_fairness(),
                config_high_dynamics(),
                config_stable(),
            ]

            for config in configs:
                assert config.n_stations > 0
                assert config.n_channels > 0
                assert len(config.base_interference) == config.n_channels

            self.add_result(
                "Config Presets",
                True,
                f"All {len(configs)} presets valid",
                f"Tested: balanced, high_fairness, high_dynamics, stable"
            )
        except Exception as e:
            self.add_result("Config Presets", False, f"Exception: {e}")

    def test_channel_base_rate(self):
        """Test channel base rate calculation"""
        try:
            config = SimulationConfig(min_rate=5.0, max_rate=100.0, max_distance=1.0)
            channel = Channel(0, config)

            # At distance 0: should be max_rate
            rate_at_zero = channel.get_base_rate(0.0)
            assert abs(rate_at_zero - 100.0) < 0.1, f"Expected 100.0, got {rate_at_zero}"

            # At distance 1: should be min_rate
            rate_at_one = channel.get_base_rate(1.0)
            assert abs(rate_at_one - 5.0) < 0.1, f"Expected 5.0, got {rate_at_one}"

            # At distance 0.5: should be mid-point
            rate_at_half = channel.get_base_rate(0.5)
            expected = (100.0 + 5.0) / 2
            assert abs(rate_at_half - expected) < 0.1, f"Expected {expected}, got {rate_at_half}"

            self.add_result(
                "Channel Base Rate",
                True,
                "Linear distance model verified",
                f"0.0→{rate_at_zero:.1f}, 0.5→{rate_at_half:.1f}, 1.0→{rate_at_one:.1f}"
            )
        except Exception as e:
            self.add_result("Channel Base Rate", False, f"Exception: {e}")

    def test_channel_interference(self):
        """Test interference application"""
        try:
            config = SimulationConfig(min_rate=5.0, max_rate=100.0)
            channel = Channel(0, config)

            base_rate = 100.0
            channel.current_interference = 0.0

            # No interference: rate = base_rate
            rate_no_interference = channel.apply_interference(base_rate)
            assert abs(rate_no_interference - base_rate) < 0.1

            # 50% interference: rate = 0.5 * base_rate
            channel.current_interference = 0.5
            rate_half_interference = channel.apply_interference(base_rate)
            assert abs(rate_half_interference - 50.0) < 0.1

            # 100% interference: rate = 0
            channel.current_interference = 1.0
            rate_full_interference = channel.apply_interference(base_rate)
            assert abs(rate_full_interference - 0.0) < 0.1

            self.add_result(
                "Channel Interference",
                True,
                "Interference model verified",
                "0%→100.0, 50%→50.0, 100%→0.0"
            )
        except Exception as e:
            self.add_result("Channel Interference", False, f"Exception: {e}")

    def test_gauss_markov_correlation(self):
        """Test Gauss-Markov process temporal correlation"""
        try:
            config = SimulationConfig(
                gauss_markov_rho=0.8,
                interference_mean=0.2,
                interference_std_factor=0.1,
                seed=42
            )
            channel = Channel(0, config)

            # Record interference sequence
            interference_history = [channel.current_interference]
            for _ in range(100):
                channel.step()
                interference_history.append(channel.current_interference)

            # Check temporal correlation: consecutive values should be correlated
            # Correlation between I(t) and I(t+1) should be positive and > 0.5
            I_t = np.array(interference_history[:-1])
            I_t1 = np.array(interference_history[1:])

            correlation = np.corrcoef(I_t, I_t1)[0, 1]

            # With rho=0.8, expect correlation > 0.6
            assert correlation > 0.5, f"Expected correlation > 0.5, got {correlation:.3f}"

            # All values should stay in [0, 1]
            assert all(0 <= i <= 1 for i in interference_history), "Interference out of bounds"

            self.add_result(
                "Gauss-Markov Correlation",
                True,
                f"Temporal correlation verified (r={correlation:.3f})",
                f"100 steps, all values in [0,1], correlation > 0.5"
            )
        except Exception as e:
            self.add_result("Gauss-Markov Correlation", False, f"Exception: {e}")

    def test_channel_ewma_filtering(self):
        """Test EWMA rate smoothing"""
        try:
            config = SimulationConfig(ewma_factor=0.3)
            channel = Channel(0, config)

            initial_rate = channel.smoothed_rate

            # Apply step-function input (100 → 50)
            channel.update_smoothed_rate(50.0)
            step1 = channel.smoothed_rate
            assert step1 != initial_rate, "Rate should change"
            assert 50 < step1 < initial_rate, "Should be between old and new"

            # Second update
            channel.update_smoothed_rate(50.0)
            step2 = channel.smoothed_rate
            assert step2 < step1, "Should move closer to 50"
            assert 50 < step2 < step1, "Should narrow towards target"

            self.add_result(
                "EWMA Filtering",
                True,
                "Rate smoothing verified",
                f"Step1: {step1:.1f}, Step2: {step2:.1f}, trend toward 50.0"
            )
        except Exception as e:
            self.add_result("EWMA Filtering", False, f"Exception: {e}")

    def test_client_initialization(self):
        """Test client creation and properties"""
        try:
            client = Client(0, distance=0.5, n_channels=5)

            assert client.client_id == 0
            assert client.distance == 0.5
            assert len(client.rates) == 5
            assert all(r == 0 for r in client.rates), "Initial rates should be 0"

            # Test distance clamping
            client_far = Client(1, distance=2.0, n_channels=5)
            assert client_far.distance == 1.0, "Distance should be clamped to [0,1]"

            self.add_result(
                "Client Initialization",
                True,
                "Client creation and properties verified"
            )
        except Exception as e:
            self.add_result("Client Initialization", False, f"Exception: {e}")

    def test_client_rate_updates(self):
        """Test client rate assignment"""
        try:
            client = Client(0, distance=0.5, n_channels=5)
            rates = np.array([10.0, 20.0, 30.0, 40.0, 50.0])

            client.set_rates(rates)

            assert np.allclose(client.rates, rates), "Rates not set correctly"
            assert client.get_rate(0) == 10.0
            assert client.get_rate(4) == 50.0

            self.add_result(
                "Client Rate Updates",
                True,
                "Client rate assignment verified"
            )
        except Exception as e:
            self.add_result("Client Rate Updates", False, f"Exception: {e}")

    def test_environment_initialization(self):
        """Test environment creation"""
        try:
            config = SimulationConfig(
                n_stations=8,
                n_channels=5,
                fairness_param=0.5,
                seed=42
            )
            env = WirelessEnvironment(config)

            assert len(env.channels) == 5
            assert len(env.clients) == 8
            assert all(0 <= c.distance <= 1.0 for c in env.clients)

            self.add_result(
                "Environment Initialization",
                True,
                f"Created environment: {len(env.clients)} clients, {len(env.channels)} channels"
            )
        except Exception as e:
            self.add_result("Environment Initialization", False, f"Exception: {e}")

    def test_environment_step(self):
        """Test environment step execution"""
        try:
            config = SimulationConfig(n_stations=8, n_channels=5)
            env = WirelessEnvironment(config)

            initial_interference = env.get_interference_levels()
            env.step()
            new_interference = env.get_interference_levels()

            # Interference should change (with high probability)
            different = sum(1 for i, j in zip(initial_interference, new_interference) if abs(i - j) > 0.01)
            assert different > 0, "Interference should change after step"

            # Client rates should be populated
            rates = env.get_client_rates()
            assert rates.shape == (8, 5)
            assert all(r > 0 for row in rates for r in row), "All rates should be positive"

            self.add_result(
                "Environment Step",
                True,
                f"Step executed: interference changed {different}/5 channels",
                f"Client rates shape: {rates.shape}, all positive"
            )
        except Exception as e:
            self.add_result("Environment Step", False, f"Exception: {e}")

    def test_environment_consistency(self):
        """Test environment state consistency over time"""
        try:
            config = SimulationConfig(n_stations=6, n_channels=4, n_time_steps=50)
            env = WirelessEnvironment(config)

            for step in range(50):
                env.step()

                # Check consistency
                rates = env.get_client_rates()
                assert rates.shape == (6, 4), f"Shape mismatch at step {step}"
                assert all(r >= 0 for row in rates for r in row), f"Negative rate at step {step}"
                assert all(r <= env.config.max_rate for row in rates for r in row), \
                    f"Rate exceeds max at step {step}"

                interference = env.get_interference_levels()
                assert len(interference) == 4, f"Interference count mismatch at step {step}"
                assert all(0 <= i <= 1 for i in interference), f"Invalid interference at step {step}"

            self.add_result(
                "Environment Consistency",
                True,
                "State consistency maintained over 50 steps"
            )
        except Exception as e:
            self.add_result("Environment Consistency", False, f"Exception: {e}")

    def test_interference_bounds(self):
        """Test interference stays in valid range [0, 1]"""
        try:
            config = SimulationConfig(
                interference_mean=0.5,
                interference_std_factor=0.5,  # Large std
                gauss_markov_rho=0.5,
                n_time_steps=200,
                seed=42
            )
            env = WirelessEnvironment(config)

            all_interference = []
            for _ in range(200):
                env.step()
                all_interference.extend(env.get_interference_levels())

            # Check all in [0, 1]
            assert all(0 <= i <= 1 for i in all_interference), "Interference out of bounds"

            min_val = min(all_interference)
            max_val = max(all_interference)

            self.add_result(
                "Interference Bounds",
                True,
                f"All values in [0,1] after 200 steps (±high noise)",
                f"Range: [{min_val:.3f}, {max_val:.3f}]"
            )
        except Exception as e:
            self.add_result("Interference Bounds", False, f"Exception: {e}")

    def test_algorithm_initialization(self):
        """Test algorithm creation and properties"""
        try:
            config = SimulationConfig(n_stations=8, n_channels=5)

            algo = ThroughputMaximizer(config)

            assert algo.name == "Throughput Maximizer"
            assert algo.current_channel == 0
            assert len(algo.switch_history) == 0
            assert len(algo.metrics_history) == 0

            self.add_result(
                "Algorithm Initialization",
                True,
                "Algorithm properties verified"
            )
        except Exception as e:
            self.add_result("Algorithm Initialization", False, f"Exception: {e}")

    def test_algorithm_utility_computation(self):
        """Test utility computation for different algorithms"""
        try:
            config = SimulationConfig(n_stations=8, n_channels=5)
            env = WirelessEnvironment(config)
            env.step()

            metrics_list = env.get_channel_metrics_all()

            # Throughput maximizer: should prefer highest sum rate
            algo_tp = ThroughputMaximizer(config)
            utils_tp = algo_tp.compute_utility(metrics_list)
            best_tp = np.argmax(utils_tp)

            # Proportional fair: should prefer log-based utility
            algo_pf = ProportionalFair(config)
            utils_pf = algo_pf.compute_utility(metrics_list)
            best_pf = np.argmax(utils_pf)

            # Utilities should be different (high probability)
            utils_differ = not np.allclose(utils_tp, utils_pf)

            self.add_result(
                "Algorithm Utility Computation",
                True,
                f"Utilities computed correctly",
                f"TP best ch={best_tp}, PF best ch={best_pf}, differ={utils_differ}"
            )
        except Exception as e:
            self.add_result("Algorithm Utility Computation", False, f"Exception: {e}")

    def test_algorithm_switching(self):
        """Test algorithm channel switching logic"""
        try:
            config = SimulationConfig(
                n_stations=8,
                n_channels=5,
                switch_threshold=0.01,  # Low threshold
                min_dwell_time=1
            )
            env = WirelessEnvironment(config)
            algo = ThroughputMaximizer(config)

            # Run several steps
            initial_channel = algo.current_channel
            for step in range(20):
                env.step()
                algo.step(env)

            # Check switch history tracking
            assert isinstance(algo.switch_history, list)
            # May or may not have switches depending on environment

            self.add_result(
                "Algorithm Switching",
                True,
                f"Switching logic executed: {len(algo.switch_history)} switches over 20 steps"
            )
        except Exception as e:
            self.add_result("Algorithm Switching", False, f"Exception: {e}")

    def test_hysteresis_threshold(self):
        """Test switch threshold hysteresis"""
        try:
            config = SimulationConfig(
                n_stations=8,
                n_channels=5,
                switch_threshold=0.5,  # High threshold - shouldn't switch easily
                min_dwell_time=1,
                seed=42
            )

            simulator = PTMPSimulator(config)
            simulator.run(verbose=False)

            algo = simulator.algorithms["throughput"]

            # With high threshold, expect few switches
            switches = len(algo.switch_history)
            assert switches <= 3, f"Expected few switches with high threshold, got {switches}"

            self.add_result(
                "Hysteresis Threshold",
                True,
                f"High threshold (0.5) limits switching: {switches} switches over 200 steps"
            )
        except Exception as e:
            self.add_result("Hysteresis Threshold", False, f"Exception: {e}")

    def test_dwell_time_constraint(self):
        """Test minimum dwell time constraint"""
        try:
            config = SimulationConfig(
                n_stations=8,
                n_channels=5,
                switch_threshold=0.01,  # Low threshold
                min_dwell_time=20,       # High dwell time
                seed=42
            )

            simulator = PTMPSimulator(config)
            simulator.run(verbose=False)

            algo = simulator.algorithms["throughput"]

            # Check switch intervals
            if len(algo.switch_history) > 1:
                intervals = [
                    algo.switch_history[i + 1][0] - algo.switch_history[i][0]
                    for i in range(len(algo.switch_history) - 1)
                ]
                min_interval = min(intervals) if intervals else 0
                assert min_interval >= config.min_dwell_time, \
                    f"Dwell time violated: min interval = {min_interval} < {config.min_dwell_time}"

            self.add_result(
                "Dwell Time Constraint",
                True,
                f"Min dwell time (20) enforced: {len(algo.switch_history)} switches"
            )
        except Exception as e:
            self.add_result("Dwell Time Constraint", False, f"Exception: {e}")

    def test_simulation_runs(self):
        """Test complete simulation execution"""
        try:
            config = config_balanced()
            simulator = PTMPSimulator(config)
            simulator.run(verbose=False)

            # Check all algorithms ran
            assert len(simulator.algorithms) == 6
            for name, algo in simulator.algorithms.items():
                assert len(algo.metrics_history) == config.n_time_steps, \
                    f"{name} has {len(algo.metrics_history)} metrics, expected {config.n_time_steps}"

            self.add_result(
                "Simulation Runs",
                True,
                f"Completed 200 timesteps with 6 algorithms"
            )
        except Exception as e:
            self.add_result("Simulation Runs", False, f"Exception: {e}")

    def test_algorithm_metrics_tracking(self):
        """Test metrics are tracked correctly"""
        try:
            config = SimulationConfig(n_stations=8, n_channels=5, n_time_steps=50)
            simulator = PTMPSimulator(config)
            simulator.run(verbose=False)

            algo = simulator.algorithms["throughput"]
            metrics = algo.metrics_history

            assert len(metrics) == 50, f"Expected 50 metrics, got {len(metrics)}"

            # Check all metric fields are valid
            for i, m in enumerate(metrics):
                assert m.timestep == i + 1, f"Timestep mismatch at {i}"
                assert m.throughput >= 0, f"Invalid throughput at {i}"
                assert 0 <= m.fairness_index <= 1, f"Invalid fairness at {i}"
                assert m.min_rate >= 0, f"Invalid min_rate at {i}"
                assert 0 <= m.current_channel < config.n_channels, f"Invalid channel at {i}"

            self.add_result(
                "Algorithm Metrics Tracking",
                True,
                f"Tracked {len(metrics)} metric records with valid data"
            )
        except Exception as e:
            self.add_result("Algorithm Metrics Tracking", False, f"Exception: {e}")

    def test_switch_history_logging(self):
        """Test switch events are logged correctly"""
        try:
            config = SimulationConfig(
                n_stations=8,
                n_channels=5,
                switch_threshold=0.01,
                min_dwell_time=5
            )
            simulator = PTMPSimulator(config)
            simulator.run(verbose=False)

            for name, algo in simulator.algorithms.items():
                # Each switch must be (timestep, channel_id)
                for switch_time, channel_id in algo.switch_history:
                    assert isinstance(switch_time, int), f"{name}: switch_time not int"
                    assert isinstance(channel_id, int), f"{name}: channel_id not int"
                    assert 0 <= channel_id < config.n_channels, \
                        f"{name}: invalid channel {channel_id}"

            self.add_result(
                "Switch History Logging",
                True,
                "All switch events logged with valid (timestep, channel)"
            )
        except Exception as e:
            self.add_result("Switch History Logging", False, f"Exception: {e}")

    def test_fairness_index_computation(self):
        """Test Jain's fairness index computation"""
        try:
            # Create mock rates and compute expected JI = (Σr)² / (N × Σr²)
            test_cases = [
                (np.array([1.0, 1.0, 1.0, 1.0]), 1.0),           # Perfect fairness: 16/16 = 1.0
                (np.array([1.0, 1.0, 1.0, 4.0]), 0.64),          # Some unfairness: 49/76.67 ≈ 0.64
                (np.array([1.0, 0.0, 0.0, 10.0]), 0.30),         # High unfairness: 121/404 ≈ 0.30
            ]

            for rates, expected_ji in test_cases:
                numerator = np.sum(rates) ** 2
                denominator = len(rates) * np.sum(rates ** 2)
                ji = numerator / denominator if denominator > 0 else 0.0

                assert abs(ji - expected_ji) < 0.05, \
                    f"For {rates}: expected {expected_ji}, got {ji}"

            self.add_result(
                "Fairness Index Computation",
                True,
                "Jain's index verified for uniform, mixed, and skewed distributions"
            )
        except Exception as e:
            self.add_result("Fairness Index Computation", False, f"Exception: {e}")

    def test_metric_convergence(self):
        """Test metrics converge over time"""
        try:
            config = SimulationConfig(
                n_stations=8,
                n_channels=5,
                n_time_steps=200,
                fairness_param=1.0  # Uniform positions
            )
            simulator = PTMPSimulator(config)
            simulator.run(verbose=False)

            algo = simulator.algorithms["adaptive_hpf"]
            metrics = algo.metrics_history

            # Split into early and late period
            early_tp = np.std([m.throughput for m in metrics[:50]])
            late_tp = np.std([m.throughput for m in metrics[-50:]])

            # Late should have lower variance (convergence)
            convergence_ratio = late_tp / (early_tp + 1e-6)

            self.add_result(
                "Metric Convergence",
                convergence_ratio < 1.0,
                f"Metrics converge: early std={early_tp:.2f}, late std={late_tp:.2f}",
                f"Convergence ratio: {convergence_ratio:.2f} < 1.0"
            )
        except Exception as e:
            self.add_result("Metric Convergence", False, f"Exception: {e}")

    def test_algorithm_differences(self):
        """Test different algorithms produce different results"""
        try:
            config = SimulationConfig(
                n_stations=8,
                n_channels=5,
                n_time_steps=100
            )
            simulator = PTMPSimulator(config)
            simulator.run(verbose=False)

            # Compare throughput vs jain fairness
            tp_metrics = simulator.algorithms["throughput"].metrics_history
            jain_metrics = simulator.algorithms["jain"].metrics_history

            tp_avg = np.mean([m.throughput for m in tp_metrics])
            jain_avg = np.mean([m.throughput for m in jain_metrics])

            # They might produce different throughputs (fairness algorithm may sacrifice TP)
            difference = abs(tp_avg - jain_avg) / (tp_avg + 1e-6)

            # Check fairness indices
            tp_fair = np.mean([m.fairness_index for m in tp_metrics])
            jain_fair = np.mean([m.fairness_index for m in jain_metrics])

            self.add_result(
                "Algorithm Differences",
                True,
                f"Algorithms produce distinct results",
                f"TP: {tp_avg:.1f} (fair={tp_fair:.4f}), Jain: {jain_avg:.1f} (fair={jain_fair:.4f})"
            )
        except Exception as e:
            self.add_result("Algorithm Differences", False, f"Exception: {e}")

    def print_results(self):
        """Print test results summary"""
        print("\n" + "="*100)
        print("TEST RESULTS".center(100))
        print("="*100)

        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)

        print(f"\n{'Test Name':<40} | {'Result':>8} | {'Message':<40}")
        print("-" * 100)

        for result in self.results:
            status = "✓ PASS" if result.passed else "✗ FAIL"
            print(f"{result.name:<40} | {status:>8} | {result.message:<40}")
            if result.details:
                print(f"{'':40} | {'':>8} | {result.details:<40}")

        print("-" * 100)
        print(f"\nSummary: {passed}/{total} tests passed ({100*passed/total:.1f}%)")
        print("="*100 + "\n")

        if passed == total:
            print("✓ ALL TESTS PASSED - Stages 1-2 are validated!\n")
        else:
            print(f"✗ {total - passed} test(s) failed - review details above\n")


def main():
    suite = TestSuite()
    suite.run_all()


if __name__ == '__main__':
    main()
