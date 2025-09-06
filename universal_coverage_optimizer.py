#!/usr/bin/env python3
"""
Universal Coverage-First Optimization System
============================================

This system implements a universal approach that lifts ALL algorithms equally
instead of creating winners and losers. Based on the coverage-first principle:
"All algorithms must achieve the same target coverage."

Key Features:
- Adaptive parameter tuning based on worst-performing scenarios
- Universal improvements that benefit all algorithms equally
- Coverage-first optimization without algorithm-specific biases
- Smart environment adaptation for consistent performance

Created: September 6, 2025
Author: GitHub Copilot
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
import json
import os
from datetime import datetime

class UniversalCoverageOptimizer:
    """
    Universal optimizer that improves all algorithms equally
    based on coverage-first principles.
    """
    
    def __init__(self):
        self.optimization_history = []
        self.baseline_results = None
        self.universal_parameters = self._get_universal_parameters()
        
    def _get_universal_parameters(self) -> Dict[str, Any]:
        """
        Define universal parameters that benefit all algorithms equally.
        These are derived from the reference algorithms analysis.
        """
        return {
            # Environment parameters (adaptive to scenario)
            'adaptive_grid_spacing': True,
            'dynamic_resolution': True,
            'smart_sensing_range': True,
            
            # Universal fitness improvements
            'balanced_weights': True,
            'gap_penalty_system': True,
            'coverage_priority': True,
            
            # Algorithm-agnostic optimizations
            'position_refinement': True,
            'convergence_acceleration': True,
            'boundary_optimization': True,
            
            # Consistency parameters
            'minimum_coverage_guarantee': 0.85,
            'maximum_algorithm_variance': 0.05,  # Max 5% difference between algorithms
            'universal_target_threshold': 0.92
        }
    
    def analyze_current_performance(self, results_folder: str) -> Dict[str, Any]:
        """
        Analyze current algorithm performance to identify universal improvement opportunities.
        """
        print("🔍 Analyzing current performance for universal optimization...")
        
        # Find the most recent results
        if not os.path.exists(results_folder):
            print(f"❌ Results folder not found: {results_folder}")
            return {}
            
        result_dirs = [d for d in os.listdir(results_folder) 
                      if d.startswith('comprehensive_experiment_') and os.path.isdir(os.path.join(results_folder, d))]
        
        if not result_dirs:
            print("❌ No comprehensive experiment results found")
            return {}
            
        # Get the most recent results
        latest_dir = max(result_dirs)
        results_path = os.path.join(results_folder, latest_dir, 'comprehensive_results.json')
        
        if not os.path.exists(results_path):
            print(f"❌ Results file not found: {results_path}")
            return {}
            
        with open(results_path, 'r') as f:
            results = json.load(f)
        
        return self._analyze_performance_patterns(results)
    
    def _analyze_performance_patterns(self, results: Dict) -> Dict[str, Any]:
        """
        Identify universal patterns that affect all algorithms.
        """
        analysis = {
            'algorithm_performance': {},
            'scenario_challenges': {},
            'universal_bottlenecks': [],
            'coverage_gaps': {},
            'recommended_adjustments': {}
        }
        
        # Analyze each algorithm's performance across scenarios
        for algo_name, algo_results in results.items():
            if not isinstance(algo_results, dict):
                continue
                
            algo_performance = {}
            for scenario, scenario_results in algo_results.items():
                if isinstance(scenario_results, dict) and 'coverage' in scenario_results:
                    coverage = scenario_results['coverage']
                    algo_performance[scenario] = coverage
            
            analysis['algorithm_performance'][algo_name] = algo_performance
        
        # Identify universal bottlenecks (scenarios where ALL algorithms struggle)
        scenario_averages = {}
        for scenario in ['small_area_few_drones', 'medium_area_standard', 'large_area_many_drones', 
                        'challenging_small_radius', 'efficiency_test', 'parallel_processing_test']:
            
            scenario_coverages = []
            for algo_performance in analysis['algorithm_performance'].values():
                if scenario in algo_performance:
                    scenario_coverages.append(algo_performance[scenario])
            
            if scenario_coverages:
                avg_coverage = np.mean(scenario_coverages)
                min_coverage = np.min(scenario_coverages)
                max_coverage = np.max(scenario_coverages)
                variance = np.var(scenario_coverages)
                
                scenario_averages[scenario] = {
                    'average': avg_coverage,
                    'minimum': min_coverage,
                    'maximum': max_coverage,
                    'variance': variance,
                    'algorithms_below_target': sum(1 for c in scenario_coverages if c < 92.0)
                }
                
                # Identify universal bottlenecks
                if avg_coverage < 85.0:
                    analysis['universal_bottlenecks'].append({
                        'scenario': scenario,
                        'issue': 'Low average coverage',
                        'average': avg_coverage
                    })
                
                if variance > 100:  # High variance between algorithms
                    analysis['universal_bottlenecks'].append({
                        'scenario': scenario,
                        'issue': 'High algorithm variance',
                        'variance': variance
                    })
                
                if scenario_averages[scenario]['algorithms_below_target'] > 10:
                    analysis['universal_bottlenecks'].append({
                        'scenario': scenario,
                        'issue': 'Most algorithms below target',
                        'count': scenario_averages[scenario]['algorithms_below_target']
                    })
        
        analysis['scenario_challenges'] = scenario_averages
        
        # Generate universal recommendations
        analysis['recommended_adjustments'] = self._generate_universal_recommendations(analysis)
        
        return analysis
    
    def _generate_universal_recommendations(self, analysis: Dict) -> Dict[str, Any]:
        """
        Generate universal adjustments that benefit all algorithms equally.
        """
        recommendations = {
            'environment_adjustments': {},
            'algorithm_parameters': {},
            'fitness_improvements': {},
            'convergence_enhancements': {}
        }
        
        # Analyze universal bottlenecks
        for bottleneck in analysis['universal_bottlenecks']:
            scenario = bottleneck['scenario']
            issue = bottleneck['issue']
            
            if issue == 'Low average coverage':
                # Universal environment improvements
                recommendations['environment_adjustments'][scenario] = {
                    'increase_iterations': True,
                    'improve_initial_positioning': True,
                    'enhance_boundary_handling': True
                }
            
            elif issue == 'High algorithm variance':
                # Standardization improvements
                recommendations['algorithm_parameters'][scenario] = {
                    'standardize_population_sizes': True,
                    'balance_exploration_exploitation': True,
                    'uniform_convergence_criteria': True
                }
            
            elif issue == 'Most algorithms below target':
                # Fitness function improvements
                recommendations['fitness_improvements'][scenario] = {
                    'increase_coverage_weight': True,
                    'reduce_energy_penalty': True,
                    'enhance_gap_detection': True
                }
        
        # Universal convergence enhancements based on reference algorithms
        recommendations['convergence_enhancements'] = {
            'adaptive_learning_rates': True,
            'smart_population_management': True,
            'dynamic_parameter_adjustment': True,
            'early_convergence_prevention': True
        }
        
        return recommendations
    
    def generate_universal_optimization_plan(self, analysis: Dict) -> Dict[str, Any]:
        """
        Generate a comprehensive universal optimization plan.
        """
        plan = {
            'optimization_strategy': 'Universal Coverage-First',
            'target_improvements': {},
            'universal_adjustments': {},
            'implementation_phases': [],
            'success_metrics': {}
        }
        
        # Set target improvements based on current performance
        current_performance = analysis['scenario_challenges']
        
        for scenario, metrics in current_performance.items():
            target_coverage = max(92.0, metrics['average'] + 10.0)  # At least 92% or +10%
            target_variance = min(50.0, metrics['variance'] * 0.5)  # Reduce variance by 50%
            
            plan['target_improvements'][scenario] = {
                'target_coverage': target_coverage,
                'target_variance': target_variance,
                'algorithms_to_improve': metrics['algorithms_below_target']
            }
        
        # Define universal adjustments
        plan['universal_adjustments'] = self._design_universal_adjustments(analysis)
        
        # Implementation phases
        plan['implementation_phases'] = [
            {
                'phase': 1,
                'name': 'Environment Standardization',
                'description': 'Optimize environment parameters universally',
                'adjustments': ['grid_spacing', 'resolution', 'boundary_handling']
            },
            {
                'phase': 2,
                'name': 'Algorithm Parameter Balancing',
                'description': 'Balance parameters to benefit all algorithms',
                'adjustments': ['population_sizes', 'iteration_counts', 'learning_rates']
            },
            {
                'phase': 3,
                'name': 'Fitness Function Enhancement',
                'description': 'Improve fitness evaluation universally',
                'adjustments': ['coverage_weights', 'gap_penalties', 'energy_balance']
            },
            {
                'phase': 4,
                'name': 'Convergence Optimization',
                'description': 'Enhance convergence for all algorithms',
                'adjustments': ['position_refinement', 'early_stopping', 'adaptive_parameters']
            }
        ]
        
        # Success metrics
        plan['success_metrics'] = {
            'minimum_coverage_improvement': 5.0,  # At least 5% improvement for worst performers
            'maximum_algorithm_variance': 50.0,   # No more than 50 variance between algorithms
            'target_achievement_rate': 0.8,      # At least 80% of algorithms reach targets
            'universal_coverage_minimum': 85.0   # All algorithms achieve at least 85%
        }
        
        return plan
    
    def _design_universal_adjustments(self, analysis: Dict) -> Dict[str, Any]:
        """
        Design specific universal adjustments based on analysis.
        """
        adjustments = {
            'environment_parameters': {
                'adaptive_grid_spacing': {
                    'small_area': 1.7,      # Tighter spacing for small areas
                    'medium_area': 1.8,     # Standard spacing
                    'large_area': 1.9,      # Looser spacing for large areas
                    'challenging': 1.6      # Very tight for challenging scenarios
                },
                'dynamic_resolution': {
                    'small_area': 80,       # Higher resolution for small areas
                    'medium_area': 75,      # Standard resolution
                    'large_area': 70,       # Lower resolution for performance
                    'challenging': 90       # Highest resolution for accuracy
                },
                'boundary_optimization': True
            },
            
            'algorithm_parameters': {
                'standardized_populations': {
                    'genetic_algorithms': 50,
                    'particle_swarm': 50,
                    'simulated_annealing': 1,
                    'grey_wolf': 30,
                    'manta_ray': 50
                },
                'balanced_iterations': {
                    'quick_algorithms': 200,
                    'standard_algorithms': 300,
                    'intensive_algorithms': 400
                },
                'universal_learning_rates': {
                    'exploration_phase': 0.8,
                    'exploitation_phase': 0.2
                }
            },
            
            'fitness_improvements': {
                'adaptive_weights': {
                    'coverage_weight': 0.65,    # Slightly higher than original
                    'energy_weight': 0.175,     # Slightly lower
                    'overlap_weight': 0.175     # Slightly lower
                },
                'smart_gap_penalties': True,
                'coverage_boost_factor': 1.2   # Moderate boost, not extreme
            },
            
            'convergence_enhancements': {
                'position_refinement_iterations': 40,  # Moderate increase from 30
                'early_stopping_patience': 20,
                'adaptive_mutation_rates': True,
                'boundary_repair_mechanism': True
            }
        }
        
        return adjustments

def main():
    """
    Main function to run universal coverage optimization analysis.
    """
    print("🚀 UNIVERSAL COVERAGE-FIRST OPTIMIZATION SYSTEM")
    print("=" * 60)
    
    optimizer = UniversalCoverageOptimizer()
    
    # Analyze current performance
    results_folder = "results"
    analysis = optimizer.analyze_current_performance(results_folder)
    
    if not analysis:
        print("❌ Could not analyze current performance")
        return
    
    print("📊 CURRENT PERFORMANCE ANALYSIS:")
    print("-" * 40)
    
    # Display scenario challenges
    print("🎯 Scenario Performance:")
    for scenario, metrics in analysis['scenario_challenges'].items():
        print(f"  {scenario}:")
        print(f"    Average: {metrics['average']:.1f}%")
        print(f"    Range: {metrics['minimum']:.1f}% - {metrics['maximum']:.1f}%")
        print(f"    Algorithms below target: {metrics['algorithms_below_target']}/14")
        print()
    
    # Display universal bottlenecks
    print("🚨 Universal Bottlenecks:")
    for bottleneck in analysis['universal_bottlenecks']:
        print(f"  {bottleneck['scenario']}: {bottleneck['issue']}")
    print()
    
    # Generate optimization plan
    plan = optimizer.generate_universal_optimization_plan(analysis)
    
    print("🎯 UNIVERSAL OPTIMIZATION PLAN:")
    print("-" * 40)
    
    print("📈 Target Improvements:")
    for scenario, targets in plan['target_improvements'].items():
        print(f"  {scenario}: {targets['target_coverage']:.1f}% coverage target")
    print()
    
    print("🔧 Implementation Phases:")
    for phase in plan['implementation_phases']:
        print(f"  Phase {phase['phase']}: {phase['name']}")
        print(f"    {phase['description']}")
    print()
    
    print("✅ Success Metrics:")
    for metric, value in plan['success_metrics'].items():
        print(f"  {metric}: {value}")
    print()
    
    # Save the plan
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plan_file = f"universal_optimization_plan_{timestamp}.json"
    
    with open(plan_file, 'w') as f:
        json.dump({
            'analysis': analysis,
            'optimization_plan': plan,
            'timestamp': timestamp
        }, f, indent=2)
    
    print(f"💾 Optimization plan saved to: {plan_file}")
    print()
    print("🚀 Ready to implement universal coverage-first optimization!")

if __name__ == "__main__":
    main()
