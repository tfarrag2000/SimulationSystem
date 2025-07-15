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
            /* Ultra-compact layout styles */
            .container-fluid { padding: 0.25rem !important; }
            .card { margin-bottom: 0.25rem !important; }
            .card-body { padding: 0.5rem !important; }
            .card-header { padding: 0.25rem 0.5rem !important; font-size: 0.9rem !important; }
            .row { margin-bottom: 0.1rem !important; }
            .form-control { padding: 0.2rem 0.4rem !important; font-size: 0.85rem !important; }
            .btn { padding: 0.2rem 0.4rem !important; font-size: 0.85rem !important; }
            .btn-sm { padding: 0.15rem 0.3rem !important; font-size: 0.8rem !important; }
            .alert { padding: 0.3rem !important; margin-bottom: 0.25rem !important; }
            .nav-link { padding: 0.4rem 0.8rem !important; font-size: 0.85rem !important; }
            .input-group-text { padding: 0.2rem 0.4rem !important; font-size: 0.85rem !important; }
            .accordion-button { padding: 0.4rem 0.6rem !important; font-size: 0.85rem !important; }
            .accordion-body { padding: 0.5rem !important; }
            .small, small { font-size: 0.8rem !important; }
            h3 { font-size: 1.5rem !important; margin: 0.5rem 0 !important; }
            h6 { font-size: 0.9rem !important; margin: 0.2rem 0 !important; }
            .Select-control { min-height: 28px !important; }
            .Select-placeholder, .Select-single-value { line-height: 26px !important; }
            .sidebar { max-height: 95vh; overflow-y: auto; }
            .js-plotly-plot { margin: 0 !important; }
            .rc-slider { margin: 0.3rem 0 !important; }
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
    # Header
    dbc.Row([
        dbc.Col([
            html.H3("🚁 Drone Optimization Simulation System", className="text-center my-2"),
        ])
    ]),
    
    # Three-Column Layout: 4-4-4 split
    dbc.Row([
        # Left Column - Main Algorithm Settings (Primary Card)
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("⚙️ Algorithm Settings"),
                dbc.CardBody([
                    # Algorithm Selection
                    html.Label("🤖 Algorithm", className="fw-bold mb-2"),
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
                        className="mb-3"
                    ),
                    
                    # Parallel Processing Toggle
                    dbc.Switch(
                        id="parallel-processing-switch",
                        label="⚡ Parallel Processing",
                        value=False,
                        disabled=True,
                        className="mb-2"
                    ),
                    html.Div(id="parallel-info", className="mb-2 text-muted small"),
                    
                    # Algorithm Parameters
                    html.Div(id='algorithm-params', className="mt-2"),
                    
                    # Main Simulation Controls
                    html.Hr(),
                    html.Label("🎮 Controls", className="fw-bold mb-2"),
                    
                    # Run Name
                    dbc.InputGroup([
                        dbc.Input(
                            id="run-name-input",
                            placeholder="Run name...",
                            value=f"Run_{datetime.now().strftime('%m%d_%H%M')}",
                            size="sm"
                        ),
                        dbc.Button("🔄", id="generate-run-name", color="secondary", size="sm")
                    ], size="sm", className="mb-2"),
                    
                    # Main control buttons
                    dbc.Button("🚀 Initialize", id="init-button", color="primary", size="sm", className="w-100 mb-1"),
                    dbc.Alert(id="sim-status-alert", children="⭕ Not Started", color="secondary", className="mb-2 text-center py-1"),
                    dbc.ButtonGroup([
                        dbc.Button("▶️", id="main-control-btn", color="success", size="sm", title="Start/Pause"),
                        dbc.Button("👣", id="step-button", color="secondary", size="sm", title="Step"),
                        dbc.Button("🔄", id="stop-reset-btn", color="info", size="sm", title="Reset"),
                    ], className="w-100")
                ])
            ])
        ], width=4),
        
        # Center Column - Main Visualization (Primary Content)
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
        ], width=4),
        
        # Right Column - Supporting Cards with Accordions (Option 3)
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
                dbc.CardHeader("📝 Live Logs", className="py-1"),
                dbc.CardBody([
                    html.Div(id="log-output", style={'height': '18vh', 'overflow': 'auto', 'font-size': '11px'})
                ], className="py-1")
            ], className="mb-2"),
            
            # Status & Quick Actions (Non-accordion - important info)
            dbc.Card([
                dbc.CardHeader("📊 Status & Actions", className="py-1"),
                dbc.CardBody([
                    html.Div(id="algorithm-status-display", children=[
                        html.P("🔍 Ready for optimization", className="mb-1 text-muted small"),
                    ], className="mb-2 p-2 bg-light rounded"),
                    
                    dbc.ButtonGroup([
                        dbc.Button("🚀", id="quick-run", color="success", size="sm", title="Quick Run"),
                        dbc.Button("📊", id="quick-compare", color="info", size="sm", title="Compare"),
                        dbc.Button("🔄", id="quick-reset", color="secondary", size="sm", title="Reset All")
                    ], className="w-100"),
                    
                    html.Div(id="current-metrics", className="small text-muted mt-2", children=[
                        "🔍 No active simulation"
                    ])
                ], className="py-1")
            ])
        ], width=4)
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

# Run the app
if __name__ == '__main__':
    print("🚁 Starting Enhanced Drone Optimization Simulation System...")
    print("📍 Open your browser to: http://127.0.0.1:8050")
    app.run_server(debug=True, host='127.0.0.1', port=8050)
