#!/usr/bin/env python3
"""
2D Grid Visualization Component for Active/Sleep Drone Management
Creates interactive visualizations showing active (green) vs sleeping (gray) drones
"""

import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

def create_2d_drone_visualization(drones_data, coverage_data, simulation_params):
    """
    Create interactive 2D visualization showing active/sleep drone deployment
    
    Args:
        drones_data: List of dicts with 'id', 'x', 'y', 'active', 'coverage_area'
        coverage_data: Dict with coverage metrics
        simulation_params: Dict with area dimensions, sensing range, etc.
    
    Returns:
        Plotly figure object
    """
    
    # Create subplot figure with coverage map and drone status
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=[
            f"Drone Deployment - {coverage_data.get('coverage', 0):.1f}% Coverage",
            f"Energy Efficiency Analysis"
        ],
        specs=[[{"type": "scatter"}, {"type": "pie"}]],
        column_widths=[0.65, 0.35],
        horizontal_spacing=0.12
    )
    
    # Extract parameters
    width = simulation_params.get('width', 60)
    height = simulation_params.get('height', 60)
    sensing_range = simulation_params.get('sensing_range', 14)
    
    # Separate active and sleeping drones
    active_drones = [d for d in drones_data if d['active']]
    sleeping_drones = [d for d in drones_data if not d['active']]
    
    # Plot 1: 2D Drone Deployment Map
    
    # Add coverage circles for active drones (light green background)
    for drone in active_drones:
        fig.add_shape(
            type="circle",
            x0=drone['x'] - sensing_range,
            y0=drone['y'] - sensing_range,
            x1=drone['x'] + sensing_range,
            y1=drone['y'] + sensing_range,
            fillcolor="rgba(144, 238, 144, 0.3)",  # Light green with transparency
            line=dict(color="rgba(144, 238, 144, 0.5)", width=1),
            row=1, col=1
        )
    
    # Add active drones (green circles)
    if active_drones:
        active_x = [d['x'] for d in active_drones]
        active_y = [d['y'] for d in active_drones]
        active_ids = [f"Drone {d['id']}" for d in active_drones]
        active_hover = [f"<b>Drone {d['id']}</b><br>Status: Active<br>Position: ({d['x']:.1f}, {d['y']:.1f})<br>Coverage Radius: {sensing_range}" 
                       for d in active_drones]
        
        fig.add_trace(
            go.Scatter(
                x=active_x,
                y=active_y,
                mode='markers+text',
                marker=dict(
                    size=16,
                    color='#2ECC71',  # Green
                    symbol='circle',
                    line=dict(width=3, color='#27AE60')  # Darker green border
                ),
                text=active_ids,
                textposition="bottom center",
                textfont=dict(size=10, color='#27AE60', family="Arial Black"),
                hovertemplate='%{customdata}<extra></extra>',
                customdata=active_hover,
                name='Active Drones',
                showlegend=True
            ),
            row=1, col=1
        )
    
    # Add sleeping drones (gray circles)
    if sleeping_drones:
        sleeping_x = [d['x'] for d in sleeping_drones]
        sleeping_y = [d['y'] for d in sleeping_drones]
        sleeping_ids = [f"Drone {d['id']}" for d in sleeping_drones]
        sleeping_hover = [f"<b>Drone {d['id']}</b><br>Status: Sleeping<br>Position: ({d['x']:.1f}, {d['y']:.1f})<br>Energy Saved" 
                         for d in sleeping_drones]
        
        fig.add_trace(
            go.Scatter(
                x=sleeping_x,
                y=sleeping_y,
                mode='markers+text',
                marker=dict(
                    size=12,
                    color='#95A5A6',  # Gray
                    symbol='circle',
                    line=dict(width=2, color='#7F8C8D')  # Darker gray border
                ),
                text=sleeping_ids,
                textposition="bottom center",
                textfont=dict(size=9, color='#7F8C8D'),
                hovertemplate='%{customdata}<extra></extra>',
                customdata=sleeping_hover,
                name='Sleeping Drones',
                showlegend=True
            ),
            row=1, col=1
        )
    
    # Add area boundary
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=width, y1=height,
        line=dict(color="black", width=2),
        fillcolor="rgba(255, 255, 255, 0)",
        row=1, col=1
    )
    
    # Plot 2: Energy Efficiency Metrics
    
    # Energy efficiency pie chart
    total_drones = len(drones_data)
    active_count = len(active_drones)
    sleeping_count = len(sleeping_drones)
    
    # Pie chart for energy distribution
    fig.add_trace(
        go.Pie(
            labels=['Active Drones', 'Sleeping Drones'],
            values=[active_count, sleeping_count],
            hole=0.4,
            marker_colors=['#2ECC71', '#95A5A6'],
            textinfo='label+percent+value',
            textfont=dict(size=12),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        ),
        row=1, col=2
    )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"<b>Active/Sleep Drone Management System</b><br>"
                 f"<span style='font-size:14px'>Energy Efficiency: {coverage_data.get('energy_saved', 0):.1f}% • "
                 f"Coverage: {coverage_data.get('coverage', 0):.1f}% • "
                 f"Active: {active_count}/{total_drones} drones</span>",
            x=0.5,
            font=dict(size=16, family="Arial Black")
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.3
        ),
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # Update subplot 1 (drone map) layout
    fig.update_xaxes(
        title_text="X Coordinate (meters)",
        range=[0, width],
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        row=1, col=1
    )
    fig.update_yaxes(
        title_text="Y Coordinate (meters)",
        range=[0, height],
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        scaleanchor="x",
        scaleratio=1,
        row=1, col=1
    )
    
    # Update subplot 2 (pie chart) layout
    fig.update_xaxes(showticklabels=False, showgrid=False, row=1, col=2)
    fig.update_yaxes(showticklabels=False, showgrid=False, row=1, col=2)
    
    return fig

