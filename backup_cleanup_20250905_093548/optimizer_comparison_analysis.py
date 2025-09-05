#!/usr/bin/env python3
"""
OPTIMIZER & HYPERPARAMETER IMPACT ANALYSIS
==========================================
Demonstrates how different optimizers and their hyperparameters 
dramatically affect drone coverage results.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from app import DroneSimulationEnvironment
from algorithms import (
    greedy_optimization, genetic_algorithm, particle_swarm_optimization,
    simulated_annealing, differential_evolution
)
import time

def analyze_optimizer_impact():
    """
    Comprehensive analysis showing how optimizer type and hyperparameters
    dramatically change final coverage results.
    """
    print("🔬 OPTIMIZER & HYPERPARAMETER IMPACT ANALYSIS")
    print("=" * 60)
    
    # Standard test scenario
    simulation = DroneSimulationEnvironment(
        area_width=50, area_height=50,
        num_drones=15, drone_range=8.0,
        grid_resolution=1.0
    )
    
    results = []
    
    print("\n📊 TESTING DIFFERENT OPTIMIZERS...")
    
    # 1. GREEDY ALGORITHM (our enhanced smart version)
    print("\n1️⃣ SMART GREEDY ALGORITHM:")
    start_time = time.time()
    activation_greedy, result_greedy = greedy_optimization(
        simulation, 
        smart_mode=True,  # Our smart position optimization
        desired_coverage=0.90
    )
    execution_time = time.time() - start_time
    coverage_greedy = result_greedy.coverage
    print(f"   Coverage: {coverage_greedy:.1f}% | Time: {execution_time:.2f}s")
    
    results.append({
        'optimizer': 'Smart Greedy',
        'coverage': coverage_greedy,
        'time': execution_time,
        'hyperparameters': 'smart_mode=True, desired_coverage=0.90'
    })
    
    # 2. GENETIC ALGORITHM - Different Population Sizes
    print("\n2️⃣ GENETIC ALGORITHM - POPULATION SIZE IMPACT:")
    
    for pop_size in [20, 50, 100]:
        start_time = time.time()
        activation_ga, result_ga = genetic_algorithm(
            simulation,
            population_size=pop_size,
            num_generations=100,
            mutation_rate=0.1,
            crossover_rate=0.8
        )
        execution_time = time.time() - start_time
        coverage_ga = result_ga.coverage
        print(f"   Pop={pop_size}: Coverage={coverage_ga:.1f}% | Time={execution_time:.2f}s")
        
        results.append({
            'optimizer': f'Genetic (Pop={pop_size})',
            'coverage': coverage_ga,
            'time': execution_time,
            'hyperparameters': f'pop_size={pop_size}, generations=100'
        })
    
    # 3. GENETIC ALGORITHM - Mutation Rate Impact
    print("\n3️⃣ GENETIC ALGORITHM - MUTATION RATE IMPACT:")
    
    for mutation_rate in [0.05, 0.1, 0.3]:
        start_time = time.time()
        activation_ga, result_ga = genetic_algorithm(
            simulation,
            population_size=50,
            num_generations=100,
            mutation_rate=mutation_rate,
            crossover_rate=0.8
        )
        execution_time = time.time() - start_time
        coverage_ga = result_ga.coverage
        print(f"   Mutation={mutation_rate}: Coverage={coverage_ga:.1f}% | Time={execution_time:.2f}s")
        
        results.append({
            'optimizer': f'Genetic (Mut={mutation_rate})',
            'coverage': coverage_ga,
            'time': execution_time,
            'hyperparameters': f'mutation_rate={mutation_rate}, pop_size=50'
        })
    
    # 4. PARTICLE SWARM OPTIMIZATION - Different Parameters
    print("\n4️⃣ PARTICLE SWARM OPTIMIZATION - PARAMETER IMPACT:")
    
    pso_configs = [
        {'swarm_size': 30, 'w': 0.5, 'c1': 1.5, 'c2': 1.5},
        {'swarm_size': 50, 'w': 0.7, 'c1': 2.0, 'c2': 2.0},
        {'swarm_size': 20, 'w': 0.9, 'c1': 1.0, 'c2': 1.0}
    ]
    
    for i, config in enumerate(pso_configs):
        start_time = time.time()
        activation_pso, result_pso = particle_swarm_optimization(
            simulation,
            swarm_size=config['swarm_size'],
            max_iterations=200,
            w=config['w'],
            c1=config['c1'],
            c2=config['c2']
        )
        execution_time = time.time() - start_time
        coverage_pso = result_pso.coverage
        print(f"   Config {i+1}: Coverage={coverage_pso:.1f}% | Time={execution_time:.2f}s")
        print(f"               (swarm={config['swarm_size']}, w={config['w']}, c1={config['c1']}, c2={config['c2']})")
        
        results.append({
            'optimizer': f'PSO Config {i+1}',
            'coverage': coverage_pso,
            'time': execution_time,
            'hyperparameters': f"swarm={config['swarm_size']}, w={config['w']}"
        })
    
    # 5. SIMULATED ANNEALING - Temperature Impact
    print("\n5️⃣ SIMULATED ANNEALING - TEMPERATURE IMPACT:")
    
    for temp in [100, 500, 1000]:
        start_time = time.time()
        activation_sa, result_sa = simulated_annealing(
            simulation,
            initial_temperature=temp,
            cooling_rate=0.95,
            max_iterations=300
        )
        execution_time = time.time() - start_time
        coverage_sa = result_sa.coverage
        print(f"   Temp={temp}: Coverage={coverage_sa:.1f}% | Time={execution_time:.2f}s")
        
        results.append({
            'optimizer': f'SA (Temp={temp})',
            'coverage': coverage_sa,
            'time': execution_time,
            'hyperparameters': f'initial_temp={temp}, cooling=0.95'
        })
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame(results)
    
    print("\n" + "=" * 60)
    print("📈 FINAL COMPARISON SUMMARY:")
    print("=" * 60)
    
    # Sort by coverage performance
    df_sorted = df.sort_values('coverage', ascending=False)
    
    for idx, row in df_sorted.iterrows():
        print(f"{row['optimizer']:20} | Coverage: {row['coverage']:5.1f}% | Time: {row['time']:5.2f}s")
    
    # Calculate performance differences
    max_coverage = df['coverage'].max()
    min_coverage = df['coverage'].min()
    coverage_range = max_coverage - min_coverage
    
    print(f"\n🎯 KEY FINDINGS:")
    print(f"   • Best Coverage: {max_coverage:.1f}%")
    print(f"   • Worst Coverage: {min_coverage:.1f}%")
    print(f"   • Performance Range: {coverage_range:.1f}% difference!")
    print(f"   • Relative Improvement: {(coverage_range/min_coverage)*100:.1f}%")
    
    # Create visualization
    create_comparison_plot(df_sorted)
    
    return df_sorted

def create_comparison_plot(df):
    """Create visualization showing optimizer performance differences."""
    
    plt.figure(figsize=(14, 8))
    
    # Coverage comparison
    plt.subplot(2, 1, 1)
    bars = plt.bar(range(len(df)), df['coverage'], 
                   color=['#2E8B57' if 'Smart Greedy' in opt else '#4682B4' if 'Genetic' in opt 
                         else '#FF6347' if 'PSO' in opt else '#9370DB' 
                         for opt in df['optimizer']])
    
    plt.title('Coverage Performance by Optimizer & Hyperparameters', fontsize=14, fontweight='bold')
    plt.ylabel('Coverage Percentage (%)', fontsize=12)
    plt.xticks(range(len(df)), df['optimizer'], rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for i, v in enumerate(df['coverage']):
        plt.text(i, v + 0.5, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # Execution time comparison
    plt.subplot(2, 1, 2)
    plt.bar(range(len(df)), df['time'], 
            color=['#2E8B57' if 'Smart Greedy' in opt else '#4682B4' if 'Genetic' in opt 
                  else '#FF6347' if 'PSO' in opt else '#9370DB' 
                  for opt in df['optimizer']], alpha=0.7)
    
    plt.title('Execution Time by Optimizer & Hyperparameters', fontsize=14, fontweight='bold')
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.xticks(range(len(df)), df['optimizer'], rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, v in enumerate(df['time']):
        plt.text(i, v + 0.02, f'{v:.2f}s', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('optimizer_hyperparameter_comparison.png', dpi=300, bbox_inches='tight')
    print(f"\n📊 Comparison plot saved: optimizer_hyperparameter_comparison.png")
    
    return plt

if __name__ == "__main__":
    # Configure matplotlib for non-interactive use
    plt.switch_backend('Agg')
    
    # Run the comprehensive analysis
    results_df = analyze_optimizer_impact()
    
    print(f"\n✅ Analysis complete! Results show dramatic differences between optimizers and hyperparameters.")
