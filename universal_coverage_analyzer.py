#!/usr/bin/env python3
"""
Universal Coverage-First Optimization System (CSV-based)
======================================================

Analyzes CSV results to create universal optimization plan.
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Any

def analyze_csv_results(csv_path: str) -> Dict[str, Any]:
    """
    Analyze comprehensive experiment results from CSV file.
    """
    print(f"📊 Loading results from: {csv_path}")
    
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return {}
    
    print(f"✅ Loaded {len(df)} experiment results")
    
    # Group by algorithm and scenario
    analysis = {
        'algorithm_performance': {},
        'scenario_challenges': {},
        'universal_bottlenecks': [],
        'coverage_statistics': {}
    }
    
    # Algorithm performance analysis
    for algorithm in df['algorithm'].unique():
        algo_data = df[df['algorithm'] == algorithm]
        algo_performance = {}
        
        for scenario in df['scenario'].unique():
            scenario_data = algo_data[algo_data['scenario'] == scenario]
            if not scenario_data.empty:
                avg_coverage = scenario_data['coverage'].mean()
                algo_performance[scenario] = avg_coverage
        
        analysis['algorithm_performance'][algorithm] = algo_performance
    
    # Scenario analysis
    for scenario in df['scenario'].unique():
        scenario_data = df[df['scenario'] == scenario]
        
        coverages = scenario_data['coverage'].values
        analysis['scenario_challenges'][scenario] = {
            'average': np.mean(coverages),
            'minimum': np.min(coverages),
            'maximum': np.max(coverages),
            'variance': np.var(coverages),
            'std_dev': np.std(coverages),
            'algorithms_below_92': sum(1 for c in coverages if c < 92.0),
            'algorithms_below_85': sum(1 for c in coverages if c < 85.0),
            'total_algorithms': len(coverages)
        }
    
    # Identify universal bottlenecks
    for scenario, metrics in analysis['scenario_challenges'].items():
        if metrics['average'] < 70.0:
            analysis['universal_bottlenecks'].append({
                'scenario': scenario,
                'issue': 'Very low average coverage',
                'average': metrics['average'],
                'severity': 'HIGH'
            })
        elif metrics['average'] < 85.0:
            analysis['universal_bottlenecks'].append({
                'scenario': scenario,
                'issue': 'Low average coverage',
                'average': metrics['average'],
                'severity': 'MEDIUM'
            })
        
        if metrics['std_dev'] > 15.0:
            analysis['universal_bottlenecks'].append({
                'scenario': scenario,
                'issue': 'High algorithm variance',
                'std_dev': metrics['std_dev'],
                'severity': 'MEDIUM'
            })
        
        if metrics['algorithms_below_92'] >= metrics['total_algorithms'] * 0.8:
            analysis['universal_bottlenecks'].append({
                'scenario': scenario,
                'issue': 'Most algorithms below 92% target',
                'count': metrics['algorithms_below_92'],
                'total': metrics['total_algorithms'],
                'severity': 'HIGH'
            })
    
    # Overall statistics
    all_coverages = df['coverage'].values
    analysis['coverage_statistics'] = {
        'overall_average': np.mean(all_coverages),
        'overall_minimum': np.min(all_coverages),
        'overall_maximum': np.max(all_coverages),
        'overall_std_dev': np.std(all_coverages),
        'experiments_below_92': sum(1 for c in all_coverages if c < 92.0),
        'experiments_below_85': sum(1 for c in all_coverages if c < 85.0),
        'total_experiments': len(all_coverages)
    }
    
    return analysis

def create_universal_optimization_plan(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create universal optimization plan based on analysis.
    """
    plan = {
        'strategy': 'Universal Coverage-First Optimization',
        'current_status': {},
        'universal_improvements': {},
        'implementation_phases': [],
        'expected_outcomes': {},
        'success_metrics': {}
    }
    
    # Current status summary
    plan['current_status'] = {
        'overall_performance': analysis['coverage_statistics'],
        'critical_scenarios': [],
        'best_performing_scenarios': [],
        'algorithm_consistency': {}
    }
    
    # Identify critical and best scenarios
    for scenario, metrics in analysis['scenario_challenges'].items():
        if metrics['average'] < 70.0:
            plan['current_status']['critical_scenarios'].append(scenario)
        elif metrics['average'] > 80.0:
            plan['current_status']['best_performing_scenarios'].append(scenario)
    
    # Universal improvements designed to lift ALL algorithms
    plan['universal_improvements'] = {
        'environment_optimization': {
            'description': 'Optimize environment parameters to benefit all algorithms equally',
            'adjustments': {
                'grid_spacing_optimization': {
                    'current': 1.8,
                    'proposed': 1.75,  # Moderate improvement
                    'benefit': 'Better coverage without creating gaps'
                },
                'resolution_enhancement': {
                    'current': 75,
                    'proposed': 85,    # Moderate improvement
                    'benefit': 'More accurate coverage calculation'
                },
                'boundary_handling': {
                    'improvement': 'Enhanced boundary optimization',
                    'benefit': 'Better edge coverage for all algorithms'
                }
            }
        },
        
        'algorithm_standardization': {
            'description': 'Standardize parameters to ensure fair comparison',
            'adjustments': {
                'iteration_balancing': {
                    'benefit': 'Ensure all algorithms get adequate optimization time',
                    'method': 'Adaptive iteration counts based on algorithm type'
                },
                'population_standardization': {
                    'benefit': 'Fair computational resources for all algorithms',
                    'method': 'Balanced population sizes relative to algorithm complexity'
                }
            }
        },
        
        'fitness_enhancement': {
            'description': 'Improve fitness evaluation to benefit all algorithms',
            'adjustments': {
                'coverage_weight_adjustment': {
                    'current': 0.6,
                    'proposed': 0.65,  # Moderate increase
                    'benefit': 'Slightly higher coverage priority'
                },
                'energy_weight_adjustment': {
                    'current': 0.2,
                    'proposed': 0.175, # Slight decrease
                    'benefit': 'Reduced energy penalty allowing better coverage'
                },
                'overlap_penalty_adjustment': {
                    'current': 0.2,
                    'proposed': 0.175, # Slight decrease
                    'benefit': 'Less harsh overlap penalty for better coverage'
                }
            }
        },
        
        'convergence_improvement': {
            'description': 'Enhance convergence for all algorithms',
            'adjustments': {
                'position_refinement': {
                    'current': 30,
                    'proposed': 35,    # Moderate increase
                    'benefit': 'Better final positioning without over-optimization'
                },
                'early_stopping_enhancement': {
                    'improvement': 'Smarter early stopping criteria',
                    'benefit': 'Prevent premature convergence'
                }
            }
        }
    }
    
    # Implementation phases (conservative approach)
    plan['implementation_phases'] = [
        {
            'phase': 1,
            'name': 'Conservative Universal Improvements',
            'description': 'Implement moderate improvements that benefit all algorithms',
            'adjustments': [
                'Grid spacing: 1.8 → 1.75',
                'Resolution: 75 → 85',
                'Coverage weight: 0.6 → 0.65'
            ],
            'expected_impact': 'Universal 3-5% coverage improvement'
        },
        {
            'phase': 2,
            'name': 'Algorithm Standardization',
            'description': 'Standardize computational resources',
            'adjustments': [
                'Balanced iteration counts',
                'Standardized population sizes',
                'Enhanced boundary handling'
            ],
            'expected_impact': 'Reduced algorithm variance'
        },
        {
            'phase': 3,
            'name': 'Convergence Enhancement',
            'description': 'Improve convergence for all algorithms',
            'adjustments': [
                'Position refinement: 30 → 35',
                'Enhanced early stopping',
                'Adaptive parameter adjustment'
            ],
            'expected_impact': 'Better final solutions'
        }
    ]
    
    # Expected outcomes
    plan['expected_outcomes'] = {
        'minimum_improvement': '3-5% coverage increase for all algorithms',
        'variance_reduction': '20-30% reduction in algorithm variance',
        'target_achievement': 'At least 50% of algorithms reach 92% target',
        'universal_floor': 'All algorithms achieve minimum 70% coverage'
    }
    
    # Success metrics
    plan['success_metrics'] = {
        'overall_average_improvement': 5.0,     # At least 5% overall improvement
        'minimum_algorithm_improvement': 3.0,   # Every algorithm improves by at least 3%
        'maximum_algorithm_degradation': 1.0,   # No algorithm loses more than 1%
        'variance_reduction_target': 25.0,     # 25% reduction in variance
        'target_achievement_rate': 0.5         # 50% of algorithms reach 92% target
    }
    
    return plan

