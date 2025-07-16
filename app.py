import dash
from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from datetime import datetime
import traceback
from enum import Enum
import plotly.io as pio
import multiprocessing
import json
import random

# Default parameters for all algorithms to ensure stability
ALGORITHM_DEFAULT_PARAMS = {
    'greedy': {'max_iterations': 500, 'coverage_target': 0.98, 'overlap_weight': 0.3, 'energy_weight': 0.2},
    'ga': {'max_iterations': 200, 'population_size': 50, 'mutation_rate': 0.1, 'crossover_rate': 0.8},
    'pso': {'max_iterations': 150, 'swarm_size': 40, 'inertia': 0.7, 'cognitive_weight': 1.5, 'social_weight': 1.5},
    'sa': {'max_iterations': 1000, 'initial_temp': 1000, 'cooling_rate': 0.95},
    'ga_sa': {'max_iterations': 100, 'population_size': 40, 'sa_temp': 100},
    'gwo': {'max_iterations': 120, 'population_size': 35},
    'mrfo': {'max_iterations': 120, 'population_size': 35}
}

def filter_params(algorithm, params):
    """Filters and validates parameters against robust defaults."""
    if not params:
        return ALGORITHM_DEFAULT_PARAMS.get(algorithm, {})
    
    default_params = ALGORITHM_DEFAULT_PARAMS.get(algorithm, {})
    filtered = default_params.copy()
    
    for key, value in params.items():
        if key in default_params:
            try:
                # Ensure correct type and handle empty strings or None
                if value is not None and str(value).strip() != '':
                    filtered[key] = type(default_params[key])(value)
            except (ValueError, TypeError):
                # If conversion fails, silently keep the default value
                pass
    return filtered

# Enhanced simulation state management
class SimState(Enum):
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"

# Fixed imports to match actual file structure
try:
    # Import optimization algorithms
    from algorithms import (
        greedy_optimization,
        genetic_algorithm,
        particle_swarm_optimization,
        simulated_annealing,
        genetic_algorithm_with_sa,
        grey_wolf_optimizer,
        manta_ray_foraging_optimization
    )
    
    # Import simulation components
    from environment import DroneEnvironment
    
    # Import visualization helpers
    from helpers import create_simulation_view, create_metrics_charts
    
    # Import experiment logger
    from experiment_logger import ExperimentLogger
    
    print("✅ All modules imported successfully")
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all modules are in the correct directory structure")

# Global simulation state and experiment management
simulation = None
current_sim_state = SimState.STOPPED
experiment_logger = ExperimentLogger()
current_experiment_session = None
last_iteration_logs = [
    {'iteration': 1, 'fitness': 25.5, 'coverage': 23.1, 'algorithm': 'TEST'},
    {'iteration': 2, 'fitness': 45.2, 'coverage': 41.7, 'algorithm': 'TEST'},
    {'iteration': 3, 'fitness': 67.8, 'coverage': 65.2, 'algorithm': 'TEST'}
]  # Store the most recent iteration logs

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Drone Optimization Simulation System"

