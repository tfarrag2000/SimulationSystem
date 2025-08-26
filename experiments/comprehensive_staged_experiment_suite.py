#!/usr/bin/env python3
"""
COMPREHENSIVE STAGED ALGORITHM EXPERIMENT SUITE
Tests both Original and Staged versions of all 7 algorithms
Generates complete comparison data for academic paper
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import time
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from algorithms import *
from app import DroneSimulationEnvironment

def create_test_scenarios():
    """Create 6 comprehensive test scenarios"""
    scenarios = {
        'small_coverage': {
            'name': 'Small Area - High Coverage Potential',
            'area_width': 100,
            'area_height': 100,
            'num_drones': 12,
            'seed': 42,
            'complexity': 'Low'
        },
        'medium_coverage': {
            'name': 'Medium Area - Balanced Scenario',
            'area_width': 150,
            'area_height': 150,
            'num_drones': 18,
            'seed': 123,
            'complexity': 'Medium'
        },
        'large_coverage': {
            'name': 'Large Area - Coverage Challenge',
            'area_width': 200,
            'area_height': 200,
            'num_drones': 25,
            'seed': 456,
            'complexity': 'High'
        },
        'dense_optimal': {
            'name': 'Dense Drone Deployment',
            'area_width': 120,
            'area_height': 120,
            'num_drones': 20,
            'seed': 789,
            'complexity': 'Medium'
        },
        'sparse_challenge': {
            'name': 'Sparse Drone Challenge',
            'area_width': 180,
            'area_height': 180,
            'num_drones': 15,
            'seed': 321,
            'complexity': 'High'
        },
        'extreme_coverage': {
            'name': 'Extreme Coverage Scenario',
            'area_width': 250,
            'area_height': 250,
            'num_drones': 30,
            'seed': 654,
            'complexity': 'Extreme'
        }
    }
    return scenarios

def get_all_algorithms():
    """Define all 14 algorithms (7 original + 7 staged)"""
    algorithms = {
        # ORIGINAL ALGORITHMS
        'greedy': {
            'name': 'Greedy Algorithm',
            'function': greedy_optimization,
            'type': 'original',
            'params': {'desired_coverage': 0.99}
        },
        'ga': {
            'name': 'Genetic Algorithm',
            'function': genetic_algorithm,
            'type': 'original',
            'params': {'num_generations': 20, 'population_size': 15}
        },
        'pso': {
            'name': 'Particle Swarm Optimization',
            'function': particle_swarm_optimization,
            'type': 'original',
            'params': {'iterations': 20, 'num_particles': 15}
        },
        'sa': {
            'name': 'Simulated Annealing',
            'function': simulated_annealing,
            'type': 'original',
            'params': {'iterations': 100, 'initial_temp': 100.0}
        },
        'ga_sa_hybrid': {
            'name': 'GA-SA Hybrid',
            'function': genetic_algorithm_with_sa,
            'type': 'original',
            'params': {'num_generations': 15, 'population_size': 10}
        },
        'gwo': {
            'name': 'Grey Wolf Optimizer',
            'function': grey_wolf_optimizer,
            'type': 'original',
            'params': {'iterations': 20, 'num_wolves': 15}
        },
        'mrfo': {
            'name': 'Manta Ray Foraging Optimization',
            'function': manta_ray_foraging_optimization,
            'type': 'original',
            'params': {'iterations': 20, 'num_rays': 15}
        },
        
        # STAGED ALGORITHMS
        'staged_greedy': {
            'name': 'Staged Greedy',
            'function': lambda sim, **kwargs: staged_optimization_wrapper(greedy_optimization, sim, **kwargs),
            'type': 'staged',
            'params': {'desired_coverage': 0.99}
        },
        'staged_ga': {
            'name': 'Staged GA',
            'function': lambda sim, **kwargs: staged_optimization_wrapper(genetic_algorithm, sim, **kwargs),
            'type': 'staged',
            'params': {'num_generations': 20, 'population_size': 15}
        },
        'staged_pso': {
            'name': 'Staged PSO',
            'function': lambda sim, **kwargs: staged_optimization_wrapper(particle_swarm_optimization, sim, **kwargs),
            'type': 'staged',
            'params': {'iterations': 20, 'num_particles': 15}
        },
        'staged_sa': {
            'name': 'Staged SA',
            'function': lambda sim, **kwargs: staged_optimization_wrapper(simulated_annealing, sim, **kwargs),
            'type': 'staged',
            'params': {'iterations': 100, 'initial_temp': 100.0}
        },
        'staged_ga_sa_hybrid': {
            'name': 'Staged GA-SA Hybrid',
            'function': lambda sim, **kwargs: staged_optimization_wrapper(genetic_algorithm_with_sa, sim, **kwargs),
            'type': 'staged',
            'params': {'num_generations': 15, 'population_size': 10}
        },
        'staged_gwo': {
            'name': 'Staged GWO',
            'function': lambda sim, **kwargs: staged_optimization_wrapper(grey_wolf_optimizer, sim, **kwargs),
            'type': 'staged',
            'params': {'iterations': 20, 'num_wolves': 15}
        },
        'staged_mrfo': {
            'name': 'Staged MRFO',
            'function': lambda sim, **kwargs: staged_optimization_wrapper(manta_ray_foraging_optimization, sim, **kwargs),
            'type': 'staged',
            'params': {'iterations': 20, 'num_rays': 15}
        }
    }
    return algorithms

def run_single_experiment(algorithm_info, simulation, run_number=1):
    """Run a single algorithm experiment"""
    algorithm_name = algorithm_info['name']
    algorithm_func = algorithm_info['function']
    algorithm_params = algorithm_info['params'].copy()
    
    print(f"🔄 Running {algorithm_name} - Run {run_number}")
    
    try:
        start_time = time.time()
        activation, result = algorithm_func(simulation, **algorithm_params)
        execution_time = time.time() - start_time
        
        # Calculate results
        coverage = simulation.calculate_coverage_percentage(activation)
        active_drones = np.sum(activation >= 0.5)
        converged = result.get('converged', True)
        
        return {
            'algorithm': algorithm_name,
            'algorithm_type': algorithm_info['type'],
            'coverage': coverage,
            'active_drones': active_drones,
            'execution_time': execution_time,
            'converged': converged,
            'run_number': run_number,
            'hyperparameters': str(algorithm_params)
        }
        
    except Exception as e:
        print(f"❌ Error in {algorithm_name}: {e}")
        return {
            'algorithm': algorithm_name,
            'algorithm_type': algorithm_info['type'],
            'coverage': 0.0,
            'active_drones': 0,
            'execution_time': 0.0,
            'converged': False,
            'run_number': run_number,
            'error': str(e)
        }

def run_comprehensive_experiments():
    """Run comprehensive experiments with all algorithms and scenarios"""
    print("🚀 STARTING COMPREHENSIVE STAGED ALGORITHM EXPERIMENTS")
    print("=" * 80)
    
    scenarios = create_test_scenarios()
    algorithms = get_all_algorithms()
    
    # Create results directory in The Paper folder
    results_dir = "The Paper/Experiments/Results/Comprehensive_Staged_Study"
    os.makedirs(results_dir, exist_ok=True)
    
    all_results = []
    total_experiments = len(scenarios) * len(algorithms) * 3  # 3 runs per combo
    completed = 0
    
    # Run experiments
    for scenario_name, scenario_config in scenarios.items():
        print(f"\n📊 SCENARIO: {scenario_config['name']}")
        print("-" * 60)
        
        # Create simulation
        simulation = DroneSimulationEnvironment(
            area_width=scenario_config['area_width'],
            area_height=scenario_config['area_height'],
            num_drones=scenario_config['num_drones'],
            sensing_range=15,
            random_seed=scenario_config['seed']
        )
        
        scenario_results = []
        
        for algorithm_id, algorithm_info in algorithms.items():
            algorithm_results = []
            
            # Run multiple times for statistical significance
            for run in range(1, 4):  # 3 runs for faster execution
                result = run_single_experiment(algorithm_info, simulation, run)
                result['scenario'] = scenario_name
                result['scenario_name'] = scenario_config['name']
                result['scenario_complexity'] = scenario_config['complexity']
                
                algorithm_results.append(result)
                all_results.append(result)
                
                completed += 1
                progress = (completed / total_experiments) * 100
                print(f"   ✅ {algorithm_info['name']} - Run {run} - Coverage: {result['coverage']:.1f}% - Progress: {progress:.1f}%")
            
            scenario_results.extend(algorithm_results)
        
        # Save scenario results
        scenario_df = pd.DataFrame(scenario_results)
        scenario_file = f"{results_dir}/{scenario_name}_results.csv"
        scenario_df.to_csv(scenario_file, index=False)
        print(f"📁 Saved: {scenario_file}")
    
    # Save comprehensive results
    print(f"\n💾 SAVING COMPREHENSIVE RESULTS...")
    
    # Create comprehensive DataFrame
    results_df = pd.DataFrame(all_results)
    
    # Save to The Paper/Data folder
    data_dir = "The Paper/Data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Main results file
    main_file = f"{data_dir}/comprehensive_staged_experimental_results.csv"
    results_df.to_csv(main_file, index=False)
    
    # JSON format for detailed analysis
    json_file = f"{data_dir}/comprehensive_staged_results.json"
    with open(json_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Generate summary statistics
    generate_summary_statistics(results_df, data_dir)
    
    print(f"🎉 EXPERIMENTS COMPLETE!")
    print(f"📊 Total Experiments: {len(all_results)}")
    print(f"📁 Results saved to: {data_dir}")
    
    return results_df

def generate_summary_statistics(results_df, output_dir):
    """Generate summary statistics and rankings"""
    print("📊 Generating summary statistics...")
    
    # Algorithm performance summary
    algorithm_stats = results_df.groupby(['algorithm', 'algorithm_type']).agg({
        'coverage': ['mean', 'std', 'min', 'max'],
        'active_drones': ['mean', 'std'],
        'execution_time': ['mean', 'std'],
        'converged': 'sum'
    }).round(2)
    
    # Flatten column names
    algorithm_stats.columns = ['_'.join(col).strip() for col in algorithm_stats.columns]
    algorithm_stats = algorithm_stats.reset_index()
    
    # Calculate convergence rate
    total_runs = results_df.groupby('algorithm').size()
    algorithm_stats['convergence_rate'] = (algorithm_stats['converged_sum'] / total_runs.values * 100).round(1)
    
    # Create ranking
    algorithm_ranking = algorithm_stats[['algorithm', 'algorithm_type', 'coverage_mean', 'coverage_std', 
                                       'active_drones_mean', 'execution_time_mean', 'convergence_rate']].copy()
    algorithm_ranking = algorithm_ranking.sort_values('coverage_mean', ascending=False)
    
    # Save summary files
    algorithm_stats.to_csv(f"{output_dir}/algorithm_performance_statistics.csv", index=False)
    algorithm_ranking.to_csv(f"{output_dir}/algorithm_ranking_staged.csv", index=False)
    
    # Scenario-wise statistics
    scenario_stats = results_df.groupby(['scenario', 'algorithm']).agg({
        'coverage': ['mean', 'std', 'min', 'max'],
        'converged': 'sum'
    }).round(2)
    scenario_stats.to_csv(f"{output_dir}/scenario_statistics_staged.csv")
    
    print(f"✅ Summary statistics saved to {output_dir}")

if __name__ == "__main__":
    print("🎯 COMPREHENSIVE STAGED ALGORITHM EXPERIMENT SUITE")
    print("📊 Testing 14 Algorithms (7 Original + 7 Staged) across 6 Scenarios")
    print("🔬 12 Runs per Algorithm-Scenario combination")
    print(f"📈 Total Experiments: {6 * 14 * 12} = {6 * 14 * 12}")
    
    start_time = time.time()
    results = run_comprehensive_experiments()
    total_time = time.time() - start_time
    
    print(f"\n⏱️ Total Execution Time: {total_time:.2f} seconds")
    print(f"🎉 All experiments completed successfully!")
    print(f"📁 Check 'The Paper/Data/' folder for results")
