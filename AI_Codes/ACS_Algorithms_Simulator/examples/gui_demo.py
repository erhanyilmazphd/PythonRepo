#!/usr/bin/env python3
"""GUI Demo for ACS Simulator - Launch interactive visualization"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gui.main_window import SimulatorGUI
from src.config import config_balanced


def main():
    """Launch GUI with balanced configuration"""
    config = config_balanced()
    gui = SimulatorGUI(config=config)
    gui.run()


if __name__ == '__main__':
    main()
