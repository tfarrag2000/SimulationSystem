# Smart optimizer availability flag (for gap/redundancy analysis)
try:
    from staged_coverage_optimizer import (
        analyze_coverage_gaps_and_redundancy,
        staged_gap_filling_optimization,
        enhanced_coverage_first_fitness
    )
    SMART_OPTIMIZER_AVAILABLE = True
    STAGED_OPTIMIZER_AVAILABLE = True
except ImportError:
    SMART_OPTIMIZER_AVAILABLE = False
    STAGED_OPTIMIZER_AVAILABLE = False
# === STANDARD ALGORITHM FUNCTIONS ===
def standard_greedy(simulation, **kwargs):
    return greedy_optimization(simulation, **kwargs)

def standard_genetic(simulation, **kwargs):
    return genetic_algorithm(simulation, **kwargs)

def standard_pso(simulation, **kwargs):
    return particle_swarm_optimization(simulation, **kwargs)

def standard_sa(simulation, **kwargs):
    return simulated_annealing(simulation, **kwargs)

def standard_ga_sa(simulation, **kwargs):
    return genetic_algorithm_with_sa(simulation, **kwargs)

def standard_gwo(simulation, **kwargs):
    return grey_wolf_optimizer(simulation, **kwargs)

def standard_mrfo(simulation, **kwargs):
    return manta_ray_foraging_optimization(simulation, **kwargs)

def standard_hexagonal(simulation, **kwargs):
    return smart_hexagonal_optimization(simulation, **kwargs)

# === STAGED ALGORITHM FUNCTIONS ===
def staged_greedy(simulation, **kwargs):
    return staged_optimization_wrapper(greedy_optimization, simulation, **kwargs)

def staged_genetic(simulation, **kwargs):
    return staged_optimization_wrapper(genetic_algorithm, simulation, **kwargs)

def staged_pso(simulation, **kwargs):
    return staged_optimization_wrapper(particle_swarm_optimization, simulation, **kwargs)

def staged_sa(simulation, **kwargs):
    return staged_optimization_wrapper(simulated_annealing, simulation, **kwargs)

def staged_ga_sa(simulation, **kwargs):
    return staged_optimization_wrapper(genetic_algorithm_with_sa, simulation, **kwargs)

def staged_gwo(simulation, **kwargs):
    return staged_optimization_wrapper(grey_wolf_optimizer, simulation, **kwargs)

def staged_mrfo(simulation, **kwargs):
    return staged_optimization_wrapper(manta_ray_foraging_optimization, simulation, **kwargs)

def staged_hexagonal(simulation, **kwargs):
    return staged_optimization_wrapper(smart_hexagonal_optimization, simulation, **kwargs)

# === EXPORT LIST ===
__all__ = [
    # Standard algorithms
    'standard_greedy', 'standard_genetic', 'standard_pso', 'standard_sa', 
    'standard_ga_sa', 'standard_gwo', 'standard_mrfo', 'standard_hexagonal',
    # Staged algorithms  
    'staged_greedy', 'staged_genetic', 'staged_pso', 'staged_sa', 
    'staged_ga_sa', 'staged_gwo', 'staged_mrfo', 'staged_hexagonal',
    # Utility functions
    'get_version_info', 'get_parallel_support', 'AlgorithmResult'
]
"""
DRONE OPTIMIZATION ALGORITHMS - ENHANCED VERSION WITH STAGED OPTIMIZATION
Multi-algorithm optimization suite for energy-efficient drone coverage optimization

Version: 5.0.0 - Added Staged Gap Filling & Redundancy Removal
Last Updated: 2025-09-05 - Code Quality Improvements
Author: Drone Optimization System

RECENT IMPROVEMENTS (2025-09-05):
✅ Fixed duplicate import logic - Consolidated staged optimizer imports  
✅ Fixed inconsistent export list - Added missing hexagonal algorithms
✅ Standardized parameter handling - Added OptimizationParams classes
✅ Improved documentation - Added comprehensive docstrings with examples
✅ Eliminated magic numbers - Extracted constants for maintainability

ARCHITECTURE:
- 16 algorithms total: 8 standard + 8 staged variants
- Universal staged optimization wrapper with multi-phase optimization
- Parallel processing support with automatic worker scaling
- Comprehensive parameter standardization across algorithms
- Constants-based configuration for easy tuning
"""

import numpy as np
import random
from multiprocessing import Pool, cpu_count
import concurrent.futures
import time
import threading
from functools import partial
from scipy.spatial.distance import cdist

# === ALGORITHM CONSTANTS ===
# Staging and optimization parameters
COVERAGE_PHASE_RATIO = 0.7  # 70% of iterations for coverage maximization
ENERGY_PHASE_RATIO = 0.3    # 30% of iterations for energy optimization
POSITION_REFINEMENT_ITERATIONS = 30
OPTIMAL_GRID_SPACING_MULTIPLIER = 1.8  # Optimal hexagonal grid spacing multiplier
DEFAULT_SENSING_OVERLAP = 0.2  # Default overlap weight for coverage calculations
MINIMUM_COVERAGE_THRESHOLD = 0.95  # Minimum coverage to maintain in energy phase
SMALL_POSITION_ADJUSTMENT_STD = 3.0  # INCREASED from 2.0 for more exploration

# Parallel processing limits
MAX_RECOMMENDED_WORKERS = 8  # Maximum recommended parallel workers
WORKER_TO_POPULATION_RATIO = 4  # Population size divided by this for worker count

# Fitness function weights
DEFAULT_COVERAGE_WEIGHT = 0.6   
DEFAULT_ENERGY_WEIGHT = 0.2  
DEFAULT_OVERLAP_WEIGHT = 0.2

# Version information
__version__ = "5.0.0"
__author__ = "Advanced Drone Optimization System with Staged Optimization"
__last_updated__ = "2025-08-25"
__description__ = "Staged Optimization with Universal Algorithm Intelligence and Enhanced AI"

# === STANDARDIZED PARAMETER CLASSES ===
class OptimizationParams:
    """Standardized parameters for all optimization algorithms"""
    def __init__(self, 
                 max_iterations: int = 300,
                 population_size: int = 50,
                 desired_coverage: float = 0.90,
                 parallel: bool = True,
                 max_workers: int = None):
        self.max_iterations = max_iterations
        self.population_size = population_size  
        self.desired_coverage = desired_coverage
        self.parallel = parallel
        self.max_workers = max_workers or min(cpu_count(), MAX_RECOMMENDED_WORKERS)

class PSOParams(OptimizationParams):
    """Particle Swarm Optimization specific parameters"""
    def __init__(self, inertia: float = 0.5, cognitive_weight: float = 1.5, 
                 social_weight: float = 1.5, **kwargs):
        super().__init__(**kwargs)
        self.inertia = inertia
        self.cognitive_weight = cognitive_weight
        self.social_weight = social_weight

class GAParams(OptimizationParams):
    """Genetic Algorithm specific parameters"""
    def __init__(self, mutation_rate: float = 0.1, crossover_rate: float = 0.8,
                 elitism: int = 10, **kwargs):
        super().__init__(**kwargs)
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism = elitism

class SAParams(OptimizationParams):
    """Simulated Annealing specific parameters"""
    def __init__(self, initial_temperature: float = 100.0, cooling_rate: float = 0.95,
                 min_temperature: float = 0.01, **kwargs):
        super().__init__(**kwargs)
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.min_temperature = min_temperature

def get_version_info():
    """Returns version information as a dictionary"""
    return {
        'version': __version__,
        'author': __author__,
        'last_updated': __last_updated__,
        'description': __description__,
        'parallel_support': True,
        'max_workers': cpu_count(),
        'algorithms': [
            'GreedyAlgorithm (Sequential)',
            'GeneticAlgorithm (Parallel)',
            'ParticleSwarmOptimization (Parallel)', 
            'SimulatedAnnealing (Sequential)',
            'HybridGASA (Parallel)',
            'GreyWolfOptimizer (Parallel)',
            'MantaRayForaging (Parallel)'
        ]
    }

def get_parallel_support():
    """Returns information about parallel processing capabilities"""
    return {
        'cpu_count': cpu_count(),
        'recommended_workers': MAX_RECOMMENDED_WORKERS,
        'parallel_algorithms': ['ga', 'pso', 'ga_sa', 'gwo', 'mrfo'],
        'sequential_algorithms': ['greedy', 'sa']
    }

