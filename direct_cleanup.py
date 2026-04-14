#!/usr/bin/env python3
"""
Direct Workspace Cleanup Script
Moves specific files to organize the workspace
"""

import os
import shutil
from pathlib import Path

def direct_cleanup():
    """Direct cleanup with specific file lists"""
    
    # Create directories
    os.makedirs("temp_files/test_scripts", exist_ok=True)
    os.makedirs("temp_files/analysis_files", exist_ok=True)
    os.makedirs("temp_files/debug_files", exist_ok=True)
    os.makedirs("temp_files/experimental_files", exist_ok=True)
    os.makedirs("temp_files/images", exist_ok=True)
    
    moved_count = 0
    
    # Get all Python files in current directory
    python_files = [f for f in os.listdir('.') if f.endswith('.py')]
    
    # Core files to keep in main directory
    core_files = {
        'algorithms.py', 'app.py', 'automatic_academic_paper_generator.py',
        'cleanup_workspace.py', 'direct_cleanup.py'
    }
    
    print("🧹 Starting direct cleanup...")
    
    # Move test files
    test_files = [f for f in python_files if f.startswith(('test_', 'quick_', 'simple_', 'debug_'))]
    for f in test_files:
        if f not in core_files:
            try:
                shutil.move(f, f'temp_files/test_scripts/{f}')
                print(f"   📁 Moved test file: {f}")
                moved_count += 1
            except Exception as e:
                print(f"   ❌ Error moving {f}: {e}")
    
    # Move analysis files
    analysis_files = [f for f in python_files if any(keyword in f for keyword in ['analysis', 'analyzer', 'comparison', 'summary', 'guide', 'demo'])]
    for f in analysis_files:
        if f not in core_files and not f.startswith('test_'):
            try:
                shutil.move(f, f'temp_files/analysis_files/{f}')
                print(f"   📊 Moved analysis file: {f}")
                moved_count += 1
            except Exception as e:
                print(f"   ❌ Error moving {f}: {e}")
    
    # Move experimental files
    experimental_files = [f for f in python_files if any(keyword in f for keyword in ['enhanced_', 'comprehensive_', 'universal_', 'smart_', 'optimizer', 'enhancement', 'implement_', 'integrate_', 'final_'])]
    for f in experimental_files:
        if f not in core_files and not f.startswith('test_') and 'analysis' not in f:
            try:
                shutil.move(f, f'temp_files/experimental_files/{f}')
                print(f"   🔬 Moved experimental file: {f}")
                moved_count += 1
            except Exception as e:
                print(f"   ❌ Error moving {f}: {e}")
    
    # Move debug files
    debug_files = [f for f in python_files if any(keyword in f for keyword in ['before_after_', 'reference_', 'validate_', 'verify_', 'manual_', 'targeted_'])]
    for f in debug_files:
        if f not in core_files:
            try:
                shutil.move(f, f'temp_files/debug_files/{f}')
                print(f"   🐛 Moved debug file: {f}")
                moved_count += 1
            except Exception as e:
                print(f"   ❌ Error moving {f}: {e}")
    
    # Move image files
    image_files = [f for f in os.listdir('.') if f.endswith(('.png', '.jpg', '.jpeg', '.gif')) and f.startswith('test')]
    for f in image_files:
        try:
            shutil.move(f, f'temp_files/images/{f}')
            print(f"   🖼️ Moved image file: {f}")
            moved_count += 1
        except Exception as e:
            print(f"   ❌ Error moving {f}: {e}")
    
    # Move documentation files (except main READMEs)
    md_files = [f for f in os.listdir('.') if f.endswith('.md') and f not in ['README.md', 'README_NEW.md']]
    for f in md_files:
        try:
            shutil.move(f, f'documentation/{f}')
            print(f"   📚 Moved documentation: {f}")
            moved_count += 1
        except Exception as e:
            print(f"   ❌ Error moving {f}: {e}")
    
    print(f"\n✅ Cleanup completed!")
    print(f"📊 Total files organized: {moved_count}")
    
    # Show remaining files
    remaining_py_files = [f for f in os.listdir('.') if f.endswith('.py')]
    print(f"\n🎯 Remaining Python files in main directory:")
    for f in sorted(remaining_py_files):
        print(f"   • {f}")
    
    return moved_count

if __name__ == "__main__":
    moved_count = direct_cleanup()
    print(f"\n🏁 Direct cleanup completed! {moved_count} files organized.")
