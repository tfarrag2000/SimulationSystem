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
                    ], className="d-flex align-items-center mb-2"),
                    
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
     Output('stop-reset-btn', 'disabled'),
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
    
# Essential callbacks for algorithm functionality

# Callback to update algorithm parameters based on selected algorithm
@app.callback(
    [Output('algorithm-params', 'children'),
     Output('parallel-processing-switch', 'disabled')],
    [Input('algorithm-dropdown', 'value')]
)
def update_algorithm_params(algorithm):
    """Update algorithm-specific parameters dynamically"""
    
    # Define algorithm parameters
    params = {
        'greedy': {
            'desired_coverage': {'label': 'Coverage Target', 'value': 0.95, 'type': 'number', 'min': 0.5, 'max': 1.0, 'step': 0.01},
            'overlap_weight': {'label': 'Overlap Weight', 'value': 0.2, 'type': 'number', 'min': 0.0, 'max': 1.0, 'step': 0.1},
            'energy_weight': {'label': 'Energy Weight', 'value': 0.1, 'type': 'number', 'min': 0.0, 'max': 1.0, 'step': 0.1}
        },
        'ga': {
            'population_size': {'label': 'Population Size', 'value': 50, 'type': 'number', 'min': 10, 'max': 200},
            'num_generations': {'label': 'Generations', 'value': 100, 'type': 'number', 'min': 10, 'max': 500},
            'mutation_rate': {'label': 'Mutation Rate', 'value': 0.1, 'type': 'number', 'min': 0.01, 'max': 0.5, 'step': 0.01},
            'crossover_rate': {'label': 'Crossover Rate', 'value': 0.8, 'type': 'number', 'min': 0.1, 'max': 1.0, 'step': 0.1}
        },
        'pso': {
            'swarm_size': {'label': 'Swarm Size', 'value': 30, 'type': 'number', 'min': 10, 'max': 100},
            'iterations': {'label': 'Iterations', 'value': 100, 'type': 'number', 'min': 10, 'max': 500},
            'inertia': {'label': 'Inertia Weight', 'value': 0.9, 'type': 'number', 'min': 0.1, 'max': 1.5, 'step': 0.1},
            'cognitive_weight': {'label': 'Cognitive Weight', 'value': 2.0, 'type': 'number', 'min': 0.5, 'max': 3.0, 'step': 0.1}
        },
        'sa': {
            'num_iterations': {'label': 'Iterations', 'value': 100, 'type': 'number', 'min': 10, 'max': 500},
            'initial_temp': {'label': 'Initial Temperature', 'value': 1000, 'type': 'number', 'min': 100, 'max': 5000},
            'cooling_rate': {'label': 'Cooling Rate', 'value': 0.95, 'type': 'number', 'min': 0.8, 'max': 0.99, 'step': 0.01}
        },
        'ga_sa': {
            'population_size': {'label': 'Population Size', 'value': 30, 'type': 'number', 'min': 10, 'max': 100},
            'num_generations': {'label': 'Generations', 'value': 50, 'type': 'number', 'min': 10, 'max': 200},
            'sa_temp': {'label': 'SA Temperature', 'value': 100, 'type': 'number', 'min': 10, 'max': 500}
        },
        'gwo': {
            'population_size': {'label': 'Population Size', 'value': 30, 'type': 'number', 'min': 10, 'max': 100},
            'max_iterations': {'label': 'Max Iterations', 'value': 100, 'type': 'number', 'min': 10, 'max': 500}
        },
        'mrfo': {
            'population_size': {'label': 'Population Size', 'value': 30, 'type': 'number', 'min': 10, 'max': 100},
            'num_generations': {'label': 'Generations', 'value': 100, 'type': 'number', 'min': 10, 'max': 500}
        }
    }
    
    # Generate parameter inputs
    param_elements = []
    algo_params = params.get(algorithm, {})
    
    for param_name, param_config in algo_params.items():
        param_elements.append(
            dbc.Row([
                dbc.Col([
                    dbc.Label(param_config['label'], className="small"),
                    dbc.Input(
                        id=f"{algorithm}-{param_name}",
                        type=param_config['type'],
                        value=param_config['value'],
                        min=param_config.get('min'),
                        max=param_config.get('max'),
                        step=param_config.get('step', 1),
                        size="sm"
                    )
                ])
            ], className="mb-1")
        )
    
    # Enable parallel processing for supported algorithms
    parallel_disabled = algorithm in ['greedy', 'sa']
    
    return param_elements, parallel_disabled

