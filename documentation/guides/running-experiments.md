# Running Experiments Guide

This guide covers the comprehensive experimental framework for evaluating drone optimization algorithms.

## 🧪 Experimental Framework

### Overview
The system provides three levels of experimental complexity:
1. **Single Algorithm** - Test one algorithm on one scenario
2. **Algorithm Comparison** - Compare multiple algorithms
3. **Comprehensive Suite** - Full 168-experiment analysis

## 🚀 Quick Start

### Run Complete Experimental Suite
```bash
python comprehensive_experimental.py
```

This executes:
- **14 algorithms** across **6 scenarios**
- **2 runs per combination** (168 total experiments)
- **Automatic result generation** and **academic figures**
- **Complete performance analysis**

### Run Single Algorithm
```python
from enhanced_experimental_suite_improved import run_single_algorithm_experiment

# Test one algorithm
results = run_single_algorithm_experiment(
    algorithm_name="smart_greedy_position_optimization",
    scenario_name="medium_area_moderate_drones"
)
```

## 📊 Experimental Scenarios

### 1. Small Area - Few Drones
```python
scenario = {
    'area_width': 30, 'area_height': 30,
    'num_drones': 8, 'drone_range': 8.0
}
```
**Purpose**: Quick testing and algorithm validation

### 2. Medium Area - Moderate Drones  
```python
scenario = {
    'area_width': 50, 'area_height': 50,
    'num_drones': 12, 'drone_range': 10.0
}
```
**Purpose**: Standard comparison benchmark

### 3. Large Area - Many Drones
```python
scenario = {
    'area_width': 80, 'area_height': 80,
    'num_drones': 20, 'drone_range': 12.0
}
```
**Purpose**: Scalability testing

### 4. Challenging Scenario
```python
scenario = {
    'area_width': 60, 'area_height': 60,
    'num_drones': 15, 'drone_range': 6.0
}
```
**Purpose**: Limited sensing radius testing

### 5. Very Large Area
```python
scenario = {
    'area_width': 100, 'area_height': 100,
    'num_drones': 25, 'drone_range': 15.0
}
```
**Purpose**: Large-scale optimization

### 6. High Density Scenario
```python
scenario = {
    'area_width': 40, 'area_height': 40,
    'num_drones': 18, 'drone_range': 7.0
}
```
**Purpose**: Dense deployment testing

## 🎯 Algorithm Categories

### Smart Algorithms (Top Performers)
1. **smart_greedy_position_optimization** - 🏆 Best overall
2. **smart_coverage_position_optimization** - Optimal coverage focus
3. **staged_genetic** - Multi-stage optimization

### Traditional Optimizers
4. **standard_genetic** - Classic genetic algorithm
5. **standard_pso** - Particle swarm optimization
6. **standard_ga_sa** - Genetic + simulated annealing

### Hybrid Approaches
7. **staged_genetic_with_refinement** - Enhanced staging
8. **smart_greedy_with_local_search** - Local optimization
9. **standard_sa_with_adaptive_temp** - Adaptive cooling

### Basic Methods
10. **standard_greedy** - Simple greedy selection
11. **standard_simulated_annealing** - Basic SA
12. **random_activation** - Random baseline

### Advanced Techniques
13. **combined_algorithms** - Multi-algorithm approach
14. **smart_coverage_optimization** - Coverage-focused

## 📈 Results Analysis

### Output Structure
```
results/comprehensive_experiment_[timestamp]/
├── detailed_results.csv          # Raw experimental data
├── algorithm_comparison.csv       # Algorithm rankings
├── scenario_performance.csv       # Performance by scenario
├── executive_summary.txt          # Key findings
└── figures/
    ├── coverage_comparison.png    # Algorithm comparison
    ├── scenario_analysis.png      # Scenario breakdown
    ├── performance_metrics.png    # Detailed metrics
    └── algorithm_rankings.png     # Overall rankings
```

### Key Metrics
- **Coverage %**: Primary performance indicator
- **Active Drones**: Resource utilization
- **Execution Time**: Algorithm efficiency
- **Convergence**: Optimization quality

### Reading Results
```python
import pandas as pd

# Load results
results = pd.read_csv('results/comprehensive_experiment_*/detailed_results.csv')

# Top performers
top_algorithms = results.groupby('Algorithm')['Coverage'].mean().sort_values(ascending=False)
print(top_algorithms.head())

# Best scenarios
scenario_performance = results.groupby('Scenario')['Coverage'].mean()
print(scenario_performance)
```

## ⚙️ Custom Experiments

### Design Custom Scenario
```python
from app import DroneSimulationEnvironment

# Create custom environment
custom_sim = DroneSimulationEnvironment(
    area_width=75,           # Custom area size
    area_height=75,
    num_drones=18,          # Custom drone count
    drone_range=9.0,        # Custom sensing radius
    grid_resolution=0.5     # Higher resolution
)

# Test algorithm
from algorithms import smart_greedy_position_optimization
activation, result = smart_greedy_position_optimization(custom_sim)
print(f"Custom scenario coverage: {result.coverage:.1f}%")
```

