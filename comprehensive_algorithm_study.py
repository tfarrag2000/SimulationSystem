#!/usr/bin/env python3
"""
Comprehensive Algorithm Comparative Study
Tests ALL algorithms (PSO, GA, SA, Greedy) with different hyperparameters
Generates detailed comparative analysis for academic research
"""

import sys
import os
import time
import json
import pandas as pd
import numpy as np
from datetime import datetime
import logging
from itertools import product

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

class ComprehensiveAlgorithmStudy:
    """Comprehensive comparative study with hyperparameter analysis"""
    
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
        
        # Test scenarios with varying complexity
        self.scenarios = {
            'Small_Sparse': {'width': 40, 'height': 40, 'drones': 8, 'radius': 12},
            'Small_Dense': {'width': 40, 'height': 40, 'drones': 16, 'radius': 8},
            'Medium_Balanced': {'width': 60, 'height': 60, 'drones': 20, 'radius': 10},
            'Large_Sparse': {'width': 80, 'height': 80, 'drones': 25, 'radius': 15},
            'Large_Dense': {'width': 80, 'height': 80, 'drones': 40, 'radius': 10},
            'Extreme': {'width': 100, 'height': 100, 'drones': 50, 'radius': 12}
        }
        
        # Hyperparameter configurations for each algorithm type
        self.hyperparameters = {
            'PSO': [
                {'swarm_size': 20, 'max_iterations': 50},
                {'swarm_size': 30, 'max_iterations': 75},
                {'swarm_size': 50, 'max_iterations': 100},
                {'swarm_size': 40, 'max_iterations': 150}
            ],
            'GA': [
                {'population_size': 20, 'max_iterations': 50},
                {'population_size': 30, 'max_iterations': 75},
                {'population_size': 50, 'max_iterations': 100},
                {'population_size': 40, 'max_iterations': 150}
            ],
            'SA': [
                {'temperature': 50.0, 'max_iterations': 50},
                {'temperature': 100.0, 'max_iterations': 75},
                {'temperature': 150.0, 'max_iterations': 100},
                {'temperature': 200.0, 'max_iterations': 150}
            ],
            'Greedy': [
                {'target_coverage': 0.85},
                {'target_coverage': 0.90},
                {'target_coverage': 0.95},
                {'target_coverage': 0.98}
            ]
        }
        
        self.results = []
        
    def get_algorithm_type(self, algorithm_name):
        """Determine algorithm type for hyperparameter selection"""
        if 'PSO' in algorithm_name:
            return 'PSO'
        elif 'GA' in algorithm_name:
            return 'GA'
        elif 'SA' in algorithm_name:
            return 'SA'
        else:
            return 'Greedy'
    
    def test_algorithm_configuration(self, algorithm_name, algorithm_func, scenario, scenario_name, hyperparams, config_id):
        """Test a single algorithm configuration"""
        print(f"🔬 {algorithm_name} | {scenario_name} | Config {config_id+1}")
        
        try:
            # Create fresh environment for each test
            env = DroneSimulationEnvironment(
                width=scenario['width'],
                height=scenario['height'],
                num_drones=scenario['drones'],
                sensing_radius=scenario['radius']
            )
            
            start_time = time.time()
            
            # Execute algorithm with specific hyperparameters
            if algorithm_name == 'Greedy':
                result = algorithm_func(env, **hyperparams)
            else:
                # Add common parameters
                params = hyperparams.copy()
                params['target_coverage'] = 0.95
                params['progress_callback'] = None
                result = algorithm_func(env, **params)
                
            execution_time = time.time() - start_time
            
            # Process results safely
            if result and isinstance(result, dict):
                coverage = result.get('final_coverage', 0)
                if coverage > 1:  # Handle percentage vs decimal
                    coverage = coverage / 100
                
                active_drones = result.get('active_drones', len(env.drones))
                total_drones = len(env.drones)
                energy_saved = ((total_drones - active_drones) / total_drones) * 100
                iterations = result.get('iterations', 0)
                
                test_result = {
                    'algorithm': algorithm_name,
                    'algorithm_type': self.get_algorithm_type(algorithm_name),
                    'scenario': scenario_name,
                    'scenario_complexity': f"{scenario['width']}x{scenario['height']}-{scenario['drones']}d",
                    'config_id': config_id + 1,
                    'hyperparameters': str(hyperparams),
                    'total_drones': total_drones,
                    'active_drones': active_drones,
                    'coverage_percentage': round(coverage * 100, 2),
                    'energy_saved_percentage': round(energy_saved, 2),
                    'execution_time_seconds': round(execution_time, 2),
                    'iterations': iterations,
                    'efficiency_score': round((coverage * 100) - (energy_saved * 0.1), 2),  # Composite score
                    'timestamp': datetime.now().isoformat()
                }
                
                # Add specific hyperparameter values for easy analysis
                for key, value in hyperparams.items():
                    test_result[f'hp_{key}'] = value
                
                print(f"   ✅ Coverage: {coverage*100:.1f}% | Active: {active_drones}/{total_drones} | Time: {execution_time:.1f}s")
                return test_result
            else:
                print(f"   ❌ Invalid result format")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return None
    
    def run_comprehensive_study(self, runs_per_config=3):
        """Run comprehensive comparative study with all algorithms and hyperparameters"""
        print("🚀 COMPREHENSIVE ALGORITHM COMPARATIVE STUDY")
        print("="*70)
        print(f"📊 Algorithms: {len(self.algorithms)}")
        print(f"📍 Scenarios: {len(self.scenarios)}")
        print(f"⚙️  Hyperparameter configs per algorithm: 4")
        print(f"🔄 Runs per configuration: {runs_per_config}")
        
        total_configs = sum(len(self.hyperparameters[self.get_algorithm_type(alg)]) 
                           for alg in self.algorithms.keys())
        total_tests = total_configs * len(self.scenarios) * runs_per_config
        print(f"🎯 Total tests: {total_tests}")
        print("="*70)
        
        current_test = 0
        
        for scenario_name, scenario in self.scenarios.items():
            print(f"\n📍 SCENARIO: {scenario_name}")
            print(f"   Area: {scenario['width']}x{scenario['height']}, Drones: {scenario['drones']}, Radius: {scenario['radius']}")
            print("-" * 60)
            
            for algorithm_name, algorithm_func in self.algorithms.items():
                alg_type = self.get_algorithm_type(algorithm_name)
                hyperparams_list = self.hyperparameters[alg_type]
                
                print(f"\n🧬 Algorithm: {algorithm_name} ({len(hyperparams_list)} configurations)")
                
                for config_id, hyperparams in enumerate(hyperparams_list):
                    print(f"   ⚙️ Config {config_id+1}: {hyperparams}")
                    
                    for run in range(runs_per_config):
                        current_test += 1
                        print(f"      Run {run+1}/{runs_per_config} ({current_test}/{total_tests})")
                        
                        result = self.test_algorithm_configuration(
                            algorithm_name, algorithm_func, scenario, scenario_name, 
                            hyperparams, config_id
                        )
                        
                        if result:
                            result['run_number'] = run + 1
                            self.results.append(result)
        
        self.save_results()
        self.generate_comparative_analysis()
    
    def save_results(self):
        """Save results to multiple formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create results directory
        results_dir = "comparative_study_results"
        os.makedirs(results_dir, exist_ok=True)
        
        # Save as JSON
        json_file = f"{results_dir}/comprehensive_study_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Save as CSV
        if self.results:
            df = pd.DataFrame(self.results)
            csv_file = f"{results_dir}/comprehensive_study_{timestamp}.csv"
            df.to_csv(csv_file, index=False)
            
            # Save hyperparameter analysis
            hp_analysis_file = f"{results_dir}/hyperparameter_analysis_{timestamp}.csv"
            self.save_hyperparameter_analysis(df, hp_analysis_file)
        
        print(f"\n💾 Results saved to: {results_dir}/")
    
    def save_hyperparameter_analysis(self, df, filename):
        """Save detailed hyperparameter analysis"""
        hp_results = []
        
        for alg_type in ['PSO', 'GA', 'SA', 'Greedy']:
            alg_data = df[df['algorithm_type'] == alg_type]
            if len(alg_data) == 0:
                continue
                
            if alg_type == 'PSO':
                for size in alg_data['hp_swarm_size'].unique():
                    for iters in alg_data['hp_max_iterations'].unique():
                        subset = alg_data[(alg_data['hp_swarm_size'] == size) & 
                                        (alg_data['hp_max_iterations'] == iters)]
                        if len(subset) > 0:
                            hp_results.append({
                                'algorithm_type': alg_type,
                                'swarm_size': size,
                                'max_iterations': iters,
                                'avg_coverage': subset['coverage_percentage'].mean(),
                                'avg_energy_saved': subset['energy_saved_percentage'].mean(),
                                'avg_time': subset['execution_time_seconds'].mean(),
                                'tests_count': len(subset)
                            })
            
            elif alg_type == 'GA':
                for size in alg_data['hp_population_size'].unique():
                    for iters in alg_data['hp_max_iterations'].unique():
                        subset = alg_data[(alg_data['hp_population_size'] == size) & 
                                        (alg_data['hp_max_iterations'] == iters)]
                        if len(subset) > 0:
                            hp_results.append({
                                'algorithm_type': alg_type,
                                'population_size': size,
                                'max_iterations': iters,
                                'avg_coverage': subset['coverage_percentage'].mean(),
                                'avg_energy_saved': subset['energy_saved_percentage'].mean(),
                                'avg_time': subset['execution_time_seconds'].mean(),
                                'tests_count': len(subset)
                            })
            
            elif alg_type == 'SA':
                for temp in alg_data['hp_temperature'].unique():
                    for iters in alg_data['hp_max_iterations'].unique():
                        subset = alg_data[(alg_data['hp_temperature'] == temp) & 
                                        (alg_data['hp_max_iterations'] == iters)]
                        if len(subset) > 0:
                            hp_results.append({
                                'algorithm_type': alg_type,
                                'temperature': temp,
                                'max_iterations': iters,
                                'avg_coverage': subset['coverage_percentage'].mean(),
                                'avg_energy_saved': subset['energy_saved_percentage'].mean(),
                                'avg_time': subset['execution_time_seconds'].mean(),
                                'tests_count': len(subset)
                            })
            
            elif alg_type == 'Greedy':
                for target in alg_data['hp_target_coverage'].unique():
                    subset = alg_data[alg_data['hp_target_coverage'] == target]
                    if len(subset) > 0:
                        hp_results.append({
                            'algorithm_type': alg_type,
                            'target_coverage': target,
                            'avg_coverage': subset['coverage_percentage'].mean(),
                            'avg_energy_saved': subset['energy_saved_percentage'].mean(),
                            'avg_time': subset['execution_time_seconds'].mean(),
                            'tests_count': len(subset)
                        })
        
        if hp_results:
            hp_df = pd.DataFrame(hp_results)
            hp_df.to_csv(filename, index=False)
            print(f"💾 Hyperparameter analysis saved to: {filename}")
    
    def generate_comparative_analysis(self):
        """Generate comprehensive comparative analysis"""
        if not self.results:
            print("❌ No results to analyze")
            return
        
        df = pd.DataFrame(self.results)
        
        print("\n📊 COMPREHENSIVE COMPARATIVE ANALYSIS")
        print("="*70)
        
        # Overall algorithm performance
        print("\n🎯 OVERALL ALGORITHM PERFORMANCE:")
        algorithm_stats = df.groupby('algorithm').agg({
            'coverage_percentage': ['mean', 'std', 'max'],
            'energy_saved_percentage': ['mean', 'std', 'max'],
            'execution_time_seconds': ['mean', 'std', 'min'],
            'efficiency_score': ['mean', 'std', 'max']
        }).round(2)
        
        for alg in algorithm_stats.index:
            coverage_mean = algorithm_stats.loc[alg, ('coverage_percentage', 'mean')]
            coverage_std = algorithm_stats.loc[alg, ('coverage_percentage', 'std')]
            time_mean = algorithm_stats.loc[alg, ('execution_time_seconds', 'mean')]
            efficiency_mean = algorithm_stats.loc[alg, ('efficiency_score', 'mean')]
            
            print(f"   {alg:15}: Coverage={coverage_mean:5.1f}%±{coverage_std:4.1f} | "
                  f"Time={time_mean:5.1f}s | Efficiency={efficiency_mean:5.1f}")
        
        # Performance by scenario complexity
        print("\n📍 PERFORMANCE BY SCENARIO COMPLEXITY:")
        scenario_stats = df.groupby(['scenario', 'algorithm'])['coverage_percentage'].mean().unstack()
        for scenario in scenario_stats.index:
            print(f"\n   {scenario}:")
            for alg in scenario_stats.columns:
                if not pd.isna(scenario_stats.loc[scenario, alg]):
                    print(f"      {alg:15}: {scenario_stats.loc[scenario, alg]:5.1f}%")
        
        # Best hyperparameters analysis
        print("\n⚙️ BEST HYPERPARAMETER CONFIGURATIONS:")
        for alg_type in ['PSO', 'GA', 'SA', 'Greedy']:
            alg_data = df[df['algorithm_type'] == alg_type]
            if len(alg_data) > 0:
                best_config = alg_data.loc[alg_data['efficiency_score'].idxmax()]
                print(f"   {alg_type:8}: {best_config['hyperparameters']} "
                      f"(Coverage: {best_config['coverage_percentage']:.1f}%, "
                      f"Efficiency: {best_config['efficiency_score']:.1f})")
        
        # Statistical significance analysis
        print("\n📈 STATISTICAL ANALYSIS:")
        print(f"   Total tests conducted: {len(df)}")
        print(f"   Algorithms tested: {df['algorithm'].nunique()}")
        print(f"   Scenarios tested: {df['scenario'].nunique()}")
        print(f"   Hyperparameter configurations: {df['config_id'].nunique()}")
        
        # Top performers
        print("\n🏆 TOP PERFORMERS:")
        best_coverage = df.loc[df['coverage_percentage'].idxmax()]
        best_efficiency = df.loc[df['efficiency_score'].idxmax()]
        fastest = df.loc[df['execution_time_seconds'].idxmin()]
        
        print(f"   Best Coverage:    {best_coverage['algorithm']} ({best_coverage['coverage_percentage']:.1f}%)")
        print(f"   Best Efficiency:  {best_efficiency['algorithm']} (Score: {best_efficiency['efficiency_score']:.1f})")
        print(f"   Fastest:          {fastest['algorithm']} ({fastest['execution_time_seconds']:.1f}s)")
        
        print(f"\n✅ COMPREHENSIVE STUDY COMPLETE!")
        print(f"📊 Ready for academic paper analysis and publication")

def main():
    """Main function to run comprehensive study"""
    print("🧪 COMPREHENSIVE ALGORITHM COMPARATIVE STUDY")
    print("Testing ALL algorithms with multiple hyperparameters")
    print("="*70)
    
    study = ComprehensiveAlgorithmStudy()
    study.run_comprehensive_study(runs_per_config=2)  # 2 runs per config for faster testing
    
    print("\n🎉 Study complete! Check the comparative_study_results/ directory for detailed results.")

if __name__ == "__main__":
    main()
