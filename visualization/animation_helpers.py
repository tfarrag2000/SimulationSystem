import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import time
from datetime import datetime

class SimulationAnimator:
    """
    Complete class for creating animated visualizations of drone simulations
    """
    
    def __init__(self, simulation_history):
        """
        Initialize animator with simulation history
        
        Args:
            simulation_history: List of simulation states over time
        """
        self.simulation_history = simulation_history
        self.frames = []
        self.current_frame = 0
    
    def create_animated_simulation(self, show_trails=True, trail_length=5):
        """
        Create animated simulation showing drone movement and coverage evolution
        
        Args:
            show_trails: Whether to show drone movement trails
            trail_length: Length of trails to show
            
        Returns:
            plotly.graph_objs.Figure: Animated figure
        """
        if not self.simulation_history:
            return go.Figure().update_layout(title="No simulation history available")
        
        frames = []
        
        for step, sim_state in enumerate(self.simulation_history):
            frame_data = []
            
            # Grid points (static)
            frame_data.append(go.Scatter(
                x=sim_state.grid_points[:, 0],
                y=sim_state.grid_points[:, 1],
                mode='markers',
                marker=dict(size=2, color='lightgray', opacity=0.3),
                name='Grid Points',
                showlegend=(step == 0)
            ))
            
            # Active drones
            active_drones = sim_state.drones[sim_state.drones['active'] == 1]
            if not active_drones.empty:
                frame_data.append(go.Scatter(
                    x=active_drones['x'],
                    y=active_drones['y'],
                    mode='markers',
                    marker=dict(
                        size=12,
                        color=active_drones['energy'],
                        colorscale='RdYlGn',
                        cmin=0, cmax=100,
                        symbol='triangle-up',
                        line=dict(width=2, color='darkgreen')
                    ),
                    name='Active Drones',
                    showlegend=(step == 0),
                    text=[f"Drone {row['id']}<br>Energy: {row['energy']:.1f}%" 
                          for _, row in active_drones.iterrows()],
                    hovertemplate="<b>%{text}</b><br>Step: " + str(step) + "<extra></extra>"
                ))
            
            # Inactive drones
            inactive_drones = sim_state.drones[sim_state.drones['active'] == 0]
            if not inactive_drones.empty:
                frame_data.append(go.Scatter(
                    x=inactive_drones['x'],
                    y=inactive_drones['y'],
                    mode='markers',
                    marker=dict(size=8, color='red', symbol='circle'),
                    name='Inactive Drones',
                    showlegend=(step == 0)
                ))
            
            # Add trails if requested
            if show_trails and step > 0:
                trail_start = max(0, step - trail_length)
                for drone_id in range(len(sim_state.drones)):
                    trail_x = []
                    trail_y = []
                    
                    for trail_step in range(trail_start, step + 1):
                        if trail_step < len(self.simulation_history):
                            hist_state = self.simulation_history[trail_step]
                            if drone_id < len(hist_state.drones):
                                trail_x.append(hist_state.drones.iloc[drone_id]['x'])
                                trail_y.append(hist_state.drones.iloc[drone_id]['y'])
                    
                    if len(trail_x) > 1:
                        frame_data.append(go.Scatter(
                            x=trail_x,
                            y=trail_y,
                            mode='lines',
                            line=dict(color='blue', width=1, dash='dot'),
                            opacity=0.5,
                            name=f'Trail {drone_id}',
                            showlegend=False,
                            hoverinfo='skip'
                        ))
            
            frames.append(go.Frame(
                data=frame_data,
                name=str(step),
                layout=go.Layout(
                    title=f"Simulation Animation - Step {step}",
                    annotations=[
                        dict(
                            text=f"Step: {step}<br>Coverage: {sim_state.metrics_history['coverage'][-1]*100:.1f}%<br>Active: {sim_state.metrics_history['active_drones'][-1]}",
                            xref="paper", yref="paper",
                            x=0.02, y=0.98, xanchor="left", yanchor="top",
                            showarrow=False,
                            bgcolor="rgba(255,255,255,0.8)",
                            bordercolor="black", borderwidth=1
                        )
                    ]
                )
            ))
        
        # Create initial figure
        first_state = self.simulation_history[0]
        fig = go.Figure(
            data=frames[0].data if frames else [],
            frames=frames
        )
        
        # Add play controls
        fig.update_layout(
            title="🎬 Drone Simulation Animation",
            xaxis=dict(range=[0, first_state.width], title="X Coordinate (m)"),
            yaxis=dict(range=[0, first_state.height], title="Y Coordinate (m)"),
            updatemenus=[{
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 500, "redraw": True},
                                   "fromcurrent": True, "transition": {"duration": 200}}],
                    "label": "▶ Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                     "mode": "immediate", "transition": {"duration": 0}}],
                    "label": "⏸ Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1, "y": 0
        }],
        sliders=[{
            "active": 0,
            "currentvalue": {"prefix": "Step: "},
            "pad": {"t": 50},
            "steps": [
                {
                    "args": [[str(k)], {"frame": {"duration": 200, "redraw": True}}],
                    "label": str(k),
                    "method": "animate"
                }
                for k in range(len(frames))
            ]
        }]
    )
    
        return fig

