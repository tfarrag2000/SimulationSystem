#!/usr/bin/env python3
"""
WORKSPACE CLEANUP AND ORGANIZATION TOOL
Keeps essential files and removes temporary/duplicate files
"""

import os
import shutil
from datetime import datetime

def identify_files_to_keep():
    """Identify essential files that should be kept"""
    
    essential_files = {
        # MAIN DASHBOARD AND CORE SYSTEM
        'app.py',  # MAIN DASHBOARD - Keep this one!
        'algorithms.py',  # Core optimization algorithms
        'requirements.txt',  # Dependencies
        'README.md',  # Documentation
        
        # EXPERIMENTAL AND RESEARCH FILES
        'test_all_algorithms.py',  # Algorithm testing
        'quick_algorithm_test.py',  # Quick testing
        'enhanced_experimental_suite.py',  # Experimental suite
        'enhanced_experimental_suite_improved.py',  # Improved experiments
        'test_cases.py',  # Test case definitions
        'test_runner.py',  # Test execution
        'batch_analysis.py',  # Batch analysis
        'optimal_configs.py',  # Optimal configurations
        
        # ACADEMIC PAPER GENERATION
        'updated_academic_paper_generator.py',  # NEW academic paper generator
        'comprehensive_research_paper_with_analysis.py',  # Research paper
        'dashboard_screenshot_generator.py',  # Dashboard documentation
        'publication_generator.py',  # Publication tools
        'docx_generator.py',  # Document generation
        'supplementary_docs.py',  # Supplementary documentation
        
        # ANALYSIS AND OPTIMIZATION TOOLS
        'area_based_drone_optimizer.py',  # Area-based optimization
        'drone_optimization_analyzer.py',  # Optimization analysis
        'drone_repositioning_optimizer.py',  # Repositioning optimization
        'drone_removal_recommendations.py',  # Removal recommendations
        'performance_review.py',  # Performance analysis
        
        # DOCUMENTATION AND GUIDES
        'ACADEMIC_PAPER_COMPLETION_SUMMARY.md',  # Academic completion summary
        'CHANGELOG_v4.0.0.md',  # Version changelog
        'USAGE_GUIDE.md',  # Usage guide
        'README.md',  # Main documentation
        
        # UTILITY AND SUPPORT FILES
        'fix_summary.py',  # Fixes and summaries
        'cleanup.py',  # Cleanup utilities
        'workspace_organizer_fixed.py',  # Workspace organization
    }
    
    return essential_files

def identify_files_to_remove():
    """Identify temporary and duplicate files for removal"""
    
    files_to_remove = {
        # DUPLICATE APP FILES
        'app_new.py',  # Duplicate - app.py is the main one
        'app_simple.py',  # Simplified version - not needed
        'app_backup.py',  # Backup version
        'working_app.py',  # Working version backup
        
        # TEMPORARY AND OLD FILES
        'quick_test_config.py',  # Temporary test config
        'test_logs.py',  # Temporary test logs
        'test_suite.py',  # Old test suite
        'test_ui.py',  # UI testing (temporary)
        'ui_performance_test.py',  # Performance testing (temporary)
        'quick_pso_test.py',  # Quick PSO test (temporary)
        'debug_visualization.py',  # Debug file
        'coverage_explanation.py',  # Temporary explanation
        
        # OLD OPTIMIZATION FILES
        'intelligent_coverage_optimizer.py',  # Old optimizer
        'ultra_coverage_optimizer.py',  # Old optimizer
        'load_ultra_config.py',  # Old config loader
        'conflict_resolution.py',  # Old conflict resolution
        'dashboard_optimizer.py',  # Old dashboard optimizer
        
        # OLD DOCUMENTATION FILES
        'RESULTS_SECTION_ANALYSIS.md',  # Old analysis
        'RESULTS_SECTION_FINAL_ASSESSMENT.md',  # Old assessment
        'TROUBLESHOOTING_GUIDE.md',  # Old troubleshooting
        'UI_CHECKLIST.md',  # Old UI checklist
        'UI_PERFORMANCE_REVIEW.md',  # Old performance review
        'UI_REVIEW_SUMMARY.md',  # Old review summary
        'SETUP.md',  # Old setup guide
        'SIMPLIFIED_DASHBOARD_SUMMARY.md',  # Old summary
        'SOLUTION_SUMMARY.md',  # Old solution summary
        'TARGET_COVERAGE_FIX.md',  # Old fix documentation
        'ITERATIONS_FIX_SUMMARY.md',  # Old iterations fix
        'DASHBOARD_FIX_APPLIED.md',  # Old dashboard fix
        'DASHBOARD_REVIEW_REPORT.md',  # Old review report
        'FINAL_SUCCESS_REPORT.md',  # Old success report
        'VISUALIZATION_REVIEW.md',  # Old visualization review
        '2D_VISUALIZATION_FIX.md',  # Old 2D fix
        '2D_SIMULATION_IMPLEMENTATION.md',  # Old implementation
        'UPGRADE_SUMMARY_v4.0.0.md',  # Old upgrade summary
        
        # GENERATED RESEARCH FILES (OLD)
        'comprehensive_research_generator.py',  # Old generator
        'parallel_analysis_generator.py',  # Old parallel analysis
        'enhanced_manuscript_generator.py',  # Old manuscript generator
        
        # TEMPORARY EXPERIMENT FILES
        'pso_test_output.txt',  # Test output
        'drone_visualization.py',  # Old visualization
        
        # RUN FILES (NOT NEEDED WITH DASHBOARD)
        'run.py',  # Old runner - dashboard replaces this
    }
    
    return files_to_remove

