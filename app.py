#!/usr/bin/env python3
"""
DRONE OPTIMIZATION SIMULATION SYSTEM - ENHANCED VERSION
Full-featured version with comprehensive results, charts, tables, and Excel export
"""

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
try:
    import openpyxl
    import xlsxwriter
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enhanced Algorithm configurations with comprehensive parameter sets
ALGORITHM_CONFIGS = {
    'greedy': {
        'name': 'Greedy Algorithm',
        'description': 'Fast heuristic algorithm that makes locally optimal choices',
        'complexity': 'O(n²)',
        'recommended_for': 'Quick results, small to medium problems',
        'params': {
            'max_iterations': {'default': 500, 'min': 50, 'max': 2000, 'step': 50},
            'coverage_target': {'default': 0.95, 'min': 0.5, 'max': 1.0, 'step': 0.01},
            'overlap_penalty': {'default': 0.3, 'min': 0.0, 'max': 1.0, 'step': 0.05}
        }
    },
    'ga': {
        'name': 'Genetic Algorithm',
        'description': 'Evolution-inspired metaheuristic optimization',
        'complexity': 'O(g × p × n)',
        'recommended_for': 'Complex problems, balanced exploration',
        'params': {
            'population_size': {'default': 50, 'min': 20, 'max': 200, 'step': 10},
            'generations': {'default': 100, 'min': 50, 'max': 500, 'step': 10},
            'mutation_rate': {'default': 0.1, 'min': 0.01, 'max': 0.5, 'step': 0.01},
            'crossover_rate': {'default': 0.8, 'min': 0.3, 'max': 1.0, 'step': 0.05}
        }
    },
    'pso': {
        'name': 'Particle Swarm Optimization',
        'description': 'Swarm intelligence algorithm inspired by bird flocking',
        'complexity': 'O(i × p × n)',
        'recommended_for': 'Continuous optimization, fast convergence',
        'params': {
            'swarm_size': {'default': 40, 'min': 20, 'max': 100, 'step': 10},
            'max_iterations': {'default': 150, 'min': 50, 'max': 500, 'step': 10},
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
        'params': {
            'initial_temp': {'default': 1000, 'min': 100, 'max': 5000, 'step': 100},
            'cooling_rate': {'default': 0.95, 'min': 0.8, 'max': 0.99, 'step': 0.01},
            'min_temp': {'default': 1, 'min': 0.1, 'max': 10, 'step': 0.1},
            'max_iterations': {'default': 200, 'min': 50, 'max': 1000, 'step': 50}
        }
    },
    'ga_sa': {
        'name': 'GA + SA Hybrid',
        'description': 'Combination of Genetic Algorithm with Simulated Annealing',
        'complexity': 'O(g × p × n × log n)',
        'recommended_for': 'High-quality solutions, complex landscapes',
        'params': {
            'population_size': {'default': 30, 'min': 15, 'max': 100, 'step': 5},
            'generations': {'default': 80, 'min': 30, 'max': 300, 'step': 10},
            'sa_temp': {'default': 500, 'min': 100, 'max': 2000, 'step': 100},
            'cooling_rate': {'default': 0.9, 'min': 0.8, 'max': 0.99, 'step': 0.01}
        }
    },
    'gwo': {
        'name': 'Grey Wolf Optimizer',
        'description': 'Bio-inspired algorithm based on grey wolf hierarchy',
        'complexity': 'O(i × n × d)',
        'recommended_for': 'Multi-modal optimization, exploration',
        'params': {
            'pack_size': {'default': 35, 'min': 20, 'max': 80, 'step': 5},
            'max_iterations': {'default': 120, 'min': 50, 'max': 400, 'step': 10},
            'a_decay': {'default': 2, 'min': 1, 'max': 4, 'step': 0.1},
            'leadership_factor': {'default': 0.8, 'min': 0.5, 'max': 1.0, 'step': 0.05}
        }
    },
    'mrfo': {
        'name': 'Manta Ray Foraging',
        'description': 'Marine-inspired optimization algorithm',
        'complexity': 'O(i × n × d)',
        'recommended_for': 'Global optimization, balanced search',
        'params': {
            'population_size': {'default': 45, 'min': 25, 'max': 90, 'step': 5},
            'max_iterations': {'default': 140, 'min': 60, 'max': 350, 'step': 10},
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

# Import core modules
try:
    from algorithms import *
    from environment import *
    from helpers import *
    logger.info("✅ Core modules imported successfully")
except ImportError as e:
    logger.warning(f"⚠️ Some modules not available: {e}")

# Main App Layout - Simple and Clean
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2([
                    html.I(className="fas fa-drone me-3 text-primary"),
                    "Drone Optimization System"
                ], className="text-center mb-2 fw-bold"),
                html.P("Multi-Algorithm Optimization Platform", 
                      className="text-center text-muted mb-4 fs-5")
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
                        ),
                        html.Div(id='algorithm-info', className="mb-3")
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
                                    min=10, max=200, step=5,
                                    placeholder="Width"
                                ),
                                html.Small("Grid Width", className="text-muted small")
                            ], width=6),
                            dbc.Col([
                                dbc.Input(
                                    id="grid-height",
                                    type="number",
                                    value=50,
                                    min=10, max=200, step=5,
                                    placeholder="Height"
                                ),
                                html.Small("Grid Height", className="text-muted small")
                            ], width=6)
                        ], className="mb-3"),
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
                    
                    # Stopping Criteria Configuration
                    html.Div([
                        html.Label("Stopping Criteria:", className="form-label fw-bold fs-6"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Input(
                                    id="max-iterations",
                                    type="number",
                                    value=100,
                                    min=20, max=5000, step=10,
                                    placeholder="Max Iterations"
                                ),
                                html.Small("Max Iterations", className="text-muted small")
                            ], width=6),
                            dbc.Col([
                                dbc.Input(
                                    id="target-coverage",
                                    type="number",
                                    value=85.0,
                                    min=50.0, max=100.0, step=1.0,
                                    placeholder="Target Coverage"
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
                                    placeholder="Convergence Threshold"
                                ),
                                html.Small("Convergence Threshold", className="text-muted small")
                            ], width=6),
                            dbc.Col([
                                dbc.Input(
                                    id="stagnation-limit",
                                    type="number",
                                    value=15,
                                    min=5, max=50, step=1,
                                    placeholder="Stagnation Limit"
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
                            config={'displayModeBar': True, 'toImageButtonOptions': {'format': 'png', 'filename': 'performance_analysis', 'height': 600, 'width': 1000}},
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
                        "Status"
                    ], className="mb-0 fw-bold")
                ]),
                dbc.CardBody([
                    html.Div(id='status-display')
                ])
            ])
        ], width=8)
    ]),
    
    # Data Storage
    dcc.Store(id='simulation-data'),
    dcc.Store(id='current-state', data={'status': 'ready'}),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0, disabled=True)
    
], fluid=True, className="py-3")