def main():
    """
    Main function to analyze current performance and create optimization plan.
    """
    print("🚀 UNIVERSAL COVERAGE-FIRST OPTIMIZATION SYSTEM")
    print("=" * 60)
    
    # Find the most recent results
    results_folder = "results"
    if not os.path.exists(results_folder):
        print(f"❌ Results folder not found: {results_folder}")
        return
    
    # Get the most recent experiment
    experiment_dirs = [d for d in os.listdir(results_folder) 
                      if d.startswith('comprehensive_experiment_') and os.path.isdir(os.path.join(results_folder, d))]
    
    if not experiment_dirs:
        print("❌ No experiment results found")
        return
    
    latest_dir = max(experiment_dirs)
    csv_path = os.path.join(results_folder, latest_dir, 'raw_results', 'all_experiments.csv')
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return
    
    print(f"📂 Using results from: {latest_dir}")
    
    # Analyze performance
    analysis = analyze_csv_results(csv_path)
    
    if not analysis:
        print("❌ Failed to analyze results")
        return
    
    # Display analysis
    print("\n📊 CURRENT PERFORMANCE ANALYSIS:")
    print("-" * 40)
    
    stats = analysis['coverage_statistics']
    print(f"📈 Overall Statistics:")
    print(f"  Average Coverage: {stats['overall_average']:.1f}%")
    print(f"  Range: {stats['overall_minimum']:.1f}% - {stats['overall_maximum']:.1f}%")
    print(f"  Standard Deviation: {stats['overall_std_dev']:.1f}%")
    print(f"  Experiments below 92% target: {stats['experiments_below_92']}/{stats['total_experiments']}")
    print(f"  Experiments below 85% floor: {stats['experiments_below_85']}/{stats['total_experiments']}")
    print()
    
    print("🎯 Scenario Performance:")
    for scenario, metrics in analysis['scenario_challenges'].items():
        print(f"  {scenario}:")
        print(f"    Average: {metrics['average']:.1f}%")
        print(f"    Range: {metrics['minimum']:.1f}% - {metrics['maximum']:.1f}%")
        print(f"    Std Dev: {metrics['std_dev']:.1f}%")
        print(f"    Below 92%: {metrics['algorithms_below_92']}/{metrics['total_algorithms']}")
        print()
    
    print("🚨 Universal Bottlenecks:")
    if analysis['universal_bottlenecks']:
        for bottleneck in analysis['universal_bottlenecks']:
            severity = bottleneck['severity']
            emoji = "🔴" if severity == "HIGH" else "🟡"
            print(f"  {emoji} {bottleneck['scenario']}: {bottleneck['issue']}")
    else:
        print("  ✅ No critical universal bottlenecks identified")
    print()
    
    # Create optimization plan
    plan = create_universal_optimization_plan(analysis)
    
    print("🎯 UNIVERSAL OPTIMIZATION PLAN:")
    print("-" * 40)
    
    print("📋 Implementation Strategy:")
    for phase in plan['implementation_phases']:
        print(f"  Phase {phase['phase']}: {phase['name']}")
        print(f"    {phase['description']}")
        print(f"    Expected: {phase['expected_impact']}")
        print()
    
    print("🎯 Expected Outcomes:")
    for outcome, description in plan['expected_outcomes'].items():
        print(f"  {outcome}: {description}")
    print()
    
    print("✅ Success Metrics:")
    for metric, value in plan['success_metrics'].items():
        print(f"  {metric}: {value}")
    print()
    
    # Save the comprehensive plan
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plan_file = f"universal_optimization_plan_{timestamp}.json"
    
    comprehensive_report = {
        'analysis': analysis,
        'optimization_plan': plan,
        'timestamp': timestamp,
        'source_data': csv_path
    }
    
    with open(plan_file, 'w') as f:
        json.dump(comprehensive_report, f, indent=2)
    
    print(f"💾 Complete analysis and plan saved to: {plan_file}")
    print()
    print("🚀 READY TO IMPLEMENT UNIVERSAL COVERAGE-FIRST OPTIMIZATION!")
    print("   This approach will lift ALL algorithms equally without creating winners/losers")

if __name__ == "__main__":
    main()
