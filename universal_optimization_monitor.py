#!/usr/bin/env python3
"""
Universal Optimization Results Monitor
=====================================

Monitors the comprehensive experimental results and compares them with
the baseline to validate universal coverage-first optimization.
"""

import os
import time
import json
import pandas as pd
from datetime import datetime
import numpy as np

def monitor_experiment_progress():
    """
    Monitor the progress of the comprehensive experiment.
    """
    print("🔍 MONITORING UNIVERSAL OPTIMIZATION EXPERIMENT")
    print("=" * 60)
    
    results_dir = "results"
    
    while True:
        # Check for new results folders
        if os.path.exists(results_dir):
            result_dirs = [d for d in os.listdir(results_dir) 
                          if d.startswith('comprehensive_experiment_') and os.path.isdir(os.path.join(results_dir, d))]
            
            if result_dirs:
                latest_dir = max(result_dirs)
                latest_path = os.path.join(results_dir, latest_dir)
                
                print(f"📂 Latest experiment: {latest_dir}")
                
                # Check for completion indicators
                log_file = os.path.join(latest_path, "experiment.log")
                csv_file = os.path.join(latest_path, "raw_results", "all_experiments.csv")
                
                if os.path.exists(csv_file):
                    try:
                        df = pd.read_csv(csv_file)
                        total_experiments = len(df)
                        unique_algos = df['algorithm'].nunique()
                        unique_scenarios = df['scenario'].nunique()
                        
                        print(f"📊 Progress: {total_experiments} experiments completed")
                        print(f"🔬 Algorithms tested: {unique_algos}")
                        print(f"🎯 Scenarios completed: {unique_scenarios}")
                        
                        if total_experiments >= 168:  # 14 algorithms × 6 scenarios × 2 runs
                            print("✅ EXPERIMENT COMPLETED!")
                            return latest_path
                        
                    except Exception as e:
                        print(f"⚠️  Error reading results: {e}")
                
                if os.path.exists(log_file):
                    try:
                        with open(log_file, 'r') as f:
                            lines = f.readlines()
                            if lines:
                                print(f"📝 Latest log: {lines[-1].strip()}")
                    except Exception as e:
                        print(f"⚠️  Error reading log: {e}")
        
        print("⏳ Waiting for more results...")
        time.sleep(30)  # Check every 30 seconds

