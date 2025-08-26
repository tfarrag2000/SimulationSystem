#!/usr/bin/env python3
"""
Quick test of staged vs original algorithms
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from algorithms import *
from app import DroneSimulationEnvironment

def quick_test():
    """Quick test of 4 algorithms"""
    print("🧪 QUICK STAGED vs ORIGINAL TEST")
    print("=" * 50)
    
    # Create simple simulation
    simulation = DroneSimulationEnvironment(
        area_width=100, 
        area_height=100, 
        num_drones=12,
        sensing_range=15,
        random_seed=42
    )
    
    results = []
    
    print("\n1. Testing Original Greedy")
    try:
        activation, result = greedy_optimization(simulation, desired_coverage=0.99)
        coverage = simulation.calculate_coverage_percentage(activation)
        active = np.sum(activation >= 0.5)
        results.append(('Original Greedy', coverage, active))
        print(f"   ✅ Coverage: {coverage:.1f}%, Active: {active}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    print("\n2. Testing Staged Greedy")
    try:
        activation, result = staged_optimization_wrapper(greedy_optimization, simulation, desired_coverage=0.99)
        coverage = simulation.calculate_coverage_percentage(activation)
        active = np.sum(activation >= 0.5)
        results.append(('Staged Greedy', coverage, active))
        print(f"   ✅ Coverage: {coverage:.1f}%, Active: {active}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    print("\n3. Testing Original PSO")
    try:
        activation, result = particle_swarm_optimization(simulation, iterations=20, num_particles=10)
        coverage = simulation.calculate_coverage_percentage(activation)
        active = np.sum(activation >= 0.5)
        results.append(('Original PSO', coverage, active))
        print(f"   ✅ Coverage: {coverage:.1f}%, Active: {active}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    print("\n4. Testing Staged PSO")
    try:
        activation, result = staged_optimization_wrapper(particle_swarm_optimization, simulation, iterations=20, num_particles=10)
        coverage = simulation.calculate_coverage_percentage(activation)
        active = np.sum(activation >= 0.5)
        results.append(('Staged PSO', coverage, active))
        print(f"   ✅ Coverage: {coverage:.1f}%, Active: {active}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    print("\n" + "=" * 50)
    print("📊 RESULTS SUMMARY:")
    for name, coverage, active in results:
        print(f"   {name:15}: {coverage:5.1f}% coverage, {active:2d} active drones")
    
    print("\n🎉 Quick test completed!")

if __name__ == "__main__":
    quick_test()