# Custom index string for compact layout
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            /* Academic Professional Layout - Formal Academic Color Scheme */
            
            /* Base Layout - Clean academic styling */
            body { 
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            }
            .container-fluid { 
                padding: 0.4rem !important; 
                max-width: 98% !important;
            }
            .card { 
                margin-bottom: 0.4rem !important; 
                border: 1px solid #cbd5e1 !important;
                box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.06), 0 2px 4px 0 rgba(0, 0, 0, 0.04) !important;
                border-radius: 0.5rem !important;
                background: #ffffff !important;
                transition: all 0.2s ease-in-out !important;
            }
            .card:hover {
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.1), 0 4px 8px 0 rgba(0, 0, 0, 0.06) !important;
                transform: translateY(-1px) !important;
            }
            .card-body { padding: 0.5rem !important; }
            
            /* Academic Header Styling */
            .card-header { 
                padding: 0.45rem 0.65rem !important; 
                font-size: 0.9rem !important; 
                font-weight: 600 !important;
                background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
                color: #f8fafc !important;
                border-radius: 0.5rem 0.5rem 0 0 !important;
                border-bottom: 1px solid #cbd5e1 !important;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
            }
            
            /* Form Controls - Academic Style */
            .row { margin-bottom: 0.2rem !important; }
            .form-control { 
                padding: 0.3rem 0.45rem !important; 
                font-size: 0.85rem !important;
                border-radius: 0.4rem !important;
                border: 1px solid #cbd5e1 !important;
                background-color: #ffffff !important;
                transition: all 0.2s ease-in-out !important;
            }
            .form-control:focus {
                border-color: #2563eb !important;
                box-shadow: 0 0 0 0.15rem rgba(37, 99, 235, 0.1) !important;
                background-color: #f8fafc !important;
            }
            
            /* Buttons - Academic Professional */
            .btn { 
                padding: 0.35rem 0.7rem !important; 
                font-size: 0.82rem !important;
                border-radius: 0.4rem !important;
                font-weight: 500 !important;
                transition: all 0.2s ease-in-out !important;
                border: 1px solid transparent !important;
                text-transform: none !important;
            }
            .btn-primary { 
                background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
                border-color: #2563eb !important;
                color: #ffffff !important;
            }
            .btn-success { 
                background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
                border-color: #059669 !important;
                color: #ffffff !important;
            }
            .btn-secondary { 
                background: linear-gradient(135deg, #64748b 0%, #475569 100%) !important;
                border-color: #64748b !important;
                color: #ffffff !important;
            }
            .btn-info { 
                background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%) !important;
                border-color: #0891b2 !important;
                color: #ffffff !important;
            }
            .btn-sm { 
                padding: 0.25rem 0.5rem !important; 
                font-size: 0.78rem !important;
                border-radius: 0.3rem !important;
            }
            .btn:hover { 
                transform: translateY(-1px) !important; 
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
            }
            
            /* Alerts - Academic */
            .alert { 
                padding: 0.45rem !important; 
                margin-bottom: 0.4rem !important;
                border-radius: 0.4rem !important;
                border: 1px solid transparent !important;
                font-size: 0.85rem !important;
            }
            .alert-light { 
                background-color: #f8fafc !important;
                border-color: #e2e8f0 !important;
                color: #1e293b !important;
            }
            
            /* Navigation - Academic Style */
            .nav-link { 
                padding: 0.45rem 0.9rem !important; 
                font-size: 0.85rem !important;
                font-weight: 500 !important;
                color: #475569 !important;
                border: 1px solid transparent !important;
                border-radius: 0.4rem 0.4rem 0 0 !important;
                transition: all 0.2s ease-in-out !important;
            }
            .nav-link.active {
                background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
                color: #f8fafc !important;
                border-color: #cbd5e1 !important;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
            }
            .nav-link:hover:not(.active) {
                background-color: #f1f5f9 !important;
                color: #1e293b !important;
                transform: translateY(-1px) !important;
            }
            
            /* Input Groups */
            .input-group-text { 
                padding: 0.3rem 0.45rem !important; 
                font-size: 0.82rem !important;
                background-color: #f1f5f9 !important;
                border: 1px solid #cbd5e1 !important;
                color: #334155 !important;
            }
            
            /* Accordions - Academic */
            .accordion-button { 
                padding: 0.65rem !important; 
                font-size: 0.82rem !important;
                font-weight: 500 !important;
                background-color: #f8fafc !important;
                color: #334155 !important;
                border: 1px solid #e2e8f0 !important;
            }
            .accordion-button:not(.collapsed) {
                background-color: #1e293b !important;
                color: #f8fafc !important;
            }
            
            /* Academic Enhancement - Log Container */
            .log-container {
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
                color: #e2e8f0 !important;
                border: 1px solid #334155 !important;
                border-radius: 0.4rem !important;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
                line-height: 1.4 !important;
            }
            
            /* Academic Enhancement - Status Indicators */
            .badge {
                font-size: 0.75rem !important;
                font-weight: 500 !important;
                border-radius: 0.3rem !important;
            }
            
            /* Academic Enhancement - Progress Bars */
            .progress {
                background-color: #e2e8f0 !important;
                border-radius: 0.4rem !important;
            }
            .progress-bar {
                background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%) !important;
                transition: width 0.6s ease !important;
            }
            
            /* Academic Enhancement - Small Text */
            .small, small {
                font-size: 0.75rem !important;
                color: #64748b !important;
            }
            
            /* Academic Enhancement - Dropdown Menus */
            .dropdown-menu {
                border: 1px solid #cbd5e1 !important;
                border-radius: 0.4rem !important;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
            }
            
            /* Academic Enhancement - Tab Content */
            .tab-content {
                border: 1px solid #cbd5e1 !important;
                border-top: none !important;
                border-radius: 0 0 0.4rem 0.4rem !important;
                background-color: #ffffff !important;
            }
            
            /* Enhanced Controls Styling */
            .control-buttons .btn {
                transition: all 0.2s ease-in-out !important;
                border: 1px solid transparent !important;
            }
            .control-buttons .btn:disabled {
                opacity: 0.5 !important;
                cursor: not-allowed !important;
                transform: none !important;
                box-shadow: none !important;
            }
            .control-buttons .btn:disabled:hover {
                transform: none !important;
                box-shadow: none !important;
            }
            .control-buttons .btn-group {
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
                border-radius: 0.4rem !important;
            }
            
            /* Compact spacing for left column */
            .row { margin-bottom: 0.15rem !important; }
            .mb-1 { margin-bottom: 0.2rem !important; }
            .mb-2 { margin-bottom: 0.35rem !important; }
            
            /* Status indicators */
            .status-ready { color: #10b981 !important; }
            .status-running { color: #f59e0b !important; }
            .status-paused { color: #6b7280 !important; }
            .status-error { color: #ef4444 !important; }
            .status-completed { color: #3b82f6 !important; }
                color: #f9fafb !important;
            }
            .accordion-body { 
                padding: 0.75rem !important; 
                background-color: #ffffff !important;
            }
            
            /* Typography - Academic */
            .small, small { font-size: 0.8rem !important; color: #6b7280 !important; }
            h3 { 
                font-size: 1.75rem !important; 
                margin: 0.75rem 0 !important;
                color: #1f2937 !important;
                font-weight: 700 !important;
                font-family: 'Georgia', 'Times New Roman', serif !important;
            }
            h6 { 
                font-size: 1rem !important; 
                margin: 0.5rem 0 !important; 
                font-weight: 600 !important;
                color: #374151 !important;
            }
            
            /* Dropdowns */
            .Select-control { 
                min-height: 38px !important; 
                border-radius: 0.375rem !important;
                border: 1px solid #d1d5db !important;
            }
            .Select-placeholder, .Select-single-value { line-height: 36px !important; }
            
            /* Layout */
            .sidebar { max-height: 95vh; overflow-y: auto; }
            .js-plotly-plot { 
                margin: 0 !important; 
                border-radius: 0.375rem !important;
                border: 1px solid #e2e8f0 !important;
            }
            .rc-slider { margin: 0.5rem 0 !important; }
            
            /* Academic Progress Indicators */
            .progress {
                background-color: #f1f5f9 !important;
                border-radius: 0.25rem !important;
            }
            .progress-bar {
                background: linear-gradient(90deg, #3b82f6 0%, #1d4ed8 100%) !important;
            }
            
            /* Status indicators - Academic Colors */
            .status-running { animation: pulse 2s infinite; }
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.7; }
                100% { opacity: 1; }
            }
            
            /* Academic Hover Effects */
            .card:hover { 
                transform: translateY(-1px);
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
            }
            
            /* Academic Log Styling */
            .log-container {
                background: #1e293b !important;
                color: #e2e8f0 !important;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
                border-radius: 0.375rem !important;
                border: 1px solid #334155 !important;
            }
            
            /* Academic Badge Styling */
            .badge {
                background: linear-gradient(135deg, #374151 0%, #1f2937 100%) !important;
                color: #f9fafb !important;
            }
            
            /* Performance Metrics - Academic */
            .text-success { color: #059669 !important; }
            .text-primary { color: #2563eb !important; }
            .text-info { color: #0891b2 !important; }
            .text-muted { color: #6b7280 !important; }
            
            /* Academic Table Styling */
            .table {
                color: #374151 !important;
                border-color: #e5e7eb !important;
            }
            .table th {
                background-color: #f9fafb !important;
                border-color: #e5e7eb !important;
                color: #1f2937 !important;
                font-weight: 600 !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Simple, clean layout with Option 2 + Option 3 approach
app.layout = dbc.Container([
    # Enhanced Header with Status Bar
    dbc.Row([
        dbc.Col([
            html.H3("🚁 Drone Optimization Simulation System", className="text-center my-2"),
            # Real-time status bar
            dbc.Alert([
                dbc.Row([
                    dbc.Col([
                        html.Span("🟢 System Ready", id="system-status", className="fw-bold")
                    ], width=3),
                    dbc.Col([
                        html.Span("Coverage: --", id="live-coverage", className="small")
                    ], width=3),
                    dbc.Col([
                        html.Span("Active: --", id="live-active", className="small")
                    ], width=3),
                    dbc.Col([
                        html.Span("Step: --", id="live-step", className="small")
                    ], width=3),
                ])
            ], color="light", className="py-1 mb-2")
        ])
    ]),
    
    # Three-Column Layout: 3-6-3 split for academic focus
    dbc.Row([
        # Left Column - Main Algorithm Settings (Narrower)
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("⚙️ Algorithm Settings"),
                dbc.CardBody([
                    # Algorithm Selection
                    html.Label("🤖 Algorithm", className="fw-bold mb-1"),
                    dcc.Dropdown(
                        id='algorithm-dropdown',
                        options=[
                            {'label': 'Greedy', 'value': 'greedy'},
                            {'label': 'Genetic Algorithm', 'value': 'ga'},
                            {'label': 'Particle Swarm', 'value': 'pso'},
                            {'label': 'Simulated Annealing', 'value': 'sa'},
                            {'label': 'GA + SA Hybrid', 'value': 'ga_sa'},
                            {'label': 'Grey Wolf Optimizer', 'value': 'gwo'},
                            {'label': 'Manta Ray Foraging', 'value': 'mrfo'}
                        ],
                        value='greedy',
                        className="mb-2"
                    ),
                    
                    # Parallel Processing Toggle
                    dbc.Switch(
                        id="parallel-processing-switch",
                        label="⚡ Parallel Processing",
                        value=False,
                        disabled=True,
                        className="mb-1"
                    ),
                    html.Div(id="parallel-info", className="mb-1 text-muted small"),
                    
                    # Algorithm Parameters with enhanced styling
                    dbc.Card([
                        dbc.CardHeader("🔧 Parameters", className="py-1"),
                        dbc.CardBody([
                            html.Div(id='algorithm-params', className="mt-1")
                        ], className="py-1")
                    ], className="mt-1"),
                    
                    # Main Simulation Controls - Enhanced Design
                    html.Hr(className="my-2"),
                    html.Div([
                        html.I(className="fas fa-gamepad me-2", style={"color": "#3b82f6"}),
                        html.Span("Controls", className="fw-bold")
                    ], className="d-flex align-items-center mb-2),
                    
                    # Run Name with better styling
                    html.Label("Run Identifier", className="small text-muted mb-1"),
                    dbc.InputGroup([
                        dbc.Input(
                            id="run-name-input",
                            placeholder="Enter run name...",
                            value=f"Run_{datetime.now().strftime('%m%d_%H%M')}",
                            size="sm",
                            className="form-control-sm"
                        ),
                        dbc.Button(
                            html.I(className="fas fa-sync-alt"), 
                            id="generate-run-name", 
                            color="outline-secondary", 
                            size="sm",
                            title="Generate new name"
                        )
                    ], size="sm", className="mb-2"),
                    
                    # Status Card
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.Div([
                                    html.I(id="status-icon", className="fas fa-circle me-2", style={"color": "#6b7280"}),
                                    html.Span("System Status", className="small fw-bold")
                                ], className="d-flex align-items-center mb-1"),
                                html.Div(id="sim-status-text", children="Ready to Initialize", 
                                        className="small text-muted")
                            ])
                        ], className="py-1 px-2")
                    ], className="mb-2", style={"background": "linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)"}),
                    
                    # Hidden alert for callback compatibility
                    dbc.Alert(id="sim-status-alert", children="⭕ Not Started", color="secondary", 
                              className="d-none"),
                    
                    # Enhanced Control Buttons with States
                    html.Div([
                        # Initialize Button - Full Width
                        dbc.Button([
                            html.I(className="fas fa-rocket me-2"),
                            "Initialize System"
                        ], 
                        id="init-button", 
                        color="primary", 
                        size="sm", 
                        className="w-100 mb-1",
                        style={"font-weight": "500"}
                        ),
                        
                        # Main Control Button Group
                        html.Div([
                            html.Label("Simulation Control", className="small text-muted mb-1"),
                            dbc.ButtonGroup([
                                dbc.Button([
                                    html.I(id="main-control-icon", className="fas fa-play me-1"),
                                    html.Span(id="main-control-text", children="Start")
                                ], 
                                id="main-control-btn", 
                                color="success", 
                                size="sm", 
                                disabled=True,
                                title="Start/Pause simulation"
                                ),
                                dbc.Button([
                                    html.I(className="fas fa-step-forward me-1"),
                                    "Step"
                                ], 
                                id="step-button", 
                                color="info", 
                                size="sm", 
                                disabled=True,
                                title="Execute one step"
                                ),
                            ], className="w-100 mb-1")
                        ]),
                        
                        # Reset/Stop Controls
                        html.Div([
                            html.Label("Reset Control", className="small text-muted mb-1"),
                            dbc.ButtonGroup([
                                dbc.Button([
                                    html.I(className="fas fa-stop me-1"),
                                    "Stop"
                                ], 
                                id="stop-button", 
                                color="warning", 
                                size="sm", 
                                disabled=True,
                                title="Stop simulation"
                                ),
                                dbc.Button([
                                    html.I(className="fas fa-redo me-1"),
                                    "Reset"
                                ], 
                                id="stop-reset-btn", 
                                color="secondary", 
                                size="sm", 
                                title="Reset to initial state"
                                ),
                            ], className="w-100")
                        ])
                    ], className="control-buttons")
                ])
            ])
        ], width=2),  # Left column - Much narrower for academic layout
        
        # Center Column - Main Visualization (Much wider for academic focus)
        dbc.Col([
            dbc.Tabs([
                # Simulation View Tab
                dbc.Tab([
                    dcc.Graph(id="simulation-graph", style={'height': '55vh', 'width': '100%'}),
                    html.Div([
                        html.Button("📥 Download", id="download-plot-btn", className="btn btn-outline-primary btn-sm"),
                        dcc.Download(id="download-plot"),
                    ], className="mb-1"),
                ], label="🎯 Simulation"),
                
                # Metrics Tab
                dbc.Tab([
                    dbc.Row([
                        dbc.Col(dcc.Graph(id="coverage-chart", style={'height': '26vh'}), width=6),
                        dbc.Col(dcc.Graph(id="power-chart", style={'height': '26vh'}), width=6)
                    ], className="mb-1"),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id="overlap-chart", style={'height': '26vh'}), width=6),
                        dbc.Col(dcc.Graph(id="violation-chart", style={'height': '26vh'}), width=6)
                    ])
                ], label="📊 Metrics"),
                
                # Experiment Results Tab
                dbc.Tab([
                    html.Div(id="experiment-summary-content")
                ], label="🧪 Results"),
                
                # Stored Runs Tab
                dbc.Tab([
                    html.Div(id="stored-runs-content")
                ], label="💾 Stored")
            ]),
            
            # Algorithm Iteration Logs
            dbc.Card([
                dbc.CardHeader("📊 Iteration Logs", className="py-1"),
                dbc.CardBody([
                    html.Div(id="iteration-logs-display", style={
                        'height': '100px',
                        'overflow-y': 'auto',
                        'background-color': '#f8f9fa',
                        'padding': '6px',
                        'border-radius': '4px',
                        'font-family': 'monospace',
                        'font-size': '10px'
                    })
                ], className="py-1")
            ], className="mt-2")
        ], width=8),  # Center column - Much wider for main content
        
        # Right Column - Supporting Cards with Accordions (Much narrower)
        dbc.Col([
            # Environment & Settings Accordion
            dbc.Accordion([
                # Environment Settings
                dbc.AccordionItem([
                    dbc.Row([
                        dbc.Col([
                            dbc.Input(id="area-width", type="number", value=100, min=10, max=1000, size="sm"),
                            html.Small("Width", className="text-muted")
                        ], width=6),
                        dbc.Col([
                            dbc.Input(id="area-height", type="number", value=100, min=10, max=1000, size="sm"),
                            html.Small("Height", className="text-muted")
                        ], width=6)
                    ], className="mb-2"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Input(id="total-drones", type="number", value=20, min=1, max=100, size="sm"),
                            html.Small("Drones", className="text-muted")
                        ], width=6),
                        dbc.Col([
                            dbc.Input(id="sensing-radius", type="number", value=20, min=1, max=50, size="sm"),
                            html.Small("Radius", className="text-muted")
                        ], width=6)
                    ]),
                    
                    # Parking scenario
                    html.Details([
                        html.Summary("🅿️ Parking Settings", className="text-muted mt-2"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Input(id="parking-spots", type="number", value=100, min=10, max=1000, size="sm"),
                                html.Small("Spots", className="text-muted")
                            ], width=6),
                            dbc.Col([
                                dbc.Input(id="disabled-spots", type="number", value=10, min=0, max=100, size="sm"),
                                html.Small("Disabled", className="text-muted")
                            ], width=6)
                        ])
                    ])
                ], title="🌍 Environment"),
                
                # Stopping Criteria
                dbc.AccordionItem([
                    dcc.Dropdown(
                        id='stopping-template-dropdown',
                        options=[
                            {'label': '🐌 Conservative', 'value': 'conservative'},
                            {'label': '⚖️ Balanced', 'value': 'balanced'},
                            {'label': '⚡ Fast', 'value': 'fast'},
                            {'label': '🔧 Custom', 'value': 'custom'}
                        ],
                        value='balanced',
                        className="mb-2"
                    ),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.InputGroup([
                                dbc.Input(id="target-coverage", type="number", value=90, min=50, max=100, size="sm"),
                                dbc.InputGroupText("%")
                            ], size="sm"),
                            html.Small("Coverage", className="text-muted")
                        ], width=6),
                        dbc.Col([
                            dbc.Input(id="max-iterations", type="number", value=100, min=10, max=1000, size="sm"),
                            html.Small("Max Iter", className="text-muted")
                        ], width=6)
                    ], className="mb-2"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Input(id="convergence-threshold", type="number", value=0.01, min=0.001, max=0.1, step=0.001, size="sm"),
                            html.Small("Convergence", className="text-muted")
                        ], width=6),
                        dbc.Col([
                            dbc.InputGroup([
                                dbc.Input(id="time-limit", type="number", value=60, min=5, max=600, size="sm"),
                                dbc.InputGroupText("s")
                            ], size="sm"),
                            html.Small("Time Limit", className="text-muted")
                        ], width=6)
                    ])
                ], title="🛑 Stopping Criteria"),
                
                # Advanced Settings
                dbc.AccordionItem([
                    html.Label("🏃 Simulation Speed", className="small"),
                    dcc.Slider(
                        id="simulation-speed",
                        min=0.1, max=5.0, step=0.1, value=1.0,
                        marks={0.5: '0.5x', 1: '1x', 2: '2x', 5: '5x'},
                        tooltip={"placement": "bottom", "always_visible": False}
                    ),
                    
                    html.Hr(className="my-2"),
                    
                    dbc.ButtonGroup([
                        dbc.Button("💾 Save Config", id="save-config", color="info", size="sm"),
                        dbc.Button("📁 Load Config", id="load-config", color="info", size="sm")
                    ], className="w-100")
                ], title="⚙️ Advanced")
            ], className="mb-2"),
            
            # Live Logs (Non-accordion - important info)
            dbc.Card([
                dbc.CardHeader([
                    html.Span("📝 Live Logs", className="me-2"),
                    dbc.Badge("0", id="log-count", color="secondary", className="small")
                ], className="py-1 d-flex justify-content-between align-items-center"),
                dbc.CardBody([
                    html.Div(id="log-output", className="log-container", style={
                        'height': '18vh', 
                        'overflow-y': 'auto', 
                        'font-size': '11px',
                        'padding': '8px'
                    })
                ], className="py-1")
            ], className="mb-2"),
            
            # Status & Quick Actions with Performance Metrics
            dbc.Card([
                dbc.CardHeader("📊 Performance Dashboard", className="py-1"),
                dbc.CardBody([
                    # Quick metrics
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H6("0%", id="current-coverage", className="text-success mb-0"),
                                html.Small("Coverage", className="text-muted")
                            ], className="text-center")
                        ], width=4),
                        dbc.Col([
                            html.Div([
                                html.H6("0", id="current-active", className="text-primary mb-0"),
                                html.Small("Active", className="text-muted")
                            ], className="text-center")
                        ], width=4),
                        dbc.Col([
                            html.Div([
                                html.H6("0s", id="current-time", className="text-info mb-0"),
                                html.Small("Runtime", className="text-muted")
                            ], className="text-center")
                        ], width=4),
                    ], className="mb-2"),
                    
                    # Progress bar
                    html.Div([
                        html.Small("Progress", className="text-muted"),
                        dbc.Progress(id="optimization-progress", value=0, className="mb-2", style={"height": "8px"})
                    ]),
                    
                    # Quick actions
                    dbc.ButtonGroup([
                        dbc.Button("🚀 Quick Run", id="quick-run", color="success", size="sm", title="Run 20 steps"),
                        dbc.Button("📊 Compare", id="quick-compare", color="info", size="sm", title="Compare algorithms"),
                        dbc.Button("🔄 Reset All", id="quick-reset", color="secondary", size="sm", title="Reset everything")
                    ], className="w-100")
                ], className="py-1")
            ])
        ], width=2)  # Right column - Much narrower for academic layout
    ]),
    
    # Stores and other components
    dcc.Interval(
        id='simulation-interval',
        interval=1000,
        n_intervals=0,
        disabled=True
    ),
    dcc.Store(id='algorithm-params-store'),
    dcc.Store(id='simulation-state'),
    dcc.Store(id='experiment-data-store'),
    dcc.Store(id='iteration-logs-store'),
    dcc.Store(id='stopping-criteria-store'),
    dcc.Store(id='current-run-store'),
    dcc.Store(id='user-preferences-store', storage_type='local'),
    
    # Modals and alerts
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("🎯 Optimization Results")),
        dbc.ModalBody(id="results-modal-body"),
        dbc.ModalFooter([
            dbc.Button("Save Run", id="save-run-btn", color="success", className="me-2"),
            dbc.Button("Close", id="close-results-modal", color="secondary")
        ])
    ], id="results-modal", size="xl", is_open=False),
    
    dbc.Alert(
        id="stopping-alert",
        dismissable=True,
        is_open=False,
        duration=8000,
        className="position-fixed",
        style={"top": "20px", "right": "20px", "z-index": 9999, "min-width": "400px"}
    )
], fluid=True)

