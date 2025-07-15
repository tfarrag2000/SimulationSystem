#!/usr/bin/env python3
"""
Quick test script for the enhanced UI
"""

def test_app_import():
    """Test if the app imports without errors"""
    try:
        from app import app
        print("✅ App imported successfully")
        return True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def test_run_app():
    """Test running the application"""
    try:
        from app import app
        print("🚀 Starting test server on port 8052...")
        print("📍 Open browser: http://127.0.0.1:8052")
        app.run_server(debug=True, port=8052, host='127.0.0.1')
    except Exception as e:
        print(f"❌ Failed to start app: {e}")

if __name__ == "__main__":
    print("🧪 Testing Enhanced UI...")
    if test_app_import():
        test_run_app()
