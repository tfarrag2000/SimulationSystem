#!/usr/bin/env python3
"""
CLEANUP SCRIPT - Remove unwanted files and organize workspace
"""

import os
import shutil

def cleanup_workspace():
    """Clean up unwanted files and organize the workspace"""
    
    print("🧹 Starting workspace cleanup...")
    
    # Files to keep (ESSENTIAL)
    essential_files = {
        'algorithms.py',  # Core optimization algorithms
        'enhanced_experimental_suite_improved.py',  # Academic paper generation
        'test_app.py',  # Working web interface
        'README.md',
        'requirements.txt',
        'run.py'
    }
    
    # Files to remove (UNWANTED DUPLICATES/BACKUPS)
    unwanted_files = {
        'app_backup_simple.py',
        'app_corrupted_backup.py', 
        'app_fixed.py',
        'app_new.py',
        'app_simple.py',
        'app_clean.py',
        'working_app.py',
        'area_based_drone_optimizer.py',
        'comprehensive_research_generator.py',
        'conflict_resolution.py',
        'dashboard_optimizer.py'
    }
    
    # Special handling for app.py (corrupted, needs fixing)
    problematic_files = {
        'app.py'  # Has Unicode issues, we'll keep test_app.py instead
    }
    
    # Count files
    removed_count = 0
    
    print("\n📋 CLEANUP PLAN:")
    print("=" * 50)
    
    print("\n✅ KEEPING (Essential files):")
    for file in essential_files:
        if os.path.exists(file):
            print(f"  • {file}")
    
    print("\n🗑️  REMOVING (Unwanted duplicates/backups):")
    for file in unwanted_files:
        if os.path.exists(file):
            print(f"  • {file}")
    
    print("\n⚠️  PROBLEMATIC (Will rename with .backup):")
    for file in problematic_files:
        if os.path.exists(file):
            print(f"  • {file} → {file}.backup")
    
    # Ask for confirmation
    response = input("\n🤔 Proceed with cleanup? (y/N): ")
    
    if response.lower() != 'y':
        print("❌ Cleanup cancelled.")
        return
    
    print("\n🧹 Performing cleanup...")
    
    # Remove unwanted files
    for file in unwanted_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"  ✅ Removed: {file}")
                removed_count += 1
            except Exception as e:
                print(f"  ❌ Failed to remove {file}: {e}")
    
    # Backup problematic files
    for file in problematic_files:
        if os.path.exists(file):
            try:
                backup_name = f"{file}.backup"
                shutil.move(file, backup_name)
                print(f"  ✅ Moved: {file} → {backup_name}")
                removed_count += 1
            except Exception as e:
                print(f"  ❌ Failed to backup {file}: {e}")
    
    # Clean __pycache__
    if os.path.exists('__pycache__'):
        try:
            shutil.rmtree('__pycache__')
            print(f"  ✅ Removed: __pycache__/")
            removed_count += 1
        except Exception as e:
            print(f"  ❌ Failed to remove __pycache__: {e}")
    
    print(f"\n🎉 Cleanup completed! Removed {removed_count} files/folders.")
    
    print("\n" + "=" * 60)
    print("📖 HOW TO RUN THE SYSTEM:")
    print("=" * 60)
    
    print("\n🚀 FOR WEB INTERFACE:")
    print("   python test_app.py")
    print("   → Opens at: http://127.0.0.1:8050/")
    print("   → Features: Interactive drone visualization, algorithm testing")
    
    print("\n📊 FOR ACADEMIC RESEARCH & PAPER GENERATION:")
    print("   python enhanced_experimental_suite_improved.py")
    print("   → Generates: Complete academic paper with 14 figures")
    print("   → Features: 42 experiments, performance analysis, publication-ready output")
    
    print("\n📁 ESSENTIAL FILES REMAINING:")
    for file in essential_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   • {file} ({size:,} bytes)")
    
    # Check if academic output exists
    if os.path.exists('academic_paper_output_20250814_010326'):
        print(f"\n📚 ACADEMIC OUTPUT AVAILABLE:")
        print(f"   • academic_paper_output_20250814_010326/")
        print(f"   → Contains: Research paper, figures, data tables")

if __name__ == '__main__':
    cleanup_workspace()
