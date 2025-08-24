#!/usr/bin/env python3
"""
SAFE FILE REMOVAL SCRIPT
Removes redundant files by moving them to backup folder
"""

import os
import shutil
from datetime import datetime

def safe_remove_redundant_files():
    """Safely remove redundant files by moving to backup"""
    
    # Create backup directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"REDUNDANT_FILES_BACKUP_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)
    
    print(f"🗑️  SAFE REMOVAL OF REDUNDANT FILES")
    print(f"=" * 50)
    print(f"📁 Backup directory: {backup_dir}")
    
    # Files to remove (redundant/old)
    files_to_remove = [
        # Old/Redundant Scripts
        'cleanup.py',
        'fix_summary.py', 
        'workspace_cleanup_tool.py',
        'workspace_organizer_fixed.py',
        'coverage_explanation.py',
        'drone_visualization.py',
        'supplementary_docs.py',
        
        # Old Documentation
        '2D_SIMULATION_IMPLEMENTATION.md',
        'ITERATIONS_FIX_SUMMARY.md',
        'MANUSCRIPT_SECTIONS.md',
        'PAPER_SECTIONS_GUIDE.md',
        'SOLUTION_SUMMARY.md',
        
        # Temporary analysis file
        'file_usage_analyzer.py'  # This script itself
    ]
    
    removed_count = 0
    
    print(f"\n🗑️  REMOVING REDUNDANT FILES:")
    for file in files_to_remove:
        if os.path.exists(file):
            try:
                shutil.move(file, os.path.join(backup_dir, file))
                print(f"   ✅ Moved: {file}")
                removed_count += 1
            except Exception as e:
                print(f"   ❌ Failed to move {file}: {e}")
        else:
            print(f"   ⚠️  Not found: {file}")
    
    print(f"\n📊 REMOVAL SUMMARY:")
    print(f"   • Files moved to backup: {removed_count}")
    print(f"   • Backup location: {backup_dir}")
    
    # Show remaining essential files
    print(f"\n✅ REMAINING ESSENTIAL FILES:")
    essential_files = [
        'app.py',
        'algorithms.py', 
        'requirements.txt',
        'README.md',
        'quick_algorithm_test.py',
        'temp_management.py'
    ]
    
    for file in essential_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (MISSING!)")
    
    # Show remaining useful tools
    print(f"\n📝 REMAINING USEFUL TOOLS:")
    useful_tools = [
        'updated_academic_paper_generator.py',
        'dashboard_screenshot_generator.py',
        'comprehensive_research_paper_with_analysis.py',
        'area_based_drone_optimizer.py',
        'drone_optimization_analyzer.py',
        'enhanced_experimental_suite.py'
    ]
    
    for file in useful_tools:
        if os.path.exists(file):
            print(f"   📝 {file}")
    
    print(f"\n🎉 CLEANUP COMPLETE!")
    print(f"💡 Workspace is now clean and organized")
    
    return removed_count, backup_dir

if __name__ == "__main__":
    removed_count, backup_dir = safe_remove_redundant_files()
