"""Tests for Stage 4: Statistics, Export, and Plotting"""

import sys
import os
import unittest
import tempfile
import json
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.statistics import MonteCarloRunner, StatisticsReport, AlgorithmStatistics
from src.export import DataExporter
from src.plotting import StatisticsPlotter
from src.config import config_balanced


class TestMonteCarloRunner(unittest.TestCase):
    """Test Monte Carlo simulation runner"""

    def setUp(self):
        self.config = config_balanced()
        self.runner = MonteCarloRunner(self.config, n_runs=3, seed=42)

    def test_runner_initialization(self):
        """Test runner initializes correctly"""
        self.assertEqual(self.runner.n_runs, 3)
        self.assertEqual(self.runner.seed, 42)
        self.assertEqual(len(self.runner.run_results), 0)

    def test_run_completes(self):
        """Test Monte Carlo runs complete"""
        results = self.runner.run(verbose=False)
        self.assertEqual(len(results), 3)

    def test_run_results_structure(self):
        """Test run results have correct structure"""
        self.runner.run(verbose=False)
        results = self.runner.run_results

        self.assertGreater(len(results), 0)
        for run_data in results:
            # Each run should have all 10 algorithms
            self.assertEqual(len(run_data), 10)

            # Each algorithm should have metrics and switches
            for algo_name, algo_result in run_data.items():
                self.assertIn('metrics_history', algo_result)
                self.assertIn('switch_history', algo_result)

    def test_statistics_computation(self):
        """Test statistics are computed correctly"""
        self.runner.run(verbose=False)
        stats = self.runner.get_statistics()

        self.assertEqual(len(stats), 10)

        for algo_name, algo_stats in stats.items():
            # Check all statistics are present
            self.assertGreater(algo_stats.throughput_mean, 0)
            self.assertGreaterEqual(algo_stats.throughput_std, 0)
            self.assertGreater(algo_stats.fairness_mean, 0)
            self.assertGreater(algo_stats.min_rate_mean, 0)

            # Check time series
            self.assertGreater(len(algo_stats.throughput_timeseries), 0)
            self.assertGreater(len(algo_stats.fairness_timeseries), 0)

    def test_reproducibility(self):
        """Test Monte Carlo with same seed produces similar results"""
        runner1 = MonteCarloRunner(config_balanced(), n_runs=2, seed=42)
        runner1.run(verbose=False)
        stats1 = runner1.get_statistics()

        runner2 = MonteCarloRunner(config_balanced(), n_runs=2, seed=42)
        runner2.run(verbose=False)
        stats2 = runner2.get_statistics()

        # Compare first algorithm's throughput
        algo = 'throughput'
        self.assertAlmostEqual(
            stats1[algo].throughput_mean,
            stats2[algo].throughput_mean,
            places=1
        )


class TestAlgorithmStatistics(unittest.TestCase):
    """Test AlgorithmStatistics dataclass"""

    def test_initialization(self):
        """Test AlgorithmStatistics initializes with defaults"""
        stats = AlgorithmStatistics(name='test_algo')
        self.assertEqual(stats.name, 'test_algo')
        self.assertEqual(stats.n_runs, 0)
        self.assertEqual(stats.throughput_mean, 0.0)

    def test_to_dict_conversion(self):
        """Test conversion to dictionary"""
        stats = AlgorithmStatistics(
            name='test_algo',
            n_runs=5,
            throughput_mean=350.0,
            fairness_mean=0.95
        )
        d = stats.to_dict()

        self.assertEqual(d['name'], 'test_algo')
        self.assertEqual(d['n_runs'], 5)
        self.assertIn('throughput', d)
        self.assertIn('fairness', d)


class TestStatisticsReport(unittest.TestCase):
    """Test StatisticsReport generation"""

    def setUp(self):
        self.runner = MonteCarloRunner(config_balanced(), n_runs=3, seed=42)
        self.runner.run(verbose=False)
        self.stats = self.runner.get_statistics()
        self.report = StatisticsReport(self.stats)

    def test_ranking_by_throughput(self):
        """Test throughput ranking"""
        ranking = self.report.get_ranking_by_throughput(5)
        self.assertEqual(len(ranking), 5)

        # Check first is higher than second
        self.assertGreater(ranking[0][1], ranking[1][1])

    def test_ranking_by_fairness(self):
        """Test fairness ranking"""
        ranking = self.report.get_ranking_by_fairness(5)
        self.assertEqual(len(ranking), 5)
        self.assertGreater(ranking[0][1], ranking[1][1])

    def test_ranking_by_score(self):
        """Test composite score ranking"""
        ranking = self.report.get_ranking_by_score(5)
        self.assertEqual(len(ranking), 5)
        self.assertGreater(ranking[0][1], ranking[1][1])

    def test_stability_ranking(self):
        """Test stability ranking"""
        ranking = self.report.get_stability_ranking(5)
        self.assertEqual(len(ranking), 5)

        # Lower CV is better (more stable) - allow for rounding
        self.assertLessEqual(ranking[0][1], ranking[1][1])


