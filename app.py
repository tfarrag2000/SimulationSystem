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

# Initialize the app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Drone Optimization Simulation System"

# App layout with enhanced experiment management and improved controls
app.layout = dbc.Container([
    # Header with experiment info
    dbc.Row([
        dbc.Col([
            html.H1("🚁 Drone Optimization Simulation System", className="text-center my-4"),
            # REMOVE experiment-status alert
            # dbc.Alert(id="experiment-status", color="info", is_open=False, dismissable=True)
        ])
    ]),
    
    # Main content split into sidebar and visualization
    dbc.Row([
        # Control Panel (Left Sidebar)
        dbc.Col([           
            # Algorithm Settings Card
            dbc.Card([
                dbc.CardHeader("⚙️ Optimization Settings"),
                dbc.CardBody([
                    # Algorithm Selection
                    html.Label("Optimization Algorithm"),
                    dcc.Dropdown(
                        id='algorithm-dropdown',
                        options=[
                            {'label': 'Greedy Algorithm', 'value': 'greedy'},
                            {'label': 'Genetic Algorithm', 'value': 'ga'},
                            {'label': 'Particle Swarm Optimization', 'value': 'pso'},
                            {'label': 'Simulated Annealing', 'value': 'sa'},
                            {'label': 'Genetic Algorithm + SA', 'value': 'ga_sa'},
                            {'label': 'Grey Wolf Optimizer', 'value': 'gwo'},
                            {'label': 'Manta Ray Foraging Optimizer', 'value': 'mrfo'}

                        ],
                        value='greedy'
                    ),
                    
                    # Parallel Processing Toggle (for supported algorithms)
                    html.Div([
                        html.Hr(),
                        html.Label("⚡ Performance Options"),
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label("Parallel Processing", className="form-label"),
                                        html.Div([
                                            dbc.Switch(
                                                id="parallel-processing-switch",
                                                label="Enable parallel execution",
                                                value=False,
                                                disabled=True  # Will be enabled for supported algorithms
                                            ),
                                            dbc.FormText("Speeds up optimization on multi-core systems", color="muted")
                                        ])
                                    ], width=12)
                                ]),
                                html.Div(id="parallel-info", className="mt-2")
                            ])
                        ], color="light", outline=True)
                    ], id="parallel-options"),
                    
                    html.Div(id='algorithm-params', className="mt-3"),
                    
                    # Simulation Parameters
                    html.Hr(),
                    html.Label("🌍 Environment Settings"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Area Width"),
                            dbc.Input(id="area-width", type="number", value=100, min=10, max=1000)
                        ]),
                        dbc.Col([
                            html.Label("Area Height"),
                            dbc.Input(id="area-height", type="number", value=100, min=10, max=1000)
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Total Drones"),
                            dbc.Input(id="total-drones", type="number", value=20, min=1, max=100)
                        ]),
                        dbc.Col([
                            html.Label("Sensing Radius"),
                            dbc.Input(id="sensing-radius", type="number", value=20, min=1, max=50)
                        ])
                    ], className="mt-2"),
                    
                    # For parking scenario
                    html.Div([
                        html.Label("🅿️ Parking Scenario Settings"),
                        dbc.Row([
                            dbc.Col([
                                html.Label("Parking Spots"),
                                dbc.Input(id="parking-spots", type="number", value=100, min=10, max=1000)
                            ]),
                            dbc.Col([
                                html.Label("Disabled Spots"),
                                dbc.Input(id="disabled-spots", type="number", value=10, min=0, max=100)
                            ])
                        ]),
                    ], className="mt-3"),
                    
                    # Enhanced Simulation Control Buttons
                    html.Hr(),
                    html.Label("🎮 Simulation Controls"),
                    
                    # Initialize button
                    dbc.Button(
                        "🚀 Initialize Simulation",
                        id="init-button",
                        color="primary",
                        size="sm",
                        className="w-100 mb-2"
                    ),
                    
                    # Status indicator
                    dbc.Alert(
                        id="sim-status-alert",
                        children="⭕ Not Started",
                        color="secondary",
                        className="mb-2 text-center"
                    ),
                    
                    # Control buttons
                    dbc.ButtonGroup([
                        dbc.Button("▶️ Start", id="main-control-btn", color="success", size="sm"),  # Start/Pause/Resume
                        dbc.Button("👣 Step", id="step-button", color="secondary", size="sm"),
                        dbc.Button("🔄 Reset", id="stop-reset-btn", color="info", size="sm"),     # Stop/Reset
                    ], className="w-100 mb-2"),
                    
                    # Simulation speed control
                    html.Hr(),
                    html.Label("🏃 Simulation Speed"),
                    dcc.Slider(
                        id="simulation-speed",
                        min=0.1,
                        max=5.0,
                        step=0.1,
                        value=1.0,
                        marks={0.5: '0.5x', 1: '1x', 2: '2x', 5: '5x'},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    
                    # Save/Load Configuration
                    html.Hr(),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Save Config", id="save-config", color="info", size="sm")
                        ], width=6),
                        dbc.Col([
                            dbc.Button("Load Config", id="load-config", color="info", size="sm")
                        ], width=6)
                    ])
                ])
            ], className="mb-2")
        ], width=2),
        
        # Main Visualization Area
        dbc.Col([
            dbc.Tabs([
                # Simulation View Tab
                dbc.Tab([
                    dcc.Graph(id="simulation-graph", style={'height': '90vh', 'width': '100%'}),
                    html.Button("Download Plot", id="download-plot-btn", className="mb-2"),
                    dcc.Download(id="download-plot"),
                ], label="🎯 Simulation View"),
                
                # Metrics Tab
                dbc.Tab([
                    dbc.Row([
                        dbc.Col(dcc.Graph(id="coverage-chart"), width=6),
                        dbc.Col(dcc.Graph(id="power-chart"), width=6)
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id="overlap-chart"), width=6),
                        dbc.Col(dcc.Graph(id="violation-chart"), width=6)
                    ])
                ], label="📊 Performance Metrics"),
                
                # Experiment Results Tab
                dbc.Tab([
                    html.Div(id="experiment-results-content")
                ], label="🧪 Experiment Results")
            ])
        ], width=10, style={"flex": "1 1 0", "minWidth": 0})
    ]),
    
    # Bottom panel - Logs and Info
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    "📝 Simulation Logs",
                    dbc.Badge("Live", color="success", className="ms-2")
                ]),
                dbc.CardBody([
                    html.Div(id="log-output", style={'height': '15vh', 'overflow': 'auto'})
                ])
            ])
        ])
    ], className="mt-3"),
    
    # Interval for continuous simulation
    dcc.Interval(
        id='simulation-interval',
        interval=1000,  # in milliseconds
        n_intervals=0,
        disabled=True
    ),
    
    # Store for holding algorithm parameters
    dcc.Store(id='algorithm-params-store'),
    
    # Store for holding simulation state
    dcc.Store(id='simulation-state'),
    
    # Store for experiment data
    dcc.Store(id='experiment-data-store')
], fluid=True)

