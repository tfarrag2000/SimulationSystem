# Comprehensive Algorithm Parameters - Research Documentation

## Overview
This document provides the complete parameter documentation for all algorithms and experimental configurations used in the drone network optimization research system.

---

## 1. ALGORITHM PARAMETER CLASSES

### 1.1 Base Optimization Parameters
```python
class OptimizationParams:
    max_iterations = 300          # Maximum optimization iterations
    population_size = 50          # Population size for population-based algorithms
    convergence_threshold = 1e-6  # Convergence tolerance
    tolerance = 1e-6             # Numerical tolerance
    random_seed = 42             # Reproducibility seed
```

### 1.2 Particle Swarm Optimization (PSO)
```python
class PSOParams:
    inertia = 0.5               # Inertia weight (w)
    cognitive_weight = 1.5      # Cognitive parameter (c1)
    social_weight = 1.5         # Social parameter (c2)
    max_velocity = 2.0          # Maximum velocity constraint
    constriction_factor = 0.729 # Constriction coefficient
```

### 1.3 Genetic Algorithm (GA)
```python
class GAParams:
    mutation_rate = 0.1         # Mutation probability
    crossover_rate = 0.8        # Crossover probability
    elitism = 10                # Number of elite individuals preserved
    tournament_size = 3         # Tournament selection size
    selection_pressure = 2.0    # Selection pressure coefficient
```

### 1.4 Simulated Annealing (SA)
```python
class SAParams:
    initial_temperature = 100.0  # Starting temperature
    cooling_rate = 0.95         # Temperature reduction factor
    min_temperature = 0.01      # Minimum temperature threshold
    temperature_schedule = "exponential"  # Cooling schedule type
    neighbor_radius = 5.0       # Neighborhood search radius
```

### 1.5 Ant Colony Optimization (ACO)
```python
class ACOParams:
    alpha = 1.0                 # Pheromone importance
    beta = 2.0                  # Heuristic importance
    evaporation_rate = 0.1      # Pheromone evaporation
    pheromone_init = 0.1        # Initial pheromone level
    ant_count = 50              # Number of ants
```

### 1.6 Differential Evolution (DE)
```python
class DEParams:
    scaling_factor = 0.8        # Mutation scaling factor (F)
    crossover_probability = 0.9 # Crossover probability (CR)
    strategy = "DE/rand/1"      # Mutation strategy
    bounds_handling = "clip"    # Boundary constraint method
```

### 1.7 Artificial Bee Colony (ABC)
```python
class ABCParams:
    employed_bees = 25          # Number of employed bees
    onlooker_bees = 25          # Number of onlooker bees
    scout_bees = 5              # Number of scout bees
    limit = 50                  # Abandonment limit
    improvement_threshold = 1e-5 # Solution improvement threshold
```

---

## 2. FITNESS FUNCTION PARAMETERS

### 2.1 Objective Weights
```python
# Standard Configuration
DEFAULT_COVERAGE_WEIGHT = 0.65      # Coverage maximization weight
DEFAULT_ENERGY_WEIGHT = 0.175       # Energy efficiency weight  
DEFAULT_OVERLAP_WEIGHT = 0.175      # Overlap minimization weight

# Enhanced Configuration (Test Case 5)
ENHANCED_COVERAGE_WEIGHT = 2000     # Increased coverage emphasis
ENHANCED_ENERGY_WEIGHT = 500        # Energy optimization emphasis
ENHANCED_OVERLAP_WEIGHT = 300       # Overlap penalty weight
```

### 2.2 Coverage Calculation Parameters
```python
GRID_RESOLUTION_X = 100             # Coverage grid width
GRID_RESOLUTION_Y = 100             # Coverage grid height
COVERAGE_THRESHOLD = 0.5            # Coverage detection threshold
OVERLAP_PENALTY_FACTOR = 2.0        # Overlap cost multiplier
```

---

## 3. EXPERIMENTAL SETUP PARAMETERS

### 3.1 Standard Experimental Configuration
```python
EXPERIMENTAL_CONFIG = {
    "max_iterations": 500,           # Extended iteration limit
    "runs_per_algorithm": 10,        # Statistical significance runs
    "convergence_threshold": 0.4,    # Early stopping criteria
    "performance_tracking": True,    # Enable progress monitoring
    "result_logging": True           # Save intermediate results
}
```

