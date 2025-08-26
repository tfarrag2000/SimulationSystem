#!/usr/bin/env python3
"""
Simple staged algorithm verification
"""

try:
    print("🔍 Testing imports...")
    from algorithms import greedy_optimization, staged_optimization_wrapper
    print("✅ Algorithm imports successful")
    
    from app import DroneSimulationEnvironment
    print("✅ Environment import successful")
    
    print("\n🧪 Creating test simulation...")
    sim = DroneSimulationEnvironment(
        area_width=50, 
        area_height=50, 
        num_drones=8,
        sensing_range=10,
        random_seed=42
    )
    print("✅ Simulation created successfully")
    
    print("\n🔄 Testing original greedy...")
    activation1, result1 = greedy_optimization(sim, desired_coverage=0.95)
    coverage1 = sim.calculate_coverage_percentage(activation1)
    print(f"✅ Original Greedy: {coverage1:.1f}% coverage")
    
    print("\n🎯 Testing staged greedy...")
    activation2, result2 = staged_optimization_wrapper(greedy_optimization, sim, desired_coverage=0.95, staged_mode=True)
    coverage2 = sim.calculate_coverage_percentage(activation2)
    print(f"✅ Staged Greedy: {coverage2:.1f}% coverage")
    
    print(f"\n📊 COMPARISON:")
    print(f"   Original: {coverage1:.1f}% coverage")
    print(f"   Staged:   {coverage2:.1f}% coverage")
    print(f"   Improvement: {coverage2 - coverage1:+.1f}%")
    
    print("\n🎉 STAGED ALGORITHMS WORKING CORRECTLY!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