# Callback to update parallel processing availability based on algorithm
@app.callback(
    [Output('parallel-processing-switch', 'disabled'),
     Output('parallel-info', 'children')],
    Input('algorithm-dropdown', 'value')
)
def update_parallel_availability(algorithm):
    """Enable/disable parallel processing based on algorithm support"""
    parallel_supported = algorithm in ['ga', 'pso']  # GA and PSO support parallel processing
    
    if parallel_supported:
        import multiprocessing
        cpu_count = multiprocessing.cpu_count()
        info = dbc.Alert(
            f"✅ Parallel processing available ({cpu_count} CPU cores detected)",
            color="success",
            className="small"
        )
        return False, info
    else:
        info = dbc.Alert(
            f"ℹ️ Parallel processing not available for {algorithm.upper()} algorithm",
            color="info",
            className="small"
        )
        return True, info

# Enhanced algorithm parameter callback with parallel processing
@app.callback(
    [Output('algorithm-params', 'children'),
     Output('algorithm-params-store', 'data')],
    [Input('algorithm-dropdown', 'value'),
     Input('parallel-processing-switch', 'value')]
)
def update_algorithm_params(algorithm, parallel_enabled):
    """Update algorithm parameter inputs based on selected algorithm"""
    try:
        # Default parameter values
        params = {'parallel_processing': parallel_enabled if algorithm in ['ga', 'pso'] else False}
        
        if algorithm == 'ga':
            params.update({
                'population_size': 50,
                'num_generations': 100,
                'mutation_rate': 0.1,
                'crossover_rate': 0.8,
                'elitism': 10
            })
            return dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Population Size"),
                            dbc.Input(id="ga-population", type="number", value=params['population_size'], min=10, max=500),
                            dbc.FormText("Larger populations explore more solutions", color="muted")
                        ], width=6),
                        dbc.Col([
                            html.Label("Generations"),
                            dbc.Input(id="ga-generations", type="number", value=params['num_generations'], min=10, max=1000),
                            dbc.FormText("More generations = better convergence", color="muted")
                        ], width=6)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Mutation Rate"),
                            dbc.Input(id="ga-mutation", type="number", value=params['mutation_rate'], min=0, max=1, step=0.01),
                            dbc.FormText("0.05-0.2 recommended", color="muted")
                        ], width=4),
                        dbc.Col([
                            html.Label("Crossover Rate"),
                            dbc.Input(id="ga-crossover", type="number", value=params['crossover_rate'], min=0, max=1, step=0.01),
                            dbc.FormText("0.6-0.9 recommended", color="muted")
                        ], width=4),
                        dbc.Col([
                            html.Label("Elite Count"),
                            dbc.Input(id="ga-elitism", type="number", value=params['elitism'], min=1, max=50),
                            dbc.FormText("Best solutions to keep", color="muted")
                        ], width=4)
                    ], className="mt-2"),
                    html.Div([
                        dbc.Alert([
                            html.I(className="bi bi-lightning-charge me-2"),
                            f"Parallel processing: {'Enabled' if parallel_enabled else 'Disabled'}"
                        ], color="success" if parallel_enabled else "secondary", className="mt-2")
                    ]) if algorithm == 'ga' else html.Div()
                ])
            ]), params
            
        elif algorithm == 'pso':
            params.update({
                'swarm_size': 30,
                'iterations': 100,
                'inertia': 0.5,
                'cognitive_weight': 1.5,
                'social_weight': 1.5
            })
            return dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Swarm Size"),
                            dbc.Input(id="pso-swarm", type="number", value=params['swarm_size'], min=10, max=500),
                            dbc.FormText("Number of particles in swarm", color="muted")
                        ], width=6),
                        dbc.Col([
                            html.Label("Iterations"),
                            dbc.Input(id="pso-iterations", type="number", value=params['iterations'], min=10, max=1000),
                            dbc.FormText("Number of optimization steps", color="muted")
                        ], width=6)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Inertia Weight"),
                            dbc.Input(id="pso-inertia", type="number", value=params['inertia'], min=0, max=1, step=0.01),
                            dbc.FormText("Controls exploration vs exploitation", color="muted")
                        ], width=4),
                        dbc.Col([
                            html.Label("Cognitive Weight"),
                            dbc.Input(id="pso-cognitive", type="number", value=params['cognitive_weight'], min=0, max=3, step=0.1),
                            dbc.FormText("Personal best influence", color="muted")
                        ], width=4),
                        dbc.Col([
                            html.Label("Social Weight"),
                            dbc.Input(id="pso-social", type="number", value=params['social_weight'], min=0, max=3, step=0.1),
                            dbc.FormText("Global best influence", color="muted")
                        ], width=4)
                    ], className="mt-2"),
                    html.Div([
                        dbc.Alert([
                            html.I(className="bi bi-lightning-charge me-2"),
                            f"Parallel processing: {'Enabled' if parallel_enabled else 'Disabled'}"
                        ], color="success" if parallel_enabled else "secondary", className="mt-2")
                    ]) if algorithm == 'pso' else html.Div()
                ])
            ]), params
            
        elif algorithm == 'sa':
            params.update({
                'initial_temp': 100,
                'cooling_rate': 0.95,
                'iterations': 100,
                'min_temp': 0.01
            })
            return dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Initial Temperature"),
                            dbc.Input(id="sa-temp", type="number", value=params['initial_temp'], min=1, max=1000),
                            dbc.FormText("Starting temperature", color="muted")
                        ], width=6),
                        dbc.Col([
                            html.Label("Cooling Rate"),
                            dbc.Input(id="sa-cooling", type="number", value=params['cooling_rate'], min=0.5, max=0.99, step=0.01),
                            dbc.FormText("Temperature reduction factor", color="muted")
                        ], width=6)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Iterations"),
                            dbc.Input(id="sa-iterations", type="number", value=params['iterations'], min=10, max=1000),
                            dbc.FormText("Number of optimization steps", color="muted")
                        ], width=6),
                        dbc.Col([
                            html.Label("Minimum Temperature"),
                            dbc.Input(id="sa-min-temp", type="number", value=params['min_temp'], min=0.001, max=1, step=0.001),
                            dbc.FormText("Stopping temperature", color="muted")
                        ], width=6)
                    ], className="mt-2"),
                    dbc.Alert("ℹ️ Simulated Annealing does not support parallel processing", color="info", className="mt-2")
                ])
            ]), params
            
        elif algorithm == 'ga_sa':
            params.update({
                'population_size': 50,
                'num_generations': 100,
                'mutation_rate': 0.1,
                'crossover_rate': 0.8,
                'elitism_fraction': 0.2,
                'sa_initial_temp': 100,
                'sa_cooling_rate': 0.95,
                'sa_iterations': 30,
                'desired_coverage': 0.95
            })
            return dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Population Size"),
                            dbc.Input(id="ga-sa-population-size", type="number", value=50, min=10, max=500),
                            dbc.FormText("Larger populations explore more solutions", color="muted")
                        ], width=6),
                        dbc.Col([
                            html.Label("Generations"),
                            dbc.Input(id="ga-sa-generations", type="number", value=100, min=10, max=1000),
                            dbc.FormText("More generations = better coverage", color="muted")
                        ], width=6)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Mutation Rate"),
                            dbc.Input(id="ga-sa-mutation-rate", type="number", value=0.1, min=0, max=1, step=0.01),
                            dbc.FormText("0.05-0.2 recommended", color="muted")
                        ], width=4),
                        dbc.Col([
                            html.Label("Crossover Rate"),
                            dbc.Input(id="ga-sa-crossover-rate", type="number", value=0.8, min=0, max=1, step=0.01),
                            dbc.FormText("0.6-0.9 recommended", color="muted")
                        ], width=4),
                        dbc.Col([
                            html.Label("Elitism Fraction"),
                            dbc.Input(id="ga-sa-elitism-fraction", type="number", value=0.2, min=0, max=1, step=0.01),
                            dbc.FormText("Top fraction of solutions to keep", color="muted")
                        ], width=4)
                    ], className="mt-2"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("SA Initial Temp"),
                            dbc.Input(id="ga-sa-sa-temp", type="number", value=100, min=1, max=1000),
                            dbc.FormText("Starting temperature for SA", color="muted")
                        ], width=6),
                        dbc.Col([
                            html.Label("SA Cooling Rate"),
                            dbc.Input(id="ga-sa-sa-cooling", type="number", value=0.95, min=0.8, max=1, step=0.01),
                            dbc.FormText("Cooling rate for SA", color="muted")
                        ], width=6)
                    ], className="mt-2"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("SA Iterations"),
                            dbc.Input(id="ga-sa-sa-iters", type="number", value=30, min=1, max=500),
                            dbc.FormText("Iterations for SA", color="muted")
                        ], width=6),
                        dbc.Col([
                            html.Label("Desired Coverage"),
                            dbc.Input(id="ga-sa-desired-coverage", type="number", value=0.95, min=0, max=1, step=0.01),
                            dbc.FormText("Target coverage percentage", color="muted")
                        ], width=6)
                    ], className="mt-2"),
                    html.Div([
                        dbc.Alert([
                            html.I(className="bi bi-lightning-charge me-2"),
                            f"Parallel processing: {'Enabled' if parallel_enabled else 'Disabled'}"
                        ], color="success" if parallel_enabled else "secondary", className="mt-2")
                    ]) if algorithm == 'ga_sa' else html.Div()
                ])
            ]), params
            
        elif algorithm == 'gwo':
            params.update({
                'population_size': 30,
                'max_iterations': 100,
                'desired_coverage': 0.9,
                'w1': 0.6,
                'w2': 0.2,
                'w3': 0.2
            })
            return dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Population Size"),
                            dbc.Input(id="gwo-population", type="number", value=params['population_size'], min=10, max=500),
                        ], width=6),
                        dbc.Col([
                            html.Label("Max Iterations"),
                            dbc.Input(id="gwo-iterations", type="number", value=params['max_iterations'], min=10, max=1000),
                        ], width=6)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Desired Coverage"),
                            dbc.Input(id="gwo-coverage", type="number", value=params['desired_coverage'], min=0.5, max=1, step=0.01),
                        ], width=4),
                        dbc.Col([
                            html.Label("w1 (Coverage Weight)"),
                            dbc.Input(id="gwo-w1", type="number", value=params['w1'], min=0, max=1, step=0.01),
                        ], width=4),
                        dbc.Col([
                            html.Label("w2 (Active Nodes Weight)"),
                            dbc.Input(id="gwo-w2", type="number", value=params['w2'], min=0, max=1, step=0.01),
                        ], width=4),
                        dbc.Col([
                            html.Label("w3 (Overlap Weight)"),
                            dbc.Input(id="gwo-w3", type="number", value=params['w3'], min=0, max=1, step=0.01),
                        ], width=4)
                    ], className="mt-2"),
                ])
            ]), params

        elif algorithm == 'mrfo':
            params.update({
                'population_size': 50,
                'num_generations': 200,
                'desired_coverage': 0.95,
                'w1': 0.6,
                'w2': 0.2,
                'w3': 0.2
            })
            return dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Population Size"),
                            dbc.Input(id="mrfo-population", type="number", value=params['population_size'], min=10, max=500),
                        ], width=6),
                        dbc.Col([
                            html.Label("Generations"),
                            dbc.Input(id="mrfo-generations", type="number", value=params['num_generations'], min=10, max=1000),
                        ], width=6)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Desired Coverage"),
                            dbc.Input(id="mrfo-coverage", type="number", value=params['desired_coverage'], min=0.5, max=1, step=0.01),
                        ], width=4),
                        dbc.Col([
                            html.Label("w1 (Coverage Weight)"),
                            dbc.Input(id="mrfo-w1", type="number", value=params['w1'], min=0, max=1, step=0.01),
                        ], width=4),
                        dbc.Col([
                            html.Label("w2 (Active Nodes Weight)"),
                            dbc.Input(id="mrfo-w2", type="number", value=params['w2'], min=0, max=1, step=0.01),
                        ], width=4),
                        dbc.Col([
                            html.Label("w3 (Overlap Weight)"),
                            dbc.Input(id="mrfo-w3", type="number", value=params['w3'], min=0, max=1, step=0.01),
                        ], width=4)
                    ], className="mt-2"),
                ])
            ]), params
            
        else:  # greedy
            params.update({
                'desired_coverage': 0.95,
                'overlap_weight': 0.2,
                'energy_weight': 0.1
            })
            return dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Desired Coverage"),
                            dbc.Input(id="greedy-coverage", type="number", value=params['desired_coverage'], min=0.5, max=1, step=0.01),
                            dbc.FormText("Target coverage percentage", color="muted")
                        ], width=4),
                        dbc.Col([
                            html.Label("Overlap Weight"),
                            dbc.Input(id="greedy-overlap", type="number", value=params['overlap_weight'], min=0, max=1, step=0.01),
                            dbc.FormText("Penalty for overlapping coverage", color="muted")
                        ], width=4),
                        dbc.Col([
                            html.Label("Energy Weight"),
                            dbc.Input(id="greedy-energy", type="number", value=params['energy_weight'], min=0, max=1, step=0.01),
                            dbc.FormText("Importance of energy conservation", color="muted")
                        ], width=4)
                    ]),
                    dbc.Alert("ℹ️ Greedy Algorithm does not support parallel processing", color="info", className="mt-2")
                ])
            ]), params
    
    except Exception as e:
        error_msg = f"Error updating algorithm params: {str(e)}"
        return dbc.Alert(error_msg, color="danger"), {}

