"""Visual styling and theming for ACS GUI"""

import matplotlib.pyplot as plt

# Color palette
COLORS = {
    'primary': '#2E86AB',        # Blue
    'secondary': '#A23B72',      # Purple
    'success': '#06A77D',        # Green
    'warning': '#F77F00',        # Orange
    'danger': '#D62828',         # Red
    'light': '#F5F5F5',          # Light gray
    'dark': '#333333',           # Dark gray
}

ALGORITHM_COLORS = {
    'throughput': '#FF6B6B',
    'proportional_fair': '#4ECDC4',
    'max_min': '#45B7D1',
    'jain': '#96CEB4',
    'hpf': '#FFEAA7',
    'adaptive_hpf': '#DDA15E',
    'weighted_tf': '#BC6C25',
    'hpf_switch_cost': '#C9ADA7',
    'adaptive_threshold': '#9A8C98',
    'channel_predictor': '#FFB703',
}

# Fonts
FONTS = {
    'title': ('Arial', 14, 'bold'),
    'subtitle': ('Arial', 12, 'bold'),
    'normal': ('Arial', 10),
    'small': ('Arial', 9),
    'mono': ('Courier', 9),
}

# Layout constants
PADDING_LARGE = 15
PADDING_NORMAL = 10
PADDING_SMALL = 5

WIDGET_HEIGHT = 25
BUTTON_WIDTH = 12

# Configure matplotlib style
def apply_matplotlib_style():
    """Apply professional matplotlib styling"""
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = '#F8F9FA'
    plt.rcParams['font.size'] = 9
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
