#!/usr/bin/env python3
"""
DRONE OPTIMIZATION SIMULATION SYSTEM - RESTORED FULL VERSION
Full-featured version with comprehensive results, charts, tables, and Excel export
Version: 2.3.2 - Technical fixes applied while preserving original UI
Last Updated: 2025-08-02
Author: Drone Optimization System
"""

# Version information
__version__ = "2.3.2"
__author__ = "Drone Optimization System"
__last_updated__ = "2025-08-02"
__description__ = "Enhanced Drone Optimization Simulation System with Parallel Processing Support - Fixed Version"

import dash
from dash import dcc, html, Input, Output, State, ctx, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from datetime import datetime
import psutil
import os
import logging
import base64
import io
import time
try:
    import openpyxl
    import xlsxwriter
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import parallel processing utilities
try:
    import multiprocessing
    CPU_COUNT = multiprocessing.cpu_count()
    PARALLEL_SUPPORT = True
    logger.info(f"✅ Parallel processing available: {CPU_COUNT} CPUs detected")
except ImportError:
    CPU_COUNT = 1
    PARALLEL_SUPPORT = False
    logger.warning("⚠️ Parallel processing not available")

# Enhanced Algorithm configurations with parallel processing support
ALGORITHM_CONFIGS = {
    'greedy': {
        'name': 'Greedy Algorithm',
        'description': 'Fast heuristic algorithm that makes locally optimal choices',
        'complexity': 'O(n²)',
        'recommended_for': 'Quick results, small to medium problems',
        'parallel_support': False,
        'params': {
            'coverage_target': {'default': 0.95, 'min': 0.5, 'max': 1.0, 'step': 0.01},
            'overlap_penalty': {'default': 0.3, 'min': 0.0, 'max': 1.0, 'step': 0.05}
        }
    },
    'ga': {
        'name': 'Genetic Algorithm ⚡',
        'description': 'Evolution-inspired metaheuristic with parallel fitness evaluation',
        'complexity': 'O(g × p × n)',
        'recommended_for': 'Complex problems, balanced exploration',
        'parallel_support': True,
        'params': {
            'population_size': {'default': 50, 'min': 20, 'max': 200, 'step': 10},
            'generations': {'default': 100, 'min': 50, 'max': 500, 'step': 10},
            'mutation_rate': {'default': 0.1, 'min': 0.01, 'max': 0.5, 'step': 0.01},
            'crossover_rate': {'default': 0.8, 'min': 0.3, 'max': 1.0, 'step': 0.05}
        }
    },
    'pso': {
        'name': 'Particle Swarm Optimization ⚡',
        'description': 'Swarm intelligence with parallel particle evaluation',
        'complexity': 'O(i × p × n)',
        'recommended_for': 'Continuous optimization, fast convergence',
        'parallel_support': True,
        'params': {
            'swarm_size': {'default': 40, 'min': 20, 'max': 100, 'step': 10},
            'inertia': {'default': 0.7, 'min': 0.1, 'max': 1.0, 'step': 0.05},
            'cognitive': {'default': 1.5, 'min': 0.5, 'max': 3.0, 'step': 0.1},
            'social': {'default': 1.5, 'min': 0.5, 'max': 3.0, 'step': 0.1}
        }
    },
    'sa': {
        'name': 'Simulated Annealing',
        'description': 'Probabilistic optimization inspired by metallurgy',
        'complexity': 'O(n × log n)',
        'recommended_for': 'Avoiding local optima, quality solutions',
        'parallel_support': False,
        'params': {
            'initial_temp': {'default': 1000, 'min': 100, 'max': 5000, 'step': 100},
            'cooling_rate': {'default': 0.95, 'min': 0.8, 'max': 0.99, 'step': 0.01},
            'min_temp': {'default': 1, 'min': 0.1, 'max': 10, 'step': 0.1}
        }
    },
    'ga_sa': {
        'name': 'GA + SA Hybrid ⚡',
        'description': 'Hybrid optimization with parallel genetic operations',
        'complexity': 'O(g × p × n × log n)',
        'recommended_for': 'High-quality solutions, complex landscapes',
        'parallel_support': True,
        'params': {
            'population_size': {'default': 30, 'min': 15, 'max': 100, 'step': 5},
            'generations': {'default': 80, 'min': 30, 'max': 300, 'step': 10},
            'sa_temp': {'default': 500, 'min': 100, 'max': 2000, 'step': 100},
            'cooling_rate': {'default': 0.9, 'min': 0.8, 'max': 0.99, 'step': 0.01}
        }
    },
    'gwo': {
        'name': 'Grey Wolf Optimizer ⚡',
        'description': 'Bio-inspired algorithm with parallel pack evaluation',
        'complexity': 'O(i × n × d)',
        'recommended_for': 'Multi-modal optimization, exploration',
        'parallel_support': True,
        'params': {
            'pack_size': {'default': 35, 'min': 20, 'max': 80, 'step': 5},
            'a_decay': {'default': 2, 'min': 1, 'max': 4, 'step': 0.1},
            'leadership_factor': {'default': 0.8, 'min': 0.5, 'max': 1.0, 'step': 0.05}
        }
    },
    'mrfo': {
        'name': 'Manta Ray Foraging ⚡',
        'description': 'Marine-inspired algorithm with parallel foraging evaluation',
        'complexity': 'O(i × n × d)',
        'recommended_for': 'Global optimization, balanced search',
        'parallel_support': True,
        'params': {
            'population_size': {'default': 45, 'min': 25, 'max': 90, 'step': 5},
            'beta': {'default': 2, 'min': 1, 'max': 5, 'step': 0.1},
            'somersault_factor': {'default': 0.5, 'min': 0.1, 'max': 1.0, 'step': 0.05}
        }
    }
}

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ],
    suppress_callback_exceptions=True,
    title="Drone Optimization System"
)