# Update parameter store callbacks for all algorithms (enhanced with parallel processing)
@app.callback(
    Output('algorithm-params-store', 'data', allow_duplicate=True),
    [Input('ga-population', 'value'),
     Input('ga-generations', 'value'),
     Input('ga-mutation', 'value'),
     Input('ga-crossover', 'value'),
     Input('ga-elitism', 'value')],
    [State('algorithm-dropdown', 'value'),
     State('algorithm-params-store', 'data'),
     State('parallel-processing-switch', 'value')],
    prevent_initial_call=True
)
def update_ga_params(population, generations, mutation, crossover, elitism, algorithm, current_params, parallel_enabled):
    """Update genetic algorithm parameters"""
    if algorithm != 'ga' or current_params is None:
        return dash.no_update
    
    try:
        current_params.update({
            'population_size': population if population is not None else 50,
            'num_generations': generations if generations is not None else 100,
            'mutation_rate': mutation if mutation is not None else 0.1,
            'crossover_rate': crossover if crossover is not None else 0.8,
            'elitism': elitism if elitism is not None else 10,
            'parallel_processing': parallel_enabled
        })
        return current_params
    except Exception:
        return current_params

# Similar callbacks for other algorithms...
@app.callback(
    Output('algorithm-params-store', 'data', allow_duplicate=True),
    [Input('pso-swarm', 'value'),
     Input('pso-iterations', 'value'),
     Input('pso-inertia', 'value'),
     Input('pso-cognitive', 'value'),
     Input('pso-social', 'value')],
    [State('algorithm-dropdown', 'value'),
     State('algorithm-params-store', 'data'),
     State('parallel-processing-switch', 'value')],
    prevent_initial_call=True
)
def update_pso_params(swarm, iterations, inertia, cognitive, social, algorithm, current_params, parallel_enabled):
    """Update PSO algorithm parameters"""
    if algorithm != 'pso' or current_params is None:
        return dash.no_update
    
    try:
        current_params.update({
            'swarm_size': swarm if swarm is not None else 30,
            'iterations': iterations if iterations is not None else 100,
            'inertia': inertia if inertia is not None else 0.5,
            'cognitive_weight': cognitive if cognitive is not None else 1.5,
            'social_weight': social if social is not None else 1.5,
            'parallel_processing': parallel_enabled
        })
        return current_params
    except Exception:
        return current_params

