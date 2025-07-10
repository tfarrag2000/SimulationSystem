import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots

def create_simulation_view(simulation):
    """
    Create the main simulation visualization

    Args:
        simulation: DroneEnvironment instance

    Returns:
        plotly.graph_objs.Figure: The simulation visualization figure
    """
    fig = go.Figure()
    grid = simulation.grid_points
    drones = simulation.drones

    # Plot grid points
    fig.add_trace(go.Scatter(
        x=grid[:, 0], y=grid[:, 1],
        mode='markers',
        marker=dict(size=3, color='lightgray', opacity=0.6),
        name='Grid Points',
        showlegend=True
    ))

    # Collect drone data for batch plotting
    active_drones_x = []
    active_drones_y = []
    inactive_drones_x = []
    inactive_drones_y = []
    
    # Plot drones and sensing circles
    for i, drone in drones.iterrows():
        is_active = drone.get('active', 1) in [1, True]
        if is_active:
            active_drones_x.append(drone['x'])
            active_drones_y.append(drone['y'])
            
            # Draw sensing circle for active drones
            theta = np.linspace(0, 2 * np.pi, 100)
            circle_x = drone['x'] + simulation.sensing_radius * np.cos(theta)
            circle_y = drone['y'] + simulation.sensing_radius * np.sin(theta)
            fig.add_trace(go.Scatter(
                x=circle_x,
                y=circle_y,
                mode='lines',
                line=dict(color='rgba(0,128,0,0.5)', width=2, dash='dot'),
                fill='toself',
                fillcolor='rgba(0,255,0,0.1)',
                name='Sensing Area' if i == 0 else '',  # Only show legend for first circle
                showlegend=(i == 0),
                legendgroup='sensing'
            ))
        else:
            inactive_drones_x.append(drone['x'])
            inactive_drones_y.append(drone['y'])
    
    # Add active drones as a single trace
    if active_drones_x:
        fig.add_trace(go.Scatter(
            x=active_drones_x, y=active_drones_y,
            mode='markers',
            marker=dict(size=15, color='green', symbol='circle', 
                       line=dict(width=2, color='darkgreen')),
            name='Active Drones',
            showlegend=True
        ))
    
    # Add inactive drones as a single trace
    if inactive_drones_x:
        fig.add_trace(go.Scatter(
            x=inactive_drones_x, y=inactive_drones_y,
            mode='markers',
            marker=dict(size=12, color='gray', symbol='x',
                       line=dict(width=2, color='darkgray')),
            name='Inactive Drones',
            showlegend=True
        ))

    # Add parking spots and vehicles if this is a parking scenario
    if hasattr(simulation, 'is_parking_scenario') and simulation.is_parking_scenario:
        if hasattr(simulation, 'parking_spots') and simulation.parking_spots is not None and not simulation.parking_spots.empty:
            # Plot parking spots
            parking_spots = simulation.parking_spots
            disabled_spots = parking_spots[parking_spots['disabled'] == 1]
            enabled_spots = parking_spots[parking_spots['disabled'] == 0]
            
            # Add enabled parking spots
            if not enabled_spots.empty:
                fig.add_trace(go.Scatter(
                    x=enabled_spots['x'], y=enabled_spots['y'],
                    mode='markers',
                    marker=dict(size=8, color='lightblue', symbol='square',
                               line=dict(width=1, color='blue')),
                    name='Parking Spots',
                    showlegend=True
                ))
            
            # Add disabled parking spots
            if not disabled_spots.empty:
                fig.add_trace(go.Scatter(
                    x=disabled_spots['x'], y=disabled_spots['y'],
                    mode='markers',
                    marker=dict(size=8, color='red', symbol='square',
                               line=dict(width=1, color='darkred')),
                    name='Disabled Spots',
                    showlegend=True
                ))
        
        # Plot vehicles if they exist and have position data
        if (hasattr(simulation, 'vehicles') and simulation.vehicles is not None and 
            not simulation.vehicles.empty and 'x' in simulation.vehicles.columns and 'y' in simulation.vehicles.columns):
            fig.add_trace(go.Scatter(
                x=simulation.vehicles['x'], y=simulation.vehicles['y'],
                mode='markers',
                marker=dict(size=10, color='orange', symbol='diamond',
                           line=dict(width=1, color='darkorange')),
                name='Vehicles',
                showlegend=True
            ))

    # Add enhanced title with metrics and step info
    coverage = simulation.metrics_history.get('coverage', [0])[-1]
    active_nodes = simulation.metrics_history.get('active_drones', [0])[-1]
    total_drones = len(simulation.drones) if hasattr(simulation, 'drones') else 0
    step_count = simulation.step_count if hasattr(simulation, 'step_count') else 0
    
    # Calculate efficiency
    efficiency = (coverage * 100) / max(active_nodes, 1) if active_nodes > 0 else 0
    
    fig.update_layout(
        title={
            'text': f"🚁 Drone Network Optimization<br><sub>Step {step_count} | Coverage: {coverage * 100:.1f}% | Active: {active_nodes}/{total_drones} | Efficiency: {efficiency:.1f}%/drone</sub>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'family': 'Arial, sans-serif'}
        },
        xaxis_title="X Coordinate (m)",
        yaxis_title="Y Coordinate (m)",
        width=1200,
        height=600,
        showlegend=True,
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="rgba(0,0,0,0.1)",
            borderwidth=1,
            font=dict(size=11)
        ),
        template="plotly_white",
        margin=dict(t=80, b=40, l=60, r=40),
        plot_bgcolor='rgba(248,249,250,0.8)',
        paper_bgcolor='white'
    )
    return fig