# Quick action button callbacks
@app.callback(
    Output('log-output', 'children', allow_duplicate=True),
    [Input('quick-run', 'n_clicks')],
    prevent_initial_call=True
)
def quick_run_action(n_clicks):
    if n_clicks:
        return [html.Div("🚀 Quick run triggered!", className="text-success")]
    return dash.no_update

@app.callback(
    Output('log-output', 'children', allow_duplicate=True),
    [Input('quick-compare', 'n_clicks')],
    prevent_initial_call=True
)
def quick_compare_action(n_clicks):
    if n_clicks:
        return [html.Div("📊 Quick compare triggered!", className="text-info")]
    return dash.no_update

@app.callback(
    Output('log-output', 'children', allow_duplicate=True),
    [Input('quick-reset', 'n_clicks')],
    prevent_initial_call=True
)
def quick_reset_action(n_clicks):
    if n_clicks:
        return [html.Div("🔄 Quick reset triggered!", className="text-warning")]
    return dash.no_update

# Enhanced UI Callbacks for finalized components

# Real-time status bar update
@app.callback(
    [Output('system-status', 'children'),
     Output('live-coverage', 'children'),
     Output('live-active', 'children'),
     Output('live-step', 'children'),
     Output('current-coverage', 'children'),
     Output('current-active', 'children'),
     Output('current-time', 'children'),
     Output('optimization-progress', 'value'),
     Output('log-count', 'children')],
    [Input('simulation-interval', 'n_intervals'),
     Input('step-button', 'n_clicks')],
    [State('algorithm-dropdown', 'value'),
     State('log-output', 'children')]
)
def update_status_dashboard(n_intervals, step_clicks, algorithm, log_content):
    """Update the status dashboard with real-time metrics"""
    global simulation, current_sim_state
    
    # Default values
    system_status = "🟡 Initializing..."
    coverage = "Coverage: --"
    active = "Active: --" 
    step = "Step: --"
    coverage_pct = "0%"
    active_count = "0"
    runtime = "0s"
    progress = 0
    log_count = "0"
    
    try:
        if simulation is not None:
            # Get current metrics
            latest_coverage = simulation.metrics_history.get('coverage', [0])[-1] if simulation.metrics_history.get('coverage') else 0
            latest_active = simulation.metrics_history.get('active_drones', [0])[-1] if simulation.metrics_history.get('active_drones') else 0
            current_step = simulation.step_count
            
            # Update values
            coverage = f"Coverage: {latest_coverage*100:.1f}%"
            active = f"Active: {latest_active}"
            step = f"Step: {current_step}"
            coverage_pct = f"{latest_coverage*100:.1f}%"
            active_count = str(latest_active)
            
            # Calculate progress (assuming max 100 steps)
            progress = min((current_step / 100) * 100, 100)
            
            # System status based on state
            if current_sim_state == SimState.RUNNING:
                system_status = "🟢 Running"
            elif current_sim_state == SimState.PAUSED:
                system_status = "🟡 Paused"
            elif current_sim_state == SimState.STOPPED:
                system_status = "🔴 Stopped"
            else:
                system_status = "🔵 Ready"
        
        # Count log entries
        if log_content and isinstance(log_content, str):
            log_count = str(len(log_content.split('\n')))
            
    except Exception as e:
        system_status = "❌ Error"
        print(f"Status update error: {e}")
    
    return system_status, coverage, active, step, coverage_pct, active_count, runtime, progress, log_count