# Initialize simulation
@app.callback(
    Output('log-output', 'children', allow_duplicate=True),
    Input('init-button', 'n_clicks'),
    [State('area-width', 'value'),
     State('area-height', 'value'),
     State('total-drones', 'value'),
     State('sensing-radius', 'value'),
     State('parking-spots', 'value'),
     State('disabled-spots', 'value')],
    prevent_initial_call=True
)
def initialize_simulation(n_clicks, width, height, drones, radius, parking, disabled_spots):
    """Initialize the simulation environment"""
    if n_clicks is None:
        return dash.no_update
    
    try:
        global simulation, current_sim_state
        simulation = DroneEnvironment(
            width=width or 100,
            height=height or 100,
            num_drones=drones or 20,
            sensing_radius=radius or 20,
            num_parking_spots=parking or 100,
            num_disabled_spots=disabled_spots or 10
        )
        
        # Reset state to stopped after initialization
        current_sim_state = SimState.STOPPED
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        return f"[{timestamp}] ✅ Simulation initialized with {drones or 20} drones in {width or 100}x{height or 100} area."
    
    except Exception as e:
        timestamp = datetime.now().strftime("%H:%M:%S")
        error_msg = f"[{timestamp}] ❌ Error initializing simulation: {str(e)}"
        print(f"Initialization error: {traceback.format_exc()}")
        return error_msg

