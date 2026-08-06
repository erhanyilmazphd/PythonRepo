#!/usr/bin/env python3
"""Entry point for ACS Simulator GUI application"""

from src.gui.main_window import SimulatorGUI
from src.config import config_balanced


if __name__ == '__main__':
    gui = SimulatorGUI(config=config_balanced())
    gui.run()
