import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import networkx as nx
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.stats import gaussian_kde

def create_network_topology_visualization(simulation, show_communication_links=True):
    """
    Create network topology visualization showing drone connectivity
    
    Args:
        simulation: DroneEnvironment instance
        show_communication_links: Whether to show communication links between drones
        
    Returns:
        Network topology figure
    """
    fig = go.Figure()
    
    # Get drone positions
    active_drones = simulation.drones[simulation.drones['active'] == 1]
    inactive_drones = simulation.drones[simulation.drones['active'] == 0]
    
    # Create network graph
    G = nx.Graph()
    
    # Add nodes for active drones
    for _, drone in active_drones.iterrows():
        G.add_node(drone['id'], pos=(drone['x'], drone['y']), 
                  energy=drone['energy'], active=True)
    
    # Add edges for communication links (based on distance)
    communication_range = simulation.sensing_radius * 1.5  # Assume comm range > sensing range
    
    if show_communication_links:
        for i, drone1 in active_drones.iterrows():
            for j, drone2 in active_drones.iterrows():
                if drone1['id'] != drone2['id']:
                    distance = np.sqrt((drone1['x'] - drone2['x'])**2 + 
                                     (drone1['y'] - drone2['y'])**2)
                    if distance <= communication_range:
                        G.add_edge(drone1['id'], drone2['id'], weight=1/distance)
    
    # Draw communication links
    if show_communication_links:
        edge_x = []
        edge_y = []
        for edge in G.edges():
            node1_pos = G.nodes[edge[0]]['pos']
            node2_pos = G.nodes[edge[1]]['pos']
            edge_x.extend([node1_pos[0], node2_pos[0], None])
            edge_y.extend([node1_pos[1], node2_pos[1], None])
        
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            mode='lines',
            line=dict(width=1, color='lightblue'),
            name='Communication Links',
            hoverinfo='none'
        ))
    
    # Draw active drone nodes
    if not active_drones.empty:
        fig.add_trace(go.Scatter(
            x=active_drones['x'],
            y=active_drones['y'],
            mode='markers+text',
            marker=dict(
                size=15,
                color=active_drones['energy'],
                colorscale='RdYlGn',
                cmin=0, cmax=100,
                symbol='circle',
                line=dict(width=2, color='darkgreen'),
                colorbar=dict(title="Energy Level (%)")
            ),
            text=[f"D{row['id']}" for _, row in active_drones.iterrows()],
            textposition="middle center",
            name='Active Drones',
            hovertemplate="<b>Drone %{text}</b><br>Energy: %{marker.color:.1f}%<br>Position: (%{x:.1f}, %{y:.1f})<extra></extra>"
        ))
    
    # Draw inactive drones
    if not inactive_drones.empty:
        fig.add_trace(go.Scatter(
            x=inactive_drones['x'],
            y=inactive_drones['y'],
            mode='markers+text',
            marker=dict(size=10, color='red', symbol='circle'),
            text=[f"D{row['id']}" for _, row in inactive_drones.iterrows()],
            textposition="middle center",
            name='Inactive Drones',
            hovertemplate="<b>Drone %{text}</b><br>Status: Inactive<br>Position: (%{x:.1f}, %{y:.1f})<extra></extra>"
        ))
    
    # Calculate network metrics
    if G.number_of_nodes() > 0:
        connectivity = nx.is_connected(G)
        avg_clustering = nx.average_clustering(G)
        num_components = nx.number_connected_components(G)
        
        # Add network info annotation
        network_info = f"Network Status:<br>Connected: {connectivity}<br>Components: {num_components}<br>Avg Clustering: {avg_clustering:.3f}"
    else:
        network_info = "Network Status:<br>No active connections"
    
    fig.update_layout(
        title="Drone Network Topology",
        xaxis_title="X Coordinate (m)",
        yaxis_title="Y Coordinate (m)",
        xaxis=dict(range=[0, simulation.width]),
        yaxis=dict(range=[0, simulation.height]),
        annotations=[
            dict(
                text=network_info,
                xref="paper", yref="paper",
                x=0.02, y=0.98, xanchor="left", yanchor="top",
                showarrow=False,
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="black", borderwidth=1
            )
        ]
    )
    
    return fig