# Enhanced Control System - REPLACES the old toggle_simulation_interval callback
@app.callback(
    [Output('simulation-interval', 'disabled'),
     Output('simulation-interval', 'interval'),
     Output('main-control-btn', 'children'),
     Output('main-control-btn', 'color'),
     Output('stop-reset-btn', 'children'),
     Output('stop-reset-btn', 'color'),
     Output('sim-status-alert', 'children'),
     Output('sim-status-alert', 'color'),
     Output('log-output', 'children', allow_duplicate=True)],
    [Input('main-control-btn', 'n_clicks'),
     Input('stop-reset-btn', 'n_clicks'),
     Input('simulation-speed', 'value')],
    [State('simulation-interval', 'disabled'),
     State('log-output', 'children')],
    prevent_initial_call=True
)
def unified_control(main_clicks, stopreset_clicks, speed_value, is_disabled, log_output):
    global current_sim_state, simulation
    triggered_id = ctx.triggered_id
    timestamp = datetime.now().strftime("%H:%M:%S")
    interval = max(100, int(1000 / (speed_value or 1.0)))

    try:
        # Button logic
        if triggered_id == 'main-control-btn':
            if current_sim_state == SimState.STOPPED:
                # Check if simulation is initialized before starting
                if simulation is None:
                    return True, interval, "▶️ Start", "danger", "🔄 Reset", "info", "❌ Error", "danger", f"[{timestamp}] ❌ Please initialize simulation first!"
                current_sim_state = SimState.RUNNING
                return False, interval, "⏸️ Pause", "warning", "⏹️ Stop", "danger", "🟢 Running", "success", f"[{timestamp}] ▶️ Simulation started"
            elif current_sim_state == SimState.RUNNING:
                current_sim_state = SimState.PAUSED
                return True, interval, "▶️ Resume", "success", "⏹️ Stop", "danger", "🟡 Paused", "warning", f"[{timestamp}] ⏸️ Simulation paused"
            elif current_sim_state == SimState.PAUSED:
                current_sim_state = SimState.RUNNING
                return False, interval, "⏸️ Pause", "warning", "⏹️ Stop", "danger", "🟢 Running", "success", f"[{timestamp}] ▶️ Simulation resumed"
        elif triggered_id == 'stop-reset-btn':
            if current_sim_state in [SimState.RUNNING, SimState.PAUSED]:
                current_sim_state = SimState.STOPPED
                return True, interval, "▶️ Start", "success", "🔄 Reset", "info", "🔴 Stopped", "danger", f"[{timestamp}] ⏹️ Simulation stopped"
            elif current_sim_state == SimState.STOPPED:
                if simulation:
                    simulation.reset_simulation()
                current_sim_state = SimState.STOPPED
                return True, interval, "▶️ Start", "success", "🔄 Reset", "info", "🔵 Reset", "info", f"[{timestamp}] 🔄 Simulation reset"
        elif triggered_id == 'simulation-speed':
            # Only update interval, keep other states
            if current_sim_state == SimState.RUNNING:
                return False, interval, "⏸️ Pause", "warning", "⏹️ Stop", "danger", "🟢 Running", "success", f"[{timestamp}] 🏃 Speed changed"
            elif current_sim_state == SimState.PAUSED:
                return True, interval, "▶️ Resume", "success", "⏹️ Stop", "danger", "🟡 Paused", "warning", f"[{timestamp}] 🏃 Speed changed"
            else:
                return True, interval, "▶️ Start", "success", "🔄 Reset", "info", "⭕ Not Started", "secondary", f"[{timestamp}] 🏃 Speed changed"
        else:
            # Default
            return is_disabled, interval, "▶️ Start", "success", "🔄 Reset", "info", "⭕ Not Started", "secondary", f"[{timestamp}] Ready"
    except Exception as e:
        error_msg = f"[{timestamp}] ❌ Control error: {str(e)}"
        return True, interval, "▶️ Start", "danger", "🔄 Reset", "danger", "❌ Error", "danger", error_msg

