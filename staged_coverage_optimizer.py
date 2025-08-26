"""
ENHANCED STAGED COVERAGE OPTIMIZER - Gap Filling & Redundancy Removal
Addresses coverage gaps and removes redundant drones for optimal efficiency
"""

import numpy as np
from scipy.spatial.distance import cdist

def analyze_coverage_gaps_and_redundancy(solution, simulation):
    """
    Analyze coverage gaps and identify redundant drones
    Returns: gaps, redundant_drones, coverage_efficiency
    """
    if hasattr(solution, 'ndim') and solution.ndim == 2:
        # Position-based solution
        active_positions = []
        active_indices = []
        for i, drone_state in enumerate(solution):
            if drone_state[2] >= 0.5:  # Active
                active_positions.append([drone_state[0], drone_state[1]])
                active_indices.append(i)
        active_positions = np.array(active_positions)
    else:
        # Binary activation array
        active_indices = np.where(solution >= 0.5)[0]
        active_positions = np.array([[simulation.drones.iloc[i]['x'], simulation.drones.iloc[i]['y']] 
                                   for i in active_indices])
    
    if len(active_positions) == 0:
        return [], [], 0.0
    
    # Create detailed coverage map
    grid_density = 100  # Higher resolution for gap analysis
    x_points = np.linspace(0, simulation.width, grid_density)
    y_points = np.linspace(0, simulation.height, grid_density)
    
    # Track which drone covers each point
    coverage_map = np.zeros((grid_density, grid_density), dtype=int)
    drone_coverage_count = np.zeros(len(active_positions))
    
    gaps = []
    covered_by_multiple = []
    
    for i, x in enumerate(x_points):
        for j, y in enumerate(y_points):
            point = np.array([x, y])
            covering_drones = []
            
            for drone_idx, drone_pos in enumerate(active_positions):
                distance = np.linalg.norm(point - drone_pos)
                if distance <= simulation.sensing_range:
                    covering_drones.append(drone_idx)
                    drone_coverage_count[drone_idx] += 1
            
            if len(covering_drones) == 0:
                gaps.append((x, y))
                coverage_map[i, j] = 0  # Uncovered
            elif len(covering_drones) == 1:
                coverage_map[i, j] = 1  # Single coverage
            else:
                coverage_map[i, j] = len(covering_drones)  # Multiple coverage
                covered_by_multiple.append((x, y, covering_drones))
    
    # Identify redundant drones (contribute little unique coverage)
    redundant_drones = []
    for drone_idx in range(len(active_positions)):
        if drone_coverage_count[drone_idx] == 0:
            redundant_drones.append(active_indices[drone_idx])
        elif drone_coverage_count[drone_idx] < (grid_density * grid_density) * 0.01:  # Less than 1% unique contribution
            # Check if removing this drone creates significant gaps
            temp_coverage = simulate_coverage_without_drone(active_positions, drone_idx, x_points, y_points, simulation.sensing_range)
            if temp_coverage > 0.95:  # Still maintains high coverage
                redundant_drones.append(active_indices[drone_idx])
    
    # Calculate coverage efficiency
    total_coverage = np.sum(coverage_map > 0) / (grid_density * grid_density)
    overlap_ratio = np.sum(coverage_map > 1) / max(1, np.sum(coverage_map > 0))
    efficiency = total_coverage / (1 + overlap_ratio)
    
    return gaps, redundant_drones, efficiency, coverage_map

def simulate_coverage_without_drone(active_positions, exclude_drone_idx, x_points, y_points, sensing_range):
    """Simulate coverage without a specific drone"""
    covered_points = 0
    total_points = len(x_points) * len(y_points)
    
    for x in x_points:
        for y in y_points:
            point = np.array([x, y])
            for drone_idx, drone_pos in enumerate(active_positions):
                if drone_idx == exclude_drone_idx:
                    continue
                distance = np.linalg.norm(point - drone_pos)
                if distance <= sensing_range:
                    covered_points += 1
                    break
    
    return covered_points / total_points

