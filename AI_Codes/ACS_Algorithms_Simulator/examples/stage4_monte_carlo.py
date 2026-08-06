#!/usr/bin/env python3
"""Stage 4: Monte Carlo Statistical Analysis with Export and Plotting

Demonstrates:
- Running N independent simulations
- Computing comprehensive statistics
- Exporting results (CSV, JSON)
- Generating publication-quality plots
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import config_balanced, config_stable, config_highly_variable
from src.statistics import MonteCarloRunner, StatisticsReport
from src.export import DataExporter
from src.plotting import StatisticsPlotter


def main():
    """Run complete Stage 4 pipeline"""
    print("\n" + "="*80)
    print("STAGE 4: MONTE CARLO STATISTICAL ANALYSIS")
    print("="*80)

    # Configuration
    config = config_balanced()
    n_runs = 5  # Can increase for more robust statistics

    print(f"\n📊 Configuration:")
    print(f"  • Config: Balanced (200 timesteps)")
    print(f"  • Monte Carlo runs: {n_runs}")
    print(f"  • Algorithms: 10")

    # Run Monte Carlo
    print(f"\n▶️  Running {n_runs} independent simulations...")
    runner = MonteCarloRunner(config, n_runs=n_runs, seed=42)
    runner.run(verbose=True)

    # Compute statistics
    print(f"\n📈 Computing statistics...")
    statistics = runner.get_statistics()

    # Print summary
    print(f"\n" + "="*80)
    report = StatisticsReport(statistics)
    report.print_summary()

    # Export data
    print(f"\n💾 Exporting results...")
    exporter = DataExporter(output_dir='stage4_output')

    # CSV exports
    csv_stats = exporter.export_statistics_to_csv(statistics)
    print(f"  ✓ Statistics CSV: {csv_stats}")

    csv_timeseries = exporter.export_timeseries_to_csv(statistics)
    print(f"  ✓ Time series CSV: {csv_timeseries}")

    # JSON export
    json_stats = exporter.export_statistics_to_json(statistics)
    print(f"  ✓ Statistics JSON: {json_stats}")

    # Text report
    text_report = exporter.create_summary_report(statistics)
    print(f"  ✓ Text report: {text_report}")

    # Generate plots
    print(f"\n📊 Generating plots...")
    plotter = StatisticsPlotter(output_dir='stage4_output')
    plots = plotter.generate_all_plots(statistics)

    print(f"\n✅ All plots generated:")
    for i, plot in enumerate(plots, 1):
        print(f"  {i}. {os.path.basename(plot)}")

    # Rankings
    print(f"\n" + "="*80)
    print("🏆 ALGORITHM RANKINGS")
    print("="*80)

    print(f"\n📊 Top 5 by Throughput:")
    for i, (name, tp) in enumerate(report.get_ranking_by_throughput(5), 1):
        print(f"  {i}. {name:30s} {tp:7.1f} Mbps")

    print(f"\n⚖️  Top 5 by Fairness:")
    for i, (name, fair) in enumerate(report.get_ranking_by_fairness(5), 1):
        print(f"  {i}. {name:30s} {fair:.4f}")

    print(f"\n🎯 Top 5 by Composite Score:")
    for i, (name, score) in enumerate(report.get_ranking_by_score(5), 1):
        print(f"  {i}. {name:30s} {score:.4f}")

    print(f"\n⏱️  Top 5 Most Stable:")
    for i, (name, cv) in enumerate(report.get_stability_ranking(5), 1):
        print(f"  {i}. {name:30s} CV={cv:.4f}")

    print(f"\n" + "="*80)
    print(f"✅ Stage 4 Complete!")
    print(f"   Output directory: stage4_output/")
    print(f"="*80 + "\n")


if __name__ == '__main__':
    main()