class TestDataExporter(unittest.TestCase):
    """Test data export functionality"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.exporter = DataExporter(output_dir=self.temp_dir)

        self.runner = MonteCarloRunner(config_balanced(), n_runs=2, seed=42)
        self.runner.run(verbose=False)
        self.stats = self.runner.get_statistics()

    def tearDown(self):
        # Cleanup
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_export_statistics_csv(self):
        """Test CSV export of statistics"""
        filepath = self.exporter.export_statistics_to_csv(
            self.stats,
            filename='test_stats.csv'
        )

        self.assertTrue(os.path.exists(filepath))

        # Verify content
        with open(filepath) as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 1)  # Header + data rows
            self.assertIn('algorithm', lines[0])
            self.assertIn('throughput_mean', lines[0])

    def test_export_statistics_json(self):
        """Test JSON export of statistics"""
        filepath = self.exporter.export_statistics_to_json(
            self.stats,
            filename='test_stats.json'
        )

        self.assertTrue(os.path.exists(filepath))

        # Verify content
        with open(filepath) as f:
            data = json.load(f)
            self.assertIn('algorithms', data)
            self.assertGreater(len(data['algorithms']), 0)

    def test_export_timeseries_csv(self):
        """Test time series export"""
        filepath = self.exporter.export_timeseries_to_csv(
            self.stats,
            filename='test_timeseries.csv'
        )

        self.assertTrue(os.path.exists(filepath))

        with open(filepath) as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 1)

    def test_create_summary_report(self):
        """Test text report generation"""
        filepath = self.exporter.create_summary_report(
            self.stats,
            filename='test_report.txt'
        )

        self.assertTrue(os.path.exists(filepath))

        with open(filepath) as f:
            content = f.read()
            self.assertIn('THROUGHPUT RANKING', content)
            self.assertIn('FAIRNESS RANKING', content)


class TestStatisticsPlotter(unittest.TestCase):
    """Test plotting functionality"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.plotter = StatisticsPlotter(output_dir=self.temp_dir)

        self.runner = MonteCarloRunner(config_balanced(), n_runs=2, seed=42)
        self.runner.run(verbose=False)
        self.stats = self.runner.get_statistics()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_plot_throughput_comparison(self):
        """Test throughput comparison plot"""
        filepath = self.plotter.plot_throughput_comparison(
            self.stats,
            filename='test_tp.png'
        )
        self.assertTrue(os.path.exists(filepath))

    def test_plot_fairness_comparison(self):
        """Test fairness comparison plot"""
        filepath = self.plotter.plot_fairness_comparison(
            self.stats,
            filename='test_fair.png'
        )
        self.assertTrue(os.path.exists(filepath))

    def test_plot_tradeoff_curve(self):
        """Test tradeoff curve plot"""
        filepath = self.plotter.plot_tradeoff_curve(
            self.stats,
            filename='test_tradeoff.png'
        )
        self.assertTrue(os.path.exists(filepath))

    def test_plot_timeseries(self):
        """Test time series plot"""
        filepath = self.plotter.plot_timeseries(
            self.stats,
            filename='test_ts.png'
        )
        self.assertTrue(os.path.exists(filepath))

    def test_plot_cdf(self):
        """Test CDF plot"""
        filepath = self.plotter.plot_cdf(
            self.stats,
            metric='throughput',
            filename='test_cdf.png'
        )
        self.assertTrue(os.path.exists(filepath))

    def test_plot_stability(self):
        """Test stability plot"""
        filepath = self.plotter.plot_stability_comparison(
            self.stats,
            filename='test_stability.png'
        )
        self.assertTrue(os.path.exists(filepath))

    def test_plot_min_rate(self):
        """Test min rate plot"""
        filepath = self.plotter.plot_min_rate_comparison(
            self.stats,
            filename='test_minrate.png'
        )
        self.assertTrue(os.path.exists(filepath))

    def test_generate_all_plots(self):
        """Test generating all plots"""
        plots = self.plotter.generate_all_plots(self.stats)

        # Should generate 8 plots
        self.assertEqual(len(plots), 8)

        # All should exist
        for plot in plots:
            self.assertTrue(os.path.exists(plot))


if __name__ == '__main__':
    unittest.main()
