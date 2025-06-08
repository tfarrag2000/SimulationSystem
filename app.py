import dash
from dash import dcc, html, Input, Output, State, callback, ALL, MATCH, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from datetime import datetime
import traceback
import json
import os

# Fixed imports to match actual file structure
try:
    # Import optimization algorithms
    from optimization.algorithms import (
        greedy_optimization,
        genetic_algorithm,
        particle_swarm_optimization,
        simulated_annealing
    )
    
    # Import simulation components
    from simulation.environment import DroneEnvironment
    from simulation import SimulationState, run_simulation_step
    
    # Import visualization helpers
    from visualization.helpers import create_simulation_view, create_metrics_charts
    
    # Import experiment logger
    from utils.experiment_logger import ExperimentLogger
    
    print("✅ All modules imported successfully")
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all modules are in the correct directory structure")
    # Fallback implementations...
    def greedy_optimization(*args, **kwargs):
        return np.ones(20), {"coverage": 50, "execution_time": 0.1}
    
    def genetic_algorithm(*args, **kwargs):
        return np.ones(20), {"coverage": 60, "execution_time": 1.0}
    
    def particle_swarm_optimization(*args, **kwargs):
        return np.ones(20), {"coverage": 55, "execution_time": 0.8}
    
    def simulated_annealing(*args, **kwargs):
        return np.ones(20), {"coverage": 45, "execution_time": 0.5}
    
    class DroneEnvironment:
        def __init__(self, **kwargs):
            self.width = kwargs.get('width', 100)
            self.height = kwargs.get('height', 100)
            self.step_count = 0
    
    class SimulationState:
        def __init__(self):
            self.current_step = 0
    
    def run_simulation_step(simulation, algorithm, params):
        return {"coverage": 0.5, "active_drones": 10}
    
    def create_simulation_view(simulation):
        return go.Figure().update_layout(title="Simulation not available")
    
    def create_metrics_charts(simulation):
        empty_fig = go.Figure().update_layout(title="Metrics not available")
        return {
            'coverage': empty_fig,
            'power': empty_fig,
            'overlap': empty_fig,
            'violations': empty_fig
        }
    
    class ExperimentLogger:
        def __init__(self):
            pass
        def log_experiment(self, data):
            return "dummy_exp_id"

# Global simulation state and experiment management
simulation = None
sim_state = SimulationState()
experiment_logger = ExperimentLogger()
current_experiment_session = None

# Initialize the app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Drone Optimization Simulation System"