def staged_gap_filling_optimization(solution, simulation, max_relocations=5):
    """
    Staged algorithm to fill gaps and remove redundancy
    """
    print("🎯 Starting Staged Gap Filling & Redundancy Removal...")
    
    # Analyze current state
    gaps, redundant_drones, efficiency, coverage_map = analyze_coverage_gaps_and_redundancy(solution, simulation)
    
    print(f"📊 Initial Analysis:")
    print(f"   • Coverage Gaps: {len(gaps)}")
    print(f"   • Redundant Drones: {len(redundant_drones)}")
    print(f"   • Coverage Efficiency: {efficiency:.2f}")
    
    if len(gaps) == 0 and len(redundant_drones) == 0:
        print("✅ Already optimally configured!")
        return solution
    
    # Create optimized solution
    optimized_solution = solution.copy()
    
    # Phase 1: Remove redundant drones
    if len(redundant_drones) > 0:
        print(f"🔧 Phase 1: Removing {len(redundant_drones)} redundant drones...")
        for drone_idx in redundant_drones:
            if hasattr(optimized_solution, 'ndim') and optimized_solution.ndim == 2:
                optimized_solution[drone_idx, 2] = 0  # Deactivate
            else:
                optimized_solution[drone_idx] = 0  # Deactivate
    
    # Phase 2: Fill critical gaps by repositioning or activating drones
    if len(gaps) > 0:
        print(f"🎯 Phase 2: Filling {len(gaps)} coverage gaps...")
        
        # Find inactive drones for potential activation
        if hasattr(optimized_solution, 'ndim') and optimized_solution.ndim == 2:
            inactive_indices = [i for i, drone in enumerate(optimized_solution) if drone[2] < 0.5]
        else:
            inactive_indices = [i for i, active in enumerate(optimized_solution) if active < 0.5]
        
        # Priority-sort gaps by importance (center gaps more critical)
        center_x, center_y = simulation.width / 2, simulation.height / 2
        gap_priorities = []
        for gap_x, gap_y in gaps:
            # Distance from center (closer = higher priority)
            center_distance = np.sqrt((gap_x - center_x)**2 + (gap_y - center_y)**2)
            # Number of nearby gaps (more isolated = higher priority)
            nearby_gaps = sum(1 for gx, gy in gaps if np.sqrt((gap_x - gx)**2 + (gap_y - gy)**2) < simulation.sensing_range)
            priority = 1.0 / (1 + center_distance * 0.1) + nearby_gaps * 0.1
            gap_priorities.append((gap_x, gap_y, priority))
        
        # Sort by priority (highest first)
        gap_priorities.sort(key=lambda x: x[2], reverse=True)
        
        # Fill critical gaps
        relocations = 0
        for gap_x, gap_y, priority in gap_priorities[:max_relocations]:
            if len(inactive_indices) > 0:
                # Activate and position a drone at the gap
                drone_idx = inactive_indices.pop(0)
                if hasattr(optimized_solution, 'ndim') and optimized_solution.ndim == 2:
                    optimized_solution[drone_idx, 0] = gap_x
                    optimized_solution[drone_idx, 1] = gap_y
                    optimized_solution[drone_idx, 2] = 1  # Activate
                else:
                    # For binary activation, find closest drone to reposition
                    optimized_solution[drone_idx] = 1  # Activate
                    simulation.drones.iloc[drone_idx, simulation.drones.columns.get_loc('x')] = gap_x
                    simulation.drones.iloc[drone_idx, simulation.drones.columns.get_loc('y')] = gap_y
                
                relocations += 1
                print(f"   ✅ Filled gap at ({gap_x:.1f}, {gap_y:.1f}) with drone {drone_idx}")
    
    # Phase 3: Validate and fine-tune
    final_gaps, final_redundant, final_efficiency, _ = analyze_coverage_gaps_and_redundancy(optimized_solution, simulation)
    
    print(f"🎉 Optimization Complete:")
    print(f"   • Gaps Remaining: {len(final_gaps)} (was {len(gaps)})")
    print(f"   • Redundant Drones: {len(final_redundant)} (was {len(redundant_drones)})")
    print(f"   • Final Efficiency: {final_efficiency:.2f} (was {efficiency:.2f})")
    print(f"   • Improvement: {((final_efficiency - efficiency) / efficiency * 100):.1f}%")
    
    return optimized_solution

def enhanced_coverage_first_fitness(solution, simulation, target_coverage=0.99, gap_penalty_weight=2.0, overlap_penalty_weight=0.5):
    """
    Enhanced fitness function that heavily penalizes gaps and rewards efficiency
    """
    # Basic coverage calculation
    coverage = calculate_coverage_with_solution(solution, simulation)
    
    # Analyze gaps and efficiency
    gaps, redundant_drones, efficiency, coverage_map = analyze_coverage_gaps_and_redundancy(solution, simulation)
    
    # Calculate penalties
    gap_penalty = len(gaps) * gap_penalty_weight  # Heavy penalty for gaps
    redundancy_penalty = len(redundant_drones) * 0.5  # Penalty for redundant drones
    
    # Calculate active drone efficiency
    if hasattr(solution, 'ndim') and solution.ndim == 2:
        active_count = np.sum(solution[:, 2] >= 0.5)
    else:
        active_count = np.sum(solution >= 0.5)
    
    total_drones = len(solution)
    efficiency_bonus = (total_drones - active_count) / total_drones * 0.1  # Bonus for using fewer drones
    
    # Enhanced fitness calculation
    if coverage >= target_coverage:
        # Reward achieving target with efficiency bonuses
        fitness = coverage * 100 + efficiency_bonus * 10 - gap_penalty - redundancy_penalty
    else:
        # Heavy penalty for not meeting target coverage
        coverage_deficit = (target_coverage - coverage) * 100
        fitness = coverage * 100 - coverage_deficit * 2 - gap_penalty - redundancy_penalty
    
    return max(0, fitness)  # Ensure non-negative fitness