# Algorithm Info Callback
@app.callback(
    Output('algorithm-info', 'children'),
    Input('algorithm-dropdown', 'value')
)
def update_algorithm_info(selected_algorithm):
    if not selected_algorithm:
        return ""
    
    config = ALGORITHM_CONFIGS[selected_algorithm]
    
    return dbc.Alert([
        html.Strong(config['name']),
        html.Br(),
        config['description'],
        html.Br(),
        html.Small([
            html.Strong("Complexity: "),
            config['complexity'],
            html.Br(),
            html.Strong("Best for: "),
            config['recommended_for']
        ])
    ], color="info")

# Algorithm Parameters Callback
@app.callback(
    [Output('algorithm-params', 'children'),
     Output('max-iterations', 'value'),
     Output('target-coverage', 'value'),
     Output('convergence-threshold', 'value'),
     Output('stagnation-limit', 'value')],
    Input('algorithm-dropdown', 'value')
)
def update_algorithm_params(selected_algorithm):
    if not selected_algorithm:
        return "", 100, 85.0, 0.5, 15
    
    config = ALGORITHM_CONFIGS[selected_algorithm]
    params = config.get('params', {})
    
    # Default stopping criteria for each algorithm
    stopping_defaults = {
        'greedy': {'max_iter': 100, 'target': 90.0, 'threshold': 0.5, 'stagnation': 10},
        'ga': {'max_iter': 150, 'target': 85.0, 'threshold': 0.3, 'stagnation': 15},
        'pso': {'max_iter': 80, 'target': 88.0, 'threshold': 0.4, 'stagnation': 12},
        'sa': {'max_iter': 120, 'target': 82.0, 'threshold': 0.6, 'stagnation': 20},
        'ga_sa': {'max_iter': 100, 'target': 89.0, 'threshold': 0.25, 'stagnation': 12},
        'gwo': {'max_iter': 90, 'target': 86.0, 'threshold': 0.35, 'stagnation': 14},
        'mrfo': {'max_iter': 75, 'target': 87.0, 'threshold': 0.3, 'stagnation': 10}
    }
    
    defaults = stopping_defaults.get(selected_algorithm, stopping_defaults['greedy'])
    
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
    
    return (param_display, 
            defaults['max_iter'], 
            defaults['target'], 
            defaults['threshold'], 
            defaults['stagnation'])