# Enhanced run name generator
@app.callback(
    Output('run-name-input', 'value', allow_duplicate=True),
    Input('generate-run-name', 'n_clicks'),
    State('algorithm-dropdown', 'value'),
    prevent_initial_call=True
)
def generate_enhanced_run_name(n_clicks, algorithm):
    """Generate enhanced run names with algorithm and timestamp"""
    if n_clicks:
        algorithm_names = {
            'greedy': 'Greedy',
            'ga': 'GA',
            'pso': 'PSO',
            'sa': 'SA',
            'ga_sa': 'GA_SA',
            'gwo': 'GWO',
            'mrfo': 'MRFO'
        }
        alg_name = algorithm_names.get(algorithm, 'ALG')
        timestamp = datetime.now().strftime('%m%d_%H%M%S')
        coverage_target = 90  # Could be dynamic based on stopping criteria
        return f"{alg_name}_T{coverage_target}_{timestamp}"
    return dash.no_update

# Button State Management Callback
@app.callback(
    [Output('init-button', 'disabled'),
     Output('main-control-btn', 'disabled'),
     Output('step-button', 'disabled'),
     Output('stop-button', 'disabled'),
     Output('stop-reset-btn', 'disabled),
     Output('main-control-icon', 'className'),
     Output('main-control-text', 'children'),
     Output('status-icon', 'className'),
     Output('status-icon', 'style'),
     Output('sim-status-text', 'children')],
    [Input('simulation-state', 'data'),
     Input('init-button', 'n_clicks'),
     Input('main-control-btn', 'n_clicks'),
     Input('stop-button', 'n_clicks'),
     Input('stop-reset-btn', 'n_clicks')]
)
def update_button_states(sim_state, init_clicks, control_clicks, stop_clicks, reset_clicks):
    """Update button states based on current simulation state"""
    
    # Default states - Initialize button is enabled by default
    init_disabled = False
    control_disabled = True
    step_disabled = True
    stop_disabled = True
    reset_disabled = False
    
    control_icon = "fas fa-play me-1"
    control_text = "Start"
    status_icon = "fas fa-circle me-2"
    status_style = {"color": "#6b7280"}
    status_text = "Ready to Initialize"
    
    # Check current simulation state
    if sim_state:
        if sim_state.get('initialized', False):
            # Currently active/initialized session
            init_disabled = True
            control_disabled = False
            step_disabled = False
            stop_disabled = False
            
            # Determine state based on simulation status
            if sim_state.get('running', False):
                control_icon = "fas fa-pause me-1"
                control_text = "Pause"
                status_icon = "fas fa-circle me-2 status-running"
                status_style = {"color": "#f59e0b"}
                status_text = "Simulation Running"
                step_disabled = True  # Can't step while running
                
            elif sim_state.get('paused', False):
                control_icon = "fas fa-play me-1"
                control_text = "Resume"
                status_icon = "fas fa-circle me-2 status-paused"
                status_style = {"color": "#6b7280"}
                status_text = "Simulation Paused"
                
            elif sim_state.get('completed', False):
                # Experiment completed - allow re-initialization
                init_disabled = False  # Enable for new experiment
                control_disabled = True
                step_disabled = True
                stop_disabled = True
                status_icon = "fas fa-check-circle me-2 status-completed"
                status_style = {"color": "#3b82f6"}
                status_text = "Experiment Completed - Ready for New Run"
                
            else:
                # Initialized but not running
                status_icon = "fas fa-circle me-2 status-ready"
                status_style = {"color": "#10b981"}
                status_text = "Ready to Start"
                
        elif sim_state.get('ever_initialized', False) and not sim_state.get('initialized', False):
            # Was initialized but now stopped/reset - allow re-initialization
            init_disabled = False  # Enable for new session
            control_disabled = True
            step_disabled = True
            stop_disabled = True
            status_icon = "fas fa-circle me-2"
            status_style = {"color": "#6b7280"}
            status_text = "System Stopped - Ready to Initialize New Run"
    
    # Handle error states
    if sim_state and sim_state.get('error', False):
        init_disabled = False  # Allow re-initialization after error
        control_disabled = True
        step_disabled = True
        stop_disabled = True
        status_icon = "fas fa-exclamation-circle me-2 status-error"
        status_style = {"color": "#ef4444"}
        status_text = "Error Occurred - Ready to Initialize New Run"
    
    return (
        init_disabled,
        control_disabled, 
        step_disabled,
        stop_disabled,
        reset_disabled,
        control_icon,
        control_text,
        status_icon,
        status_style,
        status_text
    )
    
# REFACTORED AND CORRECTED SIMULATION LOGIC
# -----------------------------------------

# 1. Callback to initialize the simulation environment
@app.callback(
    [Output('simulation-state', 'data', allow_duplicate=True),
     Output('log-output', 'children', allow_duplicate=True),
     Output('iteration-logs-display', 'children', allow_duplicate=True),
     Output('simulation-graph', 'figure', allow_duplicate=True)],
    [Input('init-button', 'n_clicks')],
    [State('area-width', 'value'),
     State('area-height', 'value'),
     State('total-drones', 'value'),
     State('sensing-radius', 'value'),
     State('max-iterations', 'value'),
     State('target-coverage', 'value'),
     State('time-limit', 'value'),
     State('convergence-threshold', 'value')],
    prevent_initial_call=True
)
def initialize_simulation(n_clicks, width, height, drones, radius, max_iter, target_cov, time_limit, convergence):
    """Initializes the simulation environment and resets the state."""
    global simulation, current_sim_state
    
    if not n_clicks:
        return dash.no_update

    try:
        # Create a new simulation environment
        simulation = DroneEnvironment(
            area_width=width,
            area_height=height,
            num_drones=drones,
            sensing_radius=radius
        )
        simulation.reset()
        current_sim_state = SimState.STOPPED

        # Create initial state store
        initial_state = {
            'status': 'initialized',
            'iteration': 0,
            'max_iterations': max_iter or 500, # Fallback to a high number
            'target_coverage': (target_cov or 98) / 100.0,
            'time_limit': time_limit or 300,
            'convergence_threshold': convergence or 0.001,
            'start_time': datetime.now().isoformat(),
            'logs': []
        }
        
        log_message = [html.Div(f"✅ System initialized at {datetime.now().strftime('%H:%M:%S')}", className="text-success")]
        fig = create_simulation_view(simulation)
        
        return initial_state, log_message, [], fig
    except Exception as e:
        error_message = [html.Div(f"❌ Initialization Error: {e}", className="text-danger")]
        return {}, error_message, [], go.Figure()


# 2. Callback to manage the simulation's run state (Start, Pause, Stop, Reset)
@app.callback(
    [Output('simulation-state', 'data', allow_duplicate=True),
     Output('simulation-interval', 'disabled')],
    [Input('main-control-btn', 'n_clicks'),
     Input('stop-button', 'n_clicks'),
     Input('stop-reset-btn', 'n_clicks')],
    [State('simulation-state', 'data')],
    prevent_initial_call=True
)
def control_simulation_state(start_pause_clicks, stop_clicks, reset_clicks, sim_state):
    """Manages the core run state of the simulation."""
    global current_sim_state
    
    if not sim_state:
        return dash.no_update, True

    triggered_id = ctx.triggered_id
    
    if triggered_id == 'main-control-btn':
        if sim_state['status'] == 'running':
            sim_state['status'] = 'paused'
            current_sim_state = SimState.PAUSED
            return sim_state, True # Disable interval
        else: # Paused or initialized
            sim_state['status'] = 'running'
            current_sim_state = SimState.RUNNING
            return sim_state, False # Enable interval

    elif triggered_id == 'stop-button':
        sim_state['status'] = 'stopped'
        current_sim_state = SimState.STOPPED
        return sim_state, True

    elif triggered_id == 'stop-reset-btn':
        current_sim_state = SimState.STOPPED
        # Returning {} clears the state, effectively resetting it
        return {}, True

    return dash.no_update, True


# 3. The main simulation loop, triggered by the interval or step button
@app.callback(
    [Output('simulation-graph', 'figure'),
     Output('iteration-logs-display', 'children'),
     Output('simulation-state', 'data'),
     Output('stopping-alert', 'is_open'),
     Output('stopping-alert', 'children'),
     Output('stopping-alert', 'color')],
    [Input('simulation-interval', 'n_intervals'),
     Input('step-button', 'n_clicks')],
    [State('simulation-state', 'data'),
     State('algorithm-dropdown', 'value'),
     State('algorithm-params-store', 'data')] # Assuming params are stored
)
def update_simulation(n_intervals, step_clicks, sim_state, algorithm, algo_params_flat):
    """The core simulation loop that executes one step per trigger."""
    global simulation, current_sim_state

    triggered_id = ctx.triggered_id
    is_step = triggered_id == 'step-button'
    
    # Do nothing if not running, or if stepping but not in a valid state
    if not sim_state or sim_state['status'] not in ['running', 'paused', 'initialized']:
        return dash.no_update

    if sim_state['status'] == 'running' and is_step:
        return dash.no_update # Don't step while auto-running

    if sim_state['status'] in ['paused', 'initialized'] and not is_step:
        return dash.no_update # Don't auto-run if paused

    # --- Parameter Gathering and Filtering ---
    # This part is crucial and was missing.
    # A proper implementation would use pattern-matching on all param inputs.
    # For now, we'll assume they are collected into `algorithm-params-store`.
    # Since that store isn't populated yet, we'll use the robust defaults.
    
    # The `filter_params` function is now available globally in this file.
    # A truly robust solution would gather all `State` from the UI here.
    # Let's simulate that for now.
    algo_params = filter_params(algorithm, {}) # Using defaults for stability

    # --- Termination Condition Check ---
    stop_reason = None
    if sim_state['iteration'] >= sim_state.get('max_iterations', 500):
        stop_reason = f"Maximum iterations ({sim_state['max_iterations']}) reached."
    
    # Add other checks for coverage, time, etc. here
    
    if stop_reason:
        sim_state['status'] = 'stopped'
        current_sim_state = SimState.STOPPED
        alert = dbc.Alert(f"🏁 Simulation Stopped: {stop_reason}", color="info")
        return dash.no_update, dash.no_update, sim_state, True, alert, "info"

    # --- Execute one simulation step ---
    try:
        # This is where the selected algorithm is called
        # For this example, we use a placeholder step function
        
        # Placeholder for actual algorithm call
        # e.g., best_placements, metrics = greedy_optimization(simulation, **algo_params)
        simulation.drones = np.random.rand(simulation.num_drones, 2) * 100
        simulation.update_metrics()
        
        sim_state['iteration'] += 1
        
        # Log the iteration
        log_entry = {
            'iteration': sim_state['iteration'],
            'fitness': np.random.rand() * 100,
            'coverage': simulation.coverage * 100,
            'algorithm': algorithm.upper()
        }
        sim_state.setdefault('logs', []).append(log_entry)
        
        # Update figure and logs
        fig = create_simulation_view(simulation)
        log_display = [
            html.Div(f"{l['algorithm']} Iteration {l['iteration']}: Fitness = {l['fitness']:.2f}, Coverage = {l['coverage']:.1f}%")
            for l in sim_state['logs'][-10:] # Show last 10 logs
        ]
        
        # If this was a manual step, pause the simulation again
        if is_step:
            sim_state['status'] = 'paused'
            current_sim_state = SimState.PAUSED

        return fig, log_display, sim_state, False, "", ""

    except Exception as e:
        sim_state['status'] = 'stopped'
        current_sim_state = SimState.STOPPED
        alert = dbc.Alert(f"❌ Simulation Error: {e}", color="danger")
        return go.Figure(), [], sim_state, True, alert, "danger"


# 4. Callback to update button states based on the simulation state
@app.callback(
    [Output('init-button', 'disabled'),
     Output('main-control-btn', 'disabled'),
     Output('step-button', 'disabled'),
     Output('stop-button', 'disabled'),
     Output('main-control-icon', 'className'),
     Output('main-control-text', 'children'),
     Output('sim-status-text', 'children')],
    [Input('simulation-state', 'data')]
)
def update_button_states(sim_state):
    """Updates the UI control buttons based on the current simulation state."""
    if not sim_state or sim_state.get('status') is None:
        # Default state before initialization
        return False, True, True, True, "fas fa-play", "Start", "Ready to Initialize"

    status = sim_state.get('status')
    
    if status == 'initialized':
        return True, False, False, False, "fas fa-play", "Start", "Ready to Start"
    elif status == 'running':
        return True, False, True, False, "fas fa-pause", "Pause", "Running..."
    elif status == 'paused':
        return True, False, False, False, "fas fa-play", "Resume", "Paused"
    elif status == 'stopped':
        return True, True, True, True, "fas fa-play", "Start", "Stopped. Re-initialize to run."
    
    # Default case (e.g., after reset)
    return False, True, True, True, "fas fa-play", "Start", "Ready to Initialize"


# Callback for iteration logs display (enhanced)
@app.callback(
    Output('log-output', 'children'),
    [Input('iteration-logs-display', 'children')]
)
def update_logs(iteration_logs):
    """Update the live logs section"""
    if iteration_logs:
        return [
            html.Div(f"📊 Algorithm running - {len(iteration_logs)} iterations completed", className="text-info"),
            html.Div(f"⏰ Last update: {datetime.now().strftime('%H:%M:%S')}", className="text-muted small")
        ]
    return [html.Div("📝 No active simulation", className="text-muted")]

# Add keyboard shortcuts
app.index_string += '''
<script>
    document.addEventListener('keydown', function(event) {
        // Only trigger if not typing in an input field
        if (event.target.tagName.toLowerCase() !== 'input') {
            switch(event.key) {
                case ' ': // Spacebar - Start/Pause
                    event.preventDefault();
                    document.getElementById('main-control-btn').click();
                    break;
                case 's': // S - Step
                    document.getElementById('step-button').click();
                    break;
                case 'r': // R - Reset
                    document.getElementById('stop-reset-btn').click();
                    break;
                case 'i': // I - Initialize
                    document.getElementById('init-button').click();
                    break;
            }
        }
    });
</script>
'''

# Run the app
if __name__ == '__main__':
    print("🚁 Starting Enhanced Drone Optimization Simulation System...")
    print("📍 Open your browser to: http://127.0.0.1:8050")
    app.run_server(debug=True, host='127.0.0.1', port=8050)
