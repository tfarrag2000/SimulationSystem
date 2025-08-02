#!/usr/bin/env python3
"""
DRONE OPTIMIZATION SIMULATION SYSTEM - CLEAN VERSION
Version: 2.3.1
"""

# Version information
__version__ = "2.3.1"
__author__ = "Drone Optimization System"
__last_updated__ = "2025-08-02"
__description__ = "Clean Drone Optimization Simulation System"

import dash
from dash import dcc, html, Input, Output, State, ctx, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from datetime import datetime
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Algorithm configurations
ALGORITHM_CONFIGS = {
    'greedy': {
        'name': 'Greedy Algorithm',
        'description': 'Fast heuristic algorithm',
        'params': {
            'coverage_target': {'default': 0.95, 'min': 0.5, 'max': 1.0, 'step': 0.01}
        }
    },
    'ga': {
        'name': 'Genetic Algorithm',
        'description': 'Evolution-inspired optimization',
        'params': {
            'population_size': {'default': 50, 'min': 20, 'max': 200, 'step': 10}
        }
    },
    'pso': {
        'name': 'Particle Swarm Optimization',
        'description': 'Swarm intelligence optimization',
        'params': {
            'swarm_size': {'default': 40, 'min': 20, 'max': 100, 'step': 10}
        }
    }
}

# Main App Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H2([
                html.I(className="fas fa-drone me-3 text-primary"),
                "Drone Optimization System"
            ], className="text-center mb-4 fw-bold")
        ])
    ]),
    
    # Main Content
    dbc.Row([
        # Left Panel - Configuration
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H6("Configuration", className="mb-0 fw-bold")
                ]),
                dbc.CardBody([
                    # Algorithm Selection
                    html.Div([
                        html.Label("Algorithm:", className="form-label fw-bold"),
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
                        html.Label("Environment:", className="form-label fw-bold"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Input(
                                    id="grid-width",
                                    type="number",
                                    value=50,
                                    min=10, max=316, step=5,
                                    placeholder="Width"
                                ),
                                html.Small("Grid Width", className="text-muted")
                            ], width=6),
                            dbc.Col([
                                dbc.Input(
                                    id="grid-height",
                                    type="number",
                                    value=50,
                                    min=10, max=316, step=5,
                                    placeholder="Height"
                                ),
                                html.Small("Grid Height", className="text-muted")
                            ], width=6)
                        ], className="mb-3")
                    ]),
                    
                    # Stopping Criteria
                    html.Div([
                        html.Label("Stopping Criteria:", className="form-label fw-bold"),
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
                                html.Small("Max Iterations", className="text-muted")
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
                                html.Small("Target Coverage (%)", className="text-muted")
                            ], width=6)
                        ], className="mb-3")
                    ]),
                    
                    # Controls
                    dbc.ButtonGroup([
                        dbc.Button("Run", id="run-btn", color="success"),
                        dbc.Button("Reset", id="reset-btn", color="secondary")
                    ], className="w-100")
                ])
            ])
        ], width=4),
        
        # Right Panel - Results
        dbc.Col([
            # Graph
            dbc.Card([
                dbc.CardHeader([
                    html.H6("Optimization Progress", className="mb-0 fw-bold")
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id='main-graph',
                        style={"height": "400px"}
                    )
                ])
            ], className="mb-4"),
            
            # Results
            dbc.Card([
                dbc.CardHeader([
                    html.H6("Results", className="mb-0 fw-bold")
                ]),
                dbc.CardBody([
                    html.Div(id='results-output')
                ])
            ])
        ], width=8)
    ]),
    
    # Data Storage
    dcc.Store(id='simulation-data'),
    dcc.Store(id='current-state', data={'status': 'ready'})
    
], fluid=True, className="py-3")

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
        
        # Generate sample data
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