def create_coverage_quality_heatmap(simulation, quality_metric='signal_strength'):
    """
    Create heatmap showing coverage quality across the area
    
    Args:
        simulation: DroneEnvironment instance
        quality_metric: Type of quality metric to display
        
    Returns:
        Coverage quality heatmap
    """
    # Create fine-grained grid
    grid_size = 50
    x = np.linspace(0, simulation.width, grid_size)
    y = np.linspace(0, simulation.height, grid_size)
    xx, yy = np.meshgrid(x, y)
    grid_points = np.column_stack([xx.ravel(), yy.ravel()])
    
    # Calculate quality metric at each point
    quality_values = np.zeros(len(grid_points))
    
    active_drones = simulation.drones[simulation.drones['active'] == 1]
    
    for point_idx, point in enumerate(grid_points):
        point_quality = 0
        
        for _, drone in active_drones.iterrows():
            drone_pos = np.array([drone['x'], drone['y']])
            distance = np.linalg.norm(point - drone_pos)
            
            if distance <= simulation.sensing_radius:
                if quality_metric == 'signal_strength':
                    # Signal strength decreases with distance
                    signal_strength = max(0, 1 - (distance / simulation.sensing_radius))
                    point_quality += signal_strength * (drone['energy'] / 100)
                elif quality_metric == 'coverage_count':
                    point_quality += 1
                elif quality_metric == 'redundancy':
                    point_quality += 1
        
        quality_values[point_idx] = point_quality
    
    # Reshape for heatmap
    quality_grid = quality_values.reshape(grid_size, grid_size)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=quality_grid,
        x=x, y=y,
        colorscale='Viridis',
        colorbar=dict(title=f"{quality_metric.replace('_', ' ').title()}")
    ))
    
    # Overlay drone positions
    if not active_drones.empty:
        fig.add_trace(go.Scatter(
            x=active_drones['x'],
            y=active_drones['y'],
            mode='markers',
            marker=dict(size=12, color='white', symbol='triangle-up', 
                       line=dict(width=2, color='black')),
            name='Active Drones',
            showlegend=True
        ))
    
    fig.update_layout(
        title=f"Coverage Quality Heatmap - {quality_metric.replace('_', ' ').title()}",
        xaxis_title="X Coordinate (m)",
        yaxis_title="Y Coordinate (m)"
    )
    
    return fig

def create_algorithm_performance_radar(experiment_results):
    """
    Create comprehensive radar chart for algorithm performance
    
    Args:
        experiment_results: List of experiment results
        
    Returns:
        Multi-dimensional performance radar chart
    """
    if not experiment_results:
        return go.Figure().update_layout(title="No experiment data available")
    
    # Define performance dimensions
    dimensions = [
        'Coverage', 'Speed', 'Energy Efficiency', 'Reliability', 
        'Scalability', 'Convergence', 'Robustness'
    ]
    
    fig = go.Figure()
    
    # Colors for different algorithms
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink']
    
    for i, result in enumerate(experiment_results[:len(colors)]):
        # Normalize metrics to 0-1 scale
        coverage = result.get('coverage', 0) / 100
        speed = 1 / (1 + result.get('execution_time', 1) / 10)  # Inverse relationship
        energy_eff = 1 - (result.get('active_nodes', 1) / result.get('total_drones', 20))
        reliability = 1 - result.get('overlap', 0) / 5  # Lower overlap is better
        scalability = min(result.get('coverage', 0) / result.get('total_drones', 20) * 20, 1)
        convergence = result.get('convergence_rate', 0.5)  # Placeholder
        robustness = result.get('stability_score', 0.7)    # Placeholder
        
        values = [coverage, speed, energy_eff, reliability, scalability, convergence, robustness]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=dimensions,
            fill='toself',
            name=result.get('algorithm', f'Algorithm {i+1}'),
            line_color=colors[i % len(colors)],
            opacity=0.6
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickvals=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                ticktext=['0%', '20%', '40%', '60%', '80%', '100%']
            )
        ),
        showlegend=True,
        title="Multi-Dimensional Algorithm Performance Analysis"
    )
    
    return fig

