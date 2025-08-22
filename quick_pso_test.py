#!/usr/bin/env python3
"""
Quick PSO Algorithm Test - Simplified Version
Testing PSO algorithm with reduced iterations for faster results
"""

import os
import sys
import numpy as np

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def quick_pso_test():
    """Test PSO algorithm quickly with minimal iterations"""
    
    print("=" * 60)
    print("QUICK PSO ALGORITHM TEST")
    print("=" * 60)
    
    try:
        # Import required modules  
        from algorithms import particle_swarm_optimization
        from app import DroneSimulationEnvironment
        
        print("✓ Successfully imported PSO algorithm and DroneSimulationEnvironment")
        
        # Create simulation environment (same as used in dashboard)
        simulation = DroneSimulationEnvironment(
            width=1000,  # 1km x 1km area
            height=1000,
            num_drones=50,
            sensing_radius=100  # 100m sensing radius
        )
        print(f"✓ Created simulation environment: {simulation.width}x{simulation.height} with {simulation.num_drones} drones")
        
        # Test environment coverage calculation first
        print(f"\n--- Environment Coverage Test ---")
        test_activation = np.ones(simulation.num_drones)  # All drones active
        if hasattr(simulation, 'calculate_coverage_percentage'):
            full_coverage = simulation.calculate_coverage_percentage(test_activation)
            print(f"Full activation coverage: {full_coverage:.2%}")
        
        # Quick PSO test with minimal iterations
        print(f"\n--- Quick PSO Test (10 iterations) ---")
        
        # Use minimal iterations for quick test
        config = {
            "swarm_size": 20, 
            "iterations": 10,  # Very few iterations for quick test
            "inertia": 0.7, 
            "cognitive_weight": 1.5, 
            "social_weight": 1.5,
            "parallel_processing": False  # Disable to avoid pickle issues
        }
        
        print(f"Configuration: {config}")
        
        # Call PSO algorithm
        activation, result = particle_swarm_optimization(simulation, **config)
        
        print(f"✓ PSO completed successfully!")
        print(f"  - Activation pattern type: {type(activation)}")
        print(f"  - Activation shape: {activation.shape if hasattr(activation, 'shape') else 'No shape'}")
        print(f"  - Result type: {type(result)}")
        
        # Analyze results
        if hasattr(result, 'coverage'):
            coverage = result.coverage
            print(f"  - Final Coverage: {coverage:.2f}%")
        elif hasattr(result, 'best_fitness'):
            print(f"  - Best Fitness: {result.best_fitness:.2f}")
            if hasattr(result, 'coverage_history') and result.coverage_history:
                final_coverage = result.coverage_history[-1]
                print(f"  - Final Coverage: {final_coverage:.2f}%")
        else:
            print(f"  - Result structure: {dir(result) if hasattr(result, '__dict__') else 'Simple type'}")
        
        # Analyze activation pattern
        if hasattr(activation, 'shape') and len(activation.shape) == 1:
            active_drones = np.sum(activation > 0.5)
            total_drones = len(activation)
            activation_ratio = active_drones / total_drones
            print(f"  - Active drones: {active_drones}/{total_drones} ({activation_ratio:.1%})")
            
            # Calculate actual coverage using the activation pattern
            actual_coverage = simulation.calculate_coverage_percentage(activation)
            print(f"  - Calculated coverage: {actual_coverage:.2%}")
            
            if actual_coverage < 0.1:  # Less than 10%
                print(f"  ⚠️ WARNING: Coverage {actual_coverage:.2%} is very low!")
                print(f"     This suggests a potential issue with the algorithm or environment")
            elif actual_coverage > 0.5:  # More than 50%
                print(f"  ✓ Coverage {actual_coverage:.2%} looks reasonable")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    quick_pso_test()
