#!/usr/bin/env python3
"""
Environment Parameters Analysis for Reference Algorithms
Analysis of the attached "all algorithms.py" file
"""

def analyze_reference_environment_parameters():
    """Analyze environment parameters from the reference algorithms file"""
    
    print("🔍 ENVIRONMENT PARAMETERS ANALYSIS")
    print("📁 Source: Attached 'all algorithms.py' file")
    print("=" * 60)
    
    # Common parameters across all algorithms
    common_params = {
        "AreaWidth": 100,
        "AreaHeight": 100,
        "SensingRange": 20,
        "NumNodes": 20,
        "GridResolution": 1
    }
    
    # Fitness function weights
    fitness_weights = {
        "w1 (Coverage)": 0.6,  # GWO, GA
        "w2 (Energy)": 0.2,    # GWO, GA  
        "w3 (Overlap)": 0.2,   # GWO, GA
        "w1_alt (Coverage)": 0.7,  # MRFO, PSO
        "w2_alt (Energy)": 0.15,   # MRFO, PSO
        "w3_alt (Overlap)": 0.15   # MRFO, PSO
    }
    
    # Algorithm-specific parameters
    algorithm_params = {
        "Grey Wolf Optimizer (GWO)": {
            "population_size": 30,
            "max_iterations": 100,
            "desired_coverage": 0.90,
            "post_pruning_threshold": 95
        },
        "Manta Ray Foraging Optimization (MRFO)": {
            "population_size": 50,
            "num_generations": 400,
            "desired_coverage": 0.99,
            "post_pruning_threshold": 95,
            "somersault_probability": 0.3,
            "flip_probability": 0.05
        },
        "Genetic Algorithm (GA)": {
            "population_size": 50,
            "num_generations": 400,
            "mutation_rate": 0.1,
            "crossover_rate": 0.8,
            "elitism": 10,
            "desired_coverage": 0.99,
            "post_pruning_threshold": 95
        },
        "GA + Simulated Annealing (GA+SA)": {
            "PopulationSize": 50,
            "MaxGenerations": 200,
            "MutationRate": 0.1,
            "CrossoverRate": 0.8,
            "EliteFraction": 0.2,
            "sa_temp": 100,
            "sa_cooling": 0.95,
            "sa_iters": 30,
            "post_pruning_threshold": 95
        },
        "Particle Swarm Optimization (PSO)": {
            "NumNodes": 30,  # Different from others!
            "NumParticles": 50,
            "MaxIterations": 300,
            "velocity_clamp": 5,
            "coverage_threshold": 95
        }
    }
    
    print("🌍 COMMON ENVIRONMENT PARAMETERS")
    print("-" * 35)
    for param, value in common_params.items():
        print(f"   {param:<15}: {value}")
    
    print(f"\n📏 CALCULATED GRID POINTS")
    print("-" * 25)
    grid_points = (common_params["AreaWidth"] + 1) * (common_params["AreaHeight"] + 1)
    print(f"   Total Grid Points: {grid_points:,}")
    print(f"   Grid Density: {grid_points / (common_params['AreaWidth'] * common_params['AreaHeight']):.2f} points/unit²")
    
    print(f"\n⚖️ FITNESS FUNCTION WEIGHTS")
    print("-" * 30)
    print("   Standard Weights (GWO, GA):")
    for weight, value in list(fitness_weights.items())[:3]:
        print(f"     {weight:<20}: {value}")
    print("   Alternative Weights (MRFO, PSO):")
    for weight, value in list(fitness_weights.items())[3:]:
        print(f"     {weight:<20}: {value}")
    
    print(f"\n🧬 ALGORITHM-SPECIFIC PARAMETERS")
    print("-" * 35)
    
    for algo_name, params in algorithm_params.items():
        print(f"\n🔹 {algo_name}")
        for param, value in params.items():
            print(f"     {param:<25}: {value}")
    
    print(f"\n🎯 KEY OBSERVATIONS")
    print("-" * 20)
    print("1. 📐 Deployment Area: 100×100 units (10,000 unit² total area)")
    print("2. 📡 Sensing Coverage: 20-unit radius per sensor")
    print("3. 🔢 Sensor Count: 20 nodes (PSO uses 30)")
    print("4. 🎪 Coverage Target: 90-99% depending on algorithm")
    print("5. 🔧 Post-processing: All algorithms use pruning at 95% threshold")
    print("6. 📊 Grid Resolution: 1-unit spacing = 10,201 evaluation points")
    
    print(f"\n📈 PERFORMANCE EXPECTATIONS")
    print("-" * 30)
    theoretical_coverage = (20 * 3.14159 * 20**2) / (100 * 100) * 100
    print(f"   Theoretical Max Coverage (no overlap): {theoretical_coverage:.1f}%")
    print(f"   Optimal Sensor Spacing: ~{2 * common_params['SensingRange']:.1f} units")
    print(f"   Expected Active Sensors: 15-20 after pruning")
    
    # Coverage area calculation
    sensor_area = 3.14159 * (common_params["SensingRange"] ** 2)
    total_area = common_params["AreaWidth"] * common_params["AreaHeight"]
    sensors_needed = total_area / sensor_area
    
    print(f"\n🧮 COVERAGE CALCULATIONS")
    print("-" * 25)
    print(f"   Single Sensor Coverage: {sensor_area:.0f} unit²")
    print(f"   Total Deployment Area: {total_area:.0f} unit²")
    print(f"   Theoretical Sensors Needed: {sensors_needed:.1f}")
    print(f"   Available Sensors: {common_params['NumNodes']}")
    print(f"   Sensor Redundancy: {common_params['NumNodes'] / sensors_needed:.1f}x")
    
    return {
        "common_params": common_params,
        "fitness_weights": fitness_weights,
        "algorithm_params": algorithm_params
    }

if __name__ == "__main__":
    params = analyze_reference_environment_parameters()