### 3.2 Test Scenarios Configuration

#### Scenario 1: Small Dense Coverage
```python
SMALL_DENSE = {
    "area_width": 25,
    "area_height": 25, 
    "num_drones": 5,
    "sensing_radius": 8,
    "target_coverage": 0.85,
    "complexity": "Low"
}
```

#### Scenario 2: Medium Standard Area
```python
MEDIUM_STANDARD = {
    "area_width": 50,
    "area_height": 50,
    "num_drones": 15, 
    "sensing_radius": 8,
    "target_coverage": 0.90,
    "complexity": "Medium"
}
```

#### Scenario 3: Large Area Many Drones
```python
LARGE_AREA = {
    "area_width": 100,
    "area_height": 100,
    "num_drones": 30,
    "sensing_radius": 12,
    "target_coverage": 0.95,
    "complexity": "High"
}
```

#### Scenario 4: Challenging Small Radius
```python
CHALLENGING_SMALL = {
    "area_width": 60,
    "area_height": 60,
    "num_drones": 20,
    "sensing_radius": 6,
    "target_coverage": 0.88,
    "complexity": "High"
}
```

#### Scenario 5: Efficiency Test
```python
EFFICIENCY_TEST = {
    "area_width": 40,
    "area_height": 40,
    "num_drones": 12,
    "sensing_radius": 10,
    "target_coverage": 0.92,
    "complexity": "Medium"
}
```

#### Scenario 6: Parallel Processing Test
```python
PARALLEL_PROCESSING = {
    "area_width": 80,
    "area_height": 80,
    "num_drones": 25,
    "sensing_radius": 10,
    "target_coverage": 0.93,
    "complexity": "High"
}
```

---

## 4. STAGED ALGORITHM ENHANCEMENTS

### 4.1 Staged Parameters
```python
STAGED_CONFIG = {
    "stage_1_iterations": 150,      # Initial exploration phase
    "stage_2_iterations": 150,      # Exploitation phase
    "transition_threshold": 0.1,    # Stage transition criteria
    "improvement_factor": 1.2,      # Parameter adjustment factor
    "adaptive_weights": True        # Dynamic weight adjustment
}
```

### 4.2 Smart Coverage Distribution
```python
SMART_COVERAGE_PARAMS = {
    "zones_horizontal": 4,          # Grid subdivision width
    "zones_vertical": 4,            # Grid subdivision height
    "coverage_threshold": 0.8,      # Zone coverage target
    "redistribution_factor": 0.3,   # Inter-zone movement factor
    "priority_weights": [1.2, 1.0, 0.8]  # Zone priority coefficients
}
```

---

## 5. ALGORITHM-SPECIFIC CONSTANTS

### 5.1 PSO Constants
```python
PSO_CONSTANTS = {
    "velocity_clamp": True,         # Velocity limiting enabled
    "velocity_max": 2.0,           # Maximum velocity magnitude
    "boundary_handling": "reflect", # Boundary constraint method
    "swarm_size": 50,              # Particle count
    "neighborhood_size": 3          # Local best neighborhood
}
```

### 5.2 GA Constants  
```python
GA_CONSTANTS = {
    "population_initialization": "random",  # Initial population method
    "selection_method": "tournament",       # Parent selection
    "crossover_type": "uniform",           # Crossover operator
    "mutation_type": "gaussian",           # Mutation operator
    "replacement_strategy": "generational" # Population replacement
}
```

### 5.3 SA Constants
```python
SA_CONSTANTS = {
    "acceptance_probability": "metropolis", # Acceptance criterion
    "perturbation_magnitude": 1.0,        # Solution modification size
    "temperature_updates": 100,            # Cooling frequency
    "equilibrium_iterations": 10           # Iterations per temperature
}
```

---

## 6. ENERGY ANALYSIS PARAMETERS

### 6.1 Energy Model Configuration
```python
ENERGY_MODEL = {
    "active_power_consumption": 15.0,      # Watts per active drone
    "sleep_power_consumption": 2.0,        # Watts per sleeping drone
    "transmission_power": 5.0,             # Communication power
    "sensing_power": 8.0,                  # Sensor operation power
    "movement_power_factor": 1.2           # Movement energy multiplier
}
```