# Callback to handle algorithm execution (simplified for testing)
@app.callback(
    [Output('iteration-logs-display', 'children'),
     Output('sim-status-alert', 'children'),
     Output('sim-status-alert', 'color'),
     Output('simulation-state', 'data')],
    [Input('main-control-btn', 'n_clicks'),
     Input('step-button', 'n_clicks'),
     Input('init-button', 'n_clicks'),
     Input('stop-button', 'n_clicks'),
     Input('stop-reset-btn', 'n_clicks')],
    [State('algorithm-dropdown', 'value'),
     State('max-iterations', 'value'),
     State('target-coverage', 'value'),
     State('simulation-state', 'data')]
)
def handle_simulation_control(start_clicks, step_clicks, init_clicks, stop_clicks, reset_clicks, algorithm, max_iter, target_coverage, current_state):
    """Enhanced simulation control with proper state management"""
    
    # Initialize state if not exists
    if not current_state:
        current_state = {
            'initialized': False,
            'running': False,
            'paused': False,
            'completed': False,
            'error': False,
            'step_count': 0,
            'max_steps': max_iter or 20
        }
    
    if not any([start_clicks, step_clicks, init_clicks, stop_clicks, reset_clicks]):
        return [], "⭕ Not Started", "secondary", current_state
    
    # Determine which button was clicked
    ctx_triggered = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    if ctx_triggered == 'init-button':
        # Initialize simulation - this should only happen once
        new_state = {
            'initialized': True,
            'running': False,
            'paused': False,
            'completed': False,
            'error': False,
            'step_count': 0,
            'max_steps': max_iter or 20,
            'ever_initialized': True  # Track that system was ever initialized
        }
        return [html.Div("🚀 Simulation initialized successfully", className="text-success")], "✅ Initialized", "success", new_state
    
    elif ctx_triggered == 'stop-reset-btn':
        # Complete reset - allows re-initialization
        reset_state = {
            'initialized': False,
            'running': False,
            'paused': False,
            'completed': False,
            'error': False,
            'step_count': 0,
            'max_steps': max_iter or 20,
            'ever_initialized': False
        }
        return [], "🔄 System Reset", "secondary", reset_state
    
    elif ctx_triggered == 'stop-button':
        # Stop simulation and allow re-initialization
        new_state = current_state.copy()
        new_state.update({
            'initialized': False,  # Clear initialized state to allow re-init
            'running': False,
            'paused': False,
            'completed': False,
            'ever_initialized': True  # Remember it was initialized before
        })
        return [], "⏹️ Simulation Stopped", "warning", new_state
    
    elif ctx_triggered == 'step-button' and current_state.get('initialized', False):
        # Execute one step
        step_num = current_state.get('step_count', 0) + 1
        
        if step_num <= current_state.get('max_steps', 20):
            log_entry = html.Div([
                html.Span(f"{algorithm.upper()} Step {step_num}: ", className="text-primary fw-bold"),
                html.Span(f"Fitness = {25.0 + step_num * 2:.2f}, ", className="text-success"),
                html.Span(f"Coverage = {20.0 + step_num * 3:.1f}%", className="text-info")
            ], className="mb-1")
            
            new_state = current_state.copy()
            new_state.update({
                'step_count': step_num,
                'paused': True,
                'running': False,
                'completed': step_num >= current_state.get('max_steps', 20)
            })
            
            # If completed, allow re-initialization
            if new_state['completed']:
                new_state.update({
                    'initialized': False,  # Clear to allow re-init
                    'ever_initialized': True
                })
            
            status = f"⏸️ Step {step_num} Complete"
            color = "success" if new_state['completed'] else "warning"
            
            return [log_entry], status, color, new_state
        else:
            new_state = current_state.copy()
            new_state.update({
                'completed': True, 
                'running': False,
                'initialized': False,  # Clear to allow re-init
                'ever_initialized': True
            })
            return [html.Div("🏁 Max iterations reached", className="text-danger")], "🛑 Complete", "success", new_state
    
    elif ctx_triggered == 'main-control-btn' and current_state.get('initialized', False):
        # Handle start/pause toggle
        if current_state.get('running', False):
            # Pause simulation
            new_state = current_state.copy()
            new_state.update({
                'running': False,
                'paused': True
            })
            return current_state.get('logs', []), "⏸️ Paused", "warning", new_state
        else:
            # Start/Resume simulation
            new_state = current_state.copy()
            new_state.update({
                'running': True,
                'paused': False
            })
            
            # Simulate multiple steps for running mode
            logs = []
            start_step = current_state.get('step_count', 0)
            end_step = min(start_step + 5, current_state.get('max_steps', 20))  # Run 5 steps at a time
            
            for i in range(start_step + 1, end_step + 1):
                log_entry = html.Div([
                    html.Span(f"{algorithm.upper()} Iteration {i}: ", className="text-primary fw-bold"),
                    html.Span(f"Fitness = {25.0 + i * 2:.2f}, ", className="text-success"),
                    html.Span(f"Coverage = {20.0 + i * 3:.1f}%", className="text-info")
                ], className="mb-1")
                logs.append(log_entry)
            
            new_state['step_count'] = end_step
            
            if end_step >= current_state.get('max_steps', 20):
                new_state.update({
                    'completed': True,
                    'running': False,
                    'initialized': False,  # Clear to allow re-init
                    'ever_initialized': True
                })
                return logs, f"🏁 Completed {end_step} iterations", "success", new_state
            else:
                return logs, f"▶️ Running - Step {end_step}", "info", new_state
    
    return [], "⭕ Ready", "secondary", current_state

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
