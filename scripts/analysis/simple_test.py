#!/usr/bin/env python3
"""
Simple test to debug the comprehensive experiment
"""

print("🧪 SIMPLE ALGORITHM TEST")
print("=" * 40)

try:
    print("1. Testing imports...")
    from algorithms import greedy_optimization, genetic_algorithm, particle_swarm_optimization
    print("   ✅ Basic algorithms imported")
    
    from algorithms import staged_optimization_wrapper  
    print("   ✅ Staged wrapper imported")
    
    import numpy as np
    print("   ✅ NumPy imported")
    
    print("\n2. Creating simple environment...")
    
    class SimpleEnv:
        def __init__(self, width, height, num_targets, coverage_radius):
            self.width = width
            self.height = height
            self.num_targets = num_targets
            self.coverage_radius = coverage_radius
            self.targets = np.random.rand(num_targets, 2) * [width, height]
            
            # Simple grid for coverage
            self.grid_points = np.array([[x, y] for x in range(0, width, 2) for y in range(0, height, 2)])
            
        def calculate_coverage_percentage(self, positions):
            if not positions or len(positions) == 0:
                return 0.0
            covered = 0
            for point in self.grid_points:
                for pos in positions:
                    if np.linalg.norm(np.array(point) - np.array(pos[:2])) <= self.coverage_radius:
                        covered += 1
                        break
            return (covered / len(self.grid_points)) * 100.0
    
    env = SimpleEnv(20, 20, 15, 2.5)
    print(f"   ✅ Environment created with {len(env.grid_points)} grid points")
    
    print("\n3. Testing single algorithm...")
    result = greedy_optimization(env)
    print(f"   ✅ Greedy algorithm result: {type(result)}")
    
    if isinstance(result, tuple):
        positions = result[0]
    else:
        positions = result
    
    if positions:
        coverage = env.calculate_coverage_percentage(positions)
        print(f"   ✅ Coverage calculated: {coverage:.1f}%")
    
    print("\n4. Testing staged algorithm...")
    staged_result = staged_optimization_wrapper(greedy_optimization, env)
    print(f"   ✅ Staged algorithm result: {type(staged_result)}")
    
    print("\n🎉 ALL TESTS PASSED!")
    print("   Ready to run comprehensive experiments")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
