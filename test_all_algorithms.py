#!/usr/bin/env python3
"""
Test All Algorithms - Comprehensive Testing
Tests PSO, GA, SA, and other algorithms with progress indicators
"""

import numpy as np
import time
from app import DroneSimulationEnvironment
from algorithms import (
    particle_swarm_optimization, 
    genetic_algorithm, 
    simulated_annealing,
    detect_and_report_duplicates
)

def progress_callback(iteration, max_iters, fitness, coverage=None):
    """Progress callback for testing"""
    progress_pct = (iteration / max_iters) * 100
    print(f"📊 Progress: {iteration}/{max_iters} ({progress_pct:.1f}%) - Fitness: {fitness:.4f}", end="")
    if coverage is not None:
        print(f" - Coverage: {coverage:.1f}%")
    else:
        print()

def test_algorithm(algorithm_name, algorithm_func, env, params):
    """Test a specific algorithm"""
    print(f"\n🧪 TESTING {algorithm_name.upper()}")
    print("=" * 50)
    
    start_time = time.time()
    
    try:
        # Check for duplicates before running
        duplicate_pairs, total_duplicates = detect_and_report_duplicates(env)
        if duplicate_pairs:
            print(f"⚠️ Found {total_duplicates} duplicate drones before optimization")
            for pair in duplicate_pairs[:3]:  # Show first 3
                print(f"   • Drone {pair['drone1_id']} & {pair['drone2_id']}: distance {pair['distance']:.2f}")
        
        # Run algorithm
        activation, result = algorithm_func(env, **params)
        
        execution_time = time.time() - start_time
        
        # Calculate final coverage
        env.set_active_drones(activation)
        final_coverage = env.calculate_coverage_percentage()  # Now returns percentage
        active_count = np.sum(activation)
        
        print(f"\n✅ {algorithm_name.upper()} Results:")
        print(f"   • Execution Time: {execution_time:.2f}s")
        print(f"   • Final Coverage: {final_coverage:.1f}%")  # No need to multiply by 100
        print(f"   • Active Drones: {active_count}/{len(env.drones)}")
        print(f"   • Energy Saved: {((len(env.drones) - active_count) / len(env.drones)) * 100:.1f}%")
        
        if hasattr(result, 'fitness_history'):
            print(f"   • Iterations: {len(result.fitness_history)}")
            print(f"   • Best Fitness: {max(result.fitness_history):.4f}")
        
        return True, {
            'algorithm': algorithm_name,
            'execution_time': execution_time,
            'final_coverage': final_coverage,
            'active_drones': active_count,
            'total_drones': len(env.drones),
            'success': True
        }
        
    except Exception as e:
        print(f"❌ {algorithm_name.upper()} FAILED: {str(e)}")
        return False, {'algorithm': algorithm_name, 'error': str(e), 'success': False}

def main():
    """Test all algorithms comprehensively"""
    print("🚁 COMPREHENSIVE ALGORITHM TESTING")
    print("=" * 60)
    
    # Create test environment
    print("🔧 Setting up test environment...")
    env = DroneSimulationEnvironment(width=50, height=50, num_drones=15, sensing_radius=8)
    
    print(f"   • Environment: 50x50 units")
    print(f"   • Drones: {len(env.drones)} drones")
    print(f"   • Sensing Radius: 8 units")
    
    # Test configurations for each algorithm
    test_configs = {
        'PSO': {
            'func': particle_swarm_optimization,
            'params': {
                'swarm_size': 30,
                'iterations': 50,
                'inertia': 0.7,
                'cognitive_weight': 1.5,
                'social_weight': 1.5,
                'parallel_processing': False,
                'desired_coverage': 0.95,
                'smart_mode': True,
                'progress_callback': progress_callback
            }
        },
        'GA': {
            'func': genetic_algorithm,
            'params': {
                'num_generations': 50,
                'target_coverage': 0.95,
                'smart_mode': True,
                'desired_coverage': 0.95,
                'progress_callback': progress_callback
            }
        },
        'SA': {
            'func': simulated_annealing,
            'params': {
                'num_iterations': 50,
                'desired_coverage': 0.95,
                'smart_mode': True,
                'progress_callback': progress_callback
            }
        }
    }
    
    # Run tests
    results = []
    successful_tests = 0
    
    for name, config in test_configs.items():
        # Create fresh environment for each test
        test_env = DroneSimulationEnvironment(width=50, height=50, num_drones=15, sensing_radius=8)
        
        success, result = test_algorithm(name, config['func'], test_env, config['params'])
        results.append(result)
        
        if success:
            successful_tests += 1
    
    # Final summary
    print(f"\n🎯 TESTING SUMMARY")
    print("=" * 30)
    print(f"Total Tests: {len(test_configs)}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {len(test_configs) - successful_tests}")
    
    print(f"\n📊 ALGORITHM COMPARISON:")
    for result in results:
        if result['success']:
            print(f"✅ {result['algorithm']}: {result['final_coverage']*100:.1f}% coverage, "
                  f"{result['active_drones']}/{result['total_drones']} drones, "
                  f"{result['execution_time']:.2f}s")
        else:
            print(f"❌ {result['algorithm']}: FAILED - {result['error']}")
    
    print(f"\n🎉 Testing Complete!")
    
    # Find best performing algorithm
    successful_results = [r for r in results if r['success']]
    if successful_results:
        best_algorithm = max(successful_results, key=lambda x: x['final_coverage'])
        print(f"🏆 Best Performance: {best_algorithm['algorithm']} with {best_algorithm['final_coverage']*100:.1f}% coverage")

if __name__ == "__main__":
    main()