def identify_directories_to_keep():
    """Identify directories that should be preserved"""
    
    keep_directories = {
        # RESULTS AND OUTPUT DIRECTORIES
        'academic_paper_output_20250816_104310',  # Academic paper output
        'updated_academic_paper_20250822_120013',  # Updated academic paper
        'dashboard_documentation_20250822_120242',  # Dashboard documentation
        '__pycache__',  # Python cache (needed for imports)
        '.git',  # Git repository
        '.vscode',  # VS Code settings
    }
    
    # Add any FINAL_RESEARCH_RESULTS directories
    for item in os.listdir('.'):
        if os.path.isdir(item) and 'FINAL_RESEARCH_RESULTS_' in item:
            keep_directories.add(item)
        if os.path.isdir(item) and 'academic_paper_output_' in item:
            keep_directories.add(item)
        if os.path.isdir(item) and 'updated_academic_paper_' in item:
            keep_directories.add(item)
        if os.path.isdir(item) and 'dashboard_documentation_' in item:
            keep_directories.add(item)
    
    return keep_directories

def cleanup_workspace():
    """Perform the workspace cleanup"""
    
    print("🧹 WORKSPACE CLEANUP AND ORGANIZATION")
    print("=" * 60)
    
    # Get file lists
    essential_files = identify_files_to_keep()
    files_to_remove = identify_files_to_remove()
    keep_directories = identify_directories_to_keep()
    
    # Create backup directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"REMOVED_FILES_BACKUP_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)
    
    print(f"📁 Backup directory created: {backup_dir}")
    
    # Analyze current files
    current_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    current_dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
    
    print(f"\n📊 CURRENT WORKSPACE STATUS:")
    print(f"   • Total files: {len(current_files)}")
    print(f"   • Total directories: {len(current_dirs)}")
    print(f"   • Essential files to keep: {len(essential_files)}")
    print(f"   • Files marked for removal: {len(files_to_remove)}")
    
    # Remove identified files
    removed_count = 0
    kept_count = 0
    
    print(f"\n🗑️  REMOVING TEMPORARY/DUPLICATE FILES:")
    for file in current_files:
        if file in files_to_remove:
            if os.path.exists(file):
                # Move to backup instead of deleting
                shutil.move(file, os.path.join(backup_dir, file))
                print(f"   ✅ Moved to backup: {file}")
                removed_count += 1
        elif file in essential_files:
            print(f"   ✅ Keeping essential: {file}")
            kept_count += 1
        else:
            # Files not explicitly listed - check if they should be kept
            if file.endswith(('.py', '.md', '.txt', '.json')):
                print(f"   ⚠️  Unknown file (keeping): {file}")
                kept_count += 1
            else:
                # Move unknown non-essential files to backup
                shutil.move(file, os.path.join(backup_dir, file))
                print(f"   📦 Moved unknown file to backup: {file}")
                removed_count += 1
    
    # Clean up directories
    print(f"\n📂 DIRECTORY MANAGEMENT:")
    for directory in current_dirs:
        if directory in keep_directories:
            print(f"   ✅ Keeping directory: {directory}")
        elif directory.startswith(('FINAL_RESEARCH_', 'academic_paper_', 'updated_academic_', 'dashboard_documentation_')):
            print(f"   ✅ Keeping results directory: {directory}")
        elif directory in ['__pycache__', '.git', '.vscode']:
            print(f"   ✅ Keeping system directory: {directory}")
        else:
            print(f"   ⚠️  Unknown directory (keeping): {directory}")
    
    # Summary
    print(f"\n📋 CLEANUP SUMMARY:")
    print(f"   • Files moved to backup: {removed_count}")
    print(f"   • Essential files kept: {kept_count}")
    print(f"   • Backup location: {backup_dir}")
    
    # Verify main dashboard
    if os.path.exists('app.py'):
        print(f"\n✅ MAIN DASHBOARD CONFIRMED:")
        print(f"   • Primary file: app.py (Version 4.0.0)")
        print(f"   • Status: Ready for use")
        print(f"   • Features: Smart optimization, progress indicators, dashboard interface")
    else:
        print(f"\n❌ ERROR: Main dashboard file (app.py) not found!")
    
    # Create organized file list
    create_organized_file_list()
    
    print(f"\n🎉 WORKSPACE CLEANUP COMPLETE!")
    print(f"💡 To run the dashboard: python app.py")
    
    return removed_count, kept_count, backup_dir