# Enhanced simulation step with experiment logging and state management
@app.callback(
    [Output('simulation-graph', 'figure'),
     Output('coverage-chart', 'figure'),
     Output('power-chart', 'figure'),
     Output('overlap-chart', 'figure'),
     Output('violation-chart', 'figure')],
    [Input('step-button', 'n_clicks'),
     Input('simulation-interval', 'n_intervals')],
    [State('algorithm-dropdown', 'value'),
     State('algorithm-params-store', 'data')]
)
def update_simulation(step_clicks, interval, algorithm, algorithm_params):
    """Update simulation visualization and metrics with experiment logging and state management"""
    global current_sim_state  # ADD THIS LINE for state management
    
    ctx_msg = ctx.triggered_id
    if ctx_msg is None or simulation is None:
        # Default empty figures
        empty_fig = go.Figure()
        empty_fig.update_layout(title="Simulation Not Started - Click Initialize")
        return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig
    
    try:
        # Enhanced state checking - only step when appropriate
        should_step = False
        if ctx_msg == 'step-button':
            should_step = True  # Manual step always allowed
        elif ctx_msg == 'simulation-interval':
            should_step = (current_sim_state == SimState.RUNNING)  # Only auto-step when running
        
        if should_step:
            # Use the stored parameters
            if algorithm_params is None:
                algorithm_params = {}
            
            start_time = datetime.now()
            
            # Run optimization based on selected algorithm with parallel processing support
            if algorithm == 'ga':
                activation_status, result = genetic_algorithm(simulation, **algorithm_params)
            elif algorithm == 'pso':
                activation_status, result = particle_swarm_optimization(simulation, **algorithm_params)
            elif algorithm == 'sa':
                activation_status, result = simulated_annealing(simulation, **algorithm_params)
            elif algorithm == 'gwo':
                filtered_params = filter_params('gwo', algorithm_params)
                activation_status, result = grey_wolf_optimizer(simulation, **filtered_params)
            elif algorithm == 'mrfo':
                filtered_params = filter_params('mrfo', algorithm_params)
                activation_status, result = manta_ray_foraging_optimization(simulation, **filtered_params)
            else:  # greedy
                algorithm_params.pop('parallel_processing', None)
                activation_status, result = greedy_optimization(simulation, **algorithm_params)
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # Apply the optimization result
            simulation.apply_activation(activation_status)
            step_result = simulation.step()
            
            # Log step data if experiment is active
            if current_experiment_session:
                step_data = {
                    'step': simulation.step_count,
                    'algorithm': algorithm,
                    'algorithm_params': algorithm_params,
                    'execution_time': execution_time,
                    'result': step_result,
                    'parallel_processing_used': algorithm_params.get('parallel_processing', False)
                }
                experiment_logger.log_step_result(step_data)
        
        # Create visualization
        simulation_fig = create_simulation_view(simulation)
        
        # Create metric charts
        metrics_charts = create_metrics_charts(simulation)
        coverage_fig = metrics_charts['coverage']
        power_fig = metrics_charts['power']
        overlap_fig = metrics_charts['overlap']
        
        # Violations chart (might be None if not a parking scenario)
        violations_fig = metrics_charts.get('violations')
        if violations_fig is None:
            violations_fig = go.Figure()
            violations_fig.update_layout(title="No Violation Data Available")
        
        return simulation_fig, coverage_fig, power_fig, overlap_fig, violations_fig
    
    except Exception as e:
        # Error handling - return error figures
        error_fig = go.Figure()
        error_msg = f"Error in simulation: {str(e)}"
        error_fig.update_layout(title=error_msg)
        print(f"Simulation error: {traceback.format_exc()}")
        return error_fig, error_fig, error_fig, error_fig, error_fig

