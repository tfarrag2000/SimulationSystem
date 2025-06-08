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
    
    # Add grid points
    fig.add_trace(go.Scatter(
        x=simulation.grid_points[:, 0],
        y=simulation.grid_points[:, 1],
        mode='markers',
        marker=dict(size=3, color='lightgray', opacity=0.3),
        name='Grid Points',
        hoverinfo='skip'
    ))
    
    # Add drones - active and inactive
    active_drones = simulation.drones[simulation.drones['active'] == 1]
    inactive_drones = simulation.drones[simulation.drones['active'] == 0]
    
    # Active drones
    fig.add_trace(go.Scatter(
        x=active_drones['x'],
        y=active_drones['y'],
        mode='markers',
        marker=dict(
            size=12, 
            color='green',
            symbol='triangle-up',
            line=dict(width=2, color='darkgreen')
        ),
        name='Active Drones',
        text=[f"Drone {row['id']}<br>Energy: {row['energy']:.1f}%" 
              for _, row in active_drones.iterrows()],
        hovertemplate="<b>%{text}</b><br>Position: (%{x:.1f}, %{y:.1f})<extra></extra>"
    ))
    
    # Inactive drones
    fig.add_trace(go.Scatter(
        x=inactive_drones['x'],
        y=inactive_drones['y'],
        mode='markers',
        marker=dict(
            size=10, 
            color='red',
            symbol='triangle-down',
            line=dict(width=1, color='darkred')
        ),
        name='Inactive Drones',
        text=[f"Drone {row['id']}<br>Energy: {row['energy']:.1f}%" 
              for _, row in inactive_drones.iterrows()],
        hovertemplate="<b>%{text}</b><br>Position: (%{x:.1f}, %{y:.1f})<extra></extra>"
    ))
    
    # Add coverage circles for active drones
    for _, drone in active_drones.iterrows():
        fig.add_shape(
            type="circle",
            xref="x", yref="y",
            x0=drone['x'] - simulation.sensing_radius,
            y0=drone['y'] - simulation.sensing_radius,
            x1=drone['x'] + simulation.sensing_radius,
            y1=drone['y'] + simulation.sensing_radius,
            line_color="green",
            line_width=1,
            fillcolor="rgba(0,255,0,0.1)"
        )
    
    # Add parking spots if this is a parking scenario
    if hasattr(simulation, 'is_parking_scenario') and simulation.is_parking_scenario:
        # Regular parking spots
        regular_spots = simulation.parking_spots[simulation.parking_spots['disabled'] == 0]
        if not regular_spots.empty:
            fig.add_trace(go.Scatter(
                x=regular_spots['x'],
                y=regular_spots['y'],
                mode='markers',
                marker=dict(size=8, color='blue', symbol='square'),
                name='Regular Parking',
                hovertemplate="Regular Parking Spot<br>Position: (%{x:.1f}, %{y:.1f})<extra></extra>"
            ))
        
        # Disabled parking spots
        disabled_spots = simulation.parking_spots[simulation.parking_spots['disabled'] == 1]
        if not disabled_spots.empty:
            fig.add_trace(go.Scatter(
                x=disabled_spots['x'],
                y=disabled_spots['y'],
                mode='markers',
                marker=dict(size=8, color='purple', symbol='square'),
                name='Disabled Parking',
                hovertemplate="Disabled Parking Spot<br>Position: (%{x:.1f}, %{y:.1f})<extra></extra>"
            ))
        
        # Parked vehicles
        occupied_spots = simulation.parking_spots[simulation.parking_spots['occupied'] == 1]
        if not occupied_spots.empty:
            fig.add_trace(go.Scatter(
                x=occupied_spots['x'],
                y=occupied_spots['y'],
                mode='markers',
                marker=dict(
                    size=6, 
                    color='orange',
                    symbol='x'
                ),
                name='Parked Vehicles',
                text=[f"Vehicle: {row['vehicle_id']}" for _, row in occupied_spots.iterrows()],
                hovertemplate="<b>%{text}</b><br>Position: (%{x:.1f}, %{y:.1f})<extra></extra>"
            ))
            
        # Highlight violations
        violations = []
        for spot_idx, spot in occupied_spots.iterrows():
            if spot['disabled'] == 1:
                vehicle_id = spot['vehicle_id']
                if vehicle_id is not None:
                    vehicle = simulation.vehicles[simulation.vehicles['license'] == vehicle_id]
                    if not vehicle.empty and vehicle.iloc[0]['disabled'] == 0:
                        violations.append(spot)
        
        if violations:
            violations_df = pd.DataFrame(violations)
            fig.add_trace(go.Scatter(
                x=violations_df['x'],
                y=violations_df['y'],
                mode='markers',
                marker=dict(size=12, color='red', symbol='circle-open', line=dict(width=3)),
                name='Violations',
                hovertemplate="<b>VIOLATION</b><br>Unauthorized disabled parking<br>Position: (%{x:.1f}, %{y:.1f})<extra></extra>"
            ))
    
    # Update layout
    fig.update_layout(
        title=f"Simulation Step {simulation.step_count}",
        xaxis_title="X Coordinate (m)",
        yaxis_title="Y Coordinate (m)",
        xaxis=dict(range=[0, simulation.width], showgrid=True, gridcolor='lightgray'),
        yaxis=dict(range=[0, simulation.height], showgrid=True, gridcolor='lightgray'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor='white',
        width=800,
        height=600
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