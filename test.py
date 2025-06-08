#!/usr/bin/env python3
"""
Quick test to verify the import fixes
"""

def test_imports():
    """Test if all imports work correctly"""
    print("🧪 Testing imports...")
    
    try:
        # Test environment import
        from simulation.environment import DroneEnvironment
        print("✅ DroneEnvironment imported successfully")
        
        # Test algorithms import
        from optimization.algorithms import greedy_optimization
        print("✅ greedy_optimization imported successfully")
        
        from optimization.algorithms import genetic_algorithm
        print("✅ genetic_algorithm imported successfully")
        
        from optimization.algorithms import particle_swarm_optimization
        print("✅ particle_swarm_optimization imported successfully")
        
        from optimization.algorithms import simulated_annealing
        print("✅ simulated_annealing imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    print("\n🔧 Testing basic functionality...")
    
    try:
        from simulation.environment import DroneEnvironment
        from optimization.algorithms import greedy_optimization
        
        # Create simulation
        sim = DroneEnvironment(width=50, height=50, num_drones=5, sensing_radius=10)
        print(f"✅ Created simulation with {len(sim.drones)} drones")
        
        # Test apply_activation method
        activation = [1, 0, 1, 0, 0]
        sim.apply_activation(activation)
        print(f"✅ Applied activation successfully")
        
        # Test algorithm
        result_activation, result = greedy_optimization(sim)
        print(f"✅ Greedy algorithm completed: {sum(result_activation)} drones activated")
        
        # Test applying algorithm result
        sim.apply_activation(result_activation)
        print(f"✅ Applied algorithm result successfully")
        
        # Test simulation step
        step_result = sim.step()
        print(f"✅ Simulation step: coverage={step_result['coverage']:.2%}")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Quick Test - Import and Basic Functionality")
    print("=" * 50)
    
    import_success = test_imports()
    functionality_success = test_basic_functionality()
    
    print("\n" + "=" * 50)
    print("📊 Results:")
    print(f"✅ Imports: {'PASSED' if import_success else 'FAILED'}")
    print(f"✅ Basic functionality: {'PASSED' if functionality_success else 'FAILED'}")
    
    if import_success and functionality_success:
        print("\n🎉 All tests passed!")
        print("🚀 The AttributeError should be fixed now.")
        print("💡 Start your app with: python run.py")
    else:
        print("\n⚠️ Some tests failed.")
        print("🔧 Make sure you've replaced the files correctly:")
        print("   - simulation/environment.py")
        print("   - optimization/algorithms.py") 
        print("   - optimization/__init__.py")