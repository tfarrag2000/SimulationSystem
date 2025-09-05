#!/usr/bin/env python3
"""
Balanced Algorithm Testing Framework
Tests ALL algorithms equally: PSO, GA, SA, Greedy
Generates comprehensive comparative data for IEEE paper
"""

import sys
import os
import time
import json
import pandas as pd
import numpy as np
from datetime import datetime
import logging

# Add the main directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from algorithms import (
    smart_particle_swarm_optimization,
    particle_swarm_optimization,
    enhanced_genetic_algorithm,
    genetic_algorithm,
    smart_simulated_annealing,
    simulated_annealing,
    greedy_coverage_algorithm
)
from app import DroneSimulationEnvironment

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

class BalancedAlgorithmTester:
    """Balanced testing framework for all algorithms"""
    
    def __init__(self):
        self.algorithms = {
            'Smart_PSO': smart_particle_swarm_optimization,
            'Standard_PSO': particle_swarm_optimization,
            'Smart_GA': enhanced_genetic_algorithm,
            'Standard_GA': genetic_algorithm,
            'Smart_SA': smart_simulated_annealing,
            'Standard_SA': simulated_annealing,
            'Greedy': greedy_coverage_algorithm
        }
        
        self.test_scenarios = {
            'Small': {'width': 40, 'height': 40, 'drones': 12, 'radius': 8},
            'Medium': {'width': 60, 'height': 60, 'drones': 20, 'radius': 10},
            'Large': {'width': 80, 'height': 80, 'drones': 30, 'radius': 12},
            'Extreme': {'width': 100, 'height': 100, 'drones': 40, 'radius': 15}
        }
        
        self.results = []
        
    def test_single_algorithm(self, algorithm_name, algorithm_func, scenario, scenario_name):
        """Test a single algorithm on a single scenario"""
        print(f"\n🧬 Testing {algorithm_name} on {scenario_name} scenario")
        
        try:
            # Create environment
            env = DroneSimulationEnvironment(
                width=scenario['width'],
                height=scenario['height'],
                num_drones=scenario['drones'],
                sensing_radius=scenario['radius']
            )
            
            # Common parameters for all algorithms
            common_params = {
                'max_iterations': 100,
                'target_coverage': 0.95,
                'progress_callback': None
            }
            
            start_time = time.time()
            
            # Execute algorithm with appropriate parameters
            if 'PSO' in algorithm_name:
                result = algorithm_func(
                    env, 
                    swarm_size=30,
                    **common_params
                )
            elif 'GA' in algorithm_name:
                result = algorithm_func(
                    env,
                    population_size=30,
                    **common_params
                )
            elif 'SA' in algorithm_name:
                result = algorithm_func(
                    env,
                    temperature=100.0,
                    **common_params
                )
            elif algorithm_name == 'Greedy':
                result = algorithm_func(
                    env,
                    target_coverage=0.95
                )
            else:
                print(f"❌ Unknown algorithm: {algorithm_name}")
                return None
                
            execution_time = time.time() - start_time
            
            # Extract results safely
            if result and isinstance(result, dict):
                coverage = result.get('final_coverage', 0) * 100
                active_drones = result.get('active_drones', 0)
                total_drones = len(env.drones)
                energy_saved = ((total_drones - active_drones) / total_drones) * 100
                iterations = result.get('iterations', 0)
                
                test_result = {
                    'algorithm': algorithm_name,
                    'scenario': scenario_name,
                    'scenario_size': f"{scenario['width']}x{scenario['height']}",
                    'total_drones': total_drones,
                    'active_drones': active_drones,
                    'coverage_percentage': round(coverage, 2),
                    'energy_saved_percentage': round(energy_saved, 2),
                    'execution_time_seconds': round(execution_time, 2),
                    'iterations': iterations,
                    'timestamp': datetime.now().isoformat()
                }
                
                print(f"✅ {algorithm_name}: Coverage={coverage:.1f}%, "
                      f"Active={active_drones}/{total_drones}, "
                      f"Energy Saved={energy_saved:.1f}%, "
                      f"Time={execution_time:.1f}s")
                
                return test_result
            else:
                print(f"❌ {algorithm_name}: Invalid result format")
                return None
                
        except Exception as e:
            print(f"❌ {algorithm_name}: Error - {str(e)}")
            return None
    
    def run_comparative_tests(self, runs_per_algorithm=3):
        """Run comparative tests across all algorithms and scenarios"""
        print("🚀 BALANCED ALGORITHM COMPARATIVE TESTING")
        print("="*60)
        
        total_tests = len(self.algorithms) * len(self.test_scenarios) * runs_per_algorithm
        current_test = 0
        
        for scenario_name, scenario in self.test_scenarios.items():
            print(f"\n📍 SCENARIO: {scenario_name.upper()}")
            print(f"   Size: {scenario['width']}x{scenario['height']}, "
                  f"Drones: {scenario['drones']}, Radius: {scenario['radius']}")
            print("-" * 50)
            
            for algorithm_name, algorithm_func in self.algorithms.items():
                print(f"\n🔬 Algorithm: {algorithm_name}")
                
                for run in range(runs_per_algorithm):
                    current_test += 1
                    print(f"   Run {run+1}/{runs_per_algorithm} ({current_test}/{total_tests})")
                    
                    result = self.test_single_algorithm(
                        algorithm_name, algorithm_func, scenario, scenario_name
                    )
                    
                    if result:
                        result['run_number'] = run + 1
                        self.results.append(result)
        
        self.save_results()
        self.generate_summary()
    
    def save_results(self):
        """Save results to multiple formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as JSON
        json_file = f"balanced_algorithm_results_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n💾 Results saved to: {json_file}")
        
        # Save as CSV
        if self.results:
            df = pd.DataFrame(self.results)
            csv_file = f"balanced_algorithm_results_{timestamp}.csv"
            df.to_csv(csv_file, index=False)
            print(f"💾 Results saved to: {csv_file}")
    
    def generate_summary(self):
        """Generate a summary analysis"""
        if not self.results:
            print("❌ No results to summarize")
            return
        
        df = pd.DataFrame(self.results)
        
        print("\n📊 COMPARATIVE ALGORITHM PERFORMANCE SUMMARY")
        print("="*60)
        
        # Group by algorithm
        algorithm_stats = df.groupby('algorithm').agg({
            'coverage_percentage': ['mean', 'std'],
            'energy_saved_percentage': ['mean', 'std'],
            'execution_time_seconds': ['mean', 'std'],
            'active_drones': 'mean'
        }).round(2)
        
        print("\n🎯 Coverage Performance (Mean ± Std):")
        for alg in algorithm_stats.index:
            coverage_mean = algorithm_stats.loc[alg, ('coverage_percentage', 'mean')]
            coverage_std = algorithm_stats.loc[alg, ('coverage_percentage', 'std')]
            print(f"   {alg:15}: {coverage_mean:5.1f}% ± {coverage_std:4.1f}%")
        
        print("\n⚡ Energy Efficiency (Mean ± Std):")
        for alg in algorithm_stats.index:
            energy_mean = algorithm_stats.loc[alg, ('energy_saved_percentage', 'mean')]
            energy_std = algorithm_stats.loc[alg, ('energy_saved_percentage', 'std')]
            print(f"   {alg:15}: {energy_mean:5.1f}% ± {energy_std:4.1f}%")
        
        print("\n⏱️  Execution Time (Mean ± Std):")
        for alg in algorithm_stats.index:
            time_mean = algorithm_stats.loc[alg, ('execution_time_seconds', 'mean')]
            time_std = algorithm_stats.loc[alg, ('execution_time_seconds', 'std')]
            print(f"   {alg:15}: {time_mean:5.1f}s ± {time_std:4.1f}s")
        
        # Best performer analysis
        print("\n🏆 BEST PERFORMERS:")
        best_coverage = df.loc[df['coverage_percentage'].idxmax()]
        best_energy = df.loc[df['energy_saved_percentage'].idxmax()]
        fastest = df.loc[df['execution_time_seconds'].idxmin()]
        
        print(f"   Coverage:       {best_coverage['algorithm']} ({best_coverage['coverage_percentage']:.1f}%)")
        print(f"   Energy Savings: {best_energy['algorithm']} ({best_energy['energy_saved_percentage']:.1f}%)")
        print(f"   Speed:          {fastest['algorithm']} ({fastest['execution_time_seconds']:.1f}s)")

def main():
    """Main testing function"""
    print("🧪 BALANCED ALGORITHM TESTING FRAMEWORK")
    print("Testing all algorithms equally: PSO, GA, SA, Greedy")
    print("="*60)
    
    tester = BalancedAlgorithmTester()
    tester.run_comparative_tests(runs_per_algorithm=3)
    
    print("\n✅ BALANCED TESTING COMPLETE!")
    print("All algorithms tested equally with comparative results generated.")

if __name__ == "__main__":
    main()
