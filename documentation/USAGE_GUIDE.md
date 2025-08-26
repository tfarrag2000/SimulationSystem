# 🎯 Drone Optimization Dashboard - Test Cases & Usage Guide

## Quick Start

### 1. Start the Dashboard
```bash
python run.py dashboard
# or
python app.py
```
Dashboard will be available at: http://127.0.0.1:8050

### 2. Run Automated Tests
```bash
python run.py test
# or
python test_runner.py
```

## 📋 Predefined Test Cases

### Small Area - Few Drones
- **Environment:** 25x25 grid, 5 drones, radius 6
- **Target:** 80% coverage in 200 iterations
- **Best for:** Quick algorithm testing

### Medium Area - Standard Setup
- **Environment:** 50x50 grid, 15 drones, radius 8
- **Target:** 85% coverage in 500 iterations
- **Best for:** Typical performance comparison

### Large Area - Many Drones
- **Environment:** 100x100 grid, 30 drones, radius 10
- **Target:** 90% coverage in 1000 iterations
- **Best for:** Stress testing and scalability

### Challenging - Small Radius
- **Environment:** 60x60 grid, 20 drones, radius 5
- **Target:** 75% coverage in 800 iterations
- **Best for:** Algorithm robustness testing

### Efficiency Test
- **Environment:** 40x40 grid, 12 drones, radius 7
- **Target:** 95% coverage in 300 iterations (no early stopping)
- **Best for:** Full algorithm comparison

### Parallel Processing Test
- **Environment:** 80x80 grid, 25 drones, radius 9
- **Target:** 85% coverage in 400 iterations
- **Best for:** Performance optimization testing

## 🧪 How to Run Tests

### Manual Testing (Dashboard)
1. Open http://127.0.0.1:8050
2. Select algorithm from dropdown
3. Configure environment parameters:
   - Grid Width/Height
   - Number of Drones
   - Coverage Radius
4. Set stopping criteria:
   - Max Iterations
   - Target Coverage %
   - Enable/Disable Early Stopping
5. Click "Run" to start simulation
6. View results in real-time

### Automated Testing
```python
# Run specific test case
python test_runner.py
# Choose option 1, enter test case name

# Run algorithm comparison
python test_runner.py
# Choose option 2, enter test case name

# Run all test cases
python test_runner.py
# Choose option 3
```

## 📊 Expected Results

### Algorithm Performance Ranges

| Algorithm | Small Area | Medium Area | Large Area | Challenging |
|-----------|------------|-------------|------------|-------------|
| Greedy    | 55-65%     | 58-68%      | 60-70%     | 50-60%      |
| GA        | 60-70%     | 63-73%      | 65-75%     | 60-70%      |
| PSO       | 65-75%     | 68-78%      | 70-80%     | 65-75%      |
| SA        | 58-68%     | 60-70%      | 62-72%     | 58-68%      |
| GA+SA     | 70-80%     | 70-80%      | 75-85%     | 68-78%      |
| GWO       | 65-75%     | 65-75%      | 68-78%     | 63-73%      |
| MRFO      | 68-78%     | 68-78%      | 70-80%     | 66-76%      |

### Iteration Ranges
- **Greedy:** Usually converges quickly (50-150 iterations)
- **GA/PSO:** Moderate convergence (100-300 iterations)
- **SA:** Slower convergence (150-400 iterations)
- **Hybrid (GA+SA):** Longest but best quality (200-500 iterations)

## 🎛️ Parameter Tuning Guidelines

### Environment Size Impact
- **Small (≤30x30):** All algorithms perform well
- **Medium (30-70x70):** Population-based algorithms excel
- **Large (>70x70):** Parallel processing becomes crucial

### Drone Density
- **Low density:** Harder optimization, longer convergence
- **High density:** Easier coverage, risk of over-optimization
- **Optimal ratio:** ~1 drone per 150-200 grid units

### Coverage Radius
- **Small radius:** More challenging, requires precise positioning
- **Large radius:** Easier coverage, more overlap issues
- **Optimal range:** 6-10 units for most scenarios

## 🔧 Advanced Testing

### Custom Test Cases
```python
# Add to test_cases.py
"custom_scenario": {
    "name": "Custom Scenario",
    "description": "Your specific use case",
    "environment": {
        "grid_width": 60,
        "grid_height": 40,
        "num_drones": 18,
        "coverage_radius": 7
    },
    "stopping_criteria": {
        "max_iterations": 600,
        "target_coverage": 88.0,
        "enable_early_stopping": True
    }
}
```

### Parallel Processing Testing
1. Enable parallel processing for GA, PSO, GA+SA, GWO, MRFO
2. Test with different worker counts
3. Compare execution times
4. Measure performance improvement

## 📈 Result Analysis

### Key Metrics
- **Final Coverage %:** Primary optimization goal
- **Iterations Used:** Efficiency indicator
- **Execution Time:** Performance measure
- **Convergence Pattern:** Algorithm behavior
- **Success Rate:** Target achievement

### Quality Indicators
- **Coverage ≥ Target:** Successful optimization
- **Early Convergence:** Efficient algorithm
- **Consistent Results:** Reliable algorithm
- **Low Variance:** Stable performance

## 🎯 Use Cases

### Research & Development
- Algorithm comparison studies
- Parameter sensitivity analysis
- Scalability testing
- Performance benchmarking

### Production Testing
- System validation
- Regression testing
- Performance monitoring
- Quality assurance

### Educational
- Algorithm demonstration
- Optimization concepts
- Comparative analysis
- Interactive learning

## 🚀 Next Steps

1. **Run Basic Tests:** Start with "medium_area_standard"
2. **Compare Algorithms:** Use algorithm comparison mode
3. **Analyze Results:** Review coverage and efficiency
4. **Optimize Parameters:** Fine-tune based on results
5. **Scale Testing:** Move to larger, more complex scenarios
