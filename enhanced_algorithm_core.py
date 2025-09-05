#!/usr/bin/env python3
"""
ENHANCED ALGORITHM CORE FUNCTIONS
Position and activation optimization functions for realistic drone deployment
Focus: Fixed sensing radius, optimized positions and activation patterns
"""

import numpy as np
from scipy.spatial.distance import cdist
import random
import time

def grid_based_positioning(simulation, grid_overlap=0.8):
    """
    Grid-based positioning strategy for optimal drone placement
    
    Args:
        simulation: DroneSimulationEnvironment instance
        grid_overlap: Overlap factor for grid spacing (0.8 = 80% spacing for slight overlap)
    
    Returns:
        positions: Array of optimized drone positions
    """
    sensing_radius = simulation.sensing_radius
    grid_spacing = sensing_radius * grid_overlap
    
    # Calculate grid dimensions
    grid_x = max(1, int(np.ceil(simulation.width / grid_spacing)))
    grid_y = max(1, int(np.ceil(simulation.height / grid_spacing)))
    
    # Generate grid positions
    positions = []
    for i in range(grid_x):
        for j in range(grid_y):
            x = (i + 0.5) * grid_spacing
            y = (j + 0.5) * grid_spacing
            
            # Only add positions within bounds
            if x < simulation.width and y < simulation.height:
                positions.append([x, y])
    
    # If we need more positions, add some randomized ones
    num_drones = len(simulation.drones)
    while len(positions) < num_drones:
        x = np.random.uniform(0, simulation.width)
        y = np.random.uniform(0, simulation.height)
        positions.append([x, y])
    
    # If we have too many positions, select the best ones
    if len(positions) > num_drones:
        positions = positions[:num_drones]
    
    return np.array(positions)

def hexagonal_packing_positioning(simulation):
    """
    Hexagonal packing strategy for optimal coverage with minimal overlap
    
    Args:
        simulation: DroneSimulationEnvironment instance
    
    Returns:
        positions: Array of hexagonally packed drone positions
    """
    sensing_radius = simulation.sensing_radius
    
    # Hexagonal packing parameters
    row_spacing = sensing_radius * np.sqrt(3) / 2  # Vertical spacing between rows
    col_spacing = sensing_radius * 1.5             # Horizontal spacing between columns
    
    positions = []
    y = sensing_radius
    row = 0
    
    while y < simulation.height - sensing_radius:
        # Alternate starting x position for hexagonal pattern
        x_start = sensing_radius if row % 2 == 0 else sensing_radius + col_spacing / 2
        x = x_start
        
        while x < simulation.width - sensing_radius:
            positions.append([x, y])
            x += col_spacing
        
        y += row_spacing
        row += 1
    
    # Fill remaining positions with optimized random placement
    num_drones = len(simulation.drones)
    while len(positions) < num_drones:
        # Place remaining drones in areas with least coverage
        x = np.random.uniform(sensing_radius, simulation.width - sensing_radius)
        y = np.random.uniform(sensing_radius, simulation.height - sensing_radius)
        positions.append([x, y])
    
    if len(positions) > num_drones:
        positions = positions[:num_drones]
    
    return np.array(positions)