def create_energy_efficiency_dashboard(results_history):
    """
    Create comprehensive energy efficiency analysis dashboard
    
    Args:
        results_history: List of result dictionaries from optimization runs
    
    Returns:
        Plotly figure with multiple energy efficiency visualizations
    """
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            "Coverage vs Active Drones Trade-off",
            "Energy Savings Over Time", 
            "Algorithm Performance Comparison",
            "Efficiency Metrics"
        ],
        specs=[
            [{"secondary_y": False}, {"secondary_y": True}],
            [{"type": "bar"}, {"type": "indicator"}]
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    if not results_history:
        # Empty dashboard if no data
        fig.add_annotation(
            text="No optimization results available",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Extract data for plotting
    iterations = list(range(len(results_history)))
    coverage_values = [r.get('coverage', 0) * 100 for r in results_history]
    active_counts = [r.get('active_count', 0) for r in results_history]
    energy_savings = [r.get('energy_savings', 0) for r in results_history]
    algorithms = [r.get('algorithm', 'Unknown') for r in results_history]
    
    # Plot 1: Coverage vs Active Drones Trade-off
    fig.add_trace(
        go.Scatter(
            x=active_counts,
            y=coverage_values,
            mode='markers+lines',
            marker=dict(
                size=8,
                color=energy_savings,
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Energy Savings %", x=0.48)
            ),
            line=dict(color='blue', width=2),
            name='Optimization Path',
            hovertemplate='<b>Trade-off Point</b><br>' +
                         'Active Drones: %{x}<br>' +
                         'Coverage: %{y:.1f}%<br>' +
                         'Energy Savings: %{marker.color:.1f}%<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Add reference target point
    if coverage_values and active_counts:
        fig.add_trace(
            go.Scatter(
                x=[12],  # Reference image target
                y=[99],  # Reference image target
                mode='markers',
                marker=dict(
                    size=15,
                    color='red',
                    symbol='star',
                    line=dict(width=2, color='darkred')
                ),
                name='Reference Target',
                hovertemplate='<b>Reference Target</b><br>' +
                             'Active Drones: 12<br>' +
                             'Coverage: 99%<extra></extra>'
            ),
            row=1, col=1
        )
    
    # Plot 2: Energy Savings Over Time
    if len(iterations) > 1:
        fig.add_trace(
            go.Scatter(
                x=iterations,
                y=energy_savings,
                mode='lines',
                line=dict(color='green', width=3),
                name='Energy Savings',
                hovertemplate='Iteration: %{x}<br>Energy Saved: %{y:.1f}%<extra></extra>'
            ),
            row=1, col=2
        )
        
        # Add coverage on secondary y-axis
        fig.add_trace(
            go.Scatter(
                x=iterations,
                y=coverage_values,
                mode='lines',
                line=dict(color='blue', width=2, dash='dot'),
                name='Coverage',
                yaxis='y2',
                hovertemplate='Iteration: %{x}<br>Coverage: %{y:.1f}%<extra></extra>'
            ),
            row=1, col=2
        )
    
    # Plot 3: Algorithm Performance Comparison
    if results_history:
        latest_result = results_history[-1]
        
        # Create performance metrics bar chart
        metrics = ['Coverage (%)', 'Energy Savings (%)', 'Efficiency Score']
        values = [
            latest_result.get('coverage', 0) * 100,
            latest_result.get('energy_savings', 0),
            latest_result.get('coverage', 0) * 100 / max(1, latest_result.get('active_count', 1))  # Coverage per drone
        ]
        colors = ['#3498DB', '#2ECC71', '#F39C12']
        
        fig.add_trace(
            go.Bar(
                x=metrics,
                y=values,
                marker_color=colors,
                name='Performance',
                hovertemplate='%{x}: %{y:.1f}<extra></extra>'
            ),
            row=2, col=1
        )
    
    # Plot 4: Key Efficiency Indicators
    if results_history:
        latest = results_history[-1]
        
        # Coverage indicator
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=latest.get('coverage', 0) * 100,
                delta={'reference': 99, 'relative': False},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#2ECC71"},
                    'steps': [
                        {'range': [0, 80], 'color': "#E74C3C"},
                        {'range': [80, 95], 'color': "#F39C12"},
                        {'range': [95, 100], 'color': "#2ECC71"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 99
                    }
                },
                title={'text': "Coverage %"},
                domain={'x': [0, 1], 'y': [0.7, 1]}
            ),
            row=2, col=2
        )
        
        # Energy savings indicator
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=latest.get('energy_savings', 0),
                gauge={
                    'axis': {'range': [0, 60]},
                    'bar': {'color': "#F39C12"},
                    'steps': [
                        {'range': [0, 20], 'color': "#E74C3C"},
                        {'range': [20, 40], 'color': "#F39C12"},
                        {'range': [40, 60], 'color': "#2ECC71"}
                    ]
                },
                title={'text': "Energy Saved %"},
                domain={'x': [0, 1], 'y': [0, 0.3]}
            ),
            row=2, col=2
        )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text="<b>Energy Efficiency Analysis Dashboard</b>",
            x=0.5,
            font=dict(size=18, family="Arial Black")
        ),
        showlegend=True,
        height=700,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # Update axes
    fig.update_xaxes(title_text="Active Drones", row=1, col=1)
    fig.update_yaxes(title_text="Coverage (%)", row=1, col=1)
    
    fig.update_xaxes(title_text="Optimization Iteration", row=1, col=2)
    fig.update_yaxes(title_text="Energy Savings (%)", row=1, col=2)
    
    fig.update_xaxes(title_text="Performance Metrics", row=2, col=1)
    fig.update_yaxes(title_text="Value", row=2, col=1)
    
    return fig