# Run Algorithm Callback
@app.callback(
    [Output('simulation-data', 'data'),
     Output('current-state', 'data')],
    [Input('run-btn', 'n_clicks'),
     Input('reset-btn', 'n_clicks')],
    [State('algorithm-dropdown', 'value'),
     State('grid-width', 'value'),
     State('grid-height', 'value'),
     State('max-iterations', 'value'),
     State('target-coverage', 'value'),
     State('current-state', 'data')]
)
def control_simulation(run_clicks, reset_clicks, 
                      algorithm, width, height, max_iterations, target_coverage, current_state):
    
    ctx_triggered = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    if ctx_triggered == 'run-btn' and run_clicks:
        logger.info(f"Starting {algorithm} optimization...")
        logger.info(f"Parameters: max_iterations={max_iterations}, target_coverage={target_coverage}")
        
        if not algorithm:
            return {}, {'status': 'error', 'message': 'No algorithm selected'}
        
        # Validate input parameters
        if not all([width, height, max_iterations, target_coverage]):
            return {}, {'status': 'error', 'message': 'Please fill in all parameters'}
        
        try:
            start_time = time.time()
            
            # Use time-based random seed for realistic variation
            random_seed = int(time.time() * 1000000) % 2147483647
            np.random.seed(random_seed)
            logger.info(f"Using random seed: {random_seed}")
            
            # Use user-defined stopping criteria
            max_iter = int(max_iterations) if max_iterations else 500
            target_cov = float(target_coverage) if target_coverage else 85.0
            
            logger.info(f"Running for maximum {max_iter} iterations, target {target_cov}% coverage")
            
            # Simulate algorithm execution
            coverage_history = []
            
            # Algorithm-specific parameters
            if algorithm == 'greedy':
                base_coverage = 60
                convergence_rate = 0.15
            elif algorithm == 'ga':
                base_coverage = 65
                convergence_rate = 0.12
            else:  # pso
                base_coverage = 70
                convergence_rate = 0.18
            
            # Run simulation
            for i in range(max_iter):
                # Calculate progress
                progress = i / max_iter
                
                # Generate realistic coverage with time-varying randomness
                base_random = np.random.normal(0, 1) * (0.5 + 0.5 * np.cos(i * 0.1))
                
                if algorithm == 'greedy':
                    coverage = base_coverage * (1 - np.exp(-progress * 6)) + base_random * 3 * (1 - progress * 0.8)
                elif algorithm == 'ga':
                    coverage = base_coverage * (1 - np.exp(-progress * 3.5)) + base_random * 4 * (1 - progress * 0.6)
                else:  # pso
                    coverage = base_coverage * (1 - np.exp(-progress * 5)) + base_random * 2.5 * (1 - progress * 0.9)
                
                coverage = max(10, min(98, coverage))
                coverage_history.append(coverage)
                
                # Check stopping criteria
                if coverage >= target_cov:
                    logger.info(f"Target coverage achieved: {coverage:.1f}% >= {target_cov}%")
                    break
                
                # Check for convergence (simplified)
                if i > 20:
                    recent_improvement = np.mean(coverage_history[-3:]) - np.mean(coverage_history[-6:-3])
                    if abs(recent_improvement) < 0.1 and i > 50:
                        logger.info(f"Algorithm converged at iteration {i}")
                        break
            
            execution_time = time.time() - start_time
            actual_iterations = len(coverage_history)
            final_coverage = coverage_history[-1]
            
            logger.info(f"Completed: {actual_iterations} iterations, {final_coverage:.1f}% coverage")
            
            # Generate result data
            result_data = {
                'algorithm': algorithm,
                'algorithm_name': ALGORITHM_CONFIGS[algorithm]['name'],
                'coverage_history': coverage_history,
                'final_coverage': final_coverage,
                'iterations': actual_iterations,
                'max_iterations': max_iter,
                'target_coverage': target_cov,
                'execution_time': execution_time,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return result_data, {'status': 'completed', 'message': f'{ALGORITHM_CONFIGS[algorithm]["name"]} completed successfully'}
            
        except Exception as e:
            logger.error(f"Algorithm execution failed: {e}")
            return {}, {'status': 'error', 'message': str(e)}
    
    elif ctx_triggered == 'reset-btn' and reset_clicks:
        return {}, {'status': 'ready', 'message': 'System reset'}
    
    return {}, current_state or {'status': 'ready'}

# Results Display Callback
@app.callback(
    Output('results-output', 'children'),
    Input('simulation-data', 'data')
)
def update_results(simulation_data):
    if not simulation_data:
        return dbc.Alert("Run an algorithm to see results", color="info")
    
    if 'final_coverage' not in simulation_data:
        return dbc.Alert("No results available", color="warning")
    
    # Create results summary
    results = [
        html.H5("Results Summary", className="mb-3"),
        html.P(f"Algorithm: {simulation_data.get('algorithm_name', 'Unknown')}"),
        html.P(f"Final Coverage: {simulation_data.get('final_coverage', 0):.1f}%"),
        html.P(f"Iterations: {simulation_data.get('iterations', 0)}/{simulation_data.get('max_iterations', 0)}"),
        html.P(f"Execution Time: {simulation_data.get('execution_time', 0):.2f} seconds"),
        html.P(f"Target Coverage: {simulation_data.get('target_coverage', 0)}%"),
        html.Hr(),
        html.P(f"Completed: {simulation_data.get('timestamp', 'Unknown')}", className="text-muted")
    ]
    
    return html.Div(results)

if __name__ == '__main__':
    logger.info("Starting Clean Drone Optimization System")
    app.run_server(debug=True, host='127.0.0.1', port=8050)