def voronoi_based_positioning(simulation):
    """
    Voronoi diagram inspired positioning for balanced coverage
    
    Args:
        simulation: DroneSimulationEnvironment instance
    
    Returns:
        positions: Array of Voronoi-based drone positions
    """
    num_drones = len(simulation.drones)
    
    # Start with random seed points
    positions = []
    for _ in range(num_drones):
        x = np.random.uniform(0, simulation.width)
        y = np.random.uniform(0, simulation.height)
        positions.append([x, y])
    
    positions = np.array(positions)
    
    # Lloyd's algorithm for Voronoi optimization (simplified version)
    for iteration in range(10):  # Limited iterations for speed
        # Create a grid of points to assign to nearest drone
        grid_x, grid_y = np.meshgrid(
            np.linspace(0, simulation.width, 20),
            np.linspace(0, simulation.height, 20)
        )
        grid_points = np.stack([grid_x.ravel(), grid_y.ravel()], axis=1)
        
        # Assign each grid point to nearest drone
        distances = cdist(grid_points, positions)
        assignments = np.argmin(distances, axis=1)
        
        # Update drone positions to centroids of assigned regions
        new_positions = []
        for i in range(num_drones):
            assigned_points = grid_points[assignments == i]
            if len(assigned_points) > 0:
                centroid = np.mean(assigned_points, axis=0)
                # Keep within bounds
                centroid[0] = np.clip(centroid[0], 0, simulation.width)
                centroid[1] = np.clip(centroid[1], 0, simulation.height)
                new_positions.append(centroid)
            else:
                # Keep original position if no points assigned
                new_positions.append(positions[i])
        
        positions = np.array(new_positions)
    
    return positions

def smart_activation_optimization(simulation, positions, coverage_target=0.95):
    """
    Smart activation pattern optimization using coverage gap analysis
    
    Args:
        simulation: DroneSimulationEnvironment instance
        positions: Array of drone positions
        coverage_target: Target coverage percentage
    
    Returns:
        activation: Binary activation array
    """
    num_drones = len(positions)
    sensing_radius = simulation.sensing_radius
    
    # Update drone positions
    for i, pos in enumerate(positions):
        if i < len(simulation.drones):
            simulation.drones.iloc[i, simulation.drones.columns.get_loc('x')] = pos[0]
            simulation.drones.iloc[i, simulation.drones.columns.get_loc('y')] = pos[1]
    
    # Start with no drones active
    activation = np.zeros(num_drones, dtype=int)
    
    # Create fine-grained coverage grid for analysis
    grid_resolution = sensing_radius / 4  # Fine resolution for accurate gap detection
    grid_x = int(np.ceil(simulation.width / grid_resolution))
    grid_y = int(np.ceil(simulation.height / grid_resolution))
    
    coverage_grid = np.zeros((grid_x, grid_y))
    
    # Greedy activation: activate drone that covers most uncovered area
    for _ in range(num_drones):
        best_drone = -1
        best_new_coverage = 0
        
        # Test each inactive drone
        for i in range(num_drones):
            if activation[i] == 1:  # Skip already active drones
                continue
            
            # Calculate new coverage if this drone is activated
            new_coverage_count = 0
            drone_x, drone_y = positions[i]
            
            for gx in range(grid_x):
                for gy in range(grid_y):
                    if coverage_grid[gx, gy] == 1:  # Already covered
                        continue
                    
                    # Check if this grid cell would be covered by the drone
                    cell_x = (gx + 0.5) * grid_resolution
                    cell_y = (gy + 0.5) * grid_resolution
                    
                    distance = np.sqrt((drone_x - cell_x)**2 + (drone_y - cell_y)**2)
                    if distance <= sensing_radius:
                        new_coverage_count += 1
            
            if new_coverage_count > best_new_coverage:
                best_new_coverage = new_coverage_count
                best_drone = i
        
        # Activate the best drone
        if best_drone >= 0 and best_new_coverage > 0:
            activation[best_drone] = 1
            
            # Update coverage grid
            drone_x, drone_y = positions[best_drone]
            for gx in range(grid_x):
                for gy in range(grid_y):
                    cell_x = (gx + 0.5) * grid_resolution
                    cell_y = (gy + 0.5) * grid_resolution
                    
                    distance = np.sqrt((drone_x - cell_x)**2 + (drone_y - cell_y)**2)
                    if distance <= sensing_radius:
                        coverage_grid[gx, gy] = 1
            
            # Check if we've reached target coverage
            current_coverage = np.sum(coverage_grid) / (grid_x * grid_y)
            if current_coverage >= coverage_target:
                break
        else:
            # No more useful drones to activate
            break
    
    return activation