def create_drone_status_table(drones_data):
    """
    Create a detailed table showing drone status and metrics
    
    Args:
        drones_data: List of drone dictionaries
    
    Returns:
        Dash DataTable component data
    """
    
    # Create DataFrame from drone data
    df_data = []
    for drone in drones_data:
        df_data.append({
            'Drone ID': drone['id'],
            'Status': '🟢 Active' if drone['active'] else '⚫ Sleeping',
            'X Position': f"{drone['x']:.1f}",
            'Y Position': f"{drone['y']:.1f}",
            'Energy State': 'Consuming' if drone['active'] else 'Saving',
            'Coverage Area': f"{drone.get('coverage_area', 0):.1f}%",
            'Strategic Score': f"{drone.get('strategic_score', 0):.2f}"
        })
    
    return df_data

# Example usage function for testing
def demo_visualization():
    """Demo function showing how to use the visualization components"""
    
    # Sample drone data
    sample_drones = [
        {'id': 1, 'x': 15, 'y': 15, 'active': True, 'coverage_area': 12.5, 'strategic_score': 0.85},
        {'id': 2, 'x': 45, 'y': 15, 'active': True, 'coverage_area': 11.8, 'strategic_score': 0.82},
        {'id': 3, 'x': 30, 'y': 30, 'active': True, 'coverage_area': 13.2, 'strategic_score': 0.90},
        {'id': 4, 'x': 10, 'y': 45, 'active': False, 'coverage_area': 0, 'strategic_score': 0.45},
        {'id': 5, 'x': 50, 'y': 45, 'active': False, 'coverage_area': 0, 'strategic_score': 0.38},
    ]
    
    # Sample coverage data
    sample_coverage = {
        'coverage': 96.5,
        'energy_saved': 40.0,
        'active_count': 3,
        'total_count': 5
    }
    
    # Sample simulation parameters
    sample_params = {
        'width': 60,
        'height': 60,
        'sensing_range': 14
    }
    
    # Create visualization
    fig = create_2d_drone_visualization(sample_drones, sample_coverage, sample_params)
    fig.show()
    
    print("✅ 2D Drone Visualization Demo Complete!")
    print("📊 Visualization shows active (green) and sleeping (gray) drones")
    print("🔋 Energy efficiency metrics included")

if __name__ == "__main__":
    demo_visualization()