def create_metrics_charts(simulation):
    """
    Create charts for performance metrics
    
    Args:
        simulation: DroneEnvironment instance
        
    Returns:
        dict: Dictionary of plotly figures for each metric
    """
    metrics = simulation.metrics_history
    steps = list(range(1, simulation.step_count + 1)) if simulation.step_count > 0 else [1]
    
    # Coverage chart
    coverage_fig = go.Figure()
    if metrics['coverage']:
        coverage_fig.add_trace(go.Scatter(
            x=steps,
            y=[c * 100 for c in metrics['coverage']],
            mode='lines+markers',
            name='Coverage %',
            line=dict(color='green', width=3),
            marker=dict(size=6)
        ))
        
        # Add trend line if enough data points
        if len(metrics['coverage']) > 2:
            z = np.polyfit(steps, [c * 100 for c in metrics['coverage']], 1)
            trend_line = np.poly1d(z)
            coverage_fig.add_trace(go.Scatter(
                x=steps,
                y=trend_line(steps),
                mode='lines',
                name='Trend',
                line=dict(color='darkgreen', dash='dash', width=2),
                opacity=0.7
            ))
    
    coverage_fig.update_layout(
        title="Area Coverage Over Time",
        xaxis_title="Simulation Step",
        yaxis_title="Coverage (%)",
        yaxis=dict(range=[0, 100]),
        showlegend=True,
        template="plotly_white"
    )
    
    # Power consumption chart
    power_fig = go.Figure()
    if metrics['power_consumption']:
        power_fig.add_trace(go.Scatter(
            x=steps,
            y=metrics['power_consumption'],
            mode='lines+markers',
            name='Power Consumption',
            line=dict(color='orange', width=2),
            marker=dict(size=6),
            fill='tonexty' if len(steps) > 1 else None,
            fillcolor='rgba(255,165,0,0.1)'
        ))
        
        # Add average line
        avg_power = np.mean(metrics['power_consumption'])
        power_fig.add_hline(
            y=avg_power,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Average: {avg_power:.1f}"
        )
    
    power_fig.update_layout(
        title="Power Consumption Over Time",
        xaxis_title="Simulation Step",
        yaxis_title="Power Units",
        template="plotly_white"
    )
    
    # Active drones chart
    active_fig = go.Figure()
    if metrics['active_drones']:
        active_fig.add_trace(go.Scatter(
            x=steps,
            y=metrics['active_drones'],
            mode='lines+markers',
            name='Active Drones',
            line=dict(color='blue', width=2),
            marker=dict(size=6)
        ))
        
        # Add efficiency indicator (coverage per active drone)
        if metrics['coverage']:
            efficiency = [c * 100 / max(a, 1) for c, a in zip(metrics['coverage'], metrics['active_drones'])]
            active_fig.add_trace(go.Scatter(
                x=steps,
                y=efficiency,
                mode='lines',
                name='Coverage per Drone',
                line=dict(color='lightblue', dash='dot'),
                yaxis='y2'
            ))
    
    active_fig.update_layout(
        title="Active Drones Over Time",
        xaxis_title="Simulation Step",
        yaxis_title="Number of Drones",
        yaxis2=dict(title="Coverage per Drone (%)", overlaying='y', side='right'),
        template="plotly_white"
    )
    
    # Overlap chart
    overlap_fig = go.Figure()
    if metrics['avg_overlap']:
        overlap_fig.add_trace(go.Scatter(
            x=steps,
            y=metrics['avg_overlap'],
            mode='lines+markers',
            name='Average Overlap',
            line=dict(color='red', width=2),
            marker=dict(size=6)
        ))
        
        # Add target overlap line (ideal would be close to 1.0)
        overlap_fig.add_hline(
            y=1.0,
            line_dash="dash",
            line_color="green",
            annotation_text="Ideal (1.0)"
        )
    
    overlap_fig.update_layout(
        title="Sensor Overlap Over Time",
        xaxis_title="Simulation Step",
        yaxis_title="Average Overlap Factor",
        template="plotly_white"
    )
    
    # Violations chart (if applicable)
    violations_fig = None
    if 'violations' in metrics and hasattr(simulation, 'is_parking_scenario') and simulation.is_parking_scenario:
        violations_fig = go.Figure()
        if metrics['violations']:
            # Cumulative violations
            cumulative_violations = np.cumsum(metrics['violations'])
            
            violations_fig.add_trace(go.Bar(
                x=steps,
                y=metrics['violations'],
                name='Violations per Step',
                marker_color='crimson',
                opacity=0.7
            ))
            
            violations_fig.add_trace(go.Scatter(
                x=steps,
                y=cumulative_violations,
                mode='lines+markers',
                name='Cumulative Violations',
                line=dict(color='darkred', width=3),
                yaxis='y2'
            ))
        
        violations_fig.update_layout(
            title="Parking Violations Over Time",
            xaxis_title="Simulation Step",
            yaxis_title="Violations per Step",
            yaxis2=dict(title="Total Violations", overlaying='y', side='right'),
            template="plotly_white"
        )
    
    return {
        'coverage': coverage_fig,
        'power': power_fig,
        'active': active_fig,
        'overlap': overlap_fig,
        'violations': violations_fig
    }