### 6.2 Energy Efficiency Metrics
```python
ENERGY_METRICS = {
    "efficiency_ratio_target": 0.7,       # Target sleep ratio
    "energy_budget_constraint": 1000.0,   # Total energy limit (Wh)
    "battery_capacity": 5000.0,           # Individual drone capacity (mAh)
    "mission_duration": 8.0               # Mission time (hours)
}
```

---

## 7. CONVERGENCE AND TERMINATION CRITERIA

### 7.1 Convergence Parameters
```python
CONVERGENCE_CONFIG = {
    "fitness_improvement_threshold": 1e-5,  # Minimum improvement
    "stagnation_generations": 50,          # No-improvement limit
    "diversity_threshold": 0.01,           # Population diversity minimum
    "relative_improvement": 0.001          # Relative fitness change
}
```

### 7.2 Early Stopping Criteria
```python
EARLY_STOPPING = {
    "target_coverage_reached": 0.95,      # Coverage achievement threshold
    "maximum_runtime": 3600,              # Time limit (seconds)
    "memory_usage_limit": 8192,           # RAM limit (MB)
    "convergence_patience": 100           # Convergence waiting period
}
```

---

## 8. PAPER GENERATION PARAMETERS

### 8.1 Academic Figure Configuration
```python
FIGURE_PARAMS = {
    "dpi_resolution": 600,                # Publication quality
    "figure_width": 12,                   # Inches
    "figure_height": 8,                   # Inches
    "font_family": "Times New Roman",     # Academic font
    "title_font_size": 14,               # Title size
    "axis_font_size": 12,                # Axis label size
    "legend_font_size": 10               # Legend size
}
```

### 8.2 Statistical Analysis Parameters
```python
STATISTICS_CONFIG = {
    "confidence_level": 0.95,            # Statistical confidence
    "significance_alpha": 0.05,          # P-value threshold
    "effect_size_threshold": 0.2,        # Minimum effect size
    "bootstrap_samples": 1000,           # Resampling iterations
    "normality_test": "shapiro-wilk"     # Distribution test method
}
```

---

## 9. RESEARCH REPRODUCIBILITY

### 9.1 Random Seed Configuration
```python
REPRODUCIBILITY = {
    "global_random_seed": 42,            # Master seed
    "numpy_seed": 42,                    # NumPy random state
    "algorithm_seeds": [42, 43, 44, 45, 46, 47, 48],  # Per-algorithm seeds
    "experiment_seed_increment": 100      # Seed spacing for experiments
}
```

### 9.2 Version Control
```python
VERSION_INFO = {
    "algorithm_version": "6.0.0",        # Algorithm implementation version
    "parameter_set_version": "2.1.0",    # Parameter configuration version
    "experiment_protocol_version": "1.3.0",  # Experimental protocol version
    "last_updated": "2024-12-27"        # Documentation date
}
```

---

## 10. HARDWARE AND PERFORMANCE PARAMETERS

### 10.1 Computational Resource Limits
```python
RESOURCE_LIMITS = {
    "max_cpu_cores": 8,                  # Parallel processing limit
    "memory_per_core": 2048,             # RAM allocation (MB)
    "disk_space_buffer": 5120,           # Storage reserve (MB)
    "processing_timeout": 7200           # Maximum processing time (seconds)
}
```

### 10.2 Optimization Performance Tuning
```python
PERFORMANCE_TUNING = {
    "vectorization_enabled": True,       # NumPy optimization
    "parallel_fitness_evaluation": True, # Multi-core fitness calculation
    "memory_efficient_mode": False,      # Reduced memory usage
    "progress_reporting_interval": 50    # Status update frequency
}
```

---

## NOTES FOR RESEARCHERS

1. **Parameter Sensitivity**: All parameters have been empirically validated across multiple test scenarios
2. **Scalability**: Parameters are designed to work across different problem sizes (25×25 to 100×100 areas)
3. **Reproducibility**: Fixed random seeds ensure consistent results across runs
4. **Adaptability**: Staged algorithms automatically adjust parameters based on performance metrics
5. **Academic Standards**: All configurations meet IEEE publication requirements for experimental rigor

## CITATION REFERENCE

When using these parameters in academic work, please reference:
- Algorithm implementation version 6.0.0
- Parameter documentation version 2.1.0  
- Experimental validation across 6 standardized test scenarios
- Statistical significance testing with 10 runs per configuration

---

*This documentation provides complete parameter transparency for research reproducibility and academic publication standards.*
