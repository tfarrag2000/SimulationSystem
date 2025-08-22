"""
Debug script to test the visualization function
"""

def test_visualization_function():
    print("🔍 Testing visualization function accessibility...")
    
    try:
        # Test if we can import from app
        import sys
        sys.path.append('.')
        
        print("📦 Importing app module...")
        import app
        
        print("🎯 Checking if create_2d_drone_visualization exists...")
        if hasattr(app, 'create_2d_drone_visualization'):
            print("✅ Function exists in app module")
            
            # Test function call
            test_drones = [{'position': (10, 10), 'status': 'active'}]
            test_coverage = {'coverage': 50, 'energy_saved': 25}
            test_params = {'width': 40, 'height': 40, 'sensing_range': 8}
            
            result = app.create_2d_drone_visualization(test_drones, test_coverage, test_params)
            print("✅ Function call successful")
            print(f"📊 Result type: {type(result)}")
            
        else:
            print("❌ Function not found in app module")
            print("Available functions:", [attr for attr in dir(app) if 'visual' in attr.lower()])
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_visualization_function()
