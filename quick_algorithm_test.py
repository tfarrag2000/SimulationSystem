#!/usr/bin/env python3
"""
Quick Algorithm Test
"""

def test_quick():
    print("🧪 QUICK ALGORITHM TEST")
    print("=" * 30)
    
    # Test imports first
    try:
        from app import DroneSimulationEnvironment
        print("✅ DroneSimulationEnvironment imported")
        
        from algorithms import particle_swarm_optimization, genetic_algorithm, simulated_annealing
        print("✅ All algorithms imported")
        
        # Create test environment
        env = DroneSimulationEnvironment(25, 25, 5, 6)
        print(f"✅ Test environment created: {len(env.drones)} drones")
        
        # Test PSO (quick)
        print("\n🔬 Testing PSO...")
        activation, result = particle_swarm_optimization(
            env, 
            swarm_size=10, 
            iterations=10, 
            smart_mode=True,
            desired_coverage=0.85
        )
        final_coverage = env.calculate_coverage_percentage(activation)
        print(f"✅ PSO: {final_coverage:.1f}% coverage, {sum(activation)}/{len(activation)} active")
        
        # Test GA (quick)
        print("\n🔬 Testing GA...")
        env2 = DroneSimulationEnvironment(25, 25, 5, 6)
        activation, result = genetic_algorithm(
            env2, 
            num_generations=10, 
            smart_mode=True,
            desired_coverage=0.85
        )
        final_coverage = env2.calculate_coverage_percentage(activation)
        print(f"✅ GA: {final_coverage:.1f}% coverage, {sum(activation)}/{len(activation)} active")
        
        # Test SA (quick)
        print("\n🔬 Testing SA...")
        env3 = DroneSimulationEnvironment(25, 25, 5, 6)
        activation, result = simulated_annealing(
            env3, 
            num_iterations=10, 
            smart_mode=True,
            desired_coverage=0.85
        )
        final_coverage = env3.calculate_coverage_percentage(activation)
        print(f"✅ SA: {final_coverage:.1f}% coverage, {sum(activation)}/{len(activation)} active")
        
        print("\n🎉 ALL ALGORITHMS WORKING!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_quick()
