#!/bin/bash
# Quick start script for PTMP ACS Simulator

echo "======================================================================"
echo "PTMP Auto-Channel Selection Simulator"
echo "======================================================================"
echo ""
echo "Select what you'd like to do:"
echo ""
echo "1) View quick start guide (5 min read)"
echo "2) Run interactive demo (2-3 min simulation)"
echo "3) Run full benchmark suite (12-15 min)"
echo "4) Run tests (10 sec)"
echo "5) Run custom scenario example (3-4 min)"
echo "6) Exit"
echo ""
echo "======================================================================"
read -p "Enter choice (1-6): " choice

case $choice in
    1)
        echo ""
        echo "Opening quick start guide..."
        cat docs/00_START_HERE.txt | head -100
        ;;
    2)
        echo ""
        echo "Running interactive demo..."
        python3 src/ptmp_acs_simulator.py
        ;;
    3)
        echo ""
        echo "Running full benchmark suite..."
        python3 src/run_simulator_headless.py
        ;;
    4)
        echo ""
        echo "Running tests..."
        python3 tests/test_simulator.py
        ;;
    5)
        echo ""
        echo "Running custom scenario..."
        python3 examples/custom_scenario.py
        ;;
    6)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice"
        ;;
esac
