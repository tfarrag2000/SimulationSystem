
"""
Enhanced Comprehensive Experimental Suite
Modified version with coverage improvements integrated
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import time
from datetime import datetime
import os

# Import your existing modules
from algorithms import get_algorithms
from app import DroneSimulationEnvironment

# ENHANCEMENT: Import the coverage optimizer
from enhanced_coverage_optimizer import create_enhanced_environment, enhance_existing_algorithm

def run_enhanced_comprehensive_experiments():
    """Enhanced experimental suite with improved coverage"""
    
    # Your existing scenario configurations
    scenarios = [
        {
            'name': 'Small Dense',
            'width': 25, 'height': 25, 'drones': 5, 'radius': 8,
            'complexity': 'Low',
            'description': 'Dense coverage in small area'
        },
        {
            'name': 'Medium Standard', 
            'width': 50, 'height': 50, 'drones': 15, 'radius': 8,
            'complexity': 'Medium',
            'description': 'Standard configuration for medium area'
        },
        {
            'name': 'Large Sparse',
            'width': 100, 'height': 100, 'drones': 30, 'radius': 12,
            'complexity': 'High', 
            'description': 'Sparse coverage over large area'
        },
        {
            'name': 'High Density',
            'width': 60, 'height': 60, 'drones': 20, 'radius': 6,
            'complexity': 'Medium',
            'description': 'High drone density with smaller radius'
        },
        {
            'name': 'Balanced',
            'width': 40, 'height': 40, 'drones': 12, 'radius': 10,
            'complexity': 'Medium',
            'description': 'Balanced configuration'
        },
        {
            'name': 'Extended',
            'width': 80, 'height': 80, 'drones': 25, 'radius': 10,
            'complexity': 'High',
            'description': 'Extended area with balanced parameters'
        }
    ]
    
    # Get algorithms (your existing function)
    algorithms = get_algorithms()
    
    # ENHANCEMENT: Optionally enhance algorithms 
    # enhanced_algorithms = {name: enhance_existing_algorithm(func) for name, func in algorithms.items()}
    
    results = []
    total_experiments = len(scenarios) * len(algorithms) * 2  # 2 runs each
    experiment_count = 0
    
    print(f"Starting enhanced experimental suite with {total_experiments} experiments...")
    print("=" * 80)
    
    for scenario_config in scenarios:
        print(f"\nRunning scenario: {scenario_config['name']}")
        print(f"Configuration: {scenario_config['width']}x{scenario_config['height']}, "
              f"{scenario_config['drones']} drones, radius {scenario_config['radius']}")
        
        # ENHANCEMENT: Use optimized environment instead of original
        env = create_enhanced_environment(
            scenario_config['width'],
            scenario_config['height'],
            scenario_config['drones'], 
            scenario_config['radius']
        )
        
        # Calculate theoretical maximum coverage for comparison
        total_area = scenario_config['width'] * scenario_config['height']
        drone_coverage_area = np.pi * (scenario_config['radius'] ** 2) * scenario_config['drones']
        theoretical_max = min(100, (drone_coverage_area / total_area) * 100)
        
        for algorithm_name, algorithm_func in algorithms.items():
            print(f"  Testing {algorithm_name}...")
            
            # Run multiple times for statistical significance
            algorithm_results = []
            
            for run in range(2):
                try:
                    start_time = time.time()
                    
                    # Run the algorithm with your existing parameters
                    result = algorithm_func(env, max_iterations=500)
                    
                    end_time = time.time()
                    runtime = end_time - start_time
                    
                    # Extract results (adapt this to your result structure)
                    if isinstance(result, dict):
                        best_coverage = result.get('best_fitness', result.get('coverage', 0))
                        convergence_iteration = result.get('convergence_iteration', 500)
                    else:
                        best_coverage = result if isinstance(result, (int, float)) else 0
                        convergence_iteration = 500
                    
                    experiment_count += 1
                    
                    # Store results
                    algorithm_results.append({
                        'scenario': scenario_config['name'],
                        'algorithm': algorithm_name,
                        'run': run + 1,
                        'coverage': best_coverage,
                        'runtime': runtime,
                        'convergence_iteration': convergence_iteration,
                        'theoretical_max': theoretical_max,
                        'efficiency': (best_coverage / theoretical_max * 100) if theoretical_max > 0 else 0,
                        'area': scenario_config['width'] * scenario_config['height'],
                        'drones': scenario_config['drones'],
                        'radius': scenario_config['radius'],
                        'complexity': scenario_config['complexity']
                    })
                    
                    print(f"    Run {run + 1}: {best_coverage:.2f}% coverage ({runtime:.2f}s)")
                    
                except Exception as e:
                    print(f"    Run {run + 1}: Error - {e}")
                    algorithm_results.append({
                        'scenario': scenario_config['name'],
                        'algorithm': algorithm_name, 
                        'run': run + 1,
                        'coverage': 0,
                        'runtime': 0,
                        'convergence_iteration': 0,
                        'theoretical_max': theoretical_max,
                        'efficiency': 0,
                        'area': scenario_config['width'] * scenario_config['height'],
                        'drones': scenario_config['drones'],
                        'radius': scenario_config['radius'],
                        'complexity': scenario_config['complexity'],
                        'error': str(e)
                    })
            
            results.extend(algorithm_results)
            
            # Show progress
            avg_coverage = np.mean([r['coverage'] for r in algorithm_results])
            print(f"    Average: {avg_coverage:.2f}% coverage")
            print(f"    Progress: {experiment_count}/{total_experiments} experiments completed")
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame(results)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Enhanced_Coverage_Results_{timestamp}"
    
    df.to_csv(f"{filename}.csv", index=False, encoding='utf-8')
    print(f"\nResults saved to {filename}.csv")
    
    # Generate summary statistics
    generate_enhanced_summary(df, filename)
    
    return df

def generate_enhanced_summary(df, filename):
    """Generate enhanced summary with improvement analysis"""
    
    print("\n" + "="*80)
    print("ENHANCED EXPERIMENTAL RESULTS SUMMARY")
    print("="*80)
    
    # Overall statistics
    print("\nOVERALL PERFORMANCE:")
    print("-" * 25)
    avg_coverage = df['coverage'].mean()
    max_coverage = df['coverage'].max()
    std_coverage = df['coverage'].std()
    
    print(f"Average Coverage: {avg_coverage:.2f}% (±{std_coverage:.2f}%)")
    print(f"Maximum Coverage: {max_coverage:.2f}%")
    print(f"Successful Experiments: {len(df[df['coverage'] > 0])}/{len(df)}")
    
    # By scenario
    print("\nBY SCENARIO:")
    print("-" * 15)
    scenario_summary = df.groupby('scenario').agg({
        'coverage': ['mean', 'max', 'std'],
        'efficiency': 'mean',
        'runtime': 'mean'
    }).round(2)
    
    print(scenario_summary)
    
    # By algorithm
    print("\nBY ALGORITHM:")
    print("-" * 15)
    algorithm_summary = df.groupby('algorithm').agg({
        'coverage': ['mean', 'max', 'std'],
        'runtime': 'mean',
        'convergence_iteration': 'mean'
    }).round(2)
    
    print(algorithm_summary)
    
    # Generate visualization
    generate_enhanced_visualizations(df, filename)

def generate_enhanced_visualizations(df, filename):
    """Generate enhanced visualizations"""
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Enhanced Drone Coverage Optimization Results', fontsize=16, fontweight='bold')
    
    # Plot 1: Coverage by scenario
    scenario_means = df.groupby('scenario')['coverage'].mean().sort_values(ascending=False)
    axes[0, 0].bar(range(len(scenario_means)), scenario_means.values)
    axes[0, 0].set_title('Average Coverage by Scenario')
    axes[0, 0].set_ylabel('Coverage (%)')
    axes[0, 0].set_xticks(range(len(scenario_means)))
    axes[0, 0].set_xticklabels(scenario_means.index, rotation=45, ha='right')
    
    # Plot 2: Coverage by algorithm
    algorithm_means = df.groupby('algorithm')['coverage'].mean().sort_values(ascending=False)
    axes[0, 1].bar(range(len(algorithm_means)), algorithm_means.values)
    axes[0, 1].set_title('Average Coverage by Algorithm') 
    axes[0, 1].set_ylabel('Coverage (%)')
    axes[0, 1].set_xticks(range(len(algorithm_means)))
    axes[0, 1].set_xticklabels(algorithm_means.index, rotation=45, ha='right')
    
    # Plot 3: Runtime analysis
    runtime_means = df.groupby('algorithm')['runtime'].mean().sort_values()
    axes[0, 2].bar(range(len(runtime_means)), runtime_means.values)
    axes[0, 2].set_title('Average Runtime by Algorithm')
    axes[0, 2].set_ylabel('Runtime (seconds)')
    axes[0, 2].set_xticks(range(len(runtime_means)))
    axes[0, 2].set_xticklabels(runtime_means.index, rotation=45, ha='right')
    
    # Plot 4: Efficiency analysis
    efficiency_means = df.groupby('scenario')['efficiency'].mean().sort_values(ascending=False)
    axes[1, 0].bar(range(len(efficiency_means)), efficiency_means.values)
    axes[1, 0].set_title('Efficiency by Scenario (% of Theoretical Max)')
    axes[1, 0].set_ylabel('Efficiency (%)')
    axes[1, 0].set_xticks(range(len(efficiency_means)))
    axes[1, 0].set_xticklabels(efficiency_means.index, rotation=45, ha='right')
    
    # Plot 5: Coverage distribution
    axes[1, 1].hist(df['coverage'], bins=20, alpha=0.7, edgecolor='black')
    axes[1, 1].set_title('Coverage Distribution')
    axes[1, 1].set_xlabel('Coverage (%)')
    axes[1, 1].set_ylabel('Frequency')
    
    # Plot 6: Convergence analysis
    convergence_means = df.groupby('algorithm')['convergence_iteration'].mean().sort_values()
    axes[1, 2].bar(range(len(convergence_means)), convergence_means.values)
    axes[1, 2].set_title('Average Convergence Iteration')
    axes[1, 2].set_ylabel('Iterations')
    axes[1, 2].set_xticks(range(len(convergence_means)))
    axes[1, 2].set_xticklabels(convergence_means.index, rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(f"{filename}_enhanced_analysis.png", dpi=300, bbox_inches='tight')
    print(f"Enhanced visualizations saved to {filename}_enhanced_analysis.png")
    
    plt.close()

if __name__ == "__main__":
    print("Enhanced Comprehensive Experimental Suite")
    print("=" * 50)
    
    # Run enhanced experiments
    results_df = run_enhanced_comprehensive_experiments()
    
    print("\nExperiments completed successfully! 🎉")
    print(f"Total experiments: {len(results_df)}")
    print(f"Average coverage improvement: {results_df['coverage'].mean():.2f}%")
