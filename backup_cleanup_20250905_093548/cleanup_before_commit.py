#!/usr/bin/env python3
"""
CLEANUP SCRIPT - Organize files before commit
Identifies test files, trial versions, and duplicates for cleanup
"""

import os
import shutil
from datetime import datetime

def identify_files_for_cleanup():
    """Identify files that should be cleaned up"""
    
    cleanup_categories = {
        'comprehensive_experimental_versions': [
            'enhanced_comprehensive_experimental.py',
            'comprehensive_experimental_fixed.py', 
            'comprehensive_experimental_clean.py',
            'comprehensive_experimental.py'  # Keep this as main version
        ],
        'test_and_demo_files': [
            'quick_enhanced_demo.py',
            'quick_coverage_demo.py', 
            'convergence_demo.py',
            'minimal_test.py',
            'simple_test.py',
            'quick_import_test.py'
        ],
        'integration_files': [
            'integrate_enhanced_algorithms.py',
            'integration_guide.py',
            'enhanced_coverage_algorithms.py'
        ],
        'temporary_files': [
            'coverage_improvement_guide.py',
            'temp_management.py'
        ]
    }
    
    # Check which files actually exist
    existing_files = {}
    for category, files in cleanup_categories.items():
        existing_files[category] = []
        for file in files:
            if os.path.exists(file):
                existing_files[category].append(file)
    
    return existing_files

def create_backup_folder():
    """Create backup folder for files being cleaned"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = f"backup_before_cleanup_{timestamp}"
    
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    
    return backup_folder

def perform_cleanup():
    """Perform the actual cleanup"""
    print("🧹 CLEANUP BEFORE COMMIT")
    print("="*40)
    
    # Identify files
    files_to_cleanup = identify_files_for_cleanup()
    
    # Create backup
    backup_folder = create_backup_folder()
    print(f"📁 Created backup folder: {backup_folder}")
    
    # Show what will be cleaned
    total_files = 0
    for category, files in files_to_cleanup.items():
        if files:
            print(f"\n📂 {category.replace('_', ' ').title()}:")
            for file in files:
                print(f"   • {file}")
                total_files += 1
    
    print(f"\n📊 Total files to clean: {total_files}")
    
    if total_files == 0:
        print("✅ No files need cleanup!")
        return backup_folder
    
    # Ask for confirmation
    response = input(f"\n❓ Proceed with cleanup? (y/n): ")
    
    if response.lower() != 'y':
        print("❌ Cleanup cancelled")
        return backup_folder
    
    # Perform cleanup
    files_moved = 0
    files_kept = []
    
    for category, files in files_to_cleanup.items():
        for file in files:
            try:
                # Special handling for main files to keep
                if file in ['comprehensive_experimental.py', 'algorithms.py', 'app.py']:
                    files_kept.append(file)
                    print(f"✅ Keeping: {file}")
                    continue
                
                # Move to backup
                shutil.move(file, os.path.join(backup_folder, file))
                files_moved += 1
                print(f"📦 Moved to backup: {file}")
                
            except Exception as e:
                print(f"❌ Error moving {file}: {e}")
    
    print(f"\n✅ CLEANUP COMPLETE!")
    print(f"   📦 Files moved to backup: {files_moved}")
    print(f"   ✅ Files kept: {len(files_kept)}")
    print(f"   📁 Backup location: {backup_folder}")
    
    return backup_folder

def show_remaining_structure():
    """Show the clean workspace structure"""
    print(f"\n📂 CLEAN WORKSPACE STRUCTURE:")
    print("="*35)
    
    important_files = [
        'app.py',
        'algorithms.py', 
        'comprehensive_experimental.py',
        'requirements.txt',
        'README.md'
    ]
    
    for file in important_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (missing)")
    
    # Show folders
    important_folders = [
        'experiments',
        'testing', 
        'documentation',
        '__pycache__'
    ]
    
    print(f"\n📁 Important Folders:")
    for folder in important_folders:
        if os.path.exists(folder):
            print(f"✅ {folder}/")
        else:
            print(f"❌ {folder}/ (missing)")

if __name__ == "__main__":
    print("🚀 WORKSPACE CLEANUP BEFORE COMMIT")
    print("="*45)
    print("This script will clean up test files and trial versions")
    print("All files will be backed up before removal\n")
    
    # Perform cleanup
    backup_folder = perform_cleanup()
    
    # Show clean structure
    show_remaining_structure()
    
    print(f"\n🎯 NEXT STEPS:")
    print("1. Review the clean workspace structure")
    print("2. Run: git add . && git commit -m 'Clean workspace before algorithm improvements'")
    print("3. Proceed with implementing new algorithms")
    print(f"4. If rollback needed: restore files from {backup_folder}")