# Download plot callback
@app.callback(
    Output("download-plot", "data"),
    Input("download-plot-btn", "n_clicks"),
    State("simulation-graph", "figure"),
    prevent_initial_call=True,
)
def download_plot(n_clicks, fig):
    if n_clicks:
        # Increase scale for higher resolution (e.g., 3 or 4)
        img_bytes = pio.to_image(fig, format="png", width=1600, height=1200, scale=3)
        return dcc.send_bytes(img_bytes, filename="simulation_plot.png")
    return dash.no_update

# Filter parameters for algorithms
def filter_params(algo, params):
    allowed = {
        'gwo': ['population_size', 'max_iterations', 'desired_coverage', 'parallel_processing', 'w1', 'w2', 'w3'],
        'mrfo': ['population_size', 'num_generations', 'desired_coverage', 'parallel_processing', 'w1', 'w2', 'w3'],
    }
    return {k: v for k, v in (params or {}).items() if k in allowed.get(algo, [])}

# Update experiment results display
@app.callback(
    Output('experiment-results-content', 'children'),
    Input('experiment-data-store', 'data')
)
def update_experiment_results(data):
    if not data:
        return html.Div("No experiment results yet.")
    # Example: Show a table of results
    df = pd.DataFrame(data)
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

# Run the app
if __name__ == '__main__':
    print("🚁 Starting Enhanced Drone Optimization Simulation System...")
    print("📍 Open your browser to: http://127.0.0.1:8050")
    app.run_server(debug=True, host='127.0.0.1', port=8050)