# Algorithms API Documentation

## Overview

The `algorithms.py` module provides 16 optimization algorithms for drone coverage optimization:
- **8 Standard algorithms**: Direct optimization approaches
- **8 Staged algorithms**: Multi-phase optimization with coverage-first strategy

## Algorithm Categories

### Standard Algorithms
- `standard_greedy` - Smart greedy with position optimization
- `standard_genetic` - Genetic algorithm with parallel processing
- `standard_pso` - Particle Swarm Optimization
- `standard_sa` - Simulated Annealing
- `standard_ga_sa` - Hybrid Genetic Algorithm + Simulated Annealing
- `standard_gwo` - Grey Wolf Optimizer
- `standard_mrfo` - Manta Ray Foraging Optimization
- `standard_hexagonal` - Smart hexagonal packing optimization

### Staged Algorithms
All standard algorithms have staged variants that use multi-phase optimization:
- Phase 1: Coverage maximization (70% of iterations)
- Phase 2: Energy optimization (30% of iterations)

## Parameter Classes

### `OptimizationParams`
Base parameter class for all algorithms:
```python
params = OptimizationParams(
    max_iterations=300,     # Maximum optimization iterations
    population_size=50,     # Population/swarm size
    desired_coverage=0.90,  # Target coverage (0.0-1.0)
    parallel=True,          # Enable parallel processing
    max_workers=None        # Auto-determine worker count
)
```

### Algorithm-Specific Parameters

#### `PSOParams` - Particle Swarm Optimization
```python
pso_params = PSOParams(
    inertia=0.5,           # Particle inertia weight
    cognitive_weight=1.5,   # Personal best influence
    social_weight=1.5,      # Global best influence
    max_iterations=300
)
```

#### `GAParams` - Genetic Algorithm
```python
ga_params = GAParams(
    mutation_rate=0.1,     # Mutation probability
    crossover_rate=0.8,    # Crossover probability
    elitism=10,            # Number of elite individuals preserved
    population_size=50
)
```

#### `SAParams` - Simulated Annealing
```python
sa_params = SAParams(
    initial_temperature=100.0,  # Starting temperature
    cooling_rate=0.95,          # Temperature reduction rate
    min_temperature=0.01,       # Minimum temperature
    max_iterations=300
)
```

## Function Signatures

### Standard Algorithm Interface
```python
def standard_algorithm(simulation, **kwargs) -> tuple[np.ndarray, AlgorithmResult]:
    """
    Args:
        simulation: DroneSimulationEnvironment instance
        **kwargs: Algorithm-specific parameters
    
    Returns:
        tuple: (activation_array, algorithm_result)
    """
```

### Example Usage
```python
from algorithms import standard_genetic, GAParams
from app import DroneSimulationEnvironment

# Create simulation
sim = DroneSimulationEnvironment(
    area_width=100, area_height=100, 
    num_drones=20, drone_range=15.0
)

# Configure parameters
params = GAParams(
    population_size=50,
    num_generations=200,
    mutation_rate=0.1,
    desired_coverage=0.90
)

# Run optimization
activation, result = standard_genetic(sim, **params.__dict__)

print(f"Coverage: {result.coverage:.1f}%")
print(f"Active drones: {result.active_nodes}")
print(f"Execution time: {result.execution_time:.2f}s")
```

## Constants Configuration

### Key Constants
```python
# Phase distribution for staged optimization
COVERAGE_PHASE_RATIO = 0.7              # 70% for coverage maximization
ENERGY_PHASE_RATIO = 0.3                # 30% for energy optimization

# Position optimization
POSITION_REFINEMENT_ITERATIONS = 30      # Refinement iterations
OPTIMAL_GRID_SPACING_MULTIPLIER = 1.8   # Grid spacing multiplier
SMALL_POSITION_ADJUSTMENT_STD = 2.0     # Position adjustment deviation

# Parallel processing
MAX_RECOMMENDED_WORKERS = 8             # Maximum parallel workers
WORKER_TO_POPULATION_RATIO = 4          # Population/worker ratio

# Fitness function weights
DEFAULT_COVERAGE_WEIGHT = 0.6           # Coverage importance
DEFAULT_ENERGY_WEIGHT = 0.2             # Energy efficiency importance
DEFAULT_OVERLAP_WEIGHT = 0.2            # Overlap penalty importance
```

## AlgorithmResult Class

```python
class AlgorithmResult:
    def __init__(self, ...):
        self.best_solution: np.ndarray      # Best drone configuration
        self.fitness_history: list          # Fitness evolution
        self.coverage: float                # Final coverage percentage
        self.active_nodes: int              # Number of active drones
        self.overlap: float                 # Coverage overlap metric
        self.execution_time: float          # Algorithm runtime (seconds)
        self.algorithm_name: str            # Algorithm identifier
        self.parameters: dict               # Algorithm parameters
        self.coverage_history: list         # Coverage evolution
        self.early_stop: bool               # Early stopping flag
        self.stop_reason: str               # Stopping criterion
```

## Utility Functions

### `get_version_info()`
Returns version and capability information:
```python
info = get_version_info()
print(f"Version: {info['version']}")
print(f"Parallel support: {info['parallel_support']}")
print(f"Available algorithms: {info['algorithms']}")
```

### `get_parallel_support()`
Returns parallel processing information:
```python
parallel_info = get_parallel_support()
print(f"CPU count: {parallel_info['cpu_count']}")
print(f"Recommended workers: {parallel_info['recommended_workers']}")
```

## Best Practices

1. **Use staged algorithms** for better coverage-energy balance
2. **Configure parallel processing** for large populations/swarms
3. **Adjust parameters** based on problem size and requirements
4. **Monitor convergence** using fitness and coverage history
5. **Use appropriate constants** rather than magic numbers

---
*API Version: 5.0.0 | Last Updated: September 5, 2025*