def create_algorithm_convergence_animation(algorithm_results_history):
    """
    Create animated visualization of algorithm convergence
    
    Args:
        algorithm_results_history: List of algorithm results over iterations
        
    Returns:
        plotly.graph_objs.Figure: Animated convergence plot
    """
    if not algorithm_results_history:
        return go.Figure().update_layout(title="No algorithm history available")
    
    frames = []
    max_iterations = len(algorithm_results_history)
    
    for iteration in range(1, max_iterations + 1):
        # Get fitness history up to this iteration
        fitness_values = []
        for i in range(iteration):
            if hasattr(algorithm_results_history[i], 'fitness_history'):
                if algorithm_results_history[i].fitness_history:
                    fitness_values.append(algorithm_results_history[i].fitness_history[-1])
                else:
                    fitness_values.append(0)
            else:
                fitness_values.append(0)
        
        frame_data = [
            go.Scatter(
                x=list(range(1, len(fitness_values) + 1)),
                y=fitness_values,
                mode='lines+markers',
                name='Fitness Evolution',
                line=dict(color='blue', width=2),
                marker=dict(size=6)
            )
        ]
        
        # Add best fitness indicator
        if fitness_values:
            best_fitness = max(fitness_values)
            best_iteration = fitness_values.index(best_fitness) + 1
            
            frame_data.append(go.Scatter(
                x=[best_iteration],
                y=[best_fitness],
                mode='markers',
                marker=dict(size=12, color='red', symbol='star'),
                name='Best Fitness',
                showlegend=(iteration == 1)
            ))
        
        frames.append(go.Frame(
            data=frame_data,
            name=str(iteration),
            layout=go.Layout(
                title=f"Algorithm Convergence - Iteration {iteration}",
                annotations=[
                    dict(
                        text=f"Iteration: {iteration}<br>Current Fitness: {fitness_values[-1] if fitness_values else 0:.3f}<br>Best Fitness: {max(fitness_values) if fitness_values else 0:.3f}",
                        xref="paper", yref="paper",
                        x=0.98, y=0.98, xanchor="right", yanchor="top",
                        showarrow=False,
                        bgcolor="rgba(255,255,255,0.8)",
                        bordercolor="black", borderwidth=1
                    )
                ]
            )
        ))
    
    # Create initial figure
    fig = go.Figure(
        data=frames[0].data if frames else [],
        frames=frames
    )
    
    fig.update_layout(
        title="🎯 Algorithm Convergence Animation",
        xaxis_title="Iteration",
        yaxis_title="Fitness Score",
        updatemenus=[{
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 300, "redraw": True}}],
                    "label": "▶ Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True}}],
                    "label": "⏸ Pause",
                    "method": "animate"
                }
            ],
            "type": "buttons",
            "x": 0.1, "y": 0
        }],
        sliders=[{
            "active": 0,
            "currentvalue": {"prefix": "Iteration: "},
            "steps": [
                {
                    "args": [[str(k)], {"frame": {"duration": 200}}],
                    "label": str(k),
                    "method": "animate"
                }
                for k in range(1, len(frames) + 1)
            ]
        }]
    )
    
    return fig