def create_algorithm_comparison_chart(results_dict):
    """
    Create a comparison chart for different algorithms
    
    Args:
        results_dict: Dictionary with algorithm names as keys and metrics as values
        
    Returns:
        plotly.graph_objs.Figure: Comparison chart
    """
    if not results_dict:
        fig = go.Figure()
        fig.update_layout(title="No Data Available for Comparison")
        return fig
    
    algorithms = list(results_dict.keys())
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Coverage Comparison', 'Active Drones', 'Execution Time', 'Efficiency'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Extract metrics
    coverage_scores = [results_dict[algo].get('coverage', 0) * 100 for algo in algorithms]
    active_nodes = [results_dict[algo].get('active_drones', 0) for algo in algorithms]
    execution_times = [results_dict[algo].get('execution_time', 0) for algo in algorithms]
    
    # Calculate efficiency (coverage per active drone)
    efficiency_scores = [c/max(a, 1) for c, a in zip(coverage_scores, active_nodes)]
    
    # Coverage comparison
    fig.add_trace(
        go.Bar(x=algorithms, y=coverage_scores, name='Coverage %', 
               marker_color='green', showlegend=False),
        row=1, col=1
    )
    
    # Active drones
    fig.add_trace(
        go.Bar(x=algorithms, y=active_nodes, name='Active Drones', 
               marker_color='blue', showlegend=False),
        row=1, col=2
    )
    
    # Execution time
    fig.add_trace(
        go.Bar(x=algorithms, y=execution_times, name='Time (s)', 
               marker_color='orange', showlegend=False),
        row=2, col=1
    )
    
    # Efficiency
    fig.add_trace(
        go.Bar(x=algorithms, y=efficiency_scores, name='Coverage/Drone', 
               marker_color='purple', showlegend=False),
        row=2, col=2
    )
    
    fig.update_layout(
        title="Algorithm Performance Comparison",
        height=600,
        template="plotly_white"
    )
    
    return fig