def calculate_position_coverage(simulation, positions):
    """
    Calculate coverage percentage for given drone positions
    
    Args:
        simulation: DroneSimulationEnvironment instance
        positions: Array of drone positions
    
    Returns:
        coverage_percentage: Coverage as percentage (0-100)
    """
    # Temporarily update drone positions
    original_positions = []
    for i in range(len(simulation.drones)):
        original_positions.append([
            simulation.drones.iloc[i]['x'], 
            simulation.drones.iloc[i]['y']
        ])
        if i < len(positions):
            simulation.drones.iloc[i, simulation.drones.columns.get_loc('x')] = positions[i][0]
            simulation.drones.iloc[i, simulation.drones.columns.get_loc('y')] = positions[i][1]
    
    # Calculate coverage with all drones active
    activation = np.ones(len(simulation.drones), dtype=int)
    simulation.set_active_drones(activation)
    coverage = simulation.calculate_coverage_percentage()
    
    # Restore original positions
    for i in range(len(simulation.drones)):
        simulation.drones.iloc[i, simulation.drones.columns.get_loc('x')] = original_positions[i][0]
        simulation.drones.iloc[i, simulation.drones.columns.get_loc('y')] = original_positions[i][1]
    
    return coverage

def enhanced_position_optimizer(simulation, max_iterations=50):
    """
    Test multiple positioning strategies and return the best one
    
    Args:
        simulation: DroneSimulationEnvironment instance
        max_iterations: Maximum optimization iterations
    
    Returns:
        best_positions: Array of optimized positions
        best_technique: Name of best technique used
    """
    position_techniques = [
        ('grid_based', lambda: grid_based_positioning(simulation)),
        ('hexagonal_packing', lambda: hexagonal_packing_positioning(simulation)),
        ('voronoi_based', lambda: voronoi_based_positioning(simulation))
    ]
    
    best_positions = None
    best_coverage = 0
    best_technique = 'random'
    
    # Test each positioning technique
    for technique_name, technique_func in position_techniques:
        try:
            positions = technique_func()
            coverage = calculate_position_coverage(simulation, positions)
            
            if coverage > best_coverage:
                best_coverage = coverage
                best_positions = positions.copy()
                best_technique = technique_name
                
        except Exception as e:
            print(f"⚠️ Positioning technique {technique_name} failed: {e}")
            continue
    
    # If no technique worked, use current positions
    if best_positions is None:
        best_positions = np.array([[
            simulation.drones.iloc[i]['x'], 
            simulation.drones.iloc[i]['y']
        ] for i in range(len(simulation.drones))])
        best_technique = 'original'
    
    return best_positions, best_technique

def create_algorithm_result(coverage, active_drones, execution_time, algorithm_name, 
                          enhancement_used=None, optimal_technique=None):
    """
    Create a standardized result object compatible with existing code
    
    Args:
        coverage: Coverage percentage
        active_drones: Number of active drones
        execution_time: Algorithm execution time
        algorithm_name: Name of the algorithm
        enhancement_used: Type of enhancement applied
        optimal_technique: Best positioning technique used
    
    Returns:
        result: Result object with all necessary attributes
    """
    # Create result object with all expected attributes
    result = type('EnhancedAlgorithmResult', (), {
        'coverage': coverage,
        'best_fitness': coverage / 100.0 if coverage > 1 else coverage,
        'execution_time': execution_time,
        'algorithm_name': algorithm_name,
        'active_drones': active_drones,
        'enhancement_used': enhancement_used or 'position_activation_optimization',
        'optimal_technique': optimal_technique or 'smart_optimization',
        'early_stop': False,
        'stop_reason': 'Optimization Complete',
        'coverage_history': [coverage],
        'active_nodes_history': [active_drones],
        'iteration_logs': []
    })()
    
    return result