def staged_optimization_wrapper(algorithm_func, simulation, desired_coverage=0.99, staged_mode=True, coverage_first=True, **kwargs):
    """
    UNIVERSAL STAGED OPTIMIZATION WRAPPER - COVERAGE-FIRST VERSION
    
    Applies multi-stage optimization to ANY algorithm with the following phases:
    Stage 1: COVERAGE MAXIMIZATION - Achieve maximum possible coverage
    Stage 2: Energy Optimization - Optimize energy while maintaining high coverage  
    Stage 3: Gap Filling & Redundancy Removal - Fine-tune for optimal efficiency
    
    Args:
        algorithm_func: The original algorithm function (pso, ga, sa, etc.)
        simulation: The simulation environment (DroneSimulationEnvironment)
        desired_coverage (float): Target coverage threshold (default: 0.99 for maximum coverage)
        staged_mode (bool): Enable staged multi-phase optimization (default: True)
        coverage_first (bool): Prioritize coverage over energy efficiency (default: True)
        **kwargs: Algorithm-specific parameters (iterations, population_size, etc.)
    
    Returns:
        tuple: (activation_array, enhanced_algorithm_result)
            - activation_array: Binary array indicating active/inactive drones
            - enhanced_algorithm_result: AlgorithmResult with multi-stage metrics
            
    Example:
        >>> activation, result = staged_optimization_wrapper(
        ...     genetic_algorithm, simulation, desired_coverage=0.95,
        ...     population_size=50, num_generations=200
        ... )
        >>> print(f"Final coverage: {result.coverage:.1f}%")
        
    Note:
        Uses constants from COVERAGE_PHASE_RATIO and MINIMUM_COVERAGE_THRESHOLD
        for phase distribution and coverage maintenance.
    """
    if not staged_mode:
        # Use original algorithm with coverage-first fitness if enabled
        if coverage_first:
            kwargs['fitness_function'] = 'coverage_first'
        return algorithm_func(simulation, desired_coverage=desired_coverage, **kwargs)
    
    print(f"🎯 STAGED COVERAGE-FIRST OPTIMIZATION: {algorithm_func.__name__.upper()}")
    print(f"   Stage 1: COVERAGE MAXIMIZATION (Target: {desired_coverage*100:.1f}%)")
    print(f"   Stage 2: Energy Optimization (Maintain coverage)")
    print(f"   Stage 3: Gap Filling & Redundancy Removal")
    
    start_time = time.time()
    
    # STAGE 1: COVERAGE MAXIMIZATION OPTIMIZATION
    print(f"🎯 Stage 1: Coverage Maximization Optimization ({kwargs.get('iterations', 50)} iterations)")
    
    # Modify kwargs for COVERAGE MAXIMIZATION focus
    phase1_kwargs = kwargs.copy()
    phase1_kwargs['fitness_function'] = 'coverage_first'  # Use coverage-first fitness
    
    # Adjust iterations for two-phase approach
    if 'iterations' in phase1_kwargs:
        total_iterations = phase1_kwargs['iterations']
        phase1_kwargs['iterations'] = int(total_iterations * COVERAGE_PHASE_RATIO)
    elif 'num_generations' in phase1_kwargs:
        total_generations = phase1_kwargs['num_generations']
        phase1_kwargs['num_generations'] = int(total_generations * COVERAGE_PHASE_RATIO)
    elif 'num_iterations' in phase1_kwargs:
        total_iterations = phase1_kwargs['num_iterations']
        phase1_kwargs['num_iterations'] = int(total_iterations * COVERAGE_PHASE_RATIO)
    
    # Run Phase 1 with COVERAGE MAXIMIZATION focus
    phase1_activation, phase1_result = algorithm_func(
        simulation, desired_coverage=desired_coverage, **phase1_kwargs
    )
    
    phase1_coverage = getattr(phase1_result, 'coverage', 0)
    if phase1_coverage > 1:  # Handle percentage format
        phase1_coverage = phase1_coverage / 100
    
    phase1_active = np.sum(phase1_activation >= 0.5) if hasattr(phase1_activation, 'ndim') else np.sum(phase1_activation)
    
    print(f"✅ Phase 1 Complete: {phase1_coverage*100:.1f}% coverage with {phase1_active} drones")
    
    # PHASE 2: ENERGY OPTIMIZATION WHILE MAINTAINING COVERAGE
    print(f"⚡ Phase 2: Energy Optimization (Maintain {phase1_coverage*100:.1f}% coverage)")
    
    # Use Phase 1 result as starting point for Phase 2
    phase2_kwargs = kwargs.copy()
    phase2_kwargs['initial_solution'] = phase1_activation  # Start from Phase 1 result
    phase2_kwargs['minimum_coverage'] = max(MINIMUM_COVERAGE_THRESHOLD, phase1_coverage)  # Don't go below Phase 1 coverage
    
    # Remaining iterations for energy optimization
    if 'iterations' in phase2_kwargs:
        phase2_kwargs['iterations'] = total_iterations - phase1_kwargs['iterations']
    elif 'num_generations' in phase2_kwargs:
        phase2_kwargs['num_generations'] = total_generations - phase1_kwargs['num_generations']
    elif 'num_iterations' in phase2_kwargs:
        phase2_kwargs['num_iterations'] = total_iterations - phase1_kwargs['num_iterations']
    
    # Set higher coverage target for phase 2
    phase2_target = min(1.0, desired_coverage + 0.1)  # Push for higher coverage
    
    # Run Phase 2 starting from Phase 1 solution
    phase2_activation, phase2_result = algorithm_func(
        simulation, desired_coverage=phase2_target, **phase2_kwargs
    )
    
    # Choose the best result between phases
    phase2_coverage = getattr(phase2_result, 'coverage', 0)
    phase2_active = np.sum(phase2_activation)
    
    # Select best phase based on coverage achievement and efficiency
    if phase2_coverage > phase1_coverage:
        final_activation = phase2_activation
        final_result = phase2_result
        best_phase = 2
        print(f"🏆 Phase 2 Selected: {phase2_coverage:.1f}% coverage with {phase2_active} drones")
    else:
        final_activation = phase1_activation
        final_result = phase1_result
        best_phase = 1
        print(f"🏆 Phase 1 Selected: {phase1_coverage:.1f}% coverage with {phase1_active} drones")
    
    # Enhance result object with smart optimization info
    final_coverage = getattr(final_result, 'coverage', 0)
    final_active = np.sum(final_activation)
    total_drones = len(simulation.drones)
    execution_time = time.time() - start_time
    
    # Create enhanced result object
    enhanced_result = type('SmartAlgorithmResult', (), {
        'coverage': final_coverage,
        'active_drones': final_active,  # Add missing active_drones attribute
        'best_fitness': getattr(final_result, 'best_fitness', 0),
        'execution_time': execution_time,
        'fitness_history': getattr(final_result, 'fitness_history', []),
        'coverage_history': getattr(final_result, 'coverage_history', []),
        'active_nodes_history': getattr(final_result, 'active_nodes_history', []),
        'convergence_iteration': getattr(final_result, 'convergence_iteration', 0),
        'algorithm_name': f'Staged {getattr(final_result, "algorithm_name", algorithm_func.__name__)}',
        'energy_saved_percentage': ((total_drones - final_active) / total_drones * 100),
        'staged_mode': True,
        'best_phase': best_phase,
        'phase1_coverage': phase1_coverage,
        'phase1_active': phase1_active,
        'phase2_coverage': phase2_coverage,
        'phase2_active': phase2_active,
        'optimization_phases': {
            'phase1': {
                'coverage': phase1_coverage,
                'active_drones': phase1_active,
                'focus': 'Energy Efficiency'
            },
            'phase2': {
                'coverage': phase2_coverage,
                'active_drones': phase2_active,
                'focus': 'Coverage Maximization'
            }
        }
    })()
    
    print(f"🎉 SMART {algorithm_func.__name__.upper()} Complete:")
    print(f"   Final Coverage: {final_coverage:.1f}%")
    print(f"   Active Drones: {final_active}/{total_drones}")
    print(f"   Energy Saved: {((total_drones - final_active) / total_drones * 100):.1f}%")
    print(f"   Best Phase: {best_phase}")
    print(f"   Total Execution Time: {execution_time:.2f}s")
    
    return final_activation, enhanced_result

def parallel_fitness_evaluation(population, fitness_func, max_workers=None):
    """Parallel fitness evaluation for population-based algorithms"""
    if max_workers is None:
        max_workers = min(cpu_count(), len(population))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        fitness_scores = list(executor.map(fitness_func, population))
    return fitness_scores

def parallel_population_operations(population, operation_func, max_workers=None):
    """Parallel operations on population (mutations, crossovers, etc.)"""
    if max_workers is None:
        max_workers = min(cpu_count(), len(population))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(operation_func, population))
    return results

class AlgorithmResult:
    """Class to store algorithm results and metadata"""
    def __init__(self, best_solution, fitness_history, coverage, active_nodes, 
                 overlap, execution_time, algorithm_name, parameters,
                 coverage_history=None, overlap_history=None, active_nodes_history=None,
                 early_stop=False, stop_reason=None, iteration_logs=None):
        self.best_solution = best_solution
        self.fitness_history = fitness_history
        self.coverage = coverage
        self.active_nodes = active_nodes
        self.overlap = overlap
        self.execution_time = execution_time
        self.algorithm_name = algorithm_name
        self.parameters = parameters
        self.timestamp = time.time()
        self.coverage_history = coverage_history or []
        self.overlap_history = overlap_history or []
        self.active_nodes_history = active_nodes_history or []
        self.early_stop = early_stop
        self.stop_reason = stop_reason
        self.iteration_logs = iteration_logs or []

def convert_to_binary_activation(particle_solution, simulation):
    """Convert particle solution to binary activation array compatible with simulation"""
    activation = np.zeros(len(simulation.drones), dtype=int)
    # Ensure particle_solution is a 2D array before processing
    if particle_solution.ndim == 1:
        # Reshape if it's a flat array from GWO
        particle_solution = particle_solution.reshape((len(simulation.drones), 3))

    for i, particle in enumerate(particle_solution):
        activation[i] = 1 if particle[2] >= 0.5 else 0
    return activation

# ===== ACTIVE/SLEEP DRONE MANAGEMENT SYSTEM =====

def calculate_energy_efficiency_fitness(solution, simulation, target_coverage=0.95, 
                                       w_coverage=100, w_energy=50, w_overlap=10):
    """
    Enhanced fitness function for Active/Sleep drone management
    Objectives: Achieve target coverage with minimum active drones (energy efficiency)
    
    Args:
        solution: Drone positions and activation states
        simulation: Simulation environment
        target_coverage: Desired coverage percentage (default 95%)
        w_coverage: Weight for coverage component
        w_energy: Weight for energy efficiency (fewer active drones)
        w_overlap: Weight for overlap penalty
    
    Returns:
        fitness: Higher values indicate better solutions
    """
    # Calculate coverage
    coverage = calculate_coverage_with_solution(solution, simulation)
    
    # Calculate active drones ratio
    if hasattr(solution, 'ndim') and solution.ndim == 2:
        active_count = np.sum(solution[:, 2] >= 0.5)
    else:
        # Handle 1D binary activation arrays
        active_count = np.sum(solution >= 0.5)
    
    total_drones = len(simulation.drones)
    energy_efficiency = 1 - (active_count / total_drones)  # Higher when fewer drones active
    
    # Calculate overlap penalty
    overlap = calculate_overlap_penalty(solution, simulation)
    
    # Multi-objective fitness calculation
    # Priority 1: Meet coverage target
    coverage_score = coverage * w_coverage
    if coverage < target_coverage:
        # Penalty for not meeting target coverage
        coverage_penalty = (target_coverage - coverage) * w_coverage * 2
        coverage_score -= coverage_penalty
    
    # Priority 2: Minimize active drones (maximize energy efficiency)
    energy_score = energy_efficiency * w_energy
    
    # Priority 3: Minimize overlap
    overlap_penalty = overlap * w_overlap
    
    fitness = coverage_score + energy_score - overlap_penalty
    return fitness

def calculate_coverage_first_fitness(solution, simulation, target_coverage=0.99, 
                                    w_coverage=2000, w_bonus=200, w_energy=10, w_overlap=3):
    """
    SMART COVERAGE-FIRST fitness function - Prioritizes maximum coverage with gap analysis
    
    Args:
        solution: Drone positions and activation states
        simulation: Simulation environment
        target_coverage: Desired coverage percentage (default 99% for maximum coverage)
        w_coverage: Weight for coverage component (HIGHEST PRIORITY)
        w_bonus: Bonus weight for exceeding coverage targets
        w_energy: Weight for energy efficiency (SECONDARY)
        w_overlap: Weight for overlap penalty (MINIMAL)
    
    Returns:
        fitness: Higher values indicate better solutions with coverage as primary goal
    """
    # Calculate coverage with enhanced gap detection
    coverage = calculate_coverage_with_solution(solution, simulation)
    
    # Calculate active drones information
    if hasattr(solution, 'ndim') and solution.ndim == 2:
        active_count = np.sum(solution[:, 2] >= 0.5)
        active_positions = solution[solution[:, 2] >= 0.5, :2]
    else:
        # Handle 1D binary activation arrays
        active_count = np.sum(solution >= 0.5)
        active_indices = np.where(solution >= 0.5)[0]
        active_positions = np.array([[simulation.drones.iloc[i]['x'], simulation.drones.iloc[i]['y']] 
                                   for i in active_indices])
    
    total_drones = len(simulation.drones)
    
    # COVERAGE FIRST: Maximum weight for coverage achievement
    coverage_score = coverage * w_coverage
    
    # SMART GAP ANALYSIS: Heavy penalty for coverage gaps
    gap_penalty = 0
    redundancy_penalty = 0
    smart_bonus = 0
    
    if SMART_OPTIMIZER_AVAILABLE and len(active_positions) > 0:
        try:
            gaps, redundant_drones, efficiency_score, _ = analyze_coverage_gaps_and_redundancy(solution, simulation)
            
            # CRITICAL: Heavy penalty for coverage gaps (gaps are coverage failures)
            gap_penalty = len(gaps) * w_coverage * 0.1  # Each gap reduces coverage score significantly
            
            # EFFICIENCY: Penalty for redundant drones
            redundancy_penalty = len(redundant_drones) * w_energy * 0.5
            
            # BONUS: Reward for high efficiency
            smart_bonus = efficiency_score * w_bonus * 0.2
            
            # Additional penalties for gap clusters (critical coverage failures)
            if len(gaps) > 0:
                # Find gap clusters (nearby uncovered areas)
                gap_clusters = 0
                processed_gaps = set()
                
                for i, (gx, gy) in enumerate(gaps):
                    if i in processed_gaps:
                        continue
                    
                    cluster_size = 1
                    processed_gaps.add(i)
                    
                    for j, (gx2, gy2) in enumerate(gaps[i+1:], i+1):
                        if j in processed_gaps:
                            continue
                        
                        distance = np.sqrt((gx - gx2)**2 + (gy - gy2)**2)
                        if distance <= simulation.sensing_range * 0.5:  # Nearby gaps
                            cluster_size += 1
                            processed_gaps.add(j)
                    
                    if cluster_size > 1:
                        gap_clusters += 1
                
                # Extra penalty for gap clusters (major coverage failures)
                gap_penalty += gap_clusters * w_coverage * 0.05
                
        except Exception as e:
            # Fallback if smart analysis fails
            print(f"⚠️ Smart analysis failed: {e}")
    
    # COVERAGE BONUS: Reward for exceeding targets
    if coverage >= 0.95:
        coverage_bonus = (coverage - 0.95) * w_bonus * 10  # Big bonus for high coverage
        coverage_score += coverage_bonus
    
    if coverage >= 0.98:
        coverage_score += w_bonus * 5  # Extra bonus for excellent coverage
    
    # SECONDARY: Energy consideration (much lower weight)
    energy_efficiency = 1 - (active_count / total_drones)
    energy_score = energy_efficiency * w_energy
    
    # MINIMAL: Traditional overlap penalty (very low weight)
    overlap = calculate_overlap_penalty(solution, simulation)
    overlap_penalty = overlap * w_overlap
    
    # SMART COVERAGE-FIRST FITNESS: Coverage dominates, gaps heavily penalized
    fitness = (coverage_score + 
               energy_score + 
               smart_bonus - 
               gap_penalty - 
               redundancy_penalty - 
               overlap_penalty)
    
    # Ensure coverage gaps are heavily discouraged
    if gap_penalty > 0:
        fitness = max(fitness * 0.9, 0)  # Reduction for gaps
    
    return max(fitness, 0)  # Ensure non-negative

