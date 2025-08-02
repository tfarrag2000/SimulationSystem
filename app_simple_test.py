#!/usr/bin/env python3
"""
SIMPLE TEST VERSION OF DRONE OPTIMIZATION SYSTEM
Testing basic functionality to isolate callback issues
"""

import dash
from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="Drone Optimization Test"
)

# Simple layout for testing
app.layout = dbc.Container([
    html.H2("Simple Dash Test", className="text-center mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("Algorithm:"),
                    dcc.Dropdown(
                        id='algorithm-dropdown',
                        options=[
                            {'label': 'Greedy', 'value': 'greedy'},
                            {'label': 'GA', 'value': 'ga'},
                            {'label': 'PSO', 'value': 'pso'}
                        ],
                        value='greedy'
                    ),
                    html.Br(),
                    html.Label("Max Iterations:"),
                    dbc.Input(
                        id="max-iterations",
                        type="number",
                        value=500,
                        min=20, max=5000
                    ),
                    html.Br(),
                    dbc.Button("Test Run", id="run-btn", color="primary")
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dcc.Graph(id='test-graph')
        ], width=6)
    ]),
    
    html.Hr(),
    html.Div(id='test-output'),
    
    # Store for data
    dcc.Store(id='test-data')
], fluid=True)

# Simple callback test
@app.callback(
    Output('test-graph', 'figure'),
    Input('algorithm-dropdown', 'value')
)
def update_test_graph(algorithm):
    """Simple graph update callback"""
    try:
        x = np.linspace(0, 100, 50)
        if algorithm == 'greedy':
            y = 90 - 30 * np.exp(-x/20)
        elif algorithm == 'ga':
            y = 80 * (1 - np.exp(-x/25)) + np.random.normal(0, 2, 50)
        else:  # pso
            y = 85 * (1 - np.exp(-x/15)) + np.random.normal(0, 1.5, 50)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x, y=np.clip(y, 0, 100),
            mode='lines',
            name=algorithm.upper(),
            line=dict(width=2)
        ))
        
        fig.update_layout(
            title=f"Algorithm: {algorithm.upper()}",
            xaxis_title="Iteration",
            yaxis_title="Coverage (%)",
            template="plotly_white"
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error in test graph callback: {e}")
        # Return empty figure on error
        fig = go.Figure()
        fig.add_annotation(text=f"Error: {str(e)}", x=0.5, y=0.5, showarrow=False)
        return fig

# Test run callback
@app.callback(
    [Output('test-output', 'children'),
     Output('test-data', 'data')],
    Input('run-btn', 'n_clicks'),
    [State('algorithm-dropdown', 'value'),
     State('max-iterations', 'value')]
)
def test_run(n_clicks, algorithm, max_iterations):
    """Simple test run callback"""
    if not n_clicks:
        return "Click 'Test Run' to start", {}
    
    try:
        logger.info(f"Test run: {algorithm} with {max_iterations} iterations")
        
        # Simple simulation
        result = {
            'algorithm': algorithm,
            'max_iterations': max_iterations,
            'status': 'completed'
        }
        
        output = dbc.Alert([
            html.H5(f"Test Completed!"),
            html.P(f"Algorithm: {algorithm}"),
            html.P(f"Max Iterations: {max_iterations}"),
            html.P("✅ All callbacks working correctly")
        ], color="success")
        
        return output, result
        
    except Exception as e:
        logger.error(f"Error in test run callback: {e}")
        error_output = dbc.Alert([
            html.H5("Test Failed!"),
            html.P(f"Error: {str(e)}")
        ], color="danger")
        
        return error_output, {}

if __name__ == '__main__':
    logger.info("🧪 Starting Simple Dash Test")
    app.run_server(debug=True, host='127.0.0.1', port=8051)
