#!/usr/bin/env python3
"""
Minimal test to check if algorithms can run
"""

print("🧪 MINIMAL ALGORITHM TEST")
print("=" * 30)

try:
    print("1. Importing algorithms...")
    from algorithms import greedy_optimization
    print("   ✅ Imported successfully")
    
    print("2. Creating minimal environment...")
    import pandas as pd
    import numpy as np
    
    class MinimalEnv:
        def __init__(self):
            self.width = 20
            self.height = 20
            self.sensing_radius = 2.5
            
            # Create grid points
            self.grid_points = np.array([[x, y] for x in range(0, 20, 2) for y in range(0, 20, 2)])
            
            # Create drones DataFrame
            self.drones = pd.DataFrame({
                'id': range(10),
                'x': np.random.uniform(0, 20, 10),
                'y': np.random.uniform(0, 20, 10),
                'energy': [100.0] * 10,
                'status': ['available'] * 10
            })
    
    env = MinimalEnv()
    print(f"   ✅ Environment created: {len(env.drones)} drones, {len(env.grid_points)} grid points")
    
    print("3. Testing algorithm...")
    result = greedy_optimization(env)
    print(f"   ✅ Algorithm executed: {type(result)}")
    
    print("🎉 SUCCESS! Basic functionality works")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