def calculate_coverage_with_solution(solution, simulation):
    """Calculate coverage percentage for a given solution with smart gap detection"""
    if hasattr(solution, 'ndim') and solution.ndim == 2:
        # Position-based solution (x, y, activation)
        active_positions = []
        for i, drone_state in enumerate(solution):
            if drone_state[2] >= 0.5:  # Active
                active_positions.append([drone_state[0], drone_state[1]])
        active_positions = np.array(active_positions)
    else:
        # Binary activation array
        active_indices = np.where(solution >= 0.5)[0]
        active_positions = np.array([[simulation.drones.iloc[i]['x'], simulation.drones.iloc[i]['y']] 
                                   for i in active_indices])
    
    if len(active_positions) == 0:
        return 0.0
    
    # Calculate coverage using enhanced grid-based approach
    grid_size = 75
    x_points = np.linspace(0, simulation.width, grid_size)
    y_points = np.linspace(0, simulation.height, grid_size)
    
    covered_points = 0
    total_points = grid_size * grid_size
    gap_clusters = []  # Track gap locations for analysis
    
    for i, x in enumerate(x_points):
        for j, y in enumerate(y_points):
            point = np.array([x, y])
            is_covered = False
            # Check if point is covered by any active drone
            for drone_pos in active_positions:
                distance = np.linalg.norm(point - drone_pos)
                if distance <= simulation.sensing_range:
                    covered_points += 1
                    is_covered = True
                    break
            
            # Track uncovered points for gap analysis
            if not is_covered:
                gap_clusters.append((x, y))
    
    # Store gap information for smart optimization
    if hasattr(simulation, 'last_gap_analysis'):
        simulation.last_gap_analysis = {
            'gaps': gap_clusters,
            'coverage_ratio': covered_points / total_points,
            'active_drones': len(active_positions)
        }
    
    return covered_points / total_points

def calculate_overlap_penalty(solution, simulation):
    """Calculate overlap penalty between active drones"""
    if hasattr(solution, 'ndim') and solution.ndim == 2:
        # Position-based solution
        active_positions = []
        for drone_state in solution:
            if drone_state[2] >= 0.5:  # Active
                active_positions.append([drone_state[0], drone_state[1]])
        active_positions = np.array(active_positions)
    else:
        # Binary activation array
        active_indices = np.where(solution >= 0.5)[0]
        active_positions = np.array([[simulation.drones.iloc[i]['x'], simulation.drones.iloc[i]['y']] 
                                   for i in active_indices])
    
    if len(active_positions) <= 1:
        return 0.0
    
    overlap_penalty = 0.0
    sensing_range = simulation.sensing_range
    
    for i in range(len(active_positions)):
        for j in range(i + 1, len(active_positions)):
            distance = np.linalg.norm(active_positions[i] - active_positions[j])
            if distance < 2 * sensing_range:
                # Overlap penalty proportional to overlap amount
                overlap_penalty += 1 - (distance / (2 * sensing_range))
    
    return overlap_penalty

def remove_duplicate_drones(simulation, min_distance_threshold=1.0):
    """
    Remove duplicate drones that are too close to each other
    
    Args:
        simulation: DroneSimulationEnvironment instance
        min_distance_threshold: Minimum distance required between drones
    
    Returns:
        updated_simulation: Simulation with duplicates removed
        removed_count: Number of drones removed
    """
    import pandas as pd
    
    # Get current drone positions
    drone_positions = simulation.drones[['x', 'y']].values
    drone_ids = simulation.drones.index.tolist()
    
    # Find duplicates/near-duplicates
    to_remove = set()
    
    for i in range(len(drone_positions)):
        if i in to_remove:
            continue
            
        for j in range(i + 1, len(drone_positions)):
            if j in to_remove:
                continue
                
            # Calculate distance between drones i and j
            distance = np.linalg.norm(drone_positions[i] - drone_positions[j])
            
            # If too close, mark the second one for removal
            if distance < min_distance_threshold:
                to_remove.add(j)
                print(f"🔧 Found duplicate drone: Drone {drone_ids[j]} too close to Drone {drone_ids[i]} (distance: {distance:.2f})")
    
    # Remove duplicates
    if to_remove:
        # Create new dataframe without duplicates
        keep_indices = [i for i in range(len(simulation.drones)) if i not in to_remove]
        simulation.drones = simulation.drones.iloc[keep_indices].reset_index(drop=True)
        
        # Update drone IDs to be sequential
        simulation.drones['id'] = range(len(simulation.drones))
        simulation.num_drones = len(simulation.drones)
        
        print(f"✅ Removed {len(to_remove)} duplicate drones. Remaining: {len(simulation.drones)} drones")
        return simulation, len(to_remove)
    
    print("✅ No duplicate drones found")
    return simulation, 0

def detect_and_report_duplicates(simulation, min_distance_threshold=1.0):
    """
    Detect and report duplicate drones without removing them
    
    Args:
        simulation: DroneSimulationEnvironment instance
        min_distance_threshold: Minimum distance required between drones
    
    Returns:
        duplicate_pairs: List of duplicate drone pairs
        total_duplicates: Number of duplicate drones found
    """
    drone_positions = simulation.drones[['x', 'y']].values
    drone_ids = simulation.drones.index.tolist()
    
    duplicate_pairs = []
    duplicate_ids = set()
    
    for i in range(len(drone_positions)):
        for j in range(i + 1, len(drone_positions)):
            distance = np.linalg.norm(drone_positions[i] - drone_positions[j])
            
            if distance < min_distance_threshold:
                duplicate_pairs.append({
                    'drone1_id': drone_ids[i],
                    'drone2_id': drone_ids[j],
                    'drone1_pos': drone_positions[i],
                    'drone2_pos': drone_positions[j],
                    'distance': distance
                })
                duplicate_ids.add(drone_ids[i])
                duplicate_ids.add(drone_ids[j])
    
    return duplicate_pairs, len(duplicate_ids)

def optimize_active_sleep_greedy(simulation, target_coverage=0.95, max_attempts=1000):
    """
    Greedy algorithm optimized for Active/Sleep management
    Prioritizes achieving target coverage with minimum active drones
    """
    start_time = time.time()
    
    total_drones = len(simulation.drones)
    best_solution = np.zeros(total_drones)
    best_coverage = 0.0
    best_active_count = total_drones
    
    # Track iteration history
    coverage_history = []
    active_history = []
    fitness_history = []
    
    # Greedy selection: start with most strategic drones
    drone_scores = []
    for i, drone in simulation.drones.iterrows():
        # Score drones based on strategic position (center is better)
        center_x, center_y = simulation.width/2, simulation.height/2
        distance_to_center = np.sqrt((drone['x'] - center_x)**2 + (drone['y'] - center_y)**2)
        max_distance = np.sqrt(center_x**2 + center_y**2)
        centrality_score = 1 - (distance_to_center / max_distance)
        drone_scores.append((i, centrality_score))
    
    # Sort drones by strategic value
    drone_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Iteratively add drones until target coverage is achieved
    current_solution = np.zeros(total_drones)
    
    for attempt in range(min(max_attempts, total_drones)):
        # Try adding the next best drone
        drone_idx = drone_scores[attempt % len(drone_scores)][0]
        if current_solution[drone_idx] == 0:
            current_solution[drone_idx] = 1
            
            # Calculate coverage with current solution
            coverage = calculate_coverage_with_solution(current_solution, simulation)
            active_count = np.sum(current_solution)
            
            # Calculate fitness
            fitness = calculate_energy_efficiency_fitness(current_solution, simulation, target_coverage)
            
            # Track progress
            coverage_history.append(coverage)
            active_history.append(active_count)
            fitness_history.append(fitness)
            
            # Update best solution if coverage target is met with fewer drones
            if coverage >= target_coverage:
                if active_count < best_active_count or (active_count == best_active_count and coverage > best_coverage):
                    best_solution = current_solution.copy()
                    best_coverage = coverage
                    best_active_count = active_count
                    break
            elif coverage > best_coverage:
                best_solution = current_solution.copy()
                best_coverage = coverage
                best_active_count = active_count
    
    execution_time = time.time() - start_time
    
    return AlgorithmResult(
        best_solution=best_solution,
        fitness_history=fitness_history,
        coverage=best_coverage,
        active_nodes=best_active_count,
        overlap=calculate_overlap_penalty(best_solution, simulation),
        execution_time=execution_time,
        algorithm_name="Active/Sleep Greedy",
        parameters={'target_coverage': target_coverage, 'max_attempts': max_attempts},
        coverage_history=coverage_history,
        active_nodes_history=active_history
    )

def get_active_sleep_statistics(solution, simulation):
    """Get detailed statistics for Active/Sleep drone deployment"""
    if hasattr(solution, 'ndim') and solution.ndim == 2:
        active_count = np.sum(solution[:, 2] >= 0.5)
    else:
        active_count = np.sum(solution >= 0.5)
    
    total_drones = len(simulation.drones)
    sleep_count = total_drones - active_count
    
    coverage = calculate_coverage_with_solution(solution, simulation)
    overlap = calculate_overlap_penalty(solution, simulation)
    
    # Energy efficiency metrics
    energy_saved = (sleep_count / total_drones) * 100  # Percentage of energy saved
    coverage_per_drone = coverage / active_count if active_count > 0 else 0
    
    return {
        'total_drones': total_drones,
        'active_drones': active_count,
        'sleeping_drones': sleep_count,
        'coverage_percentage': coverage * 100,
        'overlap_penalty': overlap,
        'energy_saved_percentage': energy_saved,
        'coverage_per_active_drone': coverage_per_drone,
        'energy_efficiency_ratio': coverage / (active_count / total_drones) if active_count > 0 else 0
    }