### Parameter Sensitivity Analysis
```python
from algorithms import standard_genetic

# Test different population sizes
pop_sizes = [20, 30, 50, 100]
results = []

for pop_size in pop_sizes:
    activation, result = standard_genetic(
        sim, population_size=pop_size, num_generations=100
    )
    results.append({
        'population_size': pop_size,
        'coverage': result.coverage,
        'time': result.total_time
    })
```

### Algorithm Comparison
```python
from algorithms import smart_greedy_position_optimization, standard_pso, standard_genetic

algorithms = [
    ('Smart Greedy', smart_greedy_position_optimization),
    ('PSO', standard_pso),
    ('Genetic', standard_genetic)
]

results = []
for name, algorithm in algorithms:
    activation, result = algorithm(sim)
    results.append({
        'algorithm': name,
        'coverage': result.coverage,
        'active_drones': sum(activation),
        'time': result.total_time
    })
```

## 📊 Statistical Analysis

### Confidence Intervals
```python
import numpy as np
from scipy import stats

# Calculate 95% confidence interval
coverage_data = results['Coverage'].values
confidence_interval = stats.t.interval(
    0.95, len(coverage_data)-1,
    loc=np.mean(coverage_data),
    scale=stats.sem(coverage_data)
)
```

### Significance Testing
```python
from scipy.stats import mannwhitneyu

# Compare two algorithms
alg1_results = results[results['Algorithm'] == 'smart_greedy_position_optimization']['Coverage']
alg2_results = results[results['Algorithm'] == 'standard_genetic']['Coverage']

statistic, p_value = mannwhitneyu(alg1_results, alg2_results)
print(f"Statistical significance: p = {p_value:.4f}")
```

## 🔧 Performance Optimization

### Parallel Execution
```python
# Enable parallel processing for genetic algorithms
activation, result = standard_genetic(
    sim, 
    population_size=50,
    parallel_processing=True  # Use multiple cores
)
```

### Memory Management
```python
# For large experiments, process in batches
import gc

results = []
for i, algorithm in enumerate(algorithms):
    activation, result = algorithm(sim)
    results.append(result)
    
    # Clear memory every 5 algorithms
    if (i + 1) % 5 == 0:
        gc.collect()
```

### Progress Monitoring
```python
# Monitor experiment progress
import time

start_time = time.time()
total_experiments = len(algorithms) * len(scenarios) * 2

for i, (algorithm, scenario) in enumerate(combinations):
    # Run experiment
    progress = (i + 1) / total_experiments * 100
    elapsed = time.time() - start_time
    eta = elapsed * (total_experiments / (i + 1) - 1)
    
    print(f"Progress: {progress:.1f}% | ETA: {eta/60:.1f} minutes")
```

## 🎨 Visualization

### Generate Academic Figures
```python
from paper_generation.generate_enhanced_figures import generate_all_academic_figures

# Create publication-ready figures
figure_paths = generate_all_academic_figures('results/latest_experiment/')
print("Generated figures:")
for path in figure_paths:
    print(f"  📊 {path}")
```

### Custom Plotting
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Algorithm performance comparison
plt.figure(figsize=(12, 8))
sns.boxplot(data=results, x='Algorithm', y='Coverage')
plt.xticks(rotation=45)
plt.title('Algorithm Performance Distribution')
plt.tight_layout()
plt.show()
```

## 📋 Experiment Checklist

### Before Running
- [ ] Check system requirements (Python 3.8+, 4GB+ RAM)
- [ ] Install all dependencies (`pip install -r requirements.txt`)
- [ ] Verify algorithm imports work
- [ ] Clear previous results if needed

### During Execution
- [ ] Monitor memory usage
- [ ] Check progress output
- [ ] Verify no error messages
- [ ] Ensure sufficient disk space for results

### After Completion
- [ ] Review executive summary
- [ ] Check all CSV files generated
- [ ] Verify figures created correctly
- [ ] Backup results if important

## 🔍 Troubleshooting

### Common Issues

#### Memory Errors
```python
# Reduce experiment scope
algorithms_subset = algorithms[:5]  # Test fewer algorithms
scenarios_subset = scenarios[:3]    # Test fewer scenarios
```

#### Slow Performance
```python
# Reduce algorithm iterations
activation, result = standard_genetic(
    sim, 
    num_generations=50,     # Reduced from 200
    population_size=20      # Reduced from 50
)
```

#### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade numpy pandas matplotlib seaborn scipy
```

### Getting Help
1. Check the [Technical Documentation](../technical/)
2. Review [API Documentation](../api/algorithms.md)
3. Examine example outputs in `results/` folder
4. Enable verbose logging for debugging

---
*For advanced experimental design, see [Algorithm Configuration Guide](./algorithm-config.md)*