def analyze_universal_optimization_results(results_path):
    """
    Analyze the results of universal optimization.
    """
    print("\n🔍 ANALYZING UNIVERSAL OPTIMIZATION RESULTS")
    print("=" * 60)
    
    # Load current results
    csv_file = os.path.join(results_path, "raw_results", "all_experiments.csv")
    if not os.path.exists(csv_file):
        print("❌ Results file not found")
        return
    
    df_current = pd.read_csv(csv_file)
    
    # Load baseline results for comparison
    baseline_path = "results/comprehensive_experiment_20250906_100009/raw_results/all_experiments.csv"
    if not os.path.exists(baseline_path):
        print("❌ Baseline results not found")
        return
    
    df_baseline = pd.read_csv(baseline_path)
    
    print("📊 UNIVERSAL OPTIMIZATION IMPACT ANALYSIS")
    print("-" * 40)
    
    # Calculate algorithm-wise improvements
    algo_improvements = {}
    scenario_improvements = {}
    
    for algo in df_current['algorithm'].unique():
        current_avg = df_current[df_current['algorithm'] == algo]['coverage'].mean()
        baseline_avg = df_baseline[df_baseline['algorithm'] == algo]['coverage'].mean()
        improvement = current_avg - baseline_avg
        
        algo_improvements[algo] = {
            'baseline': baseline_avg,
            'current': current_avg,
            'improvement': improvement,
            'improvement_pct': (improvement / baseline_avg) * 100 if baseline_avg > 0 else 0
        }
    
    # Calculate scenario-wise improvements
    for scenario in df_current['scenario'].unique():
        current_avg = df_current[df_current['scenario'] == scenario]['coverage'].mean()
        baseline_avg = df_baseline[df_baseline['scenario'] == scenario]['coverage'].mean()
        improvement = current_avg - baseline_avg
        
        scenario_improvements[scenario] = {
            'baseline': baseline_avg,
            'current': current_avg,
            'improvement': improvement,
            'improvement_pct': (improvement / baseline_avg) * 100 if baseline_avg > 0 else 0
        }
    
    # Overall statistics
    overall_baseline = df_baseline['coverage'].mean()
    overall_current = df_current['coverage'].mean()
    overall_improvement = overall_current - overall_baseline
    overall_improvement_pct = (overall_improvement / overall_baseline) * 100
    
    print(f"🎯 OVERALL IMPACT:")
    print(f"   Baseline Average: {overall_baseline:.1f}%")
    print(f"   Current Average: {overall_current:.1f}%")
    print(f"   Improvement: {overall_improvement:+.1f}% ({overall_improvement_pct:+.1f}%)")
    
    print(f"\n📈 ALGORITHM IMPROVEMENTS:")
    improvements_list = []
    degradations_list = []
    
    for algo, metrics in algo_improvements.items():
        improvement_pct = metrics['improvement_pct']
        if improvement_pct >= 0:
            status = "✅" if improvement_pct >= 3.0 else "⚠️ "
            improvements_list.append(improvement_pct)
        else:
            status = "❌"
            degradations_list.append(abs(improvement_pct))
        
        print(f"   {status} {algo}: {metrics['baseline']:.1f}% → {metrics['current']:.1f}% ({improvement_pct:+.1f}%)")
    
    print(f"\n🎯 SCENARIO IMPROVEMENTS:")
    for scenario, metrics in scenario_improvements.items():
        improvement_pct = metrics['improvement_pct']
        status = "✅" if improvement_pct >= 0 else "❌"
        print(f"   {status} {scenario}: {metrics['baseline']:.1f}% → {metrics['current']:.1f}% ({improvement_pct:+.1f}%)")
    
    # Universal optimization validation
    print(f"\n🏆 UNIVERSAL OPTIMIZATION VALIDATION:")
    print("-" * 40)
    
    algorithms_improved = len(improvements_list)
    algorithms_degraded = len(degradations_list)
    total_algorithms = len(algo_improvements)
    
    avg_improvement = np.mean(improvements_list) if improvements_list else 0
    max_degradation = max(degradations_list) if degradations_list else 0
    min_improvement = min(improvements_list) if improvements_list else 0
    
    print(f"✅ Algorithms Improved: {algorithms_improved}/{total_algorithms} ({algorithms_improved/total_algorithms*100:.1f}%)")
    print(f"❌ Algorithms Degraded: {algorithms_degraded}/{total_algorithms} ({algorithms_degraded/total_algorithms*100:.1f}%)")
    print(f"📊 Average Improvement: {avg_improvement:.1f}%")
    print(f"📈 Minimum Improvement: {min_improvement:.1f}%")
    print(f"📉 Maximum Degradation: {max_degradation:.1f}%")
    
    # Success criteria validation
    print(f"\n🎯 SUCCESS CRITERIA VALIDATION:")
    print("-" * 40)
    
    criteria = [
        ("Overall Average Improvement ≥5.0%", overall_improvement_pct >= 5.0),
        ("Minimum Algorithm Improvement ≥3.0%", min_improvement >= 3.0),
        ("Maximum Algorithm Degradation ≤1.0%", max_degradation <= 1.0),
        ("Algorithms Improved ≥80%", algorithms_improved/total_algorithms >= 0.8),
        ("Universal Benefit (no major degradations)", max_degradation <= 2.0)
    ]
    
    success_count = 0
    for criterion, passed in criteria:
        status = "✅" if passed else "❌"
        if passed:
            success_count += 1
        print(f"   {status} {criterion}")
    
    print(f"\n🏆 OVERALL SUCCESS RATE: {success_count}/{len(criteria)} ({success_count/len(criteria)*100:.1f}%)")
    
    if success_count >= 4:
        print("🎉 UNIVERSAL OPTIMIZATION SUCCESSFUL!")
        print("   All algorithms benefit from coverage-first improvements")
    elif success_count >= 3:
        print("⚠️  UNIVERSAL OPTIMIZATION PARTIALLY SUCCESSFUL")
        print("   Most criteria met, minor adjustments may be needed")
    else:
        print("❌ UNIVERSAL OPTIMIZATION NEEDS REVISION")
        print("   Significant improvements required")
    
    # Save analysis results
    analysis_results = {
        'timestamp': datetime.now().isoformat(),
        'overall_improvement': overall_improvement_pct,
        'algorithm_improvements': algo_improvements,
        'scenario_improvements': scenario_improvements,
        'success_criteria': {criterion: passed for criterion, passed in criteria},
        'success_rate': success_count / len(criteria)
    }
    
    analysis_file = os.path.join(results_path, "universal_optimization_analysis.json")
    with open(analysis_file, 'w') as f:
        json.dump(analysis_results, f, indent=2)
    
    print(f"\n💾 Analysis saved to: {analysis_file}")

def main():
    """
    Main monitoring and analysis function.
    """
    print("🚀 UNIVERSAL OPTIMIZATION MONITORING AND ANALYSIS")
    print("=" * 60)
    
    # Monitor experiment progress
    results_path = monitor_experiment_progress()
    
    if results_path:
        # Analyze results once complete
        analyze_universal_optimization_results(results_path)
    else:
        print("❌ Experiment monitoring failed")

if __name__ == "__main__":
    main()
