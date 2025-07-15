#!/usr/bin/env python3
"""
Quick test to verify iteration logs are working correctly.
"""

from environment import DroneEnvironment
from algorithms import greedy_optimization
import numpy as np

def test_iteration_logs():
    print("🧪 Testing iteration logs generation...")
    
    # Create a simple simulation
    simulation = DroneEnvironment(width=100, height=100, num_drones=10, sensing_radius=20)
    
    print(f"📊 Simulation initialized with {len(simulation.drones)} drones")
    
    # Run greedy algorithm with reduced coverage to see more steps
    print("🔄 Running greedy algorithm...")
    activation, result = greedy_optimization(
        simulation=simulation,
        desired_coverage=0.6,  # Lower coverage to see more steps
        overlap_weight=0.2,
        energy_weight=0.1
    )
    
    print(f"✅ Algorithm completed:")
    print(f"   - Algorithm Name: {result.algorithm_name}")
    print(f"   - Execution Time: {result.execution_time:.3f}s")
    print(f"   - Final Coverage: {result.coverage:.2f}%")
    print(f"   - Active Nodes: {result.active_nodes}")
    
    # Check iteration logs
    logs = getattr(result, 'iteration_logs', [])
    print(f"📋 Iteration Logs: {len(logs)} entries")
    
    if logs:
        print("   First 5 log entries:")
        for i, log in enumerate(logs[:5]):
            print(f"     {i+1}. {log}")
    else:
        print("   ❌ No iteration logs found!")
    
    return logs

if __name__ == "__main__":
    logs = test_iteration_logs()
    if logs:
        print(f"\n✅ Success! Generated {len(logs)} iteration log entries")
    else:
        print(f"\n❌ Failed! No iteration logs generated")