def create_heatmap(simulation):
    """
    Create a coverage heatmap
    
    Args:
        simulation: DroneEnvironment instance
        
    Returns:
        plotly.graph_objs.Figure: Heatmap figure
    """
    # Create a grid for the heatmap
    grid_size = max(int(simulation.width / 10), int(simulation.height / 10), 10)
    x = np.linspace(0, simulation.width, grid_size)
    y = np.linspace(0, simulation.height, grid_size)
    xx, yy = np.meshgrid(x, y)
    
    # Calculate coverage at each grid point
    grid_points = np.column_stack([xx.ravel(), yy.ravel()])
    coverage = np.zeros(len(grid_points))
    
    active_drones = simulation.drones[simulation.drones['active'] == 1]
    for _, drone in active_drones.iterrows():
        drone_pos = np.array([drone['x'], drone['y']])
        distances = np.linalg.norm(grid_points - drone_pos, axis=1)
        coverage += (distances <= simulation.sensing_radius).astype(int)
    
    # Reshape for heatmap
    coverage_grid = coverage.reshape(grid_size, grid_size)
    
    # Create heatmap
    fig = px.imshow(
        coverage_grid,
        labels=dict(x="X Coordinate", y="Y Coordinate", color="Coverage Level"),
        x=x,
        y=y,
        color_continuous_scale="Viridis",
        aspect="equal"
    )
    
    # Add drone positions as overlays
    for _, drone in active_drones.iterrows():
        fig.add_trace(go.Scatter(
            x=[drone['x']],
            y=[drone['y']],
            mode='markers',
            marker=dict(size=10, color='red', symbol='x', line=dict(width=2, color='white')),
            name=f"Drone {drone['id']}",
            showlegend=False
        ))
    
    fig.update_layout(
        title="Coverage Intensity Heatmap",
        xaxis_title="X Coordinate (m)",
        yaxis_title="Y Coordinate (m)",
        template="plotly_white"
    )
    
    return fig

def create_energy_distribution_chart(simulation):
    """
    Create energy distribution chart for all drones
    
    Args:
        simulation: DroneEnvironment instance
        
    Returns:
        plotly.graph_objs.Figure: Energy distribution chart
    """
    energy_levels = simulation.drones['energy'].values
    
    fig = go.Figure()
    
    # Histogram of energy levels
    fig.add_trace(go.Histogram(
        x=energy_levels,
        nbinsx=20,
        name='Energy Distribution',
        marker_color='lightblue',
        opacity=0.7
    ))
    
    # Add average line
    avg_energy = np.mean(energy_levels)
    fig.add_vline(
        x=avg_energy,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Average: {avg_energy:.1f}%"
    )
    
    # Add critical energy line
    fig.add_vline(
        x=20,
        line_dash="dot",
        line_color="orange",
        annotation_text="Low Energy Threshold"
    )
    
    fig.update_layout(
        title="Drone Energy Distribution",
        xaxis_title="Energy Level (%)",
        yaxis_title="Number of Drones",
        template="plotly_white"
    )
    
    return fig


def create_coverage_efficiency_scatter(simulation_results):
    """
    Create scatter plot of coverage vs efficiency for multiple simulations
    
    Args:
        simulation_results: List of simulation result dictionaries
        
    Returns:
        plotly.graph_objs.Figure: Scatter plot
    """
    if not simulation_results:
        fig = go.Figure()
        fig.update_layout(title="No Data Available")
        return fig
    
    coverage_values = []
    efficiency_values = []
    algorithm_names = []
    colors = []
    
    color_map = {
        'greedy': 'red',
        'genetic_algorithm': 'blue',
        'particle_swarm_optimization': 'green',
        'simulated_annealing': 'purple',
        'genetic_algorithm_sa': 'orange'
    }
    
    for result in simulation_results:
        coverage = result.get('coverage', 0)
        active_drones = result.get('active_drones', 1)
        algorithm = result.get('algorithm', 'unknown')
        
        efficiency = coverage / max(active_drones, 1)
        
        coverage_values.append(coverage)
        efficiency_values.append(efficiency)
        algorithm_names.append(algorithm)
        colors.append(color_map.get(algorithm, 'gray'))
    
    fig = go.Figure()
    
    # Group by algorithm
    for algorithm in set(algorithm_names):
        mask = [alg == algorithm for alg in algorithm_names]
        fig.add_trace(go.Scatter(
            x=[coverage_values[i] for i in range(len(mask)) if mask[i]],
            y=[efficiency_values[i] for i in range(len(mask)) if mask[i]],
            mode='markers',
            name=algorithm,
            marker=dict(size=10, color=color_map.get(algorithm, 'gray')),
            hovertemplate=f"<b>{algorithm}</b><br>Coverage: %{{x:.1f}}%<br>Efficiency: %{{y:.2f}}<extra></extra>"
        ))
    
    fig.update_layout(
        title="Coverage vs Efficiency Analysis",
        xaxis_title="Coverage (%)",
        yaxis_title="Efficiency (Coverage per Active Drone)",
        template="plotly_white",
        hovermode='closest'
    )
    
    return fig