def parallel_fitness_evaluation(particles, fitness_func, num_processes=None):
    """Evaluate fitness of multiple particles in parallel"""
    if num_processes is None:
        num_processes = min(cpu_count(), len(particles))
    # Using a try-except block to handle potential issues with multiprocessing
    try:
        with Pool(num_processes) as pool:
            fitness_scores = pool.map(fitness_func, particles)
        return fitness_scores
    except Exception as e:
        print(f"Parallel evaluation failed: {e}. Falling back to serial evaluation.")
        return [fitness_func(p) for p in particles]

def greedy_optimization(simulation, desired_coverage=0.85, overlap_weight=DEFAULT_OVERLAP_WEIGHT, energy_weight=DEFAULT_ENERGY_WEIGHT, **kwargs):
    """
    Smart greedy algorithm with grid-based position optimization.
    
    This algorithm uses a two-step approach:
    1. Grid-based position optimization using optimal hexagonal spacing
    2. Iterative position refinement through small random adjustments
    
    Args:
        simulation: DroneSimulationEnvironment instance
        desired_coverage (float): Target coverage percentage (default: 0.85)
        overlap_weight (float): Weight for overlap penalty (default: DEFAULT_OVERLAP_WEIGHT)
        energy_weight (float): Weight for energy efficiency (default: DEFAULT_ENERGY_WEIGHT)
        **kwargs: Additional algorithm parameters
        
    Returns:
        tuple: (activation_array, AlgorithmResult)
            - activation_array: Binary array of drone activations
            - AlgorithmResult: Contains coverage, execution time, and other metrics
            
    Example:
        >>> activation, result = greedy_optimization(sim, desired_coverage=0.90)
        >>> print(f"Coverage: {result.coverage:.1f}% with {result.active_nodes} drones")
        
    Note:
        Uses OPTIMAL_GRID_SPACING_MULTIPLIER and POSITION_REFINEMENT_ITERATIONS constants
        for optimal grid spacing and refinement iterations.
    """
    start_time = time.time()
    
    print("🧠 SMART GREEDY WITH POSITION OPTIMIZATION")
    
    # Step 1: Grid-based position optimization
    width, height = simulation.width, simulation.height
    sensing_radius = simulation.sensing_radius
    num_drones = len(simulation.drones)
    
    # Calculate optimal grid spacing (slight overlap for robustness)
    grid_spacing = sensing_radius * 1.8
    
    # Generate optimal grid positions
    cols = max(1, int(np.ceil(width / grid_spacing)))
    rows = max(1, int(np.ceil(height / grid_spacing)))
    
    positions = []
    for row in range(rows):
        for col in range(cols):
            x = (col + 0.5) * grid_spacing
            y = (row + 0.5) * grid_spacing
            
            if x < width and y < height:
                positions.append([x, y])
    
    # Fill remaining positions if needed
    while len(positions) < num_drones:
        x = np.random.uniform(sensing_radius, width - sensing_radius)
        y = np.random.uniform(sensing_radius, height - sensing_radius)
        positions.append([x, y])
    
    # Take only what we need
    positions = positions[:num_drones]
    
    # Update drone positions
    for i, pos in enumerate(positions):
        simulation.drones.iloc[i, simulation.drones.columns.get_loc('x')] = pos[0]
        simulation.drones.iloc[i, simulation.drones.columns.get_loc('y')] = pos[1]
        simulation.drones.iloc[i, simulation.drones.columns.get_loc('status')] = 'active'
    
    # Step 2: Iterative position refinement
    best_coverage = simulation.calculate_coverage_percentage()
    best_positions = np.array(positions)
    
    print(f"   Initial grid coverage: {best_coverage:.1f}%")
    
    for iteration in range(POSITION_REFINEMENT_ITERATIONS):  # Position refinement iterations
        # Try small position adjustments
        test_positions = best_positions.copy()
        
        # Randomly adjust one drone position
        drone_idx = np.random.randint(len(test_positions))
        adjustment = np.random.normal(0, SMALL_POSITION_ADJUSTMENT_STD, 2)  # Small random adjustment
        test_positions[drone_idx] += adjustment
        
        # Keep within bounds
        test_positions[drone_idx][0] = np.clip(test_positions[drone_idx][0], 0, width)
        test_positions[drone_idx][1] = np.clip(test_positions[drone_idx][1], 0, height)
        
        # Update positions and test coverage
        for i, pos in enumerate(test_positions):
            simulation.drones.iloc[i, simulation.drones.columns.get_loc('x')] = pos[0]
            simulation.drones.iloc[i, simulation.drones.columns.get_loc('y')] = pos[1]
        
        test_coverage = simulation.calculate_coverage_percentage()
        
        # Keep improvement
        if test_coverage > best_coverage:
            best_coverage = test_coverage
            best_positions = test_positions.copy()
        
        # Early stopping if target reached
        if best_coverage >= desired_coverage * 100:
            print(f"   ✅ Target coverage reached at iteration {iteration}")
            break
    
    # Apply best positions
    for i, pos in enumerate(best_positions):
        simulation.drones.iloc[i, simulation.drones.columns.get_loc('x')] = pos[0]
        simulation.drones.iloc[i, simulation.drones.columns.get_loc('y')] = pos[1]
        simulation.drones.iloc[i, simulation.drones.columns.get_loc('status')] = 'active'
    
    final_coverage = simulation.calculate_coverage_percentage()
    execution_time = time.time() - start_time
    
    print(f"   🎯 Final coverage: {final_coverage:.1f}%")
    
    # Create result object
    result = type('SmartResult', (), {
        'coverage': final_coverage,
        'active_drones': num_drones,
        'execution_time': execution_time,
        'algorithm_name': 'Smart Greedy Position Optimization',
        'position_optimization': True
    })()
    
    activation = np.ones(num_drones)
    return activation, result



def genetic_algorithm(simulation, 
                     population_size=50,
                     num_generations=200,
                     mutation_rate=0.1,
                     crossover_rate=0.8,
                     elitism=10,
                     target_coverage=0.95,  # Active/Sleep target coverage
                     parallel_processing=True,  # Enable by default
                     max_workers=None,
                     energy_efficiency_mode=True,  # Enable Active/Sleep optimization
                     smart_mode=False,  # Enable smart two-phase optimization
                     desired_coverage=0.90,  # For smart mode compatibility
                     progress_callback=None):  # NEW: Progress callback support
    """Enhanced Genetic Algorithm with Active/Sleep drone management and Smart Mode"""
    
    if smart_mode:
        # Use universal smart optimization wrapper
        return smart_optimization_wrapper(
            genetic_algorithm, simulation, desired_coverage, smart_mode=False,
            population_size=population_size, num_generations=num_generations,
            mutation_rate=mutation_rate, crossover_rate=crossover_rate,
            elitism=elitism, target_coverage=target_coverage,
            parallel_processing=parallel_processing, max_workers=max_workers,
            energy_efficiency_mode=energy_efficiency_mode
        )
    start_time = time.time()
    AreaWidth, AreaHeight = simulation.width, simulation.height
    SensingRange = simulation.sensing_radius
    NumNodes = len(simulation.drones)
    GridPoints = simulation.grid_points
    NumGridPoints = len(GridPoints)
    
    # Auto-determine optimal worker count
    if max_workers is None:
        max_workers = min(cpu_count(), population_size // WORKER_TO_POPULATION_RATIO, MAX_RECOMMENDED_WORKERS)
    
    print(f"🔄 Enhanced GA initialized: Population={population_size}, Target Coverage={target_coverage*100}%, Energy Efficient={'ON' if energy_efficiency_mode else 'OFF'}")
    
    def fitness(particle):
        if energy_efficiency_mode:
            # Use Active/Sleep energy efficiency fitness
            return calculate_energy_efficiency_fitness(particle, simulation, target_coverage)
        else:
            # Legacy fitness function for compatibility
            coverage = calculate_coverage_with_solution(particle, simulation)
            active_nodes = np.sum(particle[:, 2] >= 0.5)
            overlap = calculate_overlap_penalty(particle, simulation)
            return (DEFAULT_COVERAGE_WEIGHT * coverage * 100 - 
                    DEFAULT_ENERGY_WEIGHT * (active_nodes / NumNodes) * 100 - 
                    DEFAULT_OVERLAP_WEIGHT * overlap)

    # Initialize Population
    population = []
    for _ in range(population_size):
        particle = np.random.rand(NumNodes, 3) * [AreaWidth, AreaHeight, 1]
        population.append(particle)
        
    def mutate(particle):
        particle = particle.copy()
        coord_mask = np.random.rand(NumNodes, 2) < mutation_rate
        particle[:, :2] += (np.random.randn(NumNodes, 2) * 2) * coord_mask
        particle[:, :2] = np.clip(particle[:, :2], 0, [AreaWidth, AreaHeight])
        flip_mask = np.random.rand(NumNodes) < mutation_rate
        particle[flip_mask, 2] = 1 - particle[flip_mask, 2] # Flip activation
        return particle

    def crossover(parent1, parent2):
        if np.random.rand() < crossover_rate:
            cut_point = np.random.randint(1, NumNodes - 1) if NumNodes > 1 else 0
            child1 = np.vstack((parent1[:cut_point], parent2[cut_point:]))
            child2 = np.vstack((parent2[:cut_point], parent1[cut_point:]))
        else:
            child1, child2 = parent1.copy(), parent2.copy()
        return child1, child2

    best_particle = None
    best_fitness = -np.inf
    fitness_history = []
    coverage_history = []
    overlap_history = []
    active_nodes_history = []
    iteration_logs = []
    early_stop = False
    stop_reason = None

    for iteration in range(num_generations):
        # Parallel or sequential fitness evaluation
        if parallel_processing and len(population) > 4:  # Use parallel only if worthwhile
            fitness_scores = parallel_fitness_evaluation(population, fitness, max_workers)
        else:
            fitness_scores = [fitness(p) for p in population]
        
        sorted_indices = np.argsort(fitness_scores)[::-1]
        population = [population[i] for i in sorted_indices]
        fitness_scores = [fitness_scores[i] for i in sorted_indices]

        if fitness_scores[0] > best_fitness:
            best_fitness = fitness_scores[0]
            best_particle = population[0].copy()

        fitness_history.append(best_fitness)
        current_coverage = calculate_coverage_with_solution(best_particle, simulation)
        current_overlap = calculate_overlap_penalty(best_particle, simulation)
        coverage_history.append(current_coverage * 100)  # Convert to percentage
        overlap_history.append(current_overlap)
        active_nodes_history.append(int(np.sum(best_particle[:, 2] >= 0.5)))
        
        # Add iteration log entry
        iteration_logs.append({
            'iteration': iteration + 1,
            'fitness': best_fitness,
            'coverage': coverage_history[-1],
            'algorithm': 'Enhanced GA'
        })
        
        new_population = population[:elitism]
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:min(30, len(population))], 2)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            if len(new_population) < population_size:
                new_population.append(mutate(child2))
        population = new_population[:population_size]
        
        if iteration % 10 == 0:
            print(f"Enhanced GA Iteration {iteration + 1}: Best Fitness = {best_fitness:.2f}, "
                  f"Coverage = {coverage_history[-1]:.2f}%, Active Drones = {active_nodes_history[-1]}")
        
        # Call progress callback if provided
        if progress_callback:
            progress_callback(iteration, num_generations, best_fitness, coverage_history[-1])
                  
        if coverage_history[-1] >= target_coverage * 100:
            print(f"🎯 Target coverage {target_coverage*100}% achieved with {active_nodes_history[-1]} active drones!")
            early_stop = True
            stop_reason = "Target coverage reached with optimal energy efficiency."
            break
            
    execution_time = time.time() - start_time
    
    # Post-processing: Optimize active drone selection
    best_particle = post_prune(
        best_particle, 
        GridPoints, 
        SensingRange, 
        threshold=target_coverage*100
    )
    
    # Calculate final metrics using Active/Sleep functions
    final_coverage = calculate_coverage_with_solution(best_particle, simulation)
    final_overlap = calculate_overlap_penalty(best_particle, simulation)
    
    result = AlgorithmResult(
        best_solution=best_particle,
        fitness_history=fitness_history,
        coverage=final_coverage,
        active_nodes=int(np.sum(best_particle[:, 2] >= 0.5)),
        overlap=final_overlap,
        execution_time=execution_time,
        algorithm_name="Enhanced Genetic Algorithm (Active/Sleep)",
        parameters={
            'population_size': population_size,
            'num_generations': num_generations,
            'mutation_rate': mutation_rate,
            'crossover_rate': crossover_rate,
            'target_coverage': target_coverage,
            'energy_efficiency_mode': energy_efficiency_mode,
            'parallel_processing': parallel_processing
        },
        coverage_history=coverage_history,
        overlap_history=overlap_history,
        active_nodes_history=active_nodes_history,
        early_stop=early_stop,
        stop_reason=stop_reason,
        iteration_logs=iteration_logs
    )
    activation = convert_to_binary_activation(best_particle, simulation)
    return activation, result

