# Fixed Visualization Module for Drone Optimization System
# This module provides visualization capabilities using only existing files

# Basic visualization functions from helpers.py
from .helpers import (
    create_simulation_view,
    create_metrics_charts,
    create_algorithm_comparison_chart,
    create_heatmap,
    create_energy_distribution_chart,
    create_coverage_efficiency_scatter
)

# Enhanced visualization functions from enhanced_helpers.py
from .enhanced_helpers import (
    create_network_topology_visualization,
    create_coverage_quality_heatmap,
    create_algorithm_performance_radar,
    create_energy_consumption_analysis,
    create_optimization_landscape_contour,
    create_clustering_analysis,
    create_sensitivity_analysis_tornado,
    create_real_time_performance_monitor,
    create_comparative_time_series,
    create_pareto_frontier_analysis
)

# Animation functions from animation_helpers.py
from .animation_helpers import (
    SimulationAnimator,
    create_algorithm_convergence_animation,
    create_energy_evolution_animation,
    create_coverage_evolution_animation,
    export_animation
)

# Theme management from theme_manager.py
from .theme_manager import (
    ThemeManager,
    get_color_palette,
    apply_theme_to_figure,
    get_drone_colors
)

# Export all main visualization functions
__all__ = [
    # Basic visualization functions
    'create_simulation_view',
    'create_metrics_charts',
    'create_algorithm_comparison_chart',
    'create_heatmap',
    'create_energy_distribution_chart',
    'create_coverage_efficiency_scatter',
    
    # Enhanced visualization functions
    'create_network_topology_visualization',
    'create_coverage_quality_heatmap',
    'create_algorithm_performance_radar',
    'create_energy_consumption_analysis',
    'create_optimization_landscape_contour',
    'create_clustering_analysis',
    'create_sensitivity_analysis_tornado',
    'create_real_time_performance_monitor',
    'create_comparative_time_series',
    'create_pareto_frontier_analysis',
    
    # Animation functions
    'SimulationAnimator',
    'create_algorithm_convergence_animation',
    'create_energy_evolution_animation',
    'create_coverage_evolution_animation',
    'export_animation',
    
    # Theme management
    'ThemeManager',
    'get_color_palette',
    'apply_theme_to_figure',
    'get_drone_colors'
]

# Visualization categories for easy discovery
BASIC_VISUALIZATIONS = [
    'create_simulation_view',
    'create_metrics_charts', 
    'create_algorithm_comparison_chart',
    'create_heatmap'
]

ENHANCED_VISUALIZATIONS = [
    'create_network_topology_visualization',
    'create_coverage_quality_heatmap',
    'create_algorithm_performance_radar',
    'create_energy_consumption_analysis'
]

ANIMATIONS = [
    'SimulationAnimator',
    'create_algorithm_convergence_animation',
    'create_energy_evolution_animation',
    'create_coverage_evolution_animation'
]

ADVANCED_ANALYTICS = [
    'create_clustering_analysis',
    'create_pareto_frontier_analysis',
    'create_sensitivity_analysis_tornado'
]

REAL_TIME_MONITORING = [
    'create_real_time_performance_monitor',
    'create_comparative_time_series'
]

# Quick access functions
def get_visualization_categories():
    """Get dictionary of visualization categories and their functions"""
    return {
        'basic': BASIC_VISUALIZATIONS,
        'enhanced': ENHANCED_VISUALIZATIONS,
        'animations': ANIMATIONS,
        'advanced_analytics': ADVANCED_ANALYTICS,
        'real_time': REAL_TIME_MONITORING
    }

def create_visualization_from_name(name: str, *args, **kwargs):
    """Create visualization by function name"""
    import sys
    current_module = sys.modules[__name__]
    
    if hasattr(current_module, name):
        func = getattr(current_module, name)
        return func(*args, **kwargs)
    else:
        raise ValueError(f"Unknown visualization function: {name}")

# Preset visualization configurations
PRESET_CONFIGS = {
    'basic_dashboard': {
        'functions': ['create_simulation_view', 'create_metrics_charts'],
        'layout': 'side_by_side',
        'description': 'Basic drone simulation visualization with performance metrics'
    },
    'algorithm_analysis': {
        'functions': ['create_algorithm_comparison_chart', 'create_algorithm_performance_radar'],
        'layout': 'stacked',
        'description': 'Algorithm performance analysis and comparison'
    },
    'real_time_monitoring': {
        'functions': ['create_real_time_performance_monitor', 'create_energy_consumption_analysis'],
        'layout': 'side_by_side',
        'description': 'Live monitoring dashboard for operational deployment'
    },
    'advanced_analytics': {
        'functions': ['create_clustering_analysis', 'create_pareto_frontier_analysis', 'create_sensitivity_analysis_tornado'],
        'layout': 'grid',
        'description': 'Advanced statistical analysis and optimization insights'
    },
    'network_analysis': {
        'functions': ['create_network_topology_visualization', 'create_coverage_quality_heatmap'],
        'layout': 'side_by_side',
        'description': 'Network connectivity and coverage quality analysis'
    }
}

def create_preset_dashboard(preset_name: str, data, **kwargs):
    """
    Create preset dashboard configuration
    
    Args:
        preset_name: Name of preset configuration
        data: Simulation or experiment data
        **kwargs: Additional arguments passed to visualization functions
        
    Returns:
        Dictionary of created figures
    """
    if preset_name not in PRESET_CONFIGS:
        available_presets = list(PRESET_CONFIGS.keys())
        raise ValueError(f"Unknown preset: {preset_name}. Available presets: {available_presets}")
    
    config = PRESET_CONFIGS[preset_name]
    figures = {}
    
    print(f"Creating {preset_name} dashboard...")
    print(f"Description: {config['description']}")
    
    for func_name in config['functions']:
        try:
            print(f"  Creating {func_name}...")
            fig = create_visualization_from_name(func_name, data, **kwargs)
            figures[func_name.replace('create_', '').replace('_', ' ').title()] = fig
        except Exception as e:
            print(f"  Warning: Could not create {func_name}: {e}")
    
    print(f"Dashboard created with {len(figures)} visualizations")
    return figures

def get_available_presets():
    """Get list of available preset configurations with descriptions"""
    return {name: config['description'] for name, config in PRESET_CONFIGS.items()}

# Convenience functions for common use cases
def create_basic_analysis(simulation):
    """Create basic analysis dashboard for a simulation"""
    return create_preset_dashboard('basic_dashboard', simulation)

def create_algorithm_analysis(experiment_results):
    """Create algorithm analysis dashboard for experiment results"""
    return create_preset_dashboard('algorithm_analysis', experiment_results)

def create_monitoring_dashboard(simulation):
    """Create real-time monitoring dashboard"""
    return create_preset_dashboard('real_time_monitoring', simulation)

def create_research_analysis(experiment_data):
    """Create comprehensive research analysis"""
    return create_preset_dashboard('advanced_analytics', experiment_data)

# Version information
__version__ = "1.0.0"
__author__ = "Drone Optimization Team"
__description__ = "Visualization system for drone network optimization"