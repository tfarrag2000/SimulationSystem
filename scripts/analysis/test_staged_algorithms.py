#!/usr/bin/env python3
"""
Quick test of staged algorithms
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from algorithms import staged_optimization_wrapper, greedy_algorithm, genetic_algorithm
from environment import Simulation

def test_staged_algorithms():
    """Test staged algorithms"""
    print("🧪 Testing Staged Algorithms...")
    
    # Create simple simulation
    simulation = Simulation(area_width=100, area_height=100, num_drones=12, random_seed=42)
    
    print("\n1. Testing Original Greedy Algorithm")
    try:
        activation1, result1 = greedy_algorithm(simulation, desired_coverage=0.99)
        coverage1 = simulation.calculate_coverage_percentage(activation1)
        print(f"   ✅ Original Greedy: {coverage1:.1f}% coverage")
    except Exception as e:
        print(f"   ❌ Original Greedy failed: {e}")
    
    print("\n2. Testing Staged Greedy Algorithm")
    try:
        activation2, result2 = staged_optimization_wrapper(greedy_algorithm, simulation, desired_coverage=0.99)
        coverage2 = simulation.calculate_coverage_percentage(activation2)
        print(f"   ✅ Staged Greedy: {coverage2:.1f}% coverage")
    except Exception as e:
        print(f"   ❌ Staged Greedy failed: {e}")
    
    print("\n3. Testing Original GA Algorithm")
    try:
        activation3, result3 = genetic_algorithm(simulation, num_generations=10, population_size=10)
        coverage3 = simulation.calculate_coverage_percentage(activation3)
        print(f"   ✅ Original GA: {coverage3:.1f}% coverage")
    except Exception as e:
        print(f"   ❌ Original GA failed: {e}")
    
    print("\n4. Testing Staged GA Algorithm")
    try:
        activation4, result4 = staged_optimization_wrapper(genetic_algorithm, simulation, num_generations=10, population_size=10)
        coverage4 = simulation.calculate_coverage_percentage(activation4)
        print(f"   ✅ Staged GA: {coverage4:.1f}% coverage")
    except Exception as e:
        print(f"   ❌ Staged GA failed: {e}")
    
    print("\n🎉 Test completed!")

if __name__ == "__main__":
    test_staged_algorithms()
