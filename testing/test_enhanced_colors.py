#!/usr/bin/env python3
"""
Test the Enhanced Academic Color Dashboard
Run this to see the new colorful design
"""

import subprocess
import sys

def test_enhanced_dashboard():
    """Test the enhanced colorful dashboard"""
    
    print("🎨 Testing Enhanced Academic Color Dashboard")
    print("=" * 50)
    print()
    print("✅ Enhanced Features Applied:")
    print("   🎓 Academic header with research badges")
    print("   🌈 Colorful card headers (success, warning, danger, info)")
    print("   🚀 Enhanced control buttons with emojis")
    print("   📊 Colorful data visualization cards")
    print("   🎯 Icon-enhanced form labels")
    print()
    print("🔄 Rollback Instructions:")
    print("   If you don't like the new colors, run:")
    print("   python restore_original_colors.py")
    print()
    print("🚀 Starting enhanced dashboard...")
    
    try:
        # Run the app
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")

if __name__ == "__main__":
    test_enhanced_dashboard()
