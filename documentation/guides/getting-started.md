# Getting Started Guide

Welcome to the Drone Optimization SimulationSystem! This guide will help you get up and running quickly.

## 🚀 Quick Setup

### Prerequisites
- Python 3.8 or higher
- Windows/Linux/macOS
- At least 4GB RAM recommended

### Installation
1. **Clone or download** the project
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Verify installation**:
   ```bash
   python -c "import algorithms; print('✅ Setup complete!')"
   ```

## 🎯 First Run

### 1. Basic Simulation
Run a simple drone optimization:
```bash
python app.py
```
This opens a web interface for interactive simulation.

### 2. Single Algorithm Test
```python
from algorithms import standard_greedy
from app import DroneSimulationEnvironment

# Create simulation
sim = DroneSimulationEnvironment(
    area_width=50, area_height=50,
    num_drones=10, drone_range=8.0
)

# Run optimization
activation, result = standard_greedy(sim)
print(f"Coverage: {result.coverage:.1f}%")
```

### 3. Comprehensive Experiments
Run all 14 algorithms on 6 scenarios:
```bash
python comprehensive_experimental.py
```
This generates detailed results and analysis.

## 📊 Understanding Results

### Coverage Metrics
- **Coverage %**: Percentage of area covered by active drones
- **Active Drones**: Number of drones currently active
- **Overlap**: Amount of redundant coverage between drones
- **Efficiency**: Iterations used vs. maximum allowed

### Output Files
- **Results**: Saved to `results/comprehensive_experiment_[timestamp]/`
- **Figures**: Coverage plots and analysis charts
- **Data**: CSV files with detailed metrics

## 🔧 Configuration

### Algorithm Parameters
```python
# Genetic Algorithm example
activation, result = standard_genetic(
    sim,
    population_size=50,      # Population size
    num_generations=200,     # Number of generations
    mutation_rate=0.1,       # Mutation probability
    desired_coverage=0.90    # Target coverage
)
```

### Simulation Environment
```python
sim = DroneSimulationEnvironment(
    area_width=100,          # Area width (units)
    area_height=100,         # Area height (units)
    num_drones=20,          # Number of drones
    drone_range=15.0,       # Sensing radius
    grid_resolution=1.0     # Grid granularity
)
```

## 📈 Running Different Scenarios

### Small Area (Quick Test)
```python
sim = DroneSimulationEnvironment(20, 20, 5, 6.0)
```

### Large Area (Research)
```python
sim = DroneSimulationEnvironment(200, 200, 50, 20.0)
```

### Challenging Scenario
```python
sim = DroneSimulationEnvironment(100, 100, 20, 5.0)  # Small sensing radius
```

## 🎨 Generating Papers

### Automatic Paper Generation
```bash
python automatic_academic_paper_generator.py
```
This creates:
- IEEE-style academic paper
- 4 publication-ready figures
- Comprehensive analysis
- All saved to `paper/` folder

## 🔍 Monitoring Progress

### Real-time Progress
Most algorithms show progress during execution:
```
🧠 SMART GREEDY WITH POSITION OPTIMIZATION
   Initial grid coverage: 78.2%
   Position refinement: iteration 15/30
✅ Final coverage: 85.1% with 12 active drones
```

### Detailed Logs
Check algorithm execution details in the console output.

## ⚡ Performance Tips

1. **Use parallel processing** for genetic and PSO algorithms
2. **Start with smaller scenarios** for testing
3. **Adjust iterations** based on problem complexity
4. **Monitor memory usage** for large-scale experiments

## 🆘 Common Issues

### Import Errors
```bash
# If you see import errors:
pip install numpy pandas matplotlib seaborn scipy
```

### Memory Issues
```python
# For large experiments, reduce population sizes:
activation, result = standard_genetic(sim, population_size=20)
```

### Slow Performance
```python
# Enable parallel processing:
activation, result = standard_pso(sim, parallel_processing=True)
```

## 📚 Next Steps

1. **[Running Experiments](./running-experiments.md)** - Comprehensive experimental framework
2. **[Paper Generation](./paper-generation.md)** - Academic paper creation
3. **[Algorithm Configuration](./algorithm-config.md)** - Advanced parameter tuning
4. **[API Documentation](../api/algorithms.md)** - Complete function reference

## 💡 Examples Gallery

### Basic Optimization
```python
from algorithms import standard_pso
sim = DroneSimulationEnvironment(50, 50, 15, 10.0)
activation, result = standard_pso(sim, iterations=100)
```

### Staged Optimization
```python
from algorithms import staged_genetic
activation, result = staged_genetic(sim, staged_mode=True)
```

### Custom Parameters
```python
from algorithms import standard_ga_sa
activation, result = standard_ga_sa(
    sim,
    population_size=30,
    mutation_rate=0.15,
    temperature=50.0
)
```

---
*Need help? Check the [Troubleshooting Guide](../technical/troubleshooting.md) or review the [API Documentation](../api/)*