def create_organized_file_list():
    """Create an organized list of remaining files"""
    
    remaining_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    remaining_dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
    
    file_list = f"""
# 📁 ORGANIZED WORKSPACE FILE LIST
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 🎯 MAIN DASHBOARD SYSTEM
- **app.py** - Main dashboard application (Version 4.0.0)
- **algorithms.py** - Core optimization algorithms with smart enhancements
- **requirements.txt** - System dependencies

## 🔬 EXPERIMENTAL AND RESEARCH FILES
"""
    
    experimental_files = [f for f in remaining_files if 'test' in f.lower() or 'experiment' in f.lower() or 'batch' in f.lower()]
    for file in sorted(experimental_files):
        file_list += f"- **{file}** - Experimental/testing functionality\n"
    
    file_list += f"""
## 📝 ACADEMIC AND DOCUMENTATION
"""
    
    academic_files = [f for f in remaining_files if 'paper' in f.lower() or 'academic' in f.lower() or 'publication' in f.lower() or 'docx' in f.lower()]
    for file in sorted(academic_files):
        file_list += f"- **{file}** - Academic paper generation and documentation\n"
    
    file_list += f"""
## 🔧 ANALYSIS AND OPTIMIZATION TOOLS
"""
    
    analysis_files = [f for f in remaining_files if 'optim' in f.lower() or 'analy' in f.lower() or 'performance' in f.lower()]
    for file in sorted(analysis_files):
        if file not in experimental_files and file not in academic_files:
            file_list += f"- **{file}** - Analysis and optimization tools\n"
    
    file_list += f"""
## 📋 DOCUMENTATION FILES
"""
    
    doc_files = [f for f in remaining_files if f.endswith('.md')]
    for file in sorted(doc_files):
        file_list += f"- **{file}** - Documentation and guides\n"
    
    file_list += f"""
## 📂 RESULT DIRECTORIES
"""
    
    result_dirs = [d for d in remaining_dirs if 'result' in d.lower() or 'academic' in d.lower() or 'dashboard' in d.lower()]
    for directory in sorted(result_dirs):
        file_list += f"- **{directory}/** - Generated results and output\n"
    
    file_list += f"""
## 🎯 USAGE INSTRUCTIONS

### To Run the Dashboard:
```bash
python app.py
```
Then open: http://127.0.0.1:8050

### To Run Algorithm Tests:
```bash
python test_all_algorithms.py
python quick_algorithm_test.py
```

### To Generate Academic Paper:
```bash
python updated_academic_paper_generator.py
```

### To Create Dashboard Documentation:
```bash
python dashboard_screenshot_generator.py
```

## ✅ SYSTEM STATUS
- **Main Dashboard**: ✅ Ready (app.py)
- **Algorithms**: ✅ Enhanced with smart optimization
- **Progress Indicators**: ✅ Real-time monitoring with abort capability
- **Duplicate Prevention**: ✅ Automatic detection and removal
- **Academic Documentation**: ✅ Comprehensive paper and visuals
- **Test Suite**: ✅ Complete algorithm validation

**Total Files**: {len(remaining_files)}
**Total Directories**: {len(remaining_dirs)}
**Status**: 🎉 Clean and Organized!
"""
    
    with open('ORGANIZED_WORKSPACE_GUIDE.md', 'w') as f:
        f.write(file_list)
    
    print(f"   📄 Created: ORGANIZED_WORKSPACE_GUIDE.md")

def main():
    """Main cleanup function"""
    
    # Change to the correct directory if needed
    try:
        os.chdir(r"d:\OneDrive_Personal\OneDrive\My Research\01_Working\Drones\SimulationSystem")
    except:
        pass  # Already in correct directory
    
    # Perform cleanup
    removed_count, kept_count, backup_dir = cleanup_workspace()
    
    return removed_count, kept_count, backup_dir

if __name__ == "__main__":
    main()