def create_energy_evolution_animation(simulation_history):
    """
    Create animated visualization of drone energy levels over time
    
    Args:
        simulation_history: List of simulation states
        
    Returns:
        plotly.graph_objs.Figure: Animated energy chart
    """
    if not simulation_history:
        return go.Figure().update_layout(title="No simulation history available")
    
    frames = []
    num_drones = len(simulation_history[0].drones)
    drone_ids = list(range(num_drones))
    
    for step, sim_state in enumerate(simulation_history):
        energy_levels = sim_state.drones['energy'].values
        active_status = sim_state.drones['active'].values
        
        # Color code by activity status
        colors = ['green' if active else 'red' for active in active_status]
        
        frame_data = [
            go.Bar(
                x=drone_ids,
                y=energy_levels,
                marker_color=colors,
                name='Energy Levels',
                text=[f"{'Active' if active else 'Inactive'}" for active in active_status],
                textposition='auto'
            )
        ]
        
        # Add energy threshold lines
        frame_data.extend([
            go.Scatter(
                x=[0, num_drones-1],
                y=[20, 20],
                mode='lines',
                line=dict(color='orange', dash='dash'),
                name='Low Energy Threshold',
                showlegend=(step == 0)
            ),
            go.Scatter(
                x=[0, num_drones-1],
                y=[50, 50],
                mode='lines',
                line=dict(color='yellow', dash='dot'),
                name='Medium Energy Threshold',
                showlegend=(step == 0)
            )
        ])
        
        frames.append(go.Frame(
            data=frame_data,
            name=str(step),
            layout=go.Layout(
                title=f"Drone Energy Evolution - Step {step}",
                annotations=[
                    dict(
                        text=f"Step: {step}<br>Avg Energy: {np.mean(energy_levels):.1f}%<br>Active Drones: {np.sum(active_status)}",
                        xref="paper", yref="paper",
                        x=0.98, y=0.98, xanchor="right", yanchor="top",
                        showarrow=False,
                        bgcolor="rgba(255,255,255,0.8)"
                    )
                ]
            )
        ))
    
    # Create initial figure
    fig = go.Figure(
        data=frames[0].data if frames else [],
        frames=frames
    )
    
    fig.update_layout(
        title="🔋 Drone Energy Evolution Animation",
        xaxis_title="Drone ID",
        yaxis_title="Energy Level (%)",
        yaxis=dict(range=[0, 100]),
        updatemenus=[{
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 800, "redraw": True}}],
                    "label": "▶ Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True}}],
                    "label": "⏸ Pause",
                    "method": "animate"
                }
            ],
            "type": "buttons"
        }],
        sliders=[{
            "active": 0,
            "currentvalue": {"prefix": "Step: "},
            "steps": [
                {
                    "args": [[str(k)]],
                    "label": str(k),
                    "method": "animate"
                }
                for k in range(len(frames))
            ]
        }]
    )
    
    return fig

def export_animation(fig, filename, format='html', width=800, height=600):
    """
    Export animation to file
    
    Args:
        fig: Plotly figure with animation
        filename: Output filename
        format: Export format ('html', 'gif', 'mp4')
        width: Animation width
        height: Animation height
        
    Returns:
        str: Path to exported file
    """
    try:
        if format == 'html':
            fig.write_html(
                filename,
                include_plotlyjs='cdn',
                config={'displayModeBar': True, 'displaylogo': False}
            )
        elif format == 'gif':
            # Note: Requires kaleido package
            fig.write_image(filename, format='gif', width=width, height=height)
        elif format == 'mp4':
            # Note: Requires additional video processing libraries
            # This is a placeholder - actual implementation would need ffmpeg
            raise NotImplementedError("MP4 export requires additional setup")
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return filename
        
    except Exception as e:
        raise Exception(f"Failed to export animation: {str(e)}")

def create_coverage_evolution_animation(simulation_history):
    """
    Create animated visualization of coverage evolution over time
    
    Args:
        simulation_history: List of simulation states
        
    Returns:
        plotly.graph_objs.Figure: Animated coverage heatmap
    """
    if not simulation_history:
        return go.Figure().update_layout(title="No simulation history available")
    
    frames = []
    first_state = simulation_history[0]
    
    # Create coverage grid
    grid_size = 20
    x = np.linspace(0, first_state.width, grid_size)
    y = np.linspace(0, first_state.height, grid_size)
    xx, yy = np.meshgrid(x, y)
    grid_points = np.column_stack([xx.ravel(), yy.ravel()])
    
    for step, sim_state in enumerate(simulation_history):
        # Calculate coverage at each grid point
        coverage = np.zeros(len(grid_points))
        active_drones = sim_state.drones[sim_state.drones['active'] == 1]
        
        for _, drone in active_drones.iterrows():
            drone_pos = np.array([drone['x'], drone['y']])
            distances = np.linalg.norm(grid_points - drone_pos, axis=1)
            coverage += (distances <= sim_state.sensing_radius).astype(int)
        
        # Reshape for heatmap
        coverage_grid = coverage.reshape(grid_size, grid_size)
        
        frames.append(go.Frame(
            data=[go.Heatmap(
                z=coverage_grid,
                x=x, y=y,
                colorscale='Viridis',
                showscale=True,
                zmin=0, zmax=3  # Max expected overlap
            )],
            name=str(step),
            layout=go.Layout(
                title=f"Coverage Evolution - Step {step}",
                annotations=[
                    dict(
                        text=f"Step: {step}<br>Total Coverage: {sim_state.metrics_history['coverage'][-1]*100:.1f}%",
                        xref="paper", yref="paper",
                        x=0.02, y=0.98, xanchor="left", yanchor="top",
                        showarrow=False,
                        bgcolor="rgba(255,255,255,0.8)"
                    )
                ]
            )
        ))
    
    # Create initial figure
    fig = go.Figure(
        data=frames[0].data if frames else [],
        frames=frames
    )
    
    fig.update_layout(
        title="📈 Coverage Evolution Animation",
        xaxis_title="X Coordinate (m)",
        yaxis_title="Y Coordinate (m)",
        updatemenus=[{
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 500, "redraw": True}}],
                    "label": "▶ Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True}}],
                    "label": "⏸ Pause",
                    "method": "animate"
                }
            ],
            "type": "buttons"
        }]
    )
    
    return fig