#!/usr/bin/env python3
"""
Quick Algorithm Equality Test
Tests all algorithms (PSO, GA, SA, Greedy) equally on the same scenario
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from algorithms import (
    smart_particle_swarm_optimization,
    enhanced_genetic_algorithm, 
    smart_simulated_annealing,
    greedy_coverage_algorithm
)
from app import DroneSimulationEnvironment
import time

def test_all_algorithms_equally():
    """Test all algorithms on the same scenario"""
    print("🧪 EQUAL ALGORITHM TESTING")
    print("="*50)
    
    # Create test scenario
    env = DroneSimulationEnvironment(width=60, height=60, num_drones=20, sensing_radius=10)
    print(f"📍 Test Scenario: 60x60 area, {len(env.drones)} drones, radius=10")
    print("-"*50)
    
    algorithms = {
        'Smart PSO': smart_particle_swarm_optimization,
        'Smart GA': enhanced_genetic_algorithm,
        'Smart SA': smart_simulated_annealing,
        'Greedy': greedy_coverage_algorithm
    }
    
    results = {}
    
    for name, algorithm in algorithms.items():
        print(f"\n🧬 Testing {name}...")
        try:
            start_time = time.time()
            
            if name == 'Greedy':
                result = algorithm(env, target_coverage=0.90)
            else:
                result = algorithm(env, max_iterations=50, target_coverage=0.90)
            
            execution_time = time.time() - start_time
            
            if result:
                coverage = result.get('final_coverage', 0) * 100
                active_drones = result.get('active_drones', 0)
                total_drones = len(env.drones)
                
                results[name] = {
                    'coverage': coverage,
                    'active_drones': active_drones,
                    'total_drones': total_drones,
                    'energy_saved': ((total_drones - active_drones) / total_drones) * 100,
                    'time': execution_time
                }
                
                print(f"✅ {name}: Coverage={coverage:.1f}%, Active={active_drones}/{total_drones}, Time={execution_time:.1f}s")
            else:
                print(f"❌ {name}: No result returned")
                
        except Exception as e:
            print(f"❌ {name}: Error - {str(e)}")
    
    print("\n📊 COMPARATIVE RESULTS:")
    print("-"*50)
    for name, data in results.items():
        print(f"{name:12}: Coverage={data['coverage']:5.1f}% | Active={data['active_drones']:2d}/{data['total_drones']:2d} | Energy={data['energy_saved']:5.1f}% | Time={data['time']:5.1f}s")
    
    print(f"\n✅ ALL {len(results)} ALGORITHMS TESTED EQUALLY!")
    return results

if __name__ == "__main__":
    test_all_algorithms_equally()
