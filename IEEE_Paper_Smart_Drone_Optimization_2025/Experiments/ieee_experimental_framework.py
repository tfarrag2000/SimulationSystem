#!/usr/bin/env python3
"""
IEEE PAPER EXPERIMENTAL FRAMEWORK v2025
Comprehensive experiments with parallel/non-parallel comparison
Results-focused performance evaluation for IEEE publication
"""

import os
import sys
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
from datetime import datetime
from multiprocessing import cpu_count
import warnings
warnings.filterwarnings('ignore')

# Set professional plotting style
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

# Import system modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from app import DroneSimulationEnvironment
from algorithms import (
    particle_swarm_optimization, genetic_algorithm, simulated_annealing,
    detect_and_report_duplicates
)

class IEEE_ExperimentalFramework:
    """Comprehensive experimental framework for IEEE paper"""
    
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = {}
        self.figures_dir = os.path.join(output_dir, "Figures")
        self.data_dir = os.path.join(output_dir, "Data")
        self.experiments_dir = os.path.join(output_dir, "Experiments")
        
        # Ensure directories exist
        for dir_path in [self.figures_dir, self.data_dir, self.experiments_dir]:
            os.makedirs(dir_path, exist_ok=True)
    
    def define_test_scenarios(self):
        """Define comprehensive test scenarios - 4 scales as requested"""
        
        scenarios = {
            "Small_Scale": [
                {"width": 40, "height": 40, "drones": 12, "radius": 10, "name": "Small_Dense"},
                {"width": 40, "height": 40, "drones": 15, "radius": 8, "name": "Small_Compact"},
                {"width": 50, "height": 40, "drones": 18, "radius": 9, "name": "Small_Extended"}
            ],
            "Medium_Scale": [
                {"width": 60, "height": 60, "drones": 25, "radius": 12, "name": "Medium_Balanced"},
                {"width": 70, "height": 50, "drones": 28, "radius": 14, "name": "Medium_Wide"},
                {"width": 55, "height": 65, "drones": 22, "radius": 13, "name": "Medium_Tall"}
            ],
            "Large_Scale": [
                {"width": 80, "height": 80, "drones": 40, "radius": 15, "name": "Large_Grid"},
                {"width": 90, "height": 70, "drones": 45, "radius": 16, "name": "Large_Extended"},
                {"width": 75, "height": 85, "drones": 42, "radius": 14, "name": "Large_Vertical"}
            ],
            "Extreme_Scale": [
                {"width": 100, "height": 100, "drones": 60, "radius": 18, "name": "Extreme_Full"},
                {"width": 120, "height": 80, "drones": 65, "radius": 20, "name": "Extreme_Wide"},
                {"width": 85, "height": 115, "drones": 58, "radius": 17, "name": "Extreme_Tall"}
            ]
        }
        
        return scenarios
    
    def define_algorithms(self):
        """Define all algorithms for equal treatment comparison"""
        
        algorithms = {
            "Smart_PSO": {
                "func": particle_swarm_optimization,
                "params": {
                    "swarm_size": 50,
                    "iterations": 100,
                    "inertia": 0.7,
                    "cognitive_weight": 1.5,
                    "social_weight": 1.5,
                    "smart_mode": True,
                    "parallel_processing": False  # Will be varied
                }
            },
            "Standard_PSO": {
                "func": particle_swarm_optimization,
                "params": {
                    "swarm_size": 50,
                    "iterations": 100,
                    "inertia": 0.5,
                    "cognitive_weight": 1.5,
                    "social_weight": 1.5,
                    "smart_mode": False,
                    "parallel_processing": False
                }
            },
            "Smart_GA": {
                "func": genetic_algorithm,
                "params": {
                    "population_size": 50,
                    "num_generations": 100,
                    "mutation_rate": 0.1,
                    "crossover_rate": 0.8,
                    "smart_mode": True,
                    "parallel_processing": False
                }
            },
            "Standard_GA": {
                "func": genetic_algorithm,
                "params": {
                    "population_size": 50,
                    "num_generations": 100,
                    "mutation_rate": 0.1,
                    "crossover_rate": 0.8,
                    "smart_mode": False,
                    "parallel_processing": False
                }
            },
            "Smart_SA": {
                "func": simulated_annealing,
                "params": {
                    "num_iterations": 100,
                    "initial_temp": 100,
                    "cooling_rate": 0.95,
                    "smart_mode": True
                }
            },
            "Standard_SA": {
                "func": simulated_annealing,
                "params": {
                    "num_iterations": 100,
                    "initial_temp": 100,
                    "cooling_rate": 0.95,
                    "smart_mode": False
                }
            },
            "Greedy": {
                "func": "greedy_baseline",  # Will implement as baseline
                "params": {
                    "desired_coverage": 0.85,
                    "overlap_weight": 0.2,
                    "energy_weight": 0.1
                }
            }
        }
        
        return algorithms
    
    def run_single_experiment(self, scenario, algorithm_name, algorithm_config, parallel_mode=False):
        """Run a single experiment and collect comprehensive metrics"""
        
        try:
            # Create environment
            env = DroneSimulationEnvironment(
                width=scenario["width"],
                height=scenario["height"],
                num_drones=scenario["drones"],
                sensing_radius=scenario["radius"]
            )
            
            # Remove duplicates
            duplicate_pairs, total_duplicates = detect_and_report_duplicates(env)
            if duplicate_pairs:
                print(f"   🔧 Removed {total_duplicates} duplicate drones")
            
            # Handle greedy baseline
            if algorithm_name == "Greedy":
                # Simple greedy baseline - activate all drones
                start_time = time.time()
                activation = np.ones(len(env.drones))
                execution_time = time.time() - start_time
                result = {"message": "Greedy baseline - all drones active"}
            else:
                # Set parallel processing if applicable
                if "parallel_processing" in algorithm_config["params"]:
                    algorithm_config["params"]["parallel_processing"] = parallel_mode
                
                # Run algorithm
                start_time = time.time()
                activation, result = algorithm_config["func"](env, **algorithm_config["params"])
                execution_time = time.time() - start_time
            
            # Calculate metrics
            active_drones = np.sum(activation)
            total_drones = len(activation)
            energy_efficiency = ((total_drones - active_drones) / total_drones) * 100
            
            # Coverage calculation
            covered_points = 0
            total_points = len(env.grid_points)
            
            for point in env.grid_points:
                for i, drone in enumerate(env.drones):
                    if activation[i] > 0.5:  # Active drone
                        distance = np.linalg.norm(np.array(point) - np.array([drone.x, drone.y]))
                        if distance <= env.sensing_radius:
                            covered_points += 1
                            break
            
            coverage_percentage = (covered_points / total_points) * 100
            
            # Compile results
            experiment_result = {
                "scenario": scenario["name"],
                "algorithm": algorithm_name,
                "parallel_mode": parallel_mode,
                "coverage_percentage": coverage_percentage,
                "active_drones": int(active_drones),
                "total_drones": total_drones,
                "energy_efficiency": energy_efficiency,
                "execution_time": execution_time,
                "area_size": scenario["width"] * scenario["height"],
                "sensing_radius": scenario["radius"],
                "timestamp": datetime.now().isoformat()
            }
            
            return experiment_result
            
        except Exception as e:
            print(f"   ❌ Error in {algorithm_name}: {str(e)}")
            return {
                "scenario": scenario["name"],
                "algorithm": algorithm_name,
                "parallel_mode": parallel_mode,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def run_comprehensive_experiments(self, num_runs=5):
        """Run comprehensive experimental campaign"""
        
        print("🔬 IEEE EXPERIMENTAL FRAMEWORK - COMPREHENSIVE TESTING")
        print("=" * 70)
        
        scenarios = self.define_test_scenarios()
        algorithms = self.define_algorithms()
        all_results = []
        
        total_experiments = 0
        for scale in scenarios:
            for scenario in scenarios[scale]:
                for alg_name in algorithms:
                    total_experiments += 2 * num_runs  # Parallel + Non-parallel
        
        print(f"📊 Total experiments to run: {total_experiments}")
        print(f"🔄 Runs per configuration: {num_runs}")
        print(f"⚡ Parallel processing comparison: Enabled")
        
        experiment_count = 0
        
        # Run experiments for each scale
        for scale_name, scale_scenarios in scenarios.items():
            print(f"\n🎯 TESTING {scale_name.upper()}")
            print("-" * 50)
            
            for scenario in scale_scenarios:
                print(f"\n📍 Scenario: {scenario['name']} ({scenario['width']}×{scenario['height']}, {scenario['drones']} drones)")
                
                for algorithm_name, algorithm_config in algorithms.items():
                    print(f"   🧬 {algorithm_name}")
                    
                    # Test both parallel and non-parallel modes
                    for parallel_mode in [False, True]:
                        mode_name = "Parallel" if parallel_mode else "Sequential"
                        print(f"      {'⚡' if parallel_mode else '🔄'} {mode_name}: ", end="")
                        
                        run_results = []
                        for run in range(num_runs):
                            result = self.run_single_experiment(
                                scenario, algorithm_name, algorithm_config, parallel_mode
                            )
                            run_results.append(result)
                            print("✓", end="")
                            experiment_count += 1
                        
                        # Store results
                        all_results.extend(run_results)
                        print(f" ({experiment_count}/{total_experiments})")
        
        # Save comprehensive results
        self.save_experimental_data(all_results)
        
        print(f"\n🎉 EXPERIMENTAL CAMPAIGN COMPLETE!")
        print(f"📊 Total experiments conducted: {len(all_results)}")
        print(f"💾 Results saved to: {self.data_dir}")
        
        return all_results
    
    def save_experimental_data(self, results):
        """Save experimental data in multiple formats"""
        
        # Convert to DataFrame
        df = pd.DataFrame(results)
        
        # Save raw data
        csv_path = os.path.join(self.data_dir, f"experimental_results_{self.timestamp}.csv")
        df.to_csv(csv_path, index=False)
        
        excel_path = os.path.join(self.data_dir, f"experimental_results_{self.timestamp}.xlsx")
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Raw_Data', index=False)
            
            # Create summary sheets
            if not df.empty and 'error' not in df.columns:
                # Performance summary
                summary = df.groupby(['algorithm', 'parallel_mode']).agg({
                    'coverage_percentage': ['mean', 'std'],
                    'active_drones': ['mean', 'std'],
                    'energy_efficiency': ['mean', 'std'],
                    'execution_time': ['mean', 'std']
                }).round(2)
                summary.to_excel(writer, sheet_name='Performance_Summary')
                
                # Scale analysis
                scale_summary = df.groupby(['scenario', 'algorithm']).agg({
                    'coverage_percentage': 'mean',
                    'energy_efficiency': 'mean',
                    'execution_time': 'mean'
                }).round(2)
                scale_summary.to_excel(writer, sheet_name='Scale_Analysis')
        
        # Save JSON for detailed analysis
        json_path = os.path.join(self.data_dir, f"experimental_results_{self.timestamp}.json")
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📁 Data saved:")
        print(f"   CSV: {csv_path}")
        print(f"   Excel: {excel_path}")
        print(f"   JSON: {json_path}")

def main():
    """Main execution function"""
    
    # Set up output directory
    base_dir = "IEEE_Paper_Smart_Drone_Optimization_2025"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    # Initialize framework
    framework = IEEE_ExperimentalFramework(base_dir)
    
    # Run comprehensive experiments
    print("🚀 Starting IEEE Paper Experimental Campaign")
    print(f"💻 Available CPU cores: {cpu_count()}")
    print(f"📅 Timestamp: {framework.timestamp}")
    
    # Run experiments (5 runs per configuration for reliability)
    results = framework.run_comprehensive_experiments(num_runs=5)
    
    print("\n✅ EXPERIMENTAL FRAMEWORK COMPLETE")
    print(f"🎯 Ready for figure generation and paper writing")
    print(f"📊 {len(results)} total experimental data points collected")

if __name__ == "__main__":
    main()