def smart_particle_swarm_optimization(simulation,
                                     swarm_size=50,
                                     iterations=300,
                                     inertia=0.5,
                                     cognitive_weight=1.5,
                                     social_weight=1.5,
                                     desired_coverage=0.90,
                                     parallel_processing=False,
                                     max_workers=None,
                                     progress_callback=None):
    """
    SMART TWO-PHASE PSO OPTIMIZATION
    Phase 1: Minimize drones for target coverage (Energy Efficiency)
    Phase 2: Maximize coverage with available drones (Coverage Optimization)
    """
    start_time = time.time()
    AreaWidth, AreaHeight = simulation.width, simulation.height
    SensingRange = simulation.sensing_radius
    NumNodes = len(simulation.drones)
    GridPoints = simulation.grid_points
    NumGridPoints = len(GridPoints)
    
    print(f"🧠 SMART PSO: Two-Phase Optimization Starting...")
    print(f"   Phase 1: Energy Efficiency (Target: {desired_coverage*100:.1f}%)")
    print(f"   Phase 2: Coverage Maximization")
    
    def calculate_coverage(particle):
        covered = np.zeros(len(GridPoints), dtype=bool)
        for sensor in particle:
            if sensor[2] >= 0.5:
                distances = np.linalg.norm(GridPoints - sensor[:2], axis=1)
                covered |= distances <= SensingRange
        return (np.sum(covered) / NumGridPoints) * 100

    def calculate_gap_coverage(particle):
        """Calculate coverage focusing on gap elimination"""
        covered = np.zeros(len(GridPoints), dtype=bool)
        for sensor in particle:
            if sensor[2] >= 0.5:
                distances = np.linalg.norm(GridPoints - sensor[:2], axis=1)
                covered |= distances <= SensingRange
        
        # Calculate coverage and gap penalty
        coverage_pct = (np.sum(covered) / NumGridPoints) * 100
        
        # Find largest uncovered gap
        uncovered_points = GridPoints[~covered]
        if len(uncovered_points) > 0:
            # Penalty for large gaps
            gap_penalty = len(uncovered_points) / NumGridPoints * 50
        else:
            gap_penalty = 0
            
        return coverage_pct - gap_penalty

    def calculate_overlap(particle):
        overlap_penalty = 0
        active_nodes = particle[particle[:, 2] >= 0.5]
        for i in range(len(active_nodes)):
            for j in range(i + 1, len(active_nodes)):
                d = np.linalg.norm(active_nodes[i, :2] - active_nodes[j, :2])
                if d < 2 * SensingRange:
                    overlap_penalty += 1 - (d / (2 * SensingRange))
        return overlap_penalty

    # PHASE 1: ENERGY EFFICIENCY FITNESS
    def phase1_fitness(particle):
        """Minimize drones while achieving target coverage"""
        coverage = calculate_coverage(particle)
        active_nodes = np.sum(particle[:, 2] >= 0.5)
        overlap = calculate_overlap(particle)
        
        if coverage >= desired_coverage * 100:
            # Reward: Achieved target, minimize drones
            return coverage * 0.5 - (active_nodes / NumNodes) * 100 - overlap * 0.3
        else:
            # Penalty: Below target, focus on coverage
            return coverage * 1.2 - overlap * 0.1

    # PHASE 2: COVERAGE MAXIMIZATION FITNESS  
    def phase2_fitness(particle):
        """Maximize coverage and eliminate gaps"""
        coverage = calculate_gap_coverage(particle)
        active_nodes = np.sum(particle[:, 2] >= 0.5)
        overlap = calculate_overlap(particle)
        
        # Reward coverage, especially above target
        if coverage >= desired_coverage * 100:
            coverage_bonus = (coverage - desired_coverage * 100) * 2
            return coverage + coverage_bonus - overlap * 0.2
        else:
            return coverage * 1.1 - overlap * 0.1

    # Initialize particles
    particles = [np.random.rand(NumNodes, 3) * [AreaWidth, AreaHeight, 1] for _ in range(swarm_size)]
    velocities = [np.random.rand(NumNodes, 3) * 0.1 for _ in range(swarm_size)]
    
    # Store iteration history
    coverage_history = []
    fitness_history = []
    active_nodes_history = []
    phase_history = []
    
    # PHASE 1: ENERGY EFFICIENCY OPTIMIZATION
    print(f"🔋 Phase 1: Energy Efficiency Optimization ({iterations//2} iterations)")
    current_fitness = phase1_fitness
    
    pbest_fitness = [current_fitness(p) for p in particles]
    pbest = [p.copy() for p in particles]
    
    gbest_idx = np.argmax(pbest_fitness)
    gbest = pbest[gbest_idx].copy()
    gbest_fitness = pbest_fitness[gbest_idx]
    
    phase1_iterations = iterations // 2
    
    for iteration in range(phase1_iterations):
        for i in range(swarm_size):
            # Update velocity
            r1, r2 = np.random.rand(2)
            velocities[i] = (inertia * velocities[i] + 
                           cognitive_weight * r1 * (pbest[i] - particles[i]) +
                           social_weight * r2 * (gbest - particles[i]))
            
            # Update position
            particles[i] += velocities[i]
            
            # Apply bounds
            particles[i][:, 0] = np.clip(particles[i][:, 0], 0, AreaWidth)
            particles[i][:, 1] = np.clip(particles[i][:, 1], 0, AreaHeight)
            particles[i][:, 2] = np.clip(particles[i][:, 2], 0, 1)
            
            # Evaluate fitness
            fitness_val = current_fitness(particles[i])
            
            # Update personal best
            if fitness_val > pbest_fitness[i]:
                pbest_fitness[i] = fitness_val
                pbest[i] = particles[i].copy()
                
                # Update global best
                if fitness_val > gbest_fitness:
                    gbest_fitness = fitness_val
                    gbest = particles[i].copy()
        
        # Record history
        current_coverage = calculate_coverage(gbest)
        active_count = np.sum(gbest[:, 2] >= 0.5)
        
        coverage_history.append(current_coverage)
        fitness_history.append(gbest_fitness)
        active_nodes_history.append(active_count)
        phase_history.append(1)
        
        if iteration % 20 == 0:
            print(f"Phase 1 Iteration {iteration}: Coverage = {current_coverage:.1f}%, Active Drones = {active_count}")
        
        # Call progress callback if provided
        if progress_callback:
            progress_callback(iteration, phase1_iterations, gbest_fitness, current_coverage)

    print(f"✅ Phase 1 Complete: {current_coverage:.1f}% coverage with {active_count} drones")
    
    # PHASE 2: COVERAGE MAXIMIZATION OPTIMIZATION
    print(f"🎯 Phase 2: Coverage Maximization ({iterations - phase1_iterations} iterations)")
    current_fitness = phase2_fitness
    
    # Re-evaluate all particles with new fitness function
    pbest_fitness = [current_fitness(p) for p in pbest]
    gbest_idx = np.argmax(pbest_fitness)
    gbest = pbest[gbest_idx].copy()
    gbest_fitness = pbest_fitness[gbest_idx]
    
    for iteration in range(phase1_iterations, iterations):
        for i in range(swarm_size):
            # Update velocity with exploration boost for phase 2
            r1, r2 = np.random.rand(2)
            exploration_factor = 1.2  # Boost exploration in phase 2
            velocities[i] = (inertia * velocities[i] + 
                           cognitive_weight * r1 * (pbest[i] - particles[i]) * exploration_factor +
                           social_weight * r2 * (gbest - particles[i]) * exploration_factor)
            
            # Update position
            particles[i] += velocities[i]
            
            # Apply bounds
            particles[i][:, 0] = np.clip(particles[i][:, 0], 0, AreaWidth)
            particles[i][:, 1] = np.clip(particles[i][:, 1], 0, AreaHeight)
            particles[i][:, 2] = np.clip(particles[i][:, 2], 0, 1)
            
            # Evaluate fitness
            fitness_val = current_fitness(particles[i])
            
            # Update personal best
            if fitness_val > pbest_fitness[i]:
                pbest_fitness[i] = fitness_val
                pbest[i] = particles[i].copy()
                
                # Update global best
                if fitness_val > gbest_fitness:
                    gbest_fitness = fitness_val
                    gbest = particles[i].copy()
        
        # Record history
        current_coverage = calculate_coverage(gbest)
        active_count = np.sum(gbest[:, 2] >= 0.5)
        
        coverage_history.append(current_coverage)
        fitness_history.append(gbest_fitness)
        active_nodes_history.append(active_count)
        phase_history.append(2)
        
        if iteration % 20 == 0:
            print(f"Phase 2 Iteration {iteration}: Coverage = {current_coverage:.1f}%, Active Drones = {active_count}")
        
        # Call progress callback if provided
        if progress_callback:
            progress_callback(iteration, iterations, gbest_fitness, current_coverage)

    # Final results
    final_coverage = calculate_coverage(gbest)
    final_active = np.sum(gbest[:, 2] >= 0.5)
    execution_time = time.time() - start_time
    
    print(f"🎉 SMART PSO Complete:")
    print(f"   Pre-optimization Coverage: {final_coverage:.1f}%")
    print(f"   Pre-optimization Active Drones: {final_active}/{NumNodes}")
    
    # SMART POST-PROCESSING: Apply gap filling and redundancy removal
    if SMART_OPTIMIZER_AVAILABLE:
        print(f"🧠 Applying Smart Post-Processing...")
        try:
            # Apply smart optimization to the best solution
            optimized_gbest = staged_gap_filling_optimization(gbest, simulation, max_relocations=3)
            
            # Recalculate metrics for optimized solution
            optimized_coverage = calculate_coverage(optimized_gbest)
            optimized_active = np.sum(optimized_gbest[:, 2] >= 0.5)
            
            # Use optimized solution if it's better or uses fewer drones with similar coverage
            coverage_improvement = optimized_coverage - final_coverage
            drone_reduction = final_active - optimized_active
            
            if (coverage_improvement > 0.01 or  # Better coverage
                (abs(coverage_improvement) < 0.05 and drone_reduction > 0)):  # Similar coverage, fewer drones
                print(f"✅ Smart optimization applied:")
                print(f"   Coverage: {final_coverage:.1f}% → {optimized_coverage:.1f}% ({coverage_improvement:+.1f}%)")
                print(f"   Active Drones: {final_active} → {optimized_active} ({drone_reduction:+d})")
                
                gbest = optimized_gbest
                final_coverage = optimized_coverage
                final_active = optimized_active
            else:
                print(f"ℹ️ Original solution already optimal")
                
        except Exception as e:
            print(f"⚠️ Smart optimization failed: {e}, using original solution")
    
    print(f"🎯 Final Results:")
    print(f"   Final Coverage: {final_coverage:.1f}%")
    print(f"   Active Drones: {final_active}/{NumNodes}")
    print(f"   Energy Saved: {((NumNodes - final_active) / NumNodes * 100):.1f}%")
    print(f"   Execution Time: {execution_time:.2f}s")
    
    # Create result object
    result = type('AlgorithmResult', (), {
        'coverage': final_coverage,
        'best_fitness': gbest_fitness,
        'execution_time': execution_time,
        'fitness_history': fitness_history,
        'coverage_history': coverage_history,
        'active_nodes_history': active_nodes_history,
        'phase_history': phase_history,
        'convergence_iteration': len(coverage_history),
        'algorithm_name': 'Smart Two-Phase PSO',
        'energy_saved_percentage': ((NumNodes - final_active) / NumNodes * 100)
    })()
    
    # Convert to binary activation pattern
    activation = convert_to_binary_activation(gbest, simulation)
    
    return activation, result