# App layout with enhanced experiment management
app.layout = dbc.Container([
    # Header with experiment info
    dbc.Row([
        dbc.Col([
            html.H1("Drone Optimization Simulation System", className="text-center my-4"),
            dbc.Alert(id="experiment-status", color="info", is_open=False, dismissable=True)
        ])
    ]),
    
    # Main content split into sidebar and visualization
    dbc.Row([
        # Control Panel (Left Sidebar)
        dbc.Col([
            # Experiment Management Card
            dbc.Card([
                dbc.CardHeader("🧪 Experiment Management"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Input(
                                id="experiment-name",
                                placeholder="Enter experiment name...",
                                value="",
                                type="text"
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Button("Start Experiment", id="start-experiment", color="success", size="sm")
                        ], width=4)
                    ]),
                    html.Div(id="experiment-info", className="mt-2"),
                    html.Hr(),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Save Results", id="save-experiment", color="primary", size="sm", disabled=True)
                        ], width=4),
                        dbc.Col([
                            dbc.Button("Export Data", id="export-experiment", color="info", size="sm", disabled=True)
                        ], width=4),
                        dbc.Col([
                            dbc.Button("View History", id="view-history", color="secondary", size="sm")
                        ], width=4)
                    ])
                ])
            ], className="mb-3"),
            
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
                            {'label': 'Simulated Annealing', 'value': 'sa'}
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
                    
                    # Simulation Control Buttons
                    html.Hr(),
                    dbc.ButtonGroup([
                        dbc.Button("Initialize", id="init-button", color="primary"),
                        dbc.Button("Step", id="step-button", color="secondary"),
                        dbc.Button("Run", id="run-button", color="success"),
                        dbc.Button("Pause", id="pause-button", color="warning")
                    ], className="w-100"),
                    
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
            ], className="mb-4")
        ], width=3),
        
        # Main Visualization Area
        dbc.Col([
            dbc.Tabs([
                # Simulation View Tab
                dbc.Tab([
                    dcc.Graph(id="simulation-graph", style={'height': '60vh'})
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
        ], width=9)
    ]),
    
    # Bottom panel - Logs and Info
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📝 Simulation Logs"),
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

# Experiment management callbacks
@app.callback(
    [Output('experiment-status', 'children'),
     Output('experiment-status', 'is_open'),
     Output('experiment-status', 'color'),
     Output('save-experiment', 'disabled'),
     Output('export-experiment', 'disabled'),
     Output('experiment-info', 'children')],
    Input('start-experiment', 'n_clicks'),
    State('experiment-name', 'value')
)
def start_experiment_session(n_clicks, experiment_name):
    """Start a new experiment session"""
    if n_clicks is None:
        return "", False, "info", True, True, ""
    
    global current_experiment_session
    
    try:
        if not experiment_name or experiment_name.strip() == "":
            experiment_name = f"Experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Start experiment session
        session_config = {
            'name': experiment_name,
            'start_time': datetime.now().isoformat(),
            'algorithm_runs': []
        }
        
        current_experiment_session = experiment_logger.start_experiment_session(session_config)
        
        status_msg = f"🧪 Experiment '{experiment_name}' started!"
        experiment_info = dbc.Card([
            dbc.CardBody([
                html.H6("Active Experiment", className="card-title"),
                html.P(f"Name: {experiment_name}", className="card-text small"),
                html.P(f"Session ID: {current_experiment_session}", className="card-text small text-muted"),
                html.P(f"Started: {datetime.now().strftime('%H:%M:%S')}", className="card-text small text-muted")
            ])
        ], color="success", outline=True)
        
        return status_msg, True, "success", False, False, experiment_info
        
    except Exception as e:
        error_msg = f"Error starting experiment: {str(e)}"
        return error_msg, True, "danger", True, True, ""

# Save experiment results
@app.callback(
    Output('experiment-status', 'children', allow_duplicate=True),
    Output('experiment-status', 'is_open', allow_duplicate=True),
    Output('experiment-status', 'color', allow_duplicate=True),
    Input('save-experiment', 'n_clicks'),
    [State('algorithm-dropdown', 'value'),
     State('algorithm-params-store', 'data')],
    prevent_initial_call=True
)
def save_experiment_results(n_clicks, algorithm, algorithm_params):
    """Save current experiment results"""
    if n_clicks is None or current_experiment_session is None:
        return dash.no_update, dash.no_update, dash.no_update
    
    try:
        # Collect experiment data
        experiment_data = {
            'session_id': current_experiment_session,
            'timestamp': datetime.now().isoformat(),
            'algorithm': algorithm,
            'algorithm_parameters': algorithm_params or {},
            'simulation_parameters': {
                'width': simulation.width if simulation else 100,
                'height': simulation.height if simulation else 100,
                'num_drones': len(simulation.drones) if simulation else 20,
                'sensing_radius': simulation.sensing_radius if simulation else 20
            },
            'results': {
                'coverage': simulation.metrics_history['coverage'][-1] if simulation and simulation.metrics_history['coverage'] else 0,
                'active_drones': simulation.metrics_history['active_drones'][-1] if simulation and simulation.metrics_history['active_drones'] else 0,
                'step_count': simulation.step_count if simulation else 0,
                'metrics_history': simulation.metrics_history if simulation else {}
            }
        }
        
        # Save experiment
        exp_id = experiment_logger.log_experiment(experiment_data)
        
        return f"✅ Experiment saved successfully! ID: {exp_id}", True, "success"
        
    except Exception as e:
        return f"❌ Error saving experiment: {str(e)}", True, "danger"

# Continue with the rest of the callbacks...
# (Previous callbacks for simulation, visualization, etc. remain the same)

# Initialize simulation
@app.callback(
    Output('log-output', 'children'),
    Input('init-button', 'n_clicks'),
    [State('area-width', 'value'),
     State('area-height', 'value'),
     State('total-drones', 'value'),
     State('sensing-radius', 'value'),
     State('parking-spots', 'value'),
     State('disabled-spots', 'value')]
)
def initialize_simulation(n_clicks, width, height, drones, radius, parking, disabled_spots):
    """Initialize the simulation environment"""
    if n_clicks is None:
        return "System ready. Click 'Initialize Simulation' to begin."
    
    try:
        global simulation
        simulation = DroneEnvironment(
            width=width or 100,
            height=height or 100,
            num_drones=drones or 20,
            sensing_radius=radius or 20,
            num_parking_spots=parking or 100,
            num_disabled_spots=disabled_spots or 10
        )
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        return f"[{timestamp}] Simulation initialized with {drones or 20} drones in {width or 100}x{height or 100} area."
    
    except Exception as e:
        timestamp = datetime.now().strftime("%H:%M:%S")
        error_msg = f"[{timestamp}] Error initializing simulation: {str(e)}"
        print(f"Initialization error: {traceback.format_exc()}")
        return error_msg

# Enhanced simulation step with experiment logging
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
    """Update simulation visualization and metrics with experiment logging"""
    ctx_msg = ctx.triggered_id
    if ctx_msg is None or simulation is None:
        # Default empty figures
        empty_fig = go.Figure()
        empty_fig.update_layout(title="Simulation Not Started")
        return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig
    
    try:
        # Determine if we should run a simulation step
        if ctx_msg in ['step-button', 'simulation-interval']:
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
            else:  # greedy
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

# Callback for enabling/disabling interval for continuous simulation
@app.callback(
    Output('simulation-interval', 'disabled'),
    [Input('run-button', 'n_clicks'),
     Input('pause-button', 'n_clicks')],
    [State('simulation-interval', 'disabled')]
)
def toggle_simulation_interval(run_clicks, pause_clicks, is_disabled):
    """Toggle continuous simulation on/off"""
    ctx_msg = ctx.triggered_id
    if ctx_msg is None:
        return True  # Keep disabled by default
    
    if ctx_msg == 'run-button':
        return False  # Enable interval
    elif ctx_msg == 'pause-button':
        return True   # Disable interval
    
    return is_disabled  # No change

# Export experiment data
@app.callback(
    Output('log-output', 'children', allow_duplicate=True),
    Input('export-experiment', 'n_clicks'),
    prevent_initial_call=True
)
def export_experiment_data(n_clicks):
    """Export experiment data to file"""
    if n_clicks is None or current_experiment_session is None:
        return dash.no_update
    
    try:
        # End current experiment session and get final results
        final_exp_id = experiment_logger.end_experiment_session()
        
        # Create exports directory
        os.makedirs('exports', exist_ok=True)
        
        # Export data in multiple formats
        from utils.data_exporter import DataExporter
        exporter = DataExporter(experiment_logger)
        
        # Export HTML report
        html_report = exporter.export_experiment_report(final_exp_id, format='html')
        
        # Export raw data
        json_data = exporter.export_experiment_data(final_exp_id, format='json')
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        return f"[{timestamp}] Experiment exported: {html_report}, {json_data}"
        
    except Exception as e:
        timestamp = datetime.now().strftime("%H:%M:%S")
        return f"[{timestamp}] Export error: {str(e)}"

# View experiment history
@app.callback(
    Output('experiment-results-content', 'children'),
    Input('view-history', 'n_clicks'),
    prevent_initial_call=True
)
def view_experiment_history(n_clicks):
    """Display experiment history"""
    if n_clicks is None:
        return html.Div("Click 'View History' to see past experiments.")
    
    try:
        # Get list of experiments
        experiments = experiment_logger.list_experiments()
        
        if not experiments:
            return dbc.Alert("No experiments found.", color="info")
        
        # Create experiment history table
        experiment_cards = []
        for exp in experiments[:10]:  # Show last 10 experiments
            card = dbc.Card([
                dbc.CardBody([
                    html.H6(f"Experiment: {exp['experiment_id']}", className="card-title"),
                    html.P([
                        html.Strong("Algorithm: "), exp['algorithm'], html.Br(),
                        html.Strong("Coverage: "), f"{exp['coverage']:.1f}%", html.Br(),
                        html.Strong("Date: "), exp['timestamp'][:19].replace('T', ' ')
                    ], className="card-text small"),
                    dbc.ButtonGroup([
                        dbc.Button("View Details", size="sm", color="info"),
                        dbc.Button("Compare", size="sm", color="secondary"),
                        dbc.Button("Export", size="sm", color="success")
                    ])
                ])
            ], className="mb-2")
            experiment_cards.append(card)
        
        return html.Div([
            html.H5("Experiment History"),
            html.Hr(),
            *experiment_cards
        ])
        
    except Exception as e:
        return dbc.Alert(f"Error loading experiment history: {str(e)}", color="danger")

# Save configuration with parallel processing settings
@app.callback(
    Output('log-output', 'children', allow_duplicate=True),
    Input('save-config', 'n_clicks'),
    [State('algorithm-dropdown', 'value'),
     State('algorithm-params-store', 'data'),
     State('area-width', 'value'),
     State('area-height', 'value'),
     State('total-drones', 'value'),
     State('sensing-radius', 'value'),
     State('parallel-processing-switch', 'value')],
    prevent_initial_call=True
)
def save_configuration(n_clicks, algorithm, params, width, height, drones, radius, parallel_enabled):
    """Save current configuration including parallel processing settings"""
    if n_clicks is None:
        return dash.no_update
    
    try:
        config = {
            'algorithm': algorithm,
            'algorithm_params': params or {},
            'parallel_processing': parallel_enabled,
            'environment': {
                'width': width or 100,
                'height': height or 100,
                'num_drones': drones or 20,
                'sensing_radius': radius or 20
            },
            'timestamp': datetime.now().isoformat()
        }
        
        # Create configs directory if it doesn't exist
        os.makedirs('configs', exist_ok=True)
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"configs/config_{algorithm}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        
        return f"Configuration saved to {filename}"
    
    except Exception as e:
        return f"Error saving configuration: {str(e)}"

# Load configuration
@app.callback(
    [Output('algorithm-dropdown', 'value'),
     Output('parallel-processing-switch', 'value'),
     Output('area-width', 'value'),
     Output('area-height', 'value'),
     Output('total-drones', 'value'),
     Output('sensing-radius', 'value')],
    Input('load-config', 'n_clicks'),
    prevent_initial_call=True
)
def load_configuration(n_clicks):
    """Load most recent configuration"""
    if n_clicks is None:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    
    try:
        # Find the most recent config file
        import glob
        
        config_files = glob.glob('configs/config_*.json')
        if not config_files:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
        # Get most recent file
        latest_config = max(config_files, key=os.path.getctime)
        
        with open(latest_config, 'r') as f:
            config = json.load(f)
        
        # Extract values
        algorithm = config.get('algorithm', 'greedy')
        parallel = config.get('parallel_processing', False)
        env = config.get('environment', {})
        
        return (
            algorithm,
            parallel,
            env.get('width', 100),
            env.get('height', 100),
            env.get('num_drones', 20),
            env.get('sensing_radius', 20)
        )
        
    except Exception as e:
        print(f"Error loading configuration: {str(e)}")
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

# Status update callback for continuous updates with parallel processing info
@app.callback(
    Output('log-output', 'children', allow_duplicate=True),
    [Input('simulation-interval', 'n_intervals')],
    [State('simulation-interval', 'disabled'),
     State('algorithm-dropdown', 'value'),
     State('algorithm-params-store', 'data')],
    prevent_initial_call=True
)
def update_status(n_intervals, disabled, algorithm, algorithm_params):
    """Update status during continuous simulation with parallel processing info"""
    if disabled or simulation is None:
        return dash.no_update
    
    try:
        timestamp = datetime.now().strftime("%H:%M:%S")
        step = simulation.step_count
        
        # Check if parallel processing is enabled
        parallel_status = ""
        if algorithm_params and algorithm_params.get('parallel_processing'):
            parallel_status = " [Parallel]"
        
        # Get latest metrics if available
        if simulation.metrics_history['coverage']:
            coverage = simulation.metrics_history['coverage'][-1] * 100
            active = simulation.metrics_history['active_drones'][-1]
            return f"[{timestamp}] Step {step}: Coverage {coverage:.1f}%, Active drones: {active}{parallel_status}"
        else:
            return f"[{timestamp}] Step {step}: Running simulation...{parallel_status}"
    
    except Exception as e:
        return f"Status update error: {str(e)}"

# Keyboard shortcuts and additional interactions
app.clientside_callback(
    """
    function(n_intervals) {
        // Add keyboard shortcuts
        document.addEventListener('keydown', function(event) {
            if (event.ctrlKey) {
                switch(event.key) {
                    case 's':
                        event.preventDefault();
                        document.getElementById('step-button').click();
                        break;
                    case 'r':
                        event.preventDefault();
                        document.getElementById('run-button').click();
                        break;
                    case 'p':
                        event.preventDefault();
                        document.getElementById('pause-button').click();
                        break;
                    case 'e':
                        event.preventDefault();
                        document.getElementById('save-experiment').click();
                        break;
                }
            }
        });
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('simulation-state', 'data'),
    Input('simulation-interval', 'n_intervals')
)

# Run the app
if __name__ == '__main__':
    print("🚁 Starting Drone Optimization Simulation System...")
    print("📍 Open your browser to: http://127.0.0.1:8050")
    print("⌨️  Keyboard shortcuts:")
    print("   Ctrl+S: Step simulation")
    print("   Ctrl+R: Run continuous")
    print("   Ctrl+P: Pause simulation")
    print("   Ctrl+E: Save experiment")
    print("🔧 Features:")
    print("   ✅ Parallel Processing for GA and PSO")
    print("   ✅ Experiment Management and Export")
    print("   ✅ Advanced Algorithm Configuration")
    app.run_server(debug=True, host='127.0.0.1', port=8050)
    