#!/bin/bash
# Quick test runner for Phone Book web app

cd /home/erhan/work/learning/PythonProgramming/PythonRepo/AI_Codes/PhoneBook/

echo "Installing Flask..."
pip install -q Flask 2>/dev/null

echo "Running tests..."
python3 test_app.py
