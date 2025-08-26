#!/usr/bin/env python3
"""
Simple Comprehensive Experiment Runner - All 14 Algorithms
Quick test of all 14 algorithms with organized results
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from pathlib import Path
from datetime import datetime

# Import our modules
from algorithms import *
from environment import DroneSimulationEnvironment

# Set matplotlib backend
plt.switch_backend('Agg')

def run_quick_comprehensive_test():
    """Quick test of all 14 algorithms"""
    print("🚀 QUICK COMPREHENSIVE TEST - ALL 14 ALGORITHMS")
    print("=" * 60)
    
    # Create results directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path(f"Quick_Results_{timestamp}")
    results_dir.mkdir(exist_ok=True)
    
    # Define algorithms
    algorithms = {
        "Greedy": greedy_algorithm,
        "PSO": pso_algorithm,
        "GA": genetic_algorithm,
        "SA": simulated_annealing_algorithm,
        "GWO": grey_wolf_optimizer,
        "MRFO": manta_ray_foraging_optimization,
        "GA_SA_Hybrid": ga_sa_hybrid_algorithm,
        "Staged_Greedy": staged_greedy_algorithm,
        "Staged_PSO": staged_pso_algorithm,
        "Staged_GA": staged_genetic_algorithm,
        "Staged_SA": staged_simulated_annealing_algorithm,
        "Staged_GWO": staged_grey_wolf_optimizer,
        "Staged_MRFO": staged_manta_ray_foraging_optimization,
        "Staged_GA_SA_Hybrid": staged_ga_sa_hybrid_algorithm
    }
    
    # Define scenarios
    scenarios = {
        "Small": {"drones": 8, "targets": 20, "area": (20, 20)},
        "Medium": {"drones": 12, "targets": 30, "area": (25, 25)},
        "Large": {"drones": 16, "targets": 40, "area": (30, 30)}
    }
    
    print(f"📊 Testing {len(algorithms)} algorithms on {len(scenarios)} scenarios")
    
    # Run experiments
    results = []
    total = len(algorithms) * len(scenarios)
    current = 0
    
    for scenario_name, scenario_config in scenarios.items():
        print(f"\n📍 SCENARIO: {scenario_name}")
        
        for alg_name, alg_func in algorithms.items():
            current += 1
            progress = (current / total) * 100
            
            print(f"[{current:2d}/{total}] ({progress:5.1f}%) Testing {alg_name}...", end=" ")
            
            try:
                # Create environment
                env = DroneSimulationEnvironment(
                    area_size=scenario_config["area"],
                    num_targets=scenario_config["targets"],
                    coverage_radius=2.5
                )
                
                # Run algorithm
                start_time = time.time()
                result = alg_func(env, scenario_config["drones"])
                execution_time = time.time() - start_time
                
                # Calculate metrics
                coverage = env.calculate_coverage_percentage(result)
                active_drones = len(result)
                energy_efficiency = coverage / active_drones if active_drones > 0 else 0
                
                results.append({
                    'algorithm': alg_name,
                    'scenario': scenario_name,
                    'coverage_percentage': coverage,
                    'active_drones': active_drones,
                    'energy_efficiency': energy_efficiency,
                    'execution_time': execution_time
                })
                
                print(f"✅ {coverage:.1f}% coverage, {active_drones} drones")
                
            except Exception as e:
                print(f"❌ Error: {str(e)[:50]}")
                results.append({
                    'algorithm': alg_name,
                    'scenario': scenario_name,
                    'coverage_percentage': 0,
                    'active_drones': 0,
                    'energy_efficiency': 0,
                    'execution_time': 0,
                    'error': str(e)
                })
    
    # Save results
    df = pd.DataFrame(results)
    successful_df = df[df['coverage_percentage'] > 0]
    
    # Save CSV
    csv_path = results_dir / "quick_test_results.csv"
    successful_df.to_csv(csv_path, index=False)
    
    # Generate summary
    if len(successful_df) > 0:
        print(f"\n📊 RESULTS SUMMARY:")
        print(f"   Successful experiments: {len(successful_df)}/{len(results)}")
        
        # Algorithm ranking
        algo_ranking = successful_df.groupby('algorithm')['coverage_percentage'].mean().sort_values(ascending=False)
        print(f"\n🏆 TOP ALGORITHMS:")
        for i, (alg, coverage) in enumerate(algo_ranking.head(5).items(), 1):
            print(f"   {i}. {alg:20s}: {coverage:6.2f}%")
        
        # Staged vs Original
        original_algs = successful_df[~successful_df['algorithm'].str.startswith('Staged_')]
        staged_algs = successful_df[successful_df['algorithm'].str.startswith('Staged_')]
        
        if len(original_algs) > 0 and len(staged_algs) > 0:
            orig_avg = original_algs['coverage_percentage'].mean()
            staged_avg = staged_algs['coverage_percentage'].mean()
            improvement = staged_avg - orig_avg
            
            print(f"\n🔄 STAGED vs ORIGINAL:")
            print(f"   Original average: {orig_avg:.2f}%")
            print(f"   Staged average:   {staged_avg:.2f}%")
            print(f"   Improvement:      +{improvement:.2f}%")
        
        # Create quick visualization
        plt.figure(figsize=(12, 6))
        
        colors = ['orange' if alg.startswith('Staged_') else 'skyblue' for alg in algo_ranking.index]
        bars = plt.bar(range(len(algo_ranking)), algo_ranking.values, color=colors)
        
        plt.title('Algorithm Performance Comparison - All 14 Algorithms')
        plt.xlabel('Algorithm')
        plt.ylabel('Coverage Percentage (%)')
        plt.xticks(range(len(algo_ranking)), algo_ranking.index, rotation=45, ha='right')
        
        # Add value labels
        for bar, value in zip(bars, algo_ranking.values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{value:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(results_dir / 'algorithm_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n📁 Results saved to: {results_dir}")
        print(f"   📄 Data: quick_test_results.csv")
        print(f"   📊 Figure: algorithm_comparison.png")
        
    else:
        print("❌ No successful experiments!")
    
    return results_dir

if __name__ == "__main__":
    run_quick_comprehensive_test()