def particle_swarm_optimization(simulation,
                               swarm_size=50,
                               iterations=300,
                               inertia=0.5,
                               cognitive_weight=1.5,
                               social_weight=1.5,
                               w1=0.7, w2=0.15, w3=0.15,
                               desired_coverage=0.90,
                               parallel_processing=True,  # Enable by default
                               max_workers=None,
                               smart_mode=True,  # NEW: Enable smart mode by default
                               progress_callback=None):  # NEW: Progress callback support
    """
    Particle Swarm Optimization for drone coverage
    Now with SMART MODE option for two-phase optimization
    """
    if smart_mode:
        # Use the smart two-phase optimization
        return smart_particle_swarm_optimization(
            simulation, swarm_size, iterations, inertia, 
            cognitive_weight, social_weight, desired_coverage, 
            parallel_processing, max_workers, progress_callback
        )
    """Particle Swarm Optimization for drone coverage with parallel processing"""
    start_time = time.time()
    AreaWidth, AreaHeight = simulation.width, simulation.height
    SensingRange = simulation.sensing_radius
    NumNodes = len(simulation.drones)
    GridPoints = simulation.grid_points
    NumGridPoints = len(GridPoints)
    
    # Auto-determine optimal worker count
    if max_workers is None:
        max_workers = min(cpu_count(), swarm_size // WORKER_TO_POPULATION_RATIO, MAX_RECOMMENDED_WORKERS)
    
    print(f"🔄 PSO initialized: Swarm={swarm_size}, Parallel={'ON' if parallel_processing else 'OFF'}, Workers={max_workers if parallel_processing else 'N/A'}")
    
    def calculate_coverage(particle):
        covered = np.zeros(len(GridPoints), dtype=bool)
        for sensor in particle:
            if sensor[2] >= 0.5:
                distances = np.linalg.norm(GridPoints - sensor[:2], axis=1)
                covered |= distances <= SensingRange
        return (np.sum(covered) / NumGridPoints) * 100

    def calculate_overlap(particle):
        overlap_penalty = 0
        active_nodes = particle[particle[:, 2] >= 0.5]
        for i in range(len(active_nodes)):
            for j in range(i + 1, len(active_nodes)):
                d = np.linalg.norm(active_nodes[i, :2] - active_nodes[j, :2])
                if d < 2 * SensingRange:
                    overlap_penalty += 1 - (d / (2 * SensingRange))
        return overlap_penalty

    def fitness(particle):
        coverage = calculate_coverage(particle)
        active_nodes = np.sum(particle[:, 2] >= 0.5)
        overlap = calculate_overlap(particle)
        return w1 * coverage - w2 * (active_nodes / NumNodes) * 100 - w3 * overlap

    # Initialize particles
    particles = [np.random.rand(NumNodes, 3) * [AreaWidth, AreaHeight, 1] for _ in range(swarm_size)]
    velocities = [np.random.rand(NumNodes, 3) * 0.1 for _ in range(swarm_size)]
    
    if parallel_processing:
        pbest_fitness = parallel_fitness_evaluation(particles, fitness)
    else:
        pbest_fitness = [fitness(p) for p in particles]
        
    pbest = [p.copy() for p in particles]
    
    gbest_idx = np.argmax(pbest_fitness)
    gbest = pbest[gbest_idx].copy()
    gbest_fitness = pbest_fitness[gbest_idx]
    
    fitness_history = []
    coverage_history = []
    overlap_history = []
    active_nodes_history = []
    iteration_logs = []
    early_stop = False
    stop_reason = None
    
    for iteration in range(iterations):
        for i in range(swarm_size):
            # Update velocity
            velocities[i] = (inertia * velocities[i] +
                           cognitive_weight * np.random.rand() * (pbest[i] - particles[i]) +
                           social_weight * np.random.rand() * (gbest - particles[i]))
            
            # Update position
            particles[i] += velocities[i]
            
            # Apply bounds
            particles[i][:, :2] = np.clip(particles[i][:, :2], 0, [AreaWidth, AreaHeight])
            particles[i][:, 2] = np.clip(particles[i][:, 2], 0, 1)

        # Update personal best
        if parallel_processing:
            current_fitness_scores = parallel_fitness_evaluation(particles, fitness)
        else:
            current_fitness_scores = [fitness(p) for p in particles]

        for i in range(swarm_size):
            if current_fitness_scores[i] > pbest_fitness[i]:
                pbest[i] = particles[i].copy()
                pbest_fitness[i] = current_fitness_scores[i]

        # Update global best
        current_gbest_idx = np.argmax(pbest_fitness)
        if pbest_fitness[current_gbest_idx] > gbest_fitness:
            gbest = pbest[current_gbest_idx].copy()
            gbest_fitness = pbest_fitness[current_gbest_idx]
        
        fitness_history.append(gbest_fitness)
        coverage_history.append(calculate_coverage(gbest))
        overlap_history.append(calculate_overlap(gbest))
        active_nodes_history.append(int(np.sum(gbest[:, 2] >= 0.5)))
        
        # Add iteration log entry
        iteration_logs.append({
            'iteration': iteration + 1,
            'fitness': gbest_fitness,
            'coverage': coverage_history[-1],
            'algorithm': 'PSO'
        })
        
        if iteration % 20 == 0:
            print(f"PSO Iteration {iteration + 1}: Best Fitness = {gbest_fitness:.2f}, "
                  f"Coverage = {coverage_history[-1]:.2f}%")
                  
        if coverage_history[-1] >= desired_coverage * 100:
            print(f"Stopping early: Desired coverage reached.")
            early_stop = True
            stop_reason = "Desired coverage reached."
            break

    execution_time = time.time() - start_time
    
    gbest = post_prune(
        gbest,
        GridPoints,
        SensingRange,
        threshold=desired_coverage*100
    )

    result = AlgorithmResult(
        best_solution=gbest,
        fitness_history=fitness_history,
        coverage=calculate_coverage(gbest),
        active_nodes=int(np.sum(gbest[:, 2] >= 0.5)),
        overlap=calculate_overlap(gbest),
        execution_time=execution_time,
        algorithm_name="Particle Swarm Optimization",
        parameters={
            'swarm_size': swarm_size,
            'iterations': iterations,
            'inertia': inertia,
            'cognitive_weight': cognitive_weight,
            'social_weight': social_weight,
            'parallel_processing': parallel_processing
        },
        coverage_history=coverage_history,
        overlap_history=overlap_history,
        active_nodes_history=active_nodes_history,
        early_stop=early_stop,
        stop_reason=stop_reason,
        iteration_logs=iteration_logs
    )
    activation = convert_to_binary_activation(gbest, simulation)
    return activation, result

def genetic_algorithm_with_sa(simulation,
                              population_size=50,
                              num_generations=100,
                              mutation_rate=0.1,
                              crossover_rate=0.8,
                              elitism_fraction=0.2,
                              sa_temp=100,
                              sa_cooling=0.95,
                              sa_iters=30,
                              desired_coverage=0.95,
                              parallel_processing=False,
                              w1=0.6, w2=0.2, w3=0.2):
    """Genetic Algorithm with Simulated Annealing refinement for drone optimization"""
    start_time = time.time()
    AreaWidth, AreaHeight = simulation.width, simulation.height
    SensingRange = simulation.sensing_radius
    NumNodes = len(simulation.drones)
    GridPoints = simulation.grid_points
    NumGridPoints = len(GridPoints)

    def calculate_coverage(particle):
        covered = np.zeros(len(GridPoints), dtype=bool)
        for sensor in particle:
            if sensor[2] >= 0.5:
                distances = np.linalg.norm(GridPoints - sensor[:2], axis=1)
                covered |= distances <= SensingRange
        return (np.sum(covered) / NumGridPoints) * 100

    def calculate_overlap(particle):
        overlap_penalty = 0
        active_nodes = particle[particle[:, 2] >= 0.5]
        for i in range(len(active_nodes)):
            for j in range(i + 1, len(active_nodes)):
                d = np.linalg.norm(active_nodes[i, :2] - active_nodes[j, :2])
                if d < 2 * SensingRange:
                    overlap_penalty += 1 - (d / (2 * SensingRange))
        return overlap_penalty

    def fitness(particle):
        coverage = calculate_coverage(particle)
        active_nodes = np.sum(particle[:, 2] >= 0.5)
        overlap = calculate_overlap(particle)
        return w1 * coverage - w2 * (active_nodes / NumNodes) * 100 - w3 * overlap

    def crossover(parent1, parent2):
        if np.random.rand() < crossover_rate:
            point = np.random.randint(1, NumNodes -1) if NumNodes > 1 else 0
            child1 = np.vstack((parent1[:point], parent2[point:]))
            child2 = np.vstack((parent2[:point], parent1[point:]))
            return child1, child2
        else:
            return parent1.copy(), parent2.copy()

    def mutate(particle):
        mutated_particle = particle.copy()
        for i in range(NumNodes):
            if np.random.rand() < mutation_rate:
                mutated_particle[i, 0:2] = np.random.rand(2) * [AreaWidth, AreaHeight]
                mutated_particle[i, 2] = 1 - mutated_particle[i, 2] # Flip activation
        return mutated_particle
        
    def sa_refinement(particle):
        current_sol = particle.copy()
        best_sol = particle.copy()
        current_fitness = fitness(current_sol)
        best_fitness = current_fitness
        temp = sa_temp

        for _ in range(sa_iters):
            neighbor = current_sol.copy()
            # Tweak a random drone
            idx_to_tweak = np.random.randint(0, NumNodes)
            neighbor[idx_to_tweak, 0:2] += (np.random.rand(2) - 0.5) * 5 # Small position change
            neighbor[idx_to_tweak, 0:2] = np.clip(neighbor[idx_to_tweak, 0:2], 0, [AreaWidth, AreaHeight])
            if np.random.rand() < 0.2: # Chance to flip activation
                neighbor[idx_to_tweak, 2] = 1 - neighbor[idx_to_tweak, 2]

            neighbor_fitness = fitness(neighbor)
            delta = neighbor_fitness - current_fitness
            
            if delta > 0 or np.random.rand() < np.exp(delta / temp):
                current_sol = neighbor
                current_fitness = neighbor_fitness
                if current_fitness > best_fitness:
                    best_sol = current_sol
                    best_fitness = current_fitness
            
            temp *= sa_cooling
        return best_sol

    # GA Main Loop
    population = [np.random.rand(NumNodes, 3) * [AreaWidth, AreaHeight, 1] for _ in range(population_size)]
    
    best_particle = None
    best_fitness = -np.inf
    fitness_history = []
    coverage_history = []
    overlap_history = []
    active_nodes_history = []
    iteration_logs = []
    early_stop = False
    stop_reason = None
    
    for generation in range(num_generations):
        if parallel_processing:
            fitness_scores = parallel_fitness_evaluation(population, fitness)
        else:
            fitness_scores = [fitness(p) for p in population]

        sorted_indices = np.argsort(fitness_scores)[::-1]
        population = [population[i] for i in sorted_indices]
        fitness_scores = [fitness_scores[i] for i in sorted_indices]

        if fitness_scores[0] > best_fitness:
            best_fitness = fitness_scores[0]
            best_particle = population[0].copy()

        fitness_history.append(best_fitness)
        coverage_history.append(calculate_coverage(best_particle))
        overlap_history.append(calculate_overlap(best_particle))
        active_nodes_history.append(int(np.sum(best_particle[:, 2] >= 0.5)))
        
        # Add iteration log entry
        iteration_logs.append({
            'iteration': generation + 1,
            'fitness': best_fitness,
            'coverage': coverage_history[-1],
            'algorithm': 'GA+SA'
        })

        elite_count = int(elitism_fraction * population_size)
        elites = population[:elite_count]

        # Apply SA refinement to elites
        if parallel_processing:
            refined_elites = parallel_fitness_evaluation(elites, sa_refinement)
        else:
            refined_elites = [sa_refinement(elite) for elite in elites]
        
        new_population = refined_elites
        
        # Generate new individuals
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            if len(new_population) < population_size:
                new_population.append(mutate(child2))
        
        population = new_population[:population_size]

        if generation % 10 == 0:
            print(f"GA+SA Gen {generation + 1}: Best Fitness = {best_fitness:.2f}, "
                  f"Coverage = {coverage_history[-1]:.2f}%")

        if coverage_history[-1] >= desired_coverage * 100:
            print("Stopping early: Desired coverage reached.")
            early_stop = True
            stop_reason = "Desired coverage reached."
            break

    execution_time = time.time() - start_time
    
    best_particle = post_prune(
        best_particle, 
        GridPoints, 
        SensingRange, 
        threshold=desired_coverage*100
    )

    result = AlgorithmResult(
        best_solution=best_particle,
        fitness_history=fitness_history,
        coverage=calculate_coverage(best_particle),
        active_nodes=int(np.sum(best_particle[:, 2] >= 0.5)),
        overlap=calculate_overlap(best_particle),
        execution_time=execution_time,
        algorithm_name="Genetic Algorithm with SA",
        parameters={
            'population_size': population_size,
            'num_generations': num_generations,
            'mutation_rate': mutation_rate,
            'crossover_rate': crossover_rate,
            'elitism_fraction': elitism_fraction,
            'sa_temp': sa_temp,
            'sa_cooling': sa_cooling,
            'sa_iters': sa_iters,
            'parallel_processing': parallel_processing
        },
        coverage_history=coverage_history,
        overlap_history=overlap_history,
        active_nodes_history=active_nodes_history,
        early_stop=early_stop,
        stop_reason=stop_reason,
        iteration_logs=iteration_logs
    )

    activation = convert_to_binary_activation(best_particle, simulation)
    return activation, result

def grey_wolf_optimizer(simulation,
                        population_size=30,
                        max_iterations=100,
                        desired_coverage=0.90,
                        parallel_processing=False,
                        w1=0.6, w2=0.2, w3=0.2):
    """Grey Wolf Optimizer for drone optimization"""
    start_time = time.time()
    AreaWidth, AreaHeight = simulation.width, simulation.height
    SensingRange = simulation.sensing_radius
    NumNodes = len(simulation.drones)
    GridPoints = simulation.grid_points
    NumGridPoints = len(GridPoints)

    def calculate_coverage(particle):
        # Reshape to 2D if flat
        if particle.ndim == 1:
            particle = particle.reshape((NumNodes, 3))
        covered = np.zeros(len(GridPoints), dtype=bool)
        for sensor in particle:
            if sensor[2] >= 0.5:
                distances = np.linalg.norm(GridPoints - sensor[:2], axis=1)
                covered |= distances <= SensingRange
        return (np.sum(covered) / NumGridPoints) * 100

    def calculate_overlap(particle):
        # Reshape to 2D if flat
        if particle.ndim == 1:
            particle = particle.reshape((NumNodes, 3))
        overlap_penalty = 0
        active_nodes = particle[particle[:, 2] >= 0.5]
        for i in range(len(active_nodes)):
            for j in range(i + 1, len(active_nodes)):
                d = np.linalg.norm(active_nodes[i, :2] - active_nodes[j, :2])
                if d < 2 * SensingRange:
                    overlap_penalty += 1 - (d / (2 * SensingRange))
        return overlap_penalty
    
    def fitness(position):
        # GWO minimizes, so we negate the objective function
        coverage = calculate_coverage(position)
        active_nodes = np.sum(position.reshape(NumNodes, 3)[:, 2] >= 0.5)
        overlap = calculate_overlap(position)
        return -(w1 * coverage - w2 * (active_nodes / NumNodes) * 100 - w3 * overlap)

    # Initialize wolves
    dim = NumNodes * 3
    lb = np.tile([0, 0, 0], NumNodes)
    ub = np.tile([AreaWidth, AreaHeight, 1], NumNodes)
    wolves = np.random.uniform(0, 1, (population_size, dim)) * (ub - lb) + lb

    alpha_pos = np.zeros(dim)
    alpha_score = float("inf")
    beta_pos = np.zeros(dim)
    beta_score = float("inf")
    delta_pos = np.zeros(dim)
    delta_score = float("inf")
    
    fitness_history = []
    coverage_history = []
    overlap_history = []
    active_nodes_history = []
    iteration_logs = []
    early_stop = False
    stop_reason = None

    for iteration in range(max_iterations):
        if parallel_processing:
            scores = parallel_fitness_evaluation(wolves, fitness)
        else:
            scores = [fitness(w) for w in wolves]

        for i in range(population_size):
            wolves[i] = np.clip(wolves[i], lb, ub)
            score = scores[i]
            if score < alpha_score:
                alpha_score, alpha_pos = score, wolves[i].copy()
            elif score < beta_score:
                beta_score, beta_pos = score, wolves[i].copy()
            elif score < delta_score:
                delta_score, delta_pos = score, wolves[i].copy()

        a = 2 - iteration * (2 / max_iterations)

        for i in range(population_size):
            r1, r2 = np.random.rand(dim), np.random.rand(dim)
            A1, C1 = 2 * a * r1 - a, 2 * r2
            D_alpha = np.abs(C1 * alpha_pos - wolves[i])
            X1 = alpha_pos - A1 * D_alpha

            r1, r2 = np.random.rand(dim), np.random.rand(dim)
            A2, C2 = 2 * a * r1 - a, 2 * r2
            D_beta = np.abs(C2 * beta_pos - wolves[i])
            X2 = beta_pos - A2 * D_beta

            r1, r2 = np.random.rand(dim), np.random.rand(dim)
            A3, C3 = 2 * a * r1 - a, 2 * r2
            D_delta = np.abs(C3 * delta_pos - wolves[i])
            X3 = delta_pos - A3 * D_delta

            wolves[i] = (X1 + X2 + X3) / 3.0

        best_solution_2d = alpha_pos.reshape(NumNodes, 3)
        fitness_history.append(-alpha_score) # Store maximizing fitness
        coverage_history.append(calculate_coverage(best_solution_2d))
        overlap_history.append(calculate_overlap(best_solution_2d))
        active_nodes_history.append(int(np.sum(best_solution_2d[:, 2] >= 0.5)))
        
        # Add iteration log entry
        iteration_logs.append({
            'iteration': iteration + 1,
            'fitness': -alpha_score,
            'coverage': coverage_history[-1],
            'algorithm': 'GWO'
        })

        if iteration % 10 == 0:
            print(f"GWO Iteration {iteration + 1}: Best Fitness = {-alpha_score:.2f}, "
                  f"Coverage = {coverage_history[-1]:.2f}%")

        if coverage_history[-1] >= desired_coverage * 100:
            print(f"Stopping early: Desired coverage reached.")
            early_stop = True
            stop_reason = "Desired coverage reached."
            break

    execution_time = time.time() - start_time
    best_solution = alpha_pos.reshape(NumNodes, 3)

    best_solution = post_prune(
        best_solution,
        GridPoints,
        SensingRange,
        threshold=desired_coverage*100
    )

    result = AlgorithmResult(
        best_solution=best_solution,
        fitness_history=fitness_history,
        coverage=calculate_coverage(best_solution),
        active_nodes=int(np.sum(best_solution[:, 2] >= 0.5)),
        overlap=calculate_overlap(best_solution),
        execution_time=execution_time,
        algorithm_name="Grey Wolf Optimizer",
        parameters={
            'population_size': population_size,
            'max_iterations': max_iterations,
            'parallel_processing': parallel_processing
        },
        coverage_history=coverage_history,
        overlap_history=overlap_history,
        active_nodes_history=active_nodes_history,
        early_stop=early_stop,
        stop_reason=stop_reason,
        iteration_logs=iteration_logs
    )
    activation = convert_to_binary_activation(best_solution, simulation)
    return activation, result

def manta_ray_foraging_optimization(simulation,
                                      population_size=50,
                                      num_generations=200,
                                      desired_coverage=0.95,
                                      parallel_processing=False,
                                      w1=0.6, w2=0.2, w3=0.2):
    """Manta Ray Foraging Optimization for drone optimization"""
    start_time = time.time()
    AreaWidth, AreaHeight = simulation.width, simulation.height
    SensingRange = simulation.sensing_radius
    NumNodes = len(simulation.drones)
    GridPoints = simulation.grid_points
    NumGridPoints = len(GridPoints)

    def calculate_coverage(particle):
        covered = np.zeros(len(GridPoints), dtype=bool)
        for sensor in particle:
            if sensor[2] >= 0.5:
                distances = np.linalg.norm(GridPoints - sensor[:2], axis=1)
                covered |= distances <= SensingRange
        return (np.sum(covered) / NumGridPoints) * 100

    def calculate_overlap(particle):
        overlap_penalty = 0
        active_nodes = particle[particle[:, 2] >= 0.5]
        for i in range(len(active_nodes)):
            for j in range(i + 1, len(active_nodes)):
                d = np.linalg.norm(active_nodes[i, :2] - active_nodes[j, :2])
                if d < 2 * SensingRange:
                    overlap_penalty += 1 - (d / (2 * SensingRange))
        return overlap_penalty

    def fitness(particle):
        coverage = calculate_coverage(particle)
        active_nodes = np.sum(particle[:, 2] >= 0.5)
        overlap = calculate_overlap(particle)
        return w1 * coverage - w2 * (active_nodes / NumNodes) * 100 - w3 * overlap

    def bound_particle(particle):
        particle[:, :2] = np.clip(particle[:, :2], 0, [AreaWidth, AreaHeight])
        particle[:, 2] = np.clip(particle[:, 2], 0, 1)
        return particle

    # Initialize population
    population = [bound_particle(np.random.rand(NumNodes, 3) * [AreaWidth, AreaHeight, 1]) for _ in range(population_size)]
    
    if parallel_processing:
        fitness_scores = parallel_fitness_evaluation(population, fitness)
    else:
        fitness_scores = [fitness(p) for p in population]
        
    best_particle = population[np.argmax(fitness_scores)].copy()
    best_fitness = max(fitness_scores)
    
    fitness_history = []
    coverage_history = []
    overlap_history = []
    active_nodes_history = []
    iteration_logs = []
    early_stop = False
    stop_reason = None
    
    # Main MRFO loop
    for t in range(num_generations):
        for i in range(population_size):
            if t / num_generations < np.random.rand():
                # Cyclone foraging (exploration)
                r = np.random.rand()
                beta = 2 * np.exp(r * (num_generations - t) / num_generations) * np.sin(2 * np.pi * r)
                if (t / num_generations) < 0.5:
                    rand_pos = np.random.rand(NumNodes, 3) * [AreaWidth, AreaHeight, 1]
                    population[i] = rand_pos + r * (rand_pos - population[i]) + beta * (rand_pos - population[i])
                else:
                    population[i] = best_particle + r * (best_particle - population[i]) + beta * (best_particle - population[i])
            else:
                # Chain foraging (exploitation)
                r = np.random.rand()
                alpha = 2 * r * np.sqrt(abs(np.log(r)))
                if i == 0:
                   population[i] = population[i] + r * (best_particle - population[i]) + alpha * (best_particle - population[i])
                else:
                   population[i] = population[i] + r * (population[i-1] - population[i]) + alpha * (best_particle - population[i])

            population[i] = bound_particle(population[i])
        
        # Somersault foraging
        for i in range(population_size):
            r1 = np.random.rand()
            r2 = np.random.rand(NumNodes, 3)
            population[i] = population[i] + (2 * r1 - 1) * best_particle - (r1 * population[i])

            population[i] = bound_particle(population[i])

        # Update fitness and best solution
        if parallel_processing:
            current_fitness_scores = parallel_fitness_evaluation(population, fitness)
        else:
            current_fitness_scores = [fitness(p) for p in population]

        for i in range(population_size):
            if current_fitness_scores[i] > best_fitness:
                 best_particle = population[i].copy()
                 best_fitness = current_fitness_scores[i]
        
        fitness_history.append(best_fitness)
        coverage_history.append(calculate_coverage(best_particle))
        overlap_history.append(calculate_overlap(best_particle))
        active_nodes_history.append(int(np.sum(best_particle[:, 2] >= 0.5)))
        
        # Add iteration log entry
        iteration_logs.append({
            'iteration': t + 1,
            'fitness': best_fitness,
            'coverage': coverage_history[-1],
            'algorithm': 'MRFO'
        })
        
        print(f"MRFO Iteration {t + 1}: Best Fitness = {best_fitness:.2f}, "
              f"Coverage = {coverage_history[-1]:.2f}%")

        if coverage_history[-1] >= desired_coverage * 100:
            print(f"Stopping early: Desired coverage reached.")
            early_stop = True
            stop_reason = "Desired coverage reached."
            break
            
    execution_time = time.time() - start_time

    result = AlgorithmResult(
        best_solution=best_particle,
        fitness_history=fitness_history,
        coverage=calculate_coverage(best_particle),
        active_nodes=int(np.sum(best_particle[:, 2] >= 0.5)),
        overlap=calculate_overlap(best_particle),
        execution_time=execution_time,
        algorithm_name="Manta Ray Foraging Optimization",
        parameters={
            'population_size': population_size,
            'num_generations': num_generations,
            'parallel_processing': parallel_processing
        },
        coverage_history=coverage_history,
        overlap_history=overlap_history,
        active_nodes_history=active_nodes_history,
        early_stop=early_stop,
        stop_reason=stop_reason,
        iteration_logs=iteration_logs
    )
    activation = convert_to_binary_activation(best_particle, simulation)
    return activation, result

def simulated_annealing(
    simulation,
    num_iterations=200,
    initial_temp=100,
    cooling_rate=0.95,
    perturb_radius=5,
    desired_coverage=0.90,
    w1=0.6, w2=0.2, w3=0.2,
    smart_mode=False,  # Enable smart two-phase optimization
    progress_callback=None  # NEW: Progress callback support
):
    """Standalone Simulated Annealing for drone optimization with Smart Mode"""
    
    if smart_mode:
        # Use universal smart optimization wrapper
        return smart_optimization_wrapper(
            simulated_annealing, simulation, desired_coverage, smart_mode=False,
            num_iterations=num_iterations, initial_temp=initial_temp,
            cooling_rate=cooling_rate, perturb_radius=perturb_radius,
            w1=w1, w2=w2, w3=w3
        )
    start_time = time.time()
    AreaWidth, AreaHeight = simulation.width, simulation.height
    SensingRange = simulation.sensing_radius
    NumNodes = len(simulation.drones)
    GridPoints = simulation.grid_points
    NumGridPoints = len(GridPoints)

    def calculate_coverage(particle):
        covered = np.zeros(len(GridPoints), dtype=bool)
        for sensor in particle:
            if sensor[2] >= 0.5:
                distances = np.linalg.norm(GridPoints - sensor[:2], axis=1)
                covered |= distances <= SensingRange
        return (np.sum(covered) / NumGridPoints) * 100

    def calculate_overlap(particle):
        overlap_penalty = 0
        active_nodes = particle[particle[:, 2] >= 0.5]
        for i in range(len(active_nodes)):
            for j in range(i + 1, len(active_nodes)):
                d = np.linalg.norm(active_nodes[i, :2] - active_nodes[j, :2])
                if d < 2 * SensingRange:
                    overlap_penalty += 1 - (d / (2 * SensingRange))
        return overlap_penalty

    def fitness(particle):
        coverage = calculate_coverage(particle)
        active_nodes = np.sum(particle[:, 2] >= 0.5)
        overlap = calculate_overlap(particle)
        if active_nodes < 3:
            return -float('inf')
        return w1 * coverage - w2 * (active_nodes / NumNodes) * 100 - w3 * overlap

    # Initialize solution
    current = np.hstack((
        np.random.rand(NumNodes, 2) * [AreaWidth, AreaHeight],
        np.random.randint(0, 2, (NumNodes, 1))
    ))
    best = current.copy()
    current_fitness = fitness(current)
    best_fitness = current_fitness
    T = initial_temp

    fitness_history = [current_fitness]
    coverage_history = [calculate_coverage(current)]
    overlap_history = [calculate_overlap(current)]
    active_nodes_history = [int(np.sum(current[:, 2] >= 0.5))]
    iteration_logs = []
    early_stop = False
    stop_reason = None

    for iteration in range(num_iterations):
        # Perturb solution
        new = current.copy()
        idx = np.random.randint(0, NumNodes)
        if np.random.rand() < 0.5:
            # Move position
            new[idx, :2] += (np.random.rand(2) - 0.5) * perturb_radius
            new[idx, :2] = np.clip(new[idx, :2], 0, [AreaWidth, AreaHeight])
        else:
            # Flip activation
            new[idx, 2] = 1 - new[idx, 2]

        new_fitness = fitness(new)
        delta = new_fitness - current_fitness

        if delta > 0 or np.random.rand() < np.exp(delta / (T + 1e-8)):
            current = new
            current_fitness = new_fitness
            if new_fitness > best_fitness:
                best = new
                best_fitness = new_fitness

        T *= cooling_rate

        fitness_history.append(best_fitness)
        coverage_history.append(calculate_coverage(best))
        overlap_history.append(calculate_overlap(best))
        active_nodes_history.append(int(np.sum(best[:, 2] >= 0.5)))
        
        # Add iteration log entry
        iteration_logs.append({
            'iteration': iteration + 1,
            'fitness': best_fitness,
            'coverage': coverage_history[-1],
            'algorithm': 'SA'
        })
        
        # Call progress callback if provided
        if progress_callback:
            progress_callback(iteration, num_iterations, best_fitness, coverage_history[-1])

        if coverage_history[-1] >= desired_coverage * 100:
            print(f"Stopping early: Desired coverage reached.")
            early_stop = True
            stop_reason = "Desired coverage reached."
            break

    execution_time = time.time() - start_time

    best = post_prune(
        best,
        GridPoints,
        SensingRange,
        threshold=desired_coverage*100
    )

    result = AlgorithmResult(
        best_solution=best,
        fitness_history=fitness_history,
        coverage=calculate_coverage(best),
        active_nodes=int(np.sum(best[:, 2] >= 0.5)),
        overlap=calculate_overlap(best),
        execution_time=execution_time,
        algorithm_name="Simulated Annealing",
        parameters={
            'num_iterations': num_iterations,
            'initial_temp': initial_temp,
            'cooling_rate': cooling_rate,
            'perturb_radius': perturb_radius,
            'desired_coverage': desired_coverage,
            'w1': w1, 'w2': w2, 'w3': w3
        },
        coverage_history=coverage_history,
        overlap_history=overlap_history,
        active_nodes_history=active_nodes_history,
        early_stop=early_stop,
        stop_reason=stop_reason,
        iteration_logs=iteration_logs
    )
    activation = convert_to_binary_activation(best, simulation)
    return activation, result

def post_prune(particle, grid_points, sensing_range, threshold=95):
    """Deactivate redundant sensors while maintaining coverage above threshold."""
    particle = particle.copy()
    num_nodes = len(particle)
    def calc_cov(p):
        covered = np.zeros(len(grid_points), dtype=bool)
        for sensor in p:
            if sensor[2] >= 0.5:
                distances = np.linalg.norm(grid_points - sensor[:2], axis=1)
                covered |= distances <= sensing_range
        return (np.sum(covered) / len(grid_points)) * 100

    for i in range(num_nodes):
        if particle[i, 2] >= 0.5:
            temp = particle.copy()
            temp[i, 2] = 0
            if calc_cov(temp) >= threshold:
                particle[i, 2] = 0
    return particle

def smart_hexagonal_optimization(simulation, desired_coverage=0.90, **kwargs):
    """Smart hexagonal packing algorithm for optimal coverage"""
    start_time = time.time()
    
    print("🔶 SMART HEXAGONAL OPTIMIZATION")
    
    width, height = simulation.width, simulation.height
    sensing_radius = simulation.sensing_radius
    num_drones = len(simulation.drones)
    
    # Hexagonal packing parameters for optimal circle packing
    hex_spacing = sensing_radius * np.sqrt(3)  # Optimal hexagonal spacing
    row_height = sensing_radius * 1.5
    
    positions = []
    row = 0
    
    # Generate hexagonal grid positions
    while len(positions) < num_drones:
        y = row * row_height + sensing_radius
        if y >= height:
            break
            
        # Offset every other row for hexagonal pattern
        x_offset = (hex_spacing / 2) if row % 2 == 1 else 0
        
        col = 0
        while True:
            x = col * hex_spacing + sensing_radius + x_offset
            if x >= width:
                break
                
            if len(positions) < num_drones:
                positions.append([x, y])
            
            col += 1
        row += 1
    
    # If we need more positions, add them strategically
    while len(positions) < num_drones:
        x = np.random.uniform(sensing_radius, width - sensing_radius)
        y = np.random.uniform(sensing_radius, height - sensing_radius)
        positions.append([x, y])
    
    # Update drone positions
    for i, pos in enumerate(positions):
        simulation.drones.iloc[i, simulation.drones.columns.get_loc('x')] = pos[0]
        simulation.drones.iloc[i, simulation.drones.columns.get_loc('y')] = pos[1]
        simulation.drones.iloc[i, simulation.drones.columns.get_loc('status')] = 'active'
    
    coverage = simulation.calculate_coverage_percentage()
    execution_time = time.time() - start_time
    
    print(f"   🎯 Hexagonal packing coverage: {coverage:.1f}%")
    
    result = type('HexResult', (), {
        'coverage': coverage,
        'active_drones': num_drones,
        'execution_time': execution_time,
        'algorithm_name': 'Smart Hexagonal Optimization',
        'position_optimization': True
    })()
    
    activation = np.ones(num_drones)
    return activation, result