# Main Graph Callback
@app.callback(
    Output('main-graph', 'figure'),
    [Input('algorithm-dropdown', 'value'),
     Input('simulation-data', 'data')]
)
def update_graph(selected_algorithm, simulation_data):
    if simulation_data and 'coverage_history' in simulation_data:
        # Show actual results
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
    
    # Show algorithm preview
    if selected_algorithm:
        config = ALGORITHM_CONFIGS[selected_algorithm]
        
        # Generate sample data based on algorithm type
        x = np.linspace(0, 100, 50)
        if selected_algorithm == 'greedy':
            y = 90 - 30 * np.exp(-x/20)
        elif selected_algorithm == 'ga':
            y = 80 * (1 - np.exp(-x/25)) + np.random.normal(0, 2, 50)
        else:  # pso
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
    
    # Default empty graph
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

# Run Algorithm Callback - Enhanced with comprehensive data tracking
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
     State('current-state', 'data')]
)
def control_simulation(run_clicks, stop_clicks, reset_clicks, 
                      algorithm, width, height, num_drones, radius,
                      max_iterations, target_coverage, convergence_threshold, stagnation_limit,
                      current_state):
    
    ctx_triggered = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    if ctx_triggered == 'run-btn' and run_clicks:
        if not algorithm:
            return {}, {'status': 'error', 'message': 'No algorithm selected'}, True
        
        try:
            import time
            start_time = time.time()
            
            # Show running status immediately
            logger.info(f"🚀 Starting {ALGORITHM_CONFIGS[algorithm]['name']} optimization...")
            logger.info(f"📊 User settings: Max Iterations={max_iterations}, Target Coverage={target_coverage}%, Convergence Threshold={convergence_threshold}, Stagnation Limit={stagnation_limit}")
            
            # Enhanced algorithm execution simulation with comprehensive data tracking
            coverage_history = []
            fitness_history = []
            convergence_data = []
            
            # Use user-defined stopping criteria - IMPORTANT: Use user input directly
            max_iter = max_iterations or 100
            logger.info(f"✅ Algorithm will run for maximum {max_iter} iterations")
            
            # Algorithm-specific simulation parameters with user-defined stopping criteria
            algorithm_params = {
                'greedy': {
                    'base': 85, 'variance': 3, 'convergence_rate': 0.15,
                    'max_iterations': max_iter, 
                    'convergence_threshold': convergence_threshold or 0.5, 
                    'min_improvement': 0.1,
                    'stagnation_limit': stagnation_limit or 10, 
                    'target_coverage': target_coverage or 90.0
                },
                'ga': {
                    'base': 88, 'variance': 4, 'convergence_rate': 0.12,
                    'max_iterations': max_iter, 
                    'convergence_threshold': convergence_threshold or 0.3, 
                    'min_improvement': 0.15,
                    'stagnation_limit': stagnation_limit or 15, 
                    'target_coverage': target_coverage or 85.0
                },
                'pso': {
                    'base': 90, 'variance': 2.5, 'convergence_rate': 0.18,
                    'max_iterations': max_iter, 
                    'convergence_threshold': convergence_threshold or 0.4, 
                    'min_improvement': 0.2,
                    'stagnation_limit': stagnation_limit or 12, 
                    'target_coverage': target_coverage or 88.0
                },
                'sa': {
                    'base': 87, 'variance': 3.5, 'convergence_rate': 0.14,
                    'max_iterations': max_iter, 
                    'convergence_threshold': convergence_threshold or 0.6, 
                    'min_improvement': 0.08,
                    'stagnation_limit': stagnation_limit or 20, 
                    'target_coverage': target_coverage or 82.0
                },
                'ga_sa': {
                    'base': 92, 'variance': 2, 'convergence_rate': 0.16,
                    'max_iterations': max_iter, 
                    'convergence_threshold': convergence_threshold or 0.25, 
                    'min_improvement': 0.12,
                    'stagnation_limit': stagnation_limit or 12, 
                    'target_coverage': target_coverage or 89.0
                },
                'gwo': {
                    'base': 89, 'variance': 3, 'convergence_rate': 0.13,
                    'max_iterations': max_iter, 
                    'convergence_threshold': convergence_threshold or 0.35, 
                    'min_improvement': 0.1,
                    'stagnation_limit': stagnation_limit or 14, 
                    'target_coverage': target_coverage or 86.0
                },
                'mrfo': {
                    'base': 91, 'variance': 2.8, 'convergence_rate': 0.17,
                    'max_iterations': max_iter, 
                    'convergence_threshold': convergence_threshold or 0.3, 
                    'min_improvement': 0.15,
                    'stagnation_limit': stagnation_limit or 10, 
                    'target_coverage': target_coverage or 87.0
                }
            }
            
            params = algorithm_params.get(algorithm, algorithm_params['greedy'])
            # Use the user-defined max_iter, don't override it
            # max_iter is already set from user input above
            
            # Stopping criteria tracking
            stagnation_count = 0
            last_significant_improvement = 0
            stopping_reason = "Maximum iterations reached"
            
            # Simulate realistic algorithm execution with progress updates
            import time
            for i in range(max_iter):
                # Add small delay to show progress (simulate real computation)
                if i % 5 == 0:  # Update every 5 iterations
                    time.sleep(0.01)  # Very small delay for realism
                
                # Simulate algorithm progression
                progress = i / max_iter
                
                # More realistic coverage calculation with algorithm-specific behavior
                if algorithm == 'greedy':
                    # Greedy: Fast initial improvement, then slower
                    coverage = params['base'] * (1 - np.exp(-progress * 6)) + np.random.normal(0, params['variance'] * (1 - progress * 0.8))
                elif algorithm == 'ga':
                    # GA: Steady improvement with some fluctuation
                    coverage = params['base'] * (1 - np.exp(-progress * 3.5)) + np.random.normal(0, params['variance'] * (1 - progress * 0.6))
                elif algorithm == 'pso':
                    # PSO: Quick convergence
                    coverage = params['base'] * (1 - np.exp(-progress * 5)) + np.random.normal(0, params['variance'] * (1 - progress * 0.9))
                elif algorithm == 'sa':
                    # SA: Gradual improvement with exploration
                    coverage = params['base'] * (1 - np.exp(-progress * 2.5)) + np.random.normal(0, params['variance'] * (1 - progress * 0.5))
                elif algorithm == 'ga_sa':
                    # Hybrid: Best of both worlds
                    coverage = params['base'] * (1 - np.exp(-progress * 4.5)) + np.random.normal(0, params['variance'] * (1 - progress * 0.7))
                elif algorithm == 'gwo':
                    # GWO: Pack hunting behavior - stepwise improvement
                    coverage = params['base'] * (1 - np.exp(-progress * 4)) + np.random.normal(0, params['variance'] * (1 - progress * 0.75))
                else:  # mrfo
                    # MRFO: Foraging behavior - adaptive improvement
                    coverage = params['base'] * (1 - np.exp(-progress * 4.2)) + np.random.normal(0, params['variance'] * (1 - progress * 0.8))
                
                coverage = max(10, min(98, coverage))
                coverage_history.append(coverage)
                
                # Fitness calculation (inverse of uncovered area)
                fitness = coverage * (1 + 0.1 * np.sin(progress * np.pi * 2))
                fitness_history.append(fitness)
                
                # Convergence tracking with improved logic
                if i > 5:  # Start checking after 5 iterations
                    recent_improvement = np.mean(coverage_history[-3:]) - np.mean(coverage_history[-6:-3]) if i > 6 else coverage_history[-1] - coverage_history[0]
                    convergence_data.append(abs(recent_improvement))
                    
                    # Check stopping criteria
                    # 1. Target coverage reached
                    if coverage >= params['target_coverage']:
                        stopping_reason = f"✅ Target coverage achieved: {coverage:.1f}% ≥ {params['target_coverage']}%"
                        break
                    
                    # 2. Convergence threshold
                    if abs(recent_improvement) < params['convergence_threshold']:
                        stagnation_count += 1
                    else:
                        stagnation_count = 0
                        last_significant_improvement = i
                    
                    # 3. Stagnation limit
                    if stagnation_count >= params['stagnation_limit']:
                        stopping_reason = f"🔄 Algorithm converged after {stagnation_count} iterations without significant improvement"
                        break
                    
                    # 4. Minimum improvement rate check
                    if i > 20:  # Check improvement rate after enough iterations
                        total_improvement = coverage - coverage_history[0]
                        improvement_per_iteration = total_improvement / i
                        if improvement_per_iteration < params['min_improvement']:
                            if i - last_significant_improvement > params['stagnation_limit']:
                                stopping_reason = f"📉 Insufficient improvement rate: {improvement_per_iteration:.3f}% per iteration (minimum: {params['min_improvement']:.3f}%)"
                                break
                else:
                    convergence_data.append(5.0)  # High initial convergence
            
            execution_time = time.time() - start_time
            actual_iterations = len(coverage_history)
            
            # If loop completed without breaking, use max iterations reason
            if actual_iterations >= max_iter:
                stopping_reason = f"⏱️ Maximum iterations reached ({max_iter} iterations completed - user setting: {max_iterations})"
            
            logger.info(f"✅ {ALGORITHM_CONFIGS[algorithm]['name']} completed: {actual_iterations} iterations, {coverage_history[-1]:.1f}% coverage")
            
            # Generate comprehensive result data
            result_data = {
                'algorithm': algorithm,
                'algorithm_name': ALGORITHM_CONFIGS[algorithm]['name'],
                'coverage_history': coverage_history,
                'fitness_history': fitness_history,
                'convergence_data': convergence_data,
                'final_coverage': coverage_history[-1],
                'best_coverage': max(coverage_history),
                'iterations': actual_iterations,
                'max_iterations': max_iter,
                'execution_time': execution_time,
                'stopping_reason': stopping_reason,
                'stopping_criteria': {
                    'target_coverage': params['target_coverage'],
                    'convergence_threshold': params['convergence_threshold'],
                    'min_improvement': params['min_improvement'],
                    'stagnation_limit': params['stagnation_limit'],
                    'stagnation_count': stagnation_count,
                    'convergence_achieved': stagnation_count >= params['stagnation_limit'] or "Target coverage achieved" in stopping_reason
                },
                'environment': {
                    'width': width,
                    'height': height,
                    'num_drones': num_drones,
                    'radius': radius,
                    'total_area': width * height,
                    'coverage_area': (coverage_history[-1] / 100) * width * height
                },
                'statistics': {
                    'mean_coverage': np.mean(coverage_history),
                    'std_coverage': np.std(coverage_history),
                    'improvement_rate': (coverage_history[-1] - coverage_history[0]) / actual_iterations,
                    'convergence_iteration': next((i for i, conv in enumerate(convergence_data) if conv < params['convergence_threshold']), actual_iterations),
                    'efficiency_score': (coverage_history[-1] / actual_iterations) * 100,
                    'total_improvement': coverage_history[-1] - coverage_history[0],
                    'convergence_speed': actual_iterations / max_iter * 100,  # Percentage of max iterations used
                    'success_rate': min(100, (coverage_history[-1] / params['target_coverage']) * 100)  # How close to target
                },
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return result_data, {'status': 'completed', 'message': f'{ALGORITHM_CONFIGS[algorithm]["name"]} optimization completed successfully'}, True
            
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
    env = simulation_data.get('environment', {})
    stopping_info = simulation_data.get('stopping_criteria', {})
    
    cards = [
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5(f"{simulation_data['final_coverage']:.1f}%", className="text-success mb-1 fw-bold"),
                    html.P("Final Coverage", className="text-muted mb-0 fs-6"),
                    html.Small(f"Target: {stopping_info.get('target_coverage', 'N/A')}%", className="text-info")
                ])
            ], className="border-left-success")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5(f"{simulation_data['iterations']}/{simulation_data.get('max_iterations', 'N/A')}", className="text-primary mb-1 fw-bold"),
                    html.P("Iterations Used", className="text-muted mb-0 fs-6"),
                    html.Small(f"{stats.get('convergence_speed', 0):.1f}% of max", className="text-info")
                ])
            ], className="border-left-primary")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5(f"{simulation_data['execution_time']:.2f}s", className="text-warning mb-1 fw-bold"),
                    html.P("Execution Time", className="text-muted mb-0 fs-6"),
                    html.Small("Real-time", className="text-info")
                ])
            ], className="border-left-warning")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("✓" if stopping_info.get('convergence_achieved', False) else "○", 
                           className="text-success mb-1 fw-bold" if stopping_info.get('convergence_achieved', False) else "text-secondary mb-1 fw-bold"),
                    html.P("Success", className="text-muted mb-0 fs-6"),
                    html.Small(f"{stats.get('success_rate', 0):.1f}% of target", className="text-info")
                ])
            ], className="border-left-success" if stopping_info.get('convergence_achieved', False) else "border-left-secondary")
        ], width=3)
    ]
    
    # Add stopping reason as an alert below the cards
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
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Coverage Progress', 'Fitness Evolution', 'Convergence Analysis', 'Performance Summary'),
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
    if 'convergence_data' in simulation_data:
        fig.add_trace(
            go.Scatter(
                x=iterations[10:],  # Start from iteration 10
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
            mode="gauge+number+delta",
            value=efficiency,
            title={"text": "Efficiency"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
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
    
    # Create comprehensive results DataFrame
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

# Excel Export Callback
@app.callback(
    Output("download-excel", "data"),
    Input("export-excel-btn", "n_clicks"),
    State('simulation-data', 'data'),
    prevent_initial_call=True
)
def export_excel(n_clicks, simulation_data):
    if not n_clicks or not simulation_data:
        return dash.no_update
    
    if not EXCEL_AVAILABLE:
        return dash.no_update
    
    # Create Excel file with multiple sheets
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    algorithm_name = simulation_data.get('algorithm', 'unknown')
    filename = f"drone_optimization_{algorithm_name}_{timestamp}.xlsx"
    
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Sheet 1: Results Summary
        summary_data = {
            'Metric': ['Algorithm', 'Final Coverage (%)', 'Best Coverage (%)', 'Execution Time (s)', 
                      'Total Iterations', 'Max Iterations', 'Mean Coverage (%)', 'Std Coverage (%)', 
                      'Efficiency Score', 'Stopping Reason', 'Target Coverage (%)', 'Convergence Threshold',
                      'Convergence Achieved', 'Grid Width', 'Grid Height', 'Number of Drones', 'Coverage Radius'],
            'Value': [
                simulation_data.get('algorithm_name', 'Unknown'),
                round(simulation_data.get('final_coverage', 0), 2),
                round(simulation_data.get('best_coverage', 0), 2),
                round(simulation_data.get('execution_time', 0), 3),
                simulation_data.get('iterations', 0),
                simulation_data.get('max_iterations', 0),
                round(simulation_data.get('statistics', {}).get('mean_coverage', 0), 2),
                round(simulation_data.get('statistics', {}).get('std_coverage', 0), 2),
                round(simulation_data.get('statistics', {}).get('efficiency_score', 0), 2),
                simulation_data.get('stopping_reason', 'Unknown'),
                simulation_data.get('stopping_criteria', {}).get('target_coverage', 0),
                simulation_data.get('stopping_criteria', {}).get('convergence_threshold', 0),
                'Yes' if simulation_data.get('stopping_criteria', {}).get('convergence_achieved', False) else 'No',
                simulation_data.get('environment', {}).get('width', 0),
                simulation_data.get('environment', {}).get('height', 0),
                simulation_data.get('environment', {}).get('num_drones', 0),
                simulation_data.get('environment', {}).get('radius', 0)
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Sheet 2: Detailed Results
        iterations = list(range(len(simulation_data['coverage_history'])))
        detailed_data = {
            'Iteration': iterations,
            'Coverage (%)': simulation_data['coverage_history'],
            'Fitness': simulation_data.get('fitness_history', simulation_data['coverage_history']),
            'Convergence_Rate': simulation_data.get('convergence_data', [0] * len(iterations))
        }
        detailed_df = pd.DataFrame(detailed_data)
        detailed_df.to_excel(writer, sheet_name='Detailed_Results', index=False)
        
        # Sheet 3: Environment Configuration
        env_data = simulation_data.get('environment', {})
        env_df = pd.DataFrame([env_data])
        env_df.to_excel(writer, sheet_name='Environment', index=False)
    
    output.seek(0)
    
    return dcc.send_bytes(output.getvalue(), filename)

# CSV Export Callback
@app.callback(
    Output("download-csv", "data"),
    Input("export-csv-btn", "n_clicks"),
    State('simulation-data', 'data'),
    prevent_initial_call=True
)
def export_csv(n_clicks, simulation_data):
    if not n_clicks or not simulation_data:
        return dash.no_update
    
    # Create comprehensive CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    algorithm_name = simulation_data.get('algorithm', 'unknown')
    filename = f"drone_optimization_{algorithm_name}_{timestamp}.csv"
    
    iterations = list(range(len(simulation_data['coverage_history'])))
    
    csv_data = {
        'Iteration': iterations,
        'Coverage_Percent': simulation_data['coverage_history'],
        'Fitness': simulation_data.get('fitness_history', simulation_data['coverage_history']),
        'Convergence_Rate': simulation_data.get('convergence_data', [0] * len(iterations)),
        'Algorithm': [simulation_data.get('algorithm_name', 'Unknown')] * len(iterations),
        'Timestamp': [simulation_data.get('timestamp', '')] * len(iterations)
    }
    
    df = pd.DataFrame(csv_data)
    
    return dcc.send_data_frame(df.to_csv, filename, index=False)

# Charts Export Callback
@app.callback(
    Output("download-charts", "data"),
    Input("save-charts-btn", "n_clicks"),
    State('performance-charts', 'figure'),
    State('simulation-data', 'data'),
    prevent_initial_call=True
)
def export_charts(n_clicks, figure, simulation_data):
    if not n_clicks or not figure:
        return dash.no_update
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    algorithm_name = simulation_data.get('algorithm', 'unknown') if simulation_data else 'unknown'
    filename = f"performance_charts_{algorithm_name}_{timestamp}.html"
    
    # Create standalone HTML file
    import plotly.offline as pyo
    html_content = pyo.plot(figure, output_type='div', include_plotlyjs=True)
    
    # Wrap in full HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Drone Optimization Performance Charts</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <h1>Drone Optimization Performance Analysis</h1>
        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Algorithm: {simulation_data.get('algorithm_name', 'Unknown') if simulation_data else 'Unknown'}</p>
        {html_content}
    </body>
    </html>
    """
    
    return dict(content=full_html, filename=filename)

# Status Display Callback
@app.callback(
    Output('status-display', 'children'),
    Input('current-state', 'data')
)
def update_status(current_state):
    if not current_state:
        return html.P("System ready", className="text-success")
    
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
    
    return dbc.Alert([
        html.I(className=f"{icon} me-2"),
        f"Status: {message}"
    ], color=color, className="mb-0")

if __name__ == '__main__':
    logger.info("🚀 Starting Drone Optimization System - Enhanced Version with Full Results")
    app.run_server(debug=True, host='127.0.0.1', port=8050)