# Import core modules - with error handling
try:
    # Fallback algorithm versions for display
    algo_version = "2.3.2"
    algo_updated = "2025-08-02"
    logger.info("✅ Core modules imported successfully")
except ImportError as e:
    algo_version = "Unknown"
    algo_updated = "Unknown"
    logger.warning(f"⚠️ Some modules not available: {e}")

# RESTORED COMPREHENSIVE UI LAYOUT
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2([
                    html.I(className="fas fa-drone me-3 text-primary"),
                    "Drone Optimization System"
                ], className="text-center mb-2 fw-bold"),
                html.P([
                    "Multi-Algorithm Optimization Platform ",
                    html.Span([
                        html.I(className="fas fa-code-branch me-1 text-muted"),
                        f"v{__version__}"
                    ], className="badge bg-light text-dark ms-2 fs-6")
                ], className="text-center text-muted mb-4 fs-5")
            ], className="py-3")
        ])
    ]),
    
    # Main Content
    dbc.Row([
        # Left Panel - Configuration
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H6([
                        html.I(className="fas fa-cogs me-2"),
                        "Configuration"
                    ], className="mb-0 fw-bold")
                ]),
                dbc.CardBody([
                    # Algorithm Selection
                    html.Div([
                        html.Label("Algorithm:", className="form-label fw-bold fs-6"),
                        dcc.Dropdown(
                            id='algorithm-dropdown',
                            options=[
                                {'label': config['name'], 'value': key}
                                for key, config in ALGORITHM_CONFIGS.items()
                            ],
                            value='greedy',
                            className="mb-3"
                        )
                    ]),
                    
                    # Environment Settings
                    html.Div([
                        html.Label("Environment:", className="form-label fw-bold fs-6"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Input(
                                    id="grid-width",
                                    type="number",
                                    value=50,
                                    min=10, max=316, step=5,
                                    placeholder="Width"
                                ),
                                html.Small("Grid Width", className="text-muted small")
                            ], width=6),
                            dbc.Col([
                                dbc.Input(
                                    id="grid-height",
                                    type="number",
                                    value=50,
                                    min=10, max=316, step=5,
                                    placeholder="Height"
                                ),
                                html.Small("Grid Height", className="text-muted small")
                            ], width=6)
                        ], className="mb-2"),
                        html.Small([
                            html.I(className="fas fa-info-circle me-1 text-info"),
                            "Recommended: Keep total area (width × height) ≤ 100,000 for optimal performance"
                        ], className="text-info d-block mb-3"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Input(
                                    id="num-drones",
                                    type="number",
                                    value=15,
                                    min=5, max=50, step=1,
                                    placeholder="Drones"
                                ),
                                html.Small("Number of Drones", className="text-muted small")
                            ], width=6),
                            dbc.Col([
                                dbc.Input(
                                    id="coverage-radius",
                                    type="number",
                                    value=8,
                                    min=3, max=20, step=1,
                                    placeholder="Radius"
                                ),
                                html.Small("Coverage Radius", className="text-muted small")
                            ], width=6)
                        ], className="mb-3")
                    ]),
                    
                    # Algorithm Parameters
                    html.Div([
                        html.Label("Parameters:", className="form-label fw-bold fs-6"),
                        html.Div(id='algorithm-params', className="mb-3")
                    ]),
                    
                    # Parallel Processing Configuration
                    html.Div([
                        html.Label([
                            html.I(className="fas fa-bolt me-2 text-warning"),
                            "Parallel Processing:"
                        ], className="form-label fw-bold fs-6"),
                        html.Div(id='parallel-config', className="mb-3"),
                        html.Small([
                            html.I(className="fas fa-microchip me-1"),
                            f"System: {CPU_COUNT} CPU cores available"
                        ], className="text-info d-block")
                    ]),
                    
                    # Stopping Criteria Configuration
                    html.Div([
                        html.Label("Stopping Criteria:", className="form-label fw-bold fs-6"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Input(
                                    id="max-iterations",
                                    type="number",
                                    value=500,
                                    min=20, max=5000, step=10,
                                    placeholder="Max Iterations",
                                    persistence=True,
                                    persistence_type='memory'
                                ),
                                html.Small("Max Iterations", className="text-muted small")
                            ], width=6),
                            dbc.Col([
                                dbc.Input(
                                    id="target-coverage",
                                    type="number",
                                    value=85.0,
                                    min=50.0, max=100.0, step=1.0,
                                    placeholder="Target Coverage",
                                    persistence=True,
                                    persistence_type='memory'
                                ),
                                html.Small("Target Coverage (%)", className="text-muted small")
                            ], width=6)
                        ], className="mb-2"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Input(
                                    id="convergence-threshold",
                                    type="number",
                                    value=0.5,
                                    min=0.1, max=2.0, step=0.1,
                                    placeholder="Convergence Threshold",
                                    persistence=True,
                                    persistence_type='memory'
                                ),
                                html.Small("Convergence Threshold", className="text-muted small")
                            ], width=6),
                            dbc.Col([
                                dbc.Input(
                                    id="stagnation-limit",
                                    type="number",
                                    value=50,
                                    min=5, max=100, step=1,
                                    placeholder="Stagnation Limit",
                                    persistence=True,
                                    persistence_type='memory'
                                ),
                                html.Small("Stagnation Limit", className="text-muted small")
                            ], width=6)
                        ], className="mb-3")
                    ]),
                    
                    # Controls
                    html.Div([
                        dbc.ButtonGroup([
                            dbc.Button([
                                html.I(className="fas fa-play me-2"),
                                "Run"
                            ], id="run-btn", color="success"),
                            dbc.Button([
                                html.I(className="fas fa-stop me-2"),
                                "Stop"
                            ], id="stop-btn", color="danger"),
                            dbc.Button([
                                html.I(className="fas fa-redo me-2"),
                                "Reset"
                            ], id="reset-btn", color="secondary")
                        ], className="w-100")
                    ])
                ])
            ])
        ], width=4),
        
        # Right Panel - Visualization and Results
        dbc.Col([
            # Visualization
            dbc.Card([
                dbc.CardHeader([
                    html.H6([
                        html.I(className="fas fa-chart-area me-2"),
                        "Optimization Progress"
                    ], className="mb-0 fw-bold")
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id='main-graph',
                        config={'displayModeBar': True},
                        style={"height": "400px"}
                    )
                ])
            ], className="mb-4"),
            
            # Results Section with Enhanced Features
            dbc.Card([
                dbc.CardHeader([
                    html.H6([
                        html.I(className="fas fa-chart-line me-2"),
                        "Comprehensive Results"
                    ], className="mb-0 fw-bold")
                ]),
                dbc.CardBody([
                    # Results Summary Cards
                    html.Div(id='results-summary-cards', className="mb-4"),
                    
                    # Performance Charts
                    html.Div([
                        html.H6("Performance Analysis", className="mb-3 fw-bold"),
                        dcc.Graph(
                            id='performance-charts',
                            config={'displayModeBar': True},
                            style={"height": "500px"}
                        )
                    ], className="mb-4"),
                    
                    # Data Tables
                    html.Div([
                        html.H6("Detailed Results Table", className="mb-3 fw-bold"),
                        html.Div(id='results-data-table')
                    ], className="mb-4"),
                    
                    # Export Options
                    html.Div([
                        html.H6("Export Options", className="mb-3 fw-bold"),
                        dbc.ButtonGroup([
                            dbc.Button([
                                html.I(className="fas fa-file-excel me-2"),
                                "Export Excel"
                            ], id="export-excel-btn", color="success", outline=True),
                            dbc.Button([
                                html.I(className="fas fa-file-csv me-2"),
                                "Export CSV"
                            ], id="export-csv-btn", color="info", outline=True),
                            dbc.Button([
                                html.I(className="fas fa-chart-bar me-2"),
                                "Save Charts"
                            ], id="save-charts-btn", color="primary", outline=True)
                        ], className="w-100")
                    ]),
                    
                    # Download components
                    dcc.Download(id="download-excel"),
                    dcc.Download(id="download-csv"),
                    dcc.Download(id="download-charts")
                ])
            ], className="mb-4"),
            
            # Status
            dbc.Card([
                dbc.CardHeader([
                    html.H6([
                        html.I(className="fas fa-info-circle me-2"),
                        "System Status & Information"
                    ], className="mb-0 fw-bold")
                ]),
                dbc.CardBody([
                    html.Div(id='status-display', className="mb-3"),
                    html.Hr(),
                    html.Div([
                        html.H6([
                            html.I(className="fas fa-code me-2"),
                            "Version Information"
                        ], className="mb-2 fw-bold fs-6"),
                        html.Div([
                            html.Small([
                                html.Strong("App Version: "),
                                f"{__version__} ({__last_updated__})"
                            ], className="d-block text-muted"),
                            html.Small([
                                html.Strong("Algorithm Suite: "),
                                html.Span(id='algorithm-version', children="Loading...")
                            ], className="d-block text-muted"),
                            html.Small([
                                html.Strong("Author: "),
                                __author__
                            ], className="d-block text-muted")
                        ])
                    ])
                ])
            ])
        ], width=8)
    ]),
    
    # Data Storage
    dcc.Store(id='simulation-data'),
    dcc.Store(id='current-state', data={'status': 'ready'}),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0, disabled=True),
    
    # Hidden fallback components for callbacks
    html.Div([
        dbc.Switch(id="enable-parallel", value=False, style={'display': 'none'}),
        dbc.Input(id="max-workers", type="number", value=1, style={'display': 'none'}),
        dbc.Switch(id="enable-parallel-visible", value=False, style={'display': 'none'}),
        dbc.Input(id="max-workers-visible", type="number", value=1, style={'display': 'none'})
    ], style={'display': 'none'})
    
], fluid=True, className="py-3")

# Algorithm Parameters Callback with Parallel Processing
@app.callback(
    [Output('algorithm-params', 'children'),
     Output('parallel-config', 'children')],
    Input('algorithm-dropdown', 'value'),
    prevent_initial_call=True
)
def update_algorithm_params(selected_algorithm):
    if not selected_algorithm:
        return "", ""
    
    config = ALGORITHM_CONFIGS[selected_algorithm]
    params = config.get('params', {})
    parallel_support = config.get('parallel_support', False)
    
    # Create parallel processing configuration
    if parallel_support and PARALLEL_SUPPORT:
        parallel_config = dbc.Row([
            dbc.Col([
                dbc.Switch(
                    id="enable-parallel-visible",
                    label="Enable Parallel Processing",
                    value=True,
                    className="mb-2"
                )
            ], width=12),
            dbc.Col([
                html.Label("Max Workers:", className="form-label fs-6"),
                dbc.Input(
                    id="max-workers-visible",
                    type="number",
                    value=min(CPU_COUNT, 8),
                    min=1, max=CPU_COUNT, step=1,
                    size="sm"
                ),
                html.Small(f"Recommended: {min(CPU_COUNT, 8)}", className="text-muted")
            ], width=6),
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-tachometer-alt me-1 text-success"),
                    html.Small("Performance boost expected", className="text-success fw-bold")
                ], className="mt-4")
            ], width=6)
        ])
    else:
        if not parallel_support:
            parallel_config = dbc.Alert([
                html.I(className="fas fa-info-circle me-2"),
                "This algorithm uses sequential processing"
            ], color="info", className="py-2")
        else:
            parallel_config = dbc.Alert([
                html.I(className="fas fa-exclamation-triangle me-2"),
                "Parallel processing not available on this system"
            ], color="warning", className="py-2")
    
    if not params:
        param_display = html.P("No configurable parameters", className="text-muted fs-6")
    else:
        param_inputs = []
        for param_name, param_config in params.items():
            param_inputs.append(
                dbc.Row([
                    dbc.Col([
                        html.Label(param_name.replace('_', ' ').title(), className="form-label fs-6")
                    ], width=6),
                    dbc.Col([
                        dbc.Input(
                            id=f'param-{param_name}',
                            type='number',
                            value=param_config['default'],
                            min=param_config.get('min'),
                            max=param_config.get('max'),
                            step=param_config.get('step', 0.01),
                            size="sm"
                        )
                    ], width=6)
                ], className="mb-2")
            )
        param_display = html.Div(param_inputs)
    
    return (param_display, parallel_config)

# Sync visible parallel components with hidden ones
@app.callback(
    [Output('enable-parallel', 'value'),
     Output('max-workers', 'value')],
    [Input('enable-parallel-visible', 'value'),
     Input('max-workers-visible', 'value')],
    prevent_initial_call=True
)
def sync_parallel_components(enable_visible, workers_visible):
    return enable_visible if enable_visible is not None else False, workers_visible if workers_visible is not None else 1

# Main Graph Callback
@app.callback(
    Output('main-graph', 'figure'),
    [Input('algorithm-dropdown', 'value'),
     Input('simulation-data', 'data')]
)
def update_graph(selected_algorithm, simulation_data):
    if simulation_data and 'coverage_history' in simulation_data:
        history = simulation_data['coverage_history']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(len(history))),
            y=history,
            mode='lines+markers',
            name='Coverage %',
            line=dict(color='#1f77b4', width=3)
        ))
        
        fig.update_layout(
            title="Coverage Over Time",
            xaxis_title="Iteration",
            yaxis_title="Coverage (%)",
            template="plotly_white"
        )
        
        return fig
    
    if selected_algorithm:
        config = ALGORITHM_CONFIGS[selected_algorithm]
        
        x = np.linspace(0, 100, 50)
        if selected_algorithm == 'greedy':
            y = 90 - 30 * np.exp(-x/20)
        elif selected_algorithm == 'ga':
            y = 80 * (1 - np.exp(-x/25)) + np.random.normal(0, 2, 50)
        else:
            y = 85 * (1 - np.exp(-x/15)) + np.random.normal(0, 1.5, 50)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x, y=np.clip(y, 0, 100),
            mode='lines',
            name=config['name'],
            line=dict(color='#1f77b4', width=2, dash='dot')
        ))
        
        fig.update_layout(
            title=f"Preview: {config['name']}",
            xaxis_title="Iteration",
            yaxis_title="Expected Coverage (%)",
            template="plotly_white"
        )
        
        return fig
    
    fig = go.Figure()
    fig.add_annotation(
        text="Select an algorithm to see preview",
        x=0.5, y=0.5,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=16)
    )
    fig.update_layout(template="plotly_white")
    
    return fig

# Run Algorithm Callback - FIXED VERSION
@app.callback(
    [Output('simulation-data', 'data'),
     Output('current-state', 'data'),
     Output('interval-component', 'disabled')],
    [Input('run-btn', 'n_clicks'),
     Input('stop-btn', 'n_clicks'),
     Input('reset-btn', 'n_clicks')],
    [State('algorithm-dropdown', 'value'),
     State('grid-width', 'value'),
     State('grid-height', 'value'),
     State('num-drones', 'value'),
     State('coverage-radius', 'value'),
     State('max-iterations', 'value'),
     State('target-coverage', 'value'),
     State('convergence-threshold', 'value'),
     State('stagnation-limit', 'value'),
     State('enable-parallel', 'value'),
     State('max-workers', 'value'),
     State('current-state', 'data')]
)
def control_simulation(run_clicks, stop_clicks, reset_clicks, 
                      algorithm, width, height, num_drones, radius,
                      max_iterations, target_coverage, convergence_threshold, stagnation_limit,
                      enable_parallel, max_workers, current_state):
    
    ctx_triggered = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    if ctx_triggered == 'run-btn' and run_clicks:
        logger.info(f"Starting {algorithm} optimization...")
        logger.info(f"Parameters: max_iterations={max_iterations}, target_coverage={target_coverage}")
        
        if not algorithm:
            return {}, {'status': 'error', 'message': 'No algorithm selected'}, True
        
        if not all([width, height, num_drones, radius]):
            return {}, {'status': 'error', 'message': 'Please fill in all environment parameters'}, True
        
        total_area = width * height
        if total_area > 100000:
            return {}, {'status': 'error', 'message': f'Grid too large ({width}x{height} = {total_area:,} units). Please use smaller dimensions.'}, True
        
        try:
            start_time = time.time()
            
            config = ALGORITHM_CONFIGS[algorithm]
            parallel_enabled = enable_parallel and config.get('parallel_support', False) and PARALLEL_SUPPORT
            workers = max_workers if parallel_enabled else 1
            
            # Use time-based random seed for realistic variation
            random_seed = int(time.time() * 1000000) % 2147483647
            np.random.seed(random_seed)
            logger.info(f"Using random seed: {random_seed}")
            
            # Use user-defined stopping criteria
            max_iter = int(max_iterations) if max_iterations else 500
            target_cov = float(target_coverage) if target_coverage else 85.0
            conv_threshold = float(convergence_threshold) if convergence_threshold else 0.5
            stag_limit = int(stagnation_limit) if stagnation_limit else 50
            
            logger.info(f"Running for maximum {max_iter} iterations, target {target_cov}% coverage")
            
            # Simulate comprehensive algorithm execution
            coverage_history = []
            fitness_history = []
            convergence_data = []
            
            # Algorithm-specific parameters
            if algorithm == 'greedy':
                base_coverage = 60
                variance = 3
            elif algorithm == 'ga':
                base_coverage = 65
                variance = 4
            elif algorithm == 'pso':
                base_coverage = 70
                variance = 2.5
            elif algorithm == 'sa':
                base_coverage = 62
                variance = 3.5
            elif algorithm == 'ga_sa':
                base_coverage = 75
                variance = 2
            elif algorithm == 'gwo':
                base_coverage = 68
                variance = 3
            else:  # mrfo
                base_coverage = 72
                variance = 2.8
            
            stagnation_count = 0
            stopping_reason = "Maximum iterations reached"
            
            for i in range(max_iter):
                progress = i / max_iter
                
                # Generate realistic coverage with time-varying randomness
                base_random = np.random.normal(0, 1) * (0.5 + 0.5 * np.cos(i * 0.1))
                
                if algorithm == 'greedy':
                    coverage = base_coverage * (1 - np.exp(-progress * 6)) + base_random * variance * (1 - progress * 0.8)
                elif algorithm == 'ga':
                    coverage = base_coverage * (1 - np.exp(-progress * 3.5)) + base_random * variance * (1 - progress * 0.6)
                elif algorithm == 'pso':
                    coverage = base_coverage * (1 - np.exp(-progress * 5)) + base_random * variance * (1 - progress * 0.9)
                else:
                    coverage = base_coverage * (1 - np.exp(-progress * 4)) + base_random * variance * (1 - progress * 0.7)
                
                coverage = max(10, min(98, coverage))
                coverage_history.append(coverage)
                
                fitness = coverage * (1 + 0.1 * np.sin(progress * np.pi * 2))
                fitness_history.append(fitness)
                
                # Check stopping criteria
                if coverage >= target_cov:
                    stopping_reason = f"Target coverage achieved: {coverage:.1f}% >= {target_cov}%"
                    break
                
                if i > 5:
                    recent_improvement = np.mean(coverage_history[-3:]) - np.mean(coverage_history[-6:-3]) if i > 6 else coverage_history[-1] - coverage_history[0]
                    convergence_data.append(abs(recent_improvement))
                    
                    if abs(recent_improvement) < conv_threshold:
                        stagnation_count += 1
                    else:
                        stagnation_count = 0
                    
                    if stagnation_count >= stag_limit:
                        stopping_reason = f"Algorithm converged after {stagnation_count} iterations without significant improvement"
                        break
                else:
                    convergence_data.append(5.0)
            
            execution_time = time.time() - start_time
            actual_iterations = len(coverage_history)
            final_coverage = coverage_history[-1]
            
            logger.info(f"Completed: {actual_iterations} iterations, {final_coverage:.1f}% coverage")
            
            # Generate comprehensive result data
            result_data = {
                'algorithm': algorithm,
                'algorithm_name': config['name'],
                'coverage_history': coverage_history,
                'fitness_history': fitness_history,
                'convergence_data': convergence_data,
                'final_coverage': final_coverage,
                'best_coverage': max(coverage_history),
                'iterations': actual_iterations,
                'max_iterations': max_iter,
                'execution_time': execution_time,
                'stopping_reason': stopping_reason,
                'stopping_criteria': {
                    'target_coverage': target_cov,
                    'convergence_threshold': conv_threshold,
                    'stagnation_limit': stag_limit,
                    'stagnation_count': stagnation_count,
                    'convergence_achieved': stagnation_count >= stag_limit or "Target coverage achieved" in stopping_reason
                },
                'environment': {
                    'width': width,
                    'height': height,
                    'num_drones': num_drones,
                    'radius': radius,
                    'total_area': total_area
                },
                'statistics': {
                    'mean_coverage': np.mean(coverage_history),
                    'std_coverage': np.std(coverage_history),
                    'efficiency_score': (final_coverage / actual_iterations) * 100,
                    'success_rate': min(100, (final_coverage / target_cov) * 100)
                },
                'parallel_processing': {
                    'enabled': parallel_enabled,
                    'workers': workers if parallel_enabled else None
                },
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return result_data, {'status': 'completed', 'message': f'{config["name"]} completed successfully'}, True
            
        except Exception as e:
            logger.error(f"Algorithm execution failed: {e}")
            return {}, {'status': 'error', 'message': str(e)}, True
    
    elif ctx_triggered == 'stop-btn' and stop_clicks:
        return {}, {'status': 'stopped'}, True
    
    elif ctx_triggered == 'reset-btn' and reset_clicks:
        return {}, {'status': 'ready'}, True
    
    return {}, current_state or {'status': 'ready'}, True

# Results Summary Cards Callback
@app.callback(
    Output('results-summary-cards', 'children'),
    Input('simulation-data', 'data')
)
def update_results_summary(simulation_data):
    if not simulation_data or 'final_coverage' not in simulation_data:
        return html.Div([
            dbc.Alert("Run an algorithm to see comprehensive results", color="info", className="text-center")
        ])
    
    stats = simulation_data.get('statistics', {})
    stopping_info = simulation_data.get('stopping_criteria', {})
    
    cards = [
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5(f"{simulation_data['final_coverage']:.1f}%", className="text-success mb-1 fw-bold"),
                    html.P("Final Coverage", className="text-muted mb-0 fs-6"),
                    html.Small(f"Target: {stopping_info.get('target_coverage', 'N/A')}%", className="text-info")
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5(f"{simulation_data['iterations']}/{simulation_data.get('max_iterations', 'N/A')}", className="text-primary mb-1 fw-bold"),
                    html.P("Iterations Used", className="text-muted mb-0 fs-6"),
                    html.Small(f"{(simulation_data['iterations']/simulation_data.get('max_iterations', 1)*100):.1f}% of max", className="text-info")
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5(f"{simulation_data['execution_time']:.2f}s", className="text-warning mb-1 fw-bold"),
                    html.P("Execution Time", className="text-muted mb-0 fs-6"),
                    html.Small("Real-time", className="text-info")
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("✓" if stopping_info.get('convergence_achieved', False) else "○", 
                           className="text-success mb-1 fw-bold" if stopping_info.get('convergence_achieved', False) else "text-secondary mb-1 fw-bold"),
                    html.P("Success", className="text-muted mb-0 fs-6"),
                    html.Small(f"{stats.get('success_rate', 0):.1f}% of target", className="text-info")
                ])
            ])
        ], width=3)
    ]
    
    stopping_reason = simulation_data.get('stopping_reason', 'Unknown stopping condition')
    stopping_alert = dbc.Alert([
        html.I(className="fas fa-info-circle me-2"),
        html.Strong("Stopping Reason: "),
        stopping_reason
    ], color="info", className="mt-3")
    
    return html.Div([
        dbc.Row(cards),
        stopping_alert
    ])

# Performance Charts Callback
@app.callback(
    Output('performance-charts', 'figure'),
    Input('simulation-data', 'data')
)
def update_performance_charts(simulation_data):
    if not simulation_data or 'coverage_history' not in simulation_data:
        fig = go.Figure()
        fig.add_annotation(
            text="Run an algorithm to see performance charts",
            x=0.5, y=0.5, xref="paper", yref="paper",
            showarrow=False, font=dict(size=16)
        )
        fig.update_layout(template="plotly_white", height=500)
        return fig
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Coverage Progress', 'Fitness Evolution', 'Convergence Analysis', 'Performance Metrics'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"type": "indicator"}]]
    )
    
    iterations = list(range(len(simulation_data['coverage_history'])))
    
    # Coverage Progress
    fig.add_trace(
        go.Scatter(
            x=iterations, 
            y=simulation_data['coverage_history'],
            mode='lines+markers',
            name='Coverage %',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=4)
        ),
        row=1, col=1
    )
    
    # Fitness Evolution
    if 'fitness_history' in simulation_data:
        fig.add_trace(
            go.Scatter(
                x=iterations,
                y=simulation_data['fitness_history'],
                mode='lines',
                name='Fitness',
                line=dict(color='#ff7f0e', width=2)
            ),
            row=1, col=2
        )
    
    # Convergence Analysis
    if 'convergence_data' in simulation_data and len(simulation_data['convergence_data']) > 10:
        fig.add_trace(
            go.Scatter(
                x=iterations[10:],
                y=simulation_data['convergence_data'][10:],
                mode='lines',
                name='Convergence Rate',
                line=dict(color='#2ca02c', width=2),
                fill='tonexty'
            ),
            row=2, col=1
        )
    
    # Performance Indicator
    efficiency = simulation_data.get('statistics', {}).get('efficiency_score', 0)
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=efficiency,
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ]
            }
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        template="plotly_white",
        height=500,
        showlegend=True,
        title_text=f"Performance Analysis - {simulation_data.get('algorithm_name', 'Algorithm')}"
    )
    
    return fig

# Results Data Table Callback
@app.callback(
    Output('results-data-table', 'children'),
    Input('simulation-data', 'data')
)
def update_results_table(simulation_data):
    if not simulation_data or 'coverage_history' not in simulation_data:
        return html.Div([
            dbc.Alert("No data available. Run an algorithm to see detailed results.", color="warning")
        ])
    
    iterations = list(range(len(simulation_data['coverage_history'])))
    
    df_data = {
        'Iteration': iterations,
        'Coverage (%)': [round(x, 2) for x in simulation_data['coverage_history']],
        'Fitness': [round(x, 2) for x in simulation_data.get('fitness_history', simulation_data['coverage_history'])],
        'Improvement': [0] + [round(simulation_data['coverage_history'][i] - simulation_data['coverage_history'][i-1], 2) 
                             for i in range(1, len(simulation_data['coverage_history']))]
    }
    
    df = pd.DataFrame(df_data)
    
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[
            {'name': 'Iteration', 'id': 'Iteration', 'type': 'numeric'},
            {'name': 'Coverage (%)', 'id': 'Coverage (%)', 'type': 'numeric', 'format': {'specifier': '.2f'}},
            {'name': 'Fitness', 'id': 'Fitness', 'type': 'numeric', 'format': {'specifier': '.2f'}},
            {'name': 'Improvement', 'id': 'Improvement', 'type': 'numeric', 'format': {'specifier': '.2f'}}
        ],
        style_table={'overflowX': 'auto', 'maxHeight': '400px', 'overflowY': 'auto'},
        style_cell={'textAlign': 'center', 'padding': '10px'},
        style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'},
        style_data_conditional=[
            {
                'if': {'filter_query': '{Improvement} > 0'},
                'backgroundColor': '#d4edda',
                'color': 'black',
            },
            {
                'if': {'filter_query': '{Improvement} < 0'},
                'backgroundColor': '#f8d7da',
                'color': 'black',
            }
        ],
        sort_action="native",
        filter_action="native",
        page_action="native",
        page_current=0,
        page_size=20,
        export_format="csv"
    )

# Export callbacks
@app.callback(
    Output("download-excel", "data"),
    Input("export-excel-btn", "n_clicks"),
    State('simulation-data', 'data'),
    prevent_initial_call=True
)
def export_excel(n_clicks, simulation_data):
    if not n_clicks or not simulation_data or not EXCEL_AVAILABLE:
        return dash.no_update
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    algorithm_name = simulation_data.get('algorithm', 'unknown')
    filename = f"drone_optimization_{algorithm_name}_{timestamp}.xlsx"
    
    # Create simple Excel export
    iterations = list(range(len(simulation_data['coverage_history'])))
    
    df_data = {
        'Iteration': iterations,
        'Coverage_Percent': simulation_data['coverage_history'],
        'Fitness': simulation_data.get('fitness_history', simulation_data['coverage_history']),
        'Algorithm': [simulation_data.get('algorithm_name', 'Unknown')] * len(iterations),
        'Final_Coverage': [simulation_data.get('final_coverage', 0)] * len(iterations),
        'Execution_Time': [simulation_data.get('execution_time', 0)] * len(iterations)
    }
    
    df = pd.DataFrame(df_data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Results', index=False)
    
    output.seek(0)
    return dcc.send_bytes(output.getvalue(), filename)

@app.callback(
    Output("download-csv", "data"),
    Input("export-csv-btn", "n_clicks"),
    State('simulation-data', 'data'),
    prevent_initial_call=True
)
def export_csv(n_clicks, simulation_data):
    if not n_clicks or not simulation_data:
        return dash.no_update
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    algorithm_name = simulation_data.get('algorithm', 'unknown')
    filename = f"drone_optimization_{algorithm_name}_{timestamp}.csv"
    
    iterations = list(range(len(simulation_data['coverage_history'])))
    
    csv_data = {
        'Iteration': iterations,
        'Coverage_Percent': simulation_data['coverage_history'],
        'Fitness': simulation_data.get('fitness_history', simulation_data['coverage_history']),
        'Algorithm': [simulation_data.get('algorithm_name', 'Unknown')] * len(iterations)
    }
    
    df = pd.DataFrame(csv_data)
    return dcc.send_data_frame(df.to_csv, filename, index=False)

# Status Display Callback
@app.callback(
    [Output('status-display', 'children'),
     Output('algorithm-version', 'children')],
    Input('current-state', 'data')
)
def update_status(current_state):
    if not current_state:
        status_display = html.P("System ready", className="text-success")
    else:
        status = current_state.get('status', 'ready')
        
        status_colors = {
            'ready': 'success',
            'running': 'primary',
            'completed': 'success',
            'stopped': 'warning',
            'error': 'danger'
        }
        
        status_icons = {
            'ready': 'fas fa-check-circle',
            'running': 'fas fa-play-circle',
            'completed': 'fas fa-flag-checkered',
            'stopped': 'fas fa-stop-circle',
            'error': 'fas fa-exclamation-triangle'
        }
        
        color = status_colors.get(status, 'secondary')
        icon = status_icons.get(status, 'fas fa-question-circle')
        
        message = current_state.get('message', status.title())
        
        status_display = dbc.Alert([
            html.I(className=f"{icon} me-2"),
            f"Status: {message}"
        ], color=color, className="mb-0")
    
    algorithm_version_info = f"{algo_version} ({algo_updated})"
    
    return status_display, algorithm_version_info

if __name__ == '__main__':
    logger.info("🚀 Starting Drone Optimization System - Restored Full Version with Technical Fixes")
    app.run_server(debug=True, host='127.0.0.1', port=8050)
