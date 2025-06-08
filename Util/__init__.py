# Utils module initialization
# This module provides utility functions for the drone optimization system

from .config_manager import ConfigManager
from .data_exporter import DataExporter

# Import the experiment logger
try:
    from .experiment_logger import ExperimentLogger
except ImportError:
    # If experiment_logger is not available, provide a dummy implementation
    class ExperimentLogger:
        def __init__(self, *args, **kwargs):
            print("Warning: Using dummy ExperimentLogger")
        
        def log_experiment(self, data):
            return "dummy_exp_id"
        
        def load_experiment(self, exp_id):
            return {}
        
        def compare_experiments(self, exp_ids):
            import pandas as pd
            return pd.DataFrame()

__all__ = [
    'ConfigManager',
    'DataExporter', 
    'ExperimentLogger'
]

# Version information
__version__ = "1.0.0"
__description__ = "Utility functions for drone optimization system"