def create_energy_consumption_analysis(simulation_history):
    """
    Create detailed energy consumption analysis
    
    Args:
        simulation_history: List of simulation states
        
    Returns:
        Energy consumption analysis dashboard
    """
    if not simulation_history:
        return go.Figure().update_layout(title="No simulation history available")
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Energy Over Time', 'Energy Distribution', 
                       'Consumption Rate', 'Battery Status'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"type": "indicator"}]]
    )
    
    # Extract energy data
    steps = list(range(len(simulation_history)))
    num_drones = len(simulation_history[0].drones)
    
    # Energy over time for each drone
    for drone_id in range(min(num_drones, 5)):  # Show first 5 drones
        energy_timeline = []
        for state in simulation_history:
            if drone_id < len(state.drones):
                energy_timeline.append(state.drones.iloc[drone_id]['energy'])
            else:
                energy_timeline.append(0)
        
        fig.add_trace(
            go.Scatter(x=steps, y=energy_timeline, mode='lines', 
                      name=f'Drone {drone_id}', opacity=0.7),
            row=1, col=1
        )
    
    # Current energy distribution
    current_state = simulation_history[-1]
    energy_levels = current_state.drones['energy'].values
    
    fig.add_trace(
        go.Histogram(x=energy_levels, nbinsx=20, name='Energy Distribution',
                    marker_color='lightblue', opacity=0.7),
        row=1, col=2
    )
    
    # Consumption rate analysis
    if len(simulation_history) > 1:
        consumption_rates = []
        for i in range(1, len(simulation_history)):
            prev_energy = simulation_history[i-1].drones['energy'].sum()
            curr_energy = simulation_history[i].drones['energy'].sum()
            consumption_rates.append(prev_energy - curr_energy)
        
        fig.add_trace(
            go.Scatter(x=steps[1:], y=consumption_rates, mode='lines+markers',
                      name='Consumption Rate', line=dict(color='red')),
            row=2, col=1
        )
    
    # Battery status indicator
    avg_energy = np.mean(energy_levels)
    critical_count = np.sum(energy_levels < 20)
    
    fig.add_trace(
        go.Indicator(
            mode="gauge+number+delta",
            value=avg_energy,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Average Energy"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 25], 'color': "lightgray"},
                    {'range': [25, 50], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 20
                }
            }
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        title="Energy Consumption Analysis Dashboard",
        height=700,
        showlegend=True
    )
    
    return fig

def create_optimization_landscape_contour(parameter_results):
    """
    Create contour plot of optimization landscape
    
    Args:
        parameter_results: Results from parameter sweep
        
    Returns:
        Optimization landscape contour plot
    """
    if not parameter_results:
        return go.Figure().update_layout(title="No parameter sweep data available")
    
    # Extract parameter data
    param_names = list(parameter_results.keys())
    if len(param_names) < 2:
        return go.Figure().update_layout(title="Need at least 2 parameters for contour plot")
    
    param1_name, param2_name = param_names[0], param_names[1]
    
    # Create grid of parameter values
    param1_values = []
    param2_values = []
    fitness_values = []
    
    for key, result in parameter_results.items():
        if isinstance(key, tuple) and len(key) >= 2:
            param1_values.append(key[0])
            param2_values.append(key[1])
            fitness_values.append(result.get('coverage', 0))
    
    # Create meshgrid for contour plot
    if param1_values and param2_values:
        # Convert to numpy arrays
        param1_array = np.array(param1_values)
        param2_array = np.array(param2_values)
        fitness_array = np.array(fitness_values)
        
        # Create regular grid
        param1_unique = np.unique(param1_array)
        param2_unique = np.unique(param2_array)
        
        if len(param1_unique) > 1 and len(param2_unique) > 1:
            param1_grid, param2_grid = np.meshgrid(param1_unique, param2_unique)
            
            # Interpolate fitness values onto grid
            from scipy.interpolate import griddata
            fitness_grid = griddata(
                (param1_array, param2_array), fitness_array,
                (param1_grid, param2_grid), method='cubic', fill_value=0
            )
            
            # Create contour plot
            fig = go.Figure()
            
            # Add contour
            fig.add_trace(go.Contour(
                z=fitness_grid,
                x=param1_unique,
                y=param2_unique,
                colorscale='Viridis',
                contours_coloring="heatmap",
                line_smoothing=0.85,
                colorbar=dict(title="Fitness Score")
            ))
            
            # Add scatter points for actual data
            fig.add_trace(go.Scatter(
                x=param1_array,
                y=param2_array,
                mode='markers',
                marker=dict(
                    size=8,
                    color=fitness_array,
                    colorscale='Viridis',
                    line=dict(width=1, color='white')
                ),
                text=[f"Fitness: {f:.2f}" for f in fitness_array],
                name='Experiment Points',
                hovertemplate="<b>%{text}</b><br>" + f"{param1_name}: %{{x}}<br>{param2_name}: %{{y}}<extra></extra>"
            ))
            
            # Find and mark optimal point
            max_idx = np.argmax(fitness_array)
            fig.add_trace(go.Scatter(
                x=[param1_array[max_idx]],
                y=[param2_array[max_idx]],
                mode='markers',
                marker=dict(size=15, color='red', symbol='star'),
                name='Optimal Point',
                hovertemplate=f"<b>Optimal</b><br>{param1_name}: %{{x}}<br>{param2_name}: %{{y}}<br>Fitness: {fitness_array[max_idx]:.2f}<extra></extra>"
            ))
            
            fig.update_layout(
                title="Optimization Landscape Contour Plot",
                xaxis_title=param1_name,
                yaxis_title=param2_name
            )
            
            return fig
    
    return go.Figure().update_layout(title="Insufficient data for contour plot")

def create_clustering_analysis(simulation_results):
    """
    Create clustering analysis of simulation results
    
    Args:
        simulation_results: List of simulation results
        
    Returns:
        Clustering analysis visualization
    """
    if not simulation_results or len(simulation_results) < 3:
        return go.Figure().update_layout(title="Insufficient data for clustering analysis")
    
    # Extract features for clustering
    features = []
    labels = []
    
    for result in simulation_results:
        feature_vector = [
            result.get('coverage', 0),
            result.get('active_nodes', 0),
            result.get('execution_time', 0),
            result.get('overlap', 0)
        ]
        features.append(feature_vector)
        labels.append(result.get('algorithm', 'unknown'))
    
    features_array = np.array(features)
    
    # Normalize features
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    features_normalized = scaler.fit_transform(features_array)
    
    # Perform hierarchical clustering
    linkage_matrix = linkage(features_normalized, method='ward')
    
    # Create dendrogram
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Algorithm Clustering Dendrogram', 'Feature Scatter Plot'),
        specs=[[{"type": "scatter"}, {"type": "scatter"}]]
    )
    
    # Create dendrogram data
    from scipy.cluster.hierarchy import dendrogram
    dend = dendrogram(linkage_matrix, labels=labels, no_plot=True)
    
    # Add dendrogram traces
    for i, d in enumerate(zip(dend['icoord'], dend['dcoord'])):
        x, y = d
        fig.add_trace(
            go.Scatter(x=x, y=y, mode='lines', line=dict(color='black'), 
                      showlegend=False, hoverinfo='skip'),
            row=1, col=1
        )
    
    # Add scatter plot of first two principal components
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    features_pca = pca.fit_transform(features_normalized)
    
    # Color by algorithm
    unique_algorithms = list(set(labels))
    colors = px.colors.qualitative.Set1[:len(unique_algorithms)]
    
    for i, algorithm in enumerate(unique_algorithms):
        mask = [label == algorithm for label in labels]
        algorithm_features = features_pca[mask]
        
        if len(algorithm_features) > 0:
            fig.add_trace(
                go.Scatter(
                    x=algorithm_features[:, 0],
                    y=algorithm_features[:, 1],
                    mode='markers',
                    marker=dict(size=10, color=colors[i]),
                    name=algorithm,
                    hovertemplate=f"<b>{algorithm}</b><br>PC1: %{{x:.2f}}<br>PC2: %{{y:.2f}}<extra></extra>"
                ),
                row=1, col=2
            )
    
    fig.update_layout(
        title="Algorithm Performance Clustering Analysis",
        height=500
    )
    
    return fig

def create_sensitivity_analysis_tornado(parameter_sensitivities):
    """
    Create tornado plot for parameter sensitivity analysis
    
    Args:
        parameter_sensitivities: Dictionary with parameter names and sensitivity values
        
    Returns:
        Tornado plot for sensitivity analysis
    """
    if not parameter_sensitivities:
        return go.Figure().update_layout(title="No sensitivity data available")
    
    # Sort parameters by sensitivity (absolute value)
    sorted_params = sorted(parameter_sensitivities.items(), 
                          key=lambda x: abs(x[1]), reverse=True)
    
    param_names = [item[0] for item in sorted_params]
    sensitivity_values = [item[1] for item in sorted_params]
    
    # Create colors based on positive/negative sensitivity
    colors = ['green' if val > 0 else 'red' for val in sensitivity_values]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=param_names,
        x=sensitivity_values,
        orientation='h',
        marker_color=colors,
        text=[f"{val:+.3f}" for val in sensitivity_values],
        textposition='auto',
        hovertemplate="<b>%{y}</b><br>Sensitivity: %{x:+.3f}<extra></extra>"
    ))
    
    # Add vertical line at zero
    fig.add_vline(x=0, line_dash="dash", line_color="black", line_width=1)
    
    fig.update_layout(
        title="Parameter Sensitivity Analysis (Tornado Plot)",
        xaxis_title="Sensitivity Coefficient",
        yaxis_title="Parameters",
        annotations=[
            dict(
                text="Green: Positive impact<br>Red: Negative impact",
                xref="paper", yref="paper",
                x=0.98, y=0.02, xanchor="right", yanchor="bottom",
                showarrow=False,
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="black", borderwidth=1
            )
        ]
    )
    
    return fig

def create_real_time_performance_monitor(simulation, metrics_buffer_size=100):
    """
    Create real-time performance monitoring dashboard
    
    Args:
        simulation: Current simulation state
        metrics_buffer_size: Size of metrics buffer for real-time display
        
    Returns:
        Real-time performance monitoring figure
    """
    # Create subplots for different metrics
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=('Coverage %', 'Active Drones', 'Energy Levels',
                       'Network Health', 'Performance Score', 'Status Indicators'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}, {"type": "indicator"}],
               [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]]
    )
    
    # Get recent metrics (last N steps)
    metrics = simulation.metrics_history
    recent_steps = list(range(max(0, simulation.step_count - metrics_buffer_size), 
                             simulation.step_count + 1))
    
    if metrics['coverage']:
        recent_coverage = metrics['coverage'][-metrics_buffer_size:]
        fig.add_trace(
            go.Scatter(x=recent_steps[-len(recent_coverage):], 
                      y=[c*100 for c in recent_coverage],
                      mode='lines', name='Coverage',
                      line=dict(color='green', width=2)),
            row=1, col=1
        )
    
    if metrics['active_drones']:
        recent_active = metrics['active_drones'][-metrics_buffer_size:]
        fig.add_trace(
            go.Scatter(x=recent_steps[-len(recent_active):], 
                      y=recent_active,
                      mode='lines', name='Active Drones',
                      line=dict(color='blue', width=2)),
            row=1, col=2
        )
    
    # Current energy status
    current_energy = simulation.drones['energy'].mean()
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=current_energy,
            title={'text': "Avg Energy"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [{'range': [0, 20], 'color': "red"},
                         {'range': [20, 50], 'color': "yellow"},
                         {'range': [50, 100], 'color': "green"}],
                'threshold': {'line': {'color': "red", 'width': 4},
                            'thickness': 0.75, 'value': 20}
            }
        ),
        row=1, col=3
    )
    
    # Network connectivity health
    active_drones = simulation.drones[simulation.drones['active'] == 1]
    connectivity_score = len(active_drones) / len(simulation.drones) * 100
    
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=connectivity_score,
            title={'text': "Network Health %"},
            delta={'reference': 80, 'position': "top"},
            number={'font': {'size': 40}}
        ),
        row=2, col=1
    )
    
    # Overall performance score
    if metrics['coverage']:
        performance_score = (metrics['coverage'][-1] * 70 + 
                           (len(active_drones) / len(simulation.drones)) * 30)
        performance_score *= 100
    else:
        performance_score = 0
    
    fig.add_trace(
        go.Indicator(
            mode="gauge+number+delta",
            value=performance_score,
            title={'text': "Performance Score"},
            delta={'reference': 75},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "purple"},
                'steps': [{'range': [0, 40], 'color': "red"},
                         {'range': [40, 70], 'color': "yellow"},
                         {'range': [70, 100], 'color': "green"}]
            }
        ),
        row=2, col=2
    )
    
    # System status
    system_status = "OPTIMAL" if performance_score > 80 else "GOOD" if performance_score > 60 else "WARNING"
    status_color = "green" if system_status == "OPTIMAL" else "orange" if system_status == "GOOD" else "red"
    
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=1,
            title={'text': f"Status: {system_status}"},
            number={'font': {'color': status_color, 'size': 30}}
        ),
        row=2, col=3
    )
    
    fig.update_layout(
        title="🔴 Real-Time Performance Monitor",
        height=600,
        showlegend=False
    )
    
    return fig

def create_comparative_time_series(experiment_timeseries_data):
    """
    Create comparative time series analysis for multiple experiments
    
    Args:
        experiment_timeseries_data: Dictionary with experiment IDs and their time series data
        
    Returns:
        Comparative time series figure
    """
    if not experiment_timeseries_data:
        return go.Figure().update_layout(title="No time series data available")
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Coverage Evolution', 'Energy Consumption', 
                       'Active Drones', 'Performance Score'),
        shared_xaxes=True
    )
    
    colors = px.colors.qualitative.Set1
    
    for i, (exp_id, data) in enumerate(experiment_timeseries_data.items()):
        color = colors[i % len(colors)]
        steps = list(range(len(data.get('coverage', []))))
        
        # Coverage evolution
        if 'coverage' in data:
            fig.add_trace(
                go.Scatter(x=steps, y=[c*100 for c in data['coverage']], 
                          mode='lines', name=f'Exp {exp_id}', 
                          line=dict(color=color), legendgroup=exp_id),
                row=1, col=1
            )
        
        # Energy consumption
        if 'energy' in data:
            fig.add_trace(
                go.Scatter(x=steps, y=data['energy'], 
                          mode='lines', name=f'Exp {exp_id}', 
                          line=dict(color=color), showlegend=False, 
                          legendgroup=exp_id),
                row=1, col=2
            )
        
        # Active drones
        if 'active_drones' in data:
            fig.add_trace(
                go.Scatter(x=steps, y=data['active_drones'], 
                          mode='lines', name=f'Exp {exp_id}', 
                          line=dict(color=color), showlegend=False,
                          legendgroup=exp_id),
                row=2, col=1
            )
        
        # Performance score (composite metric)
        if 'coverage' in data and 'active_drones' in data:
            performance = [c*80 + (a/20)*20 for c, a in zip(data['coverage'], data['active_drones'])]
            fig.add_trace(
                go.Scatter(x=steps, y=performance, 
                          mode='lines', name=f'Exp {exp_id}', 
                          line=dict(color=color), showlegend=False,
                          legendgroup=exp_id),
                row=2, col=2
            )
    
    fig.update_layout(
        title="Comparative Time Series Analysis",
        height=600,
        hovermode='x unified'
    )
    
    return fig

def create_pareto_frontier_analysis(multi_objective_results):
    """
    Create Pareto frontier analysis for multi-objective optimization
    
    Args:
        multi_objective_results: Results with multiple objectives
        
    Returns:
        Pareto frontier visualization
    """
    if not multi_objective_results:
        return go.Figure().update_layout(title="No multi-objective data available")
    
    # Extract objectives
    coverage_values = [r.get('coverage', 0) for r in multi_objective_results]
    energy_efficiency = [r.get('energy_efficiency', 0) for r in multi_objective_results]
    execution_time = [r.get('execution_time', float('inf')) for r in multi_objective_results]
    algorithm_names = [r.get('algorithm', 'unknown') for r in multi_objective_results]
    
    # Normalize execution time (convert to efficiency: lower time = higher efficiency)
    max_time = max(execution_time) if execution_time else 1
    time_efficiency = [1 - (t / max_time) for t in execution_time]
    
    # Create 3D scatter plot
    fig = go.Figure()
    
    # Color by algorithm
    unique_algorithms = list(set(algorithm_names))
    colors = px.colors.qualitative.Set1[:len(unique_algorithms)]
    algorithm_colors = {alg: colors[i] for i, alg in enumerate(unique_algorithms)}
    
    for algorithm in unique_algorithms:
        mask = [alg == algorithm for alg in algorithm_names]
        alg_coverage = [coverage_values[i] for i in range(len(mask)) if mask[i]]
        alg_energy = [energy_efficiency[i] for i in range(len(mask)) if mask[i]]
        alg_time = [time_efficiency[i] for i in range(len(mask)) if mask[i]]
        
        fig.add_trace(go.Scatter3d(
            x=alg_coverage,
            y=alg_energy,
            z=alg_time,
            mode='markers',
            marker=dict(
                size=8,
                color=algorithm_colors[algorithm],
                opacity=0.8
            ),
            name=algorithm,
            hovertemplate=f"<b>{algorithm}</b><br>Coverage: %{{x:.1f}}%<br>Energy Eff: %{{y:.2f}}<br>Time Eff: %{{z:.2f}}<extra></extra>"
        ))
    
    # Find and highlight Pareto frontier points
    pareto_indices = []
    for i in range(len(coverage_values)):
        is_pareto = True
        for j in range(len(coverage_values)):
            if (i != j and 
                coverage_values[j] >= coverage_values[i] and 
                energy_efficiency[j] >= energy_efficiency[i] and 
                time_efficiency[j] >= time_efficiency[i] and
                (coverage_values[j] > coverage_values[i] or 
                 energy_efficiency[j] > energy_efficiency[i] or 
                 time_efficiency[j] > time_efficiency[i])):
                is_pareto = False
                break
        if is_pareto:
            pareto_indices.append(i)
    
    # Add Pareto frontier points
    if pareto_indices:
        pareto_coverage = [coverage_values[i] for i in pareto_indices]
        pareto_energy = [energy_efficiency[i] for i in pareto_indices]
        pareto_time = [time_efficiency[i] for i in pareto_indices]
        
        fig.add_trace(go.Scatter3d(
            x=pareto_coverage,
            y=pareto_energy,
            z=pareto_time,
            mode='markers',
            marker=dict(
                size=12,
                color='gold',
                symbol='diamond',
                line=dict(color='black', width=2)
            ),
            name='Pareto Frontier',
            hovertemplate="<b>Pareto Optimal</b><br>Coverage: %{x:.1f}%<br>Energy Eff: %{y:.2f}<br>Time Eff: %{z:.2f}<extra></extra>"
        ))
    
    fig.update_layout(
        title="Multi-Objective Pareto Frontier Analysis",
        scene=dict(
            xaxis_title="Coverage (%)",
            yaxis_title="Energy Efficiency",
            zaxis_title="Time Efficiency",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        height=600
    )
    
    return fig