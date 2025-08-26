#!/usr/bin/env python3
"""
Quick import test
"""

print("Testing imports...")

try:
    print("1. Testing algorithms import...")
    from algorithms import *
    print("   ✅ Algorithms imported successfully")
    
    print("2. Testing app import...")
    from app import DroneSimulationEnvironment
    print("   ✅ DroneSimulationEnvironment imported successfully")
    
    print("3. Testing environment creation...")
    env = DroneSimulationEnvironment(area_size=(10, 10), num_targets=5, coverage_radius=2.5)
    print("   ✅ Environment created successfully")
    
    print("4. Testing algorithm function...")
    result = greedy_optimization(env)
    print(f"   ✅ Algorithm executed successfully - result type: {type(result)}")
    
    print("\n🎉 ALL TESTS PASSED! Ready for comprehensive experiment.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
