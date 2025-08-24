#!/usr/bin/env python3
"""
FILE USAGE ANALYSIS
Analyzes which files are actually used vs redundant
"""

import os

def analyze_file_usage():
    """Analyze which files are essential vs redundant"""
    
    # Core system files (ESSENTIAL - Always needed)
    essential_core = {
        'app.py': 'Main dashboard application - CORE',
        'algorithms.py': 'Core optimization algorithms - CORE', 
        'requirements.txt': 'Dependencies - CORE',
        'README.md': 'Documentation - CORE'
    }
    
    # Currently used files (ACTIVE - Being used)
    active_files = {
        'quick_algorithm_test.py': 'Quick testing - ACTIVE',
        'temp_management.py': 'Temp file management - ACTIVE'
    }
    
    # Academic and research tools (USEFUL - Keep for research)
    research_tools = {
        'updated_academic_paper_generator.py': 'Academic paper generation',
        'dashboard_screenshot_generator.py': 'Dashboard documentation',
        'comprehensive_research_paper_with_analysis.py': 'Research analysis',
        'publication_generator.py': 'Publication tools',
        'docx_generator.py': 'Document generation'
    }
    
    # Analysis and optimization tools (USEFUL - Keep for analysis)
    analysis_tools = {
        'area_based_drone_optimizer.py': 'Area-based optimization',
        'drone_optimization_analyzer.py': 'Optimization analysis',
        'drone_repositioning_optimizer.py': 'Repositioning optimization',
        'drone_removal_recommendations.py': 'Removal recommendations',
        'performance_review.py': 'Performance analysis',
        'batch_analysis.py': 'Batch analysis',
        'optimal_configs.py': 'Optimal configurations'
    }
    
    # Experimental suites (USEFUL - Keep for experiments)
    experimental_tools = {
        'enhanced_experimental_suite.py': 'Experimental suite',
        'enhanced_experimental_suite_improved.py': 'Improved experiments'
    }
    
    # Documentation files (KEEP - Useful for reference)
    documentation = {
        'ORGANIZED_WORKSPACE_GUIDE.md': 'Workspace organization guide',
        'USAGE_GUIDE.md': 'Usage instructions',
        'ACADEMIC_PAPER_COMPLETION_SUMMARY.md': 'Academic completion summary',
        'CHANGELOG_v4.0.0.md': 'Version changelog',
        'RESEARCH_WORKFLOW_COMPLETE.md': 'Research workflow',
        'SYSTEM_STATUS_COMPLETE.md': 'System status',
        'TEAM_LEAD_SUMMARY.md': 'Team lead summary'
    }
    
    # Redundant/cleanup files (REMOVE - Not needed)
    redundant_files = {
        'cleanup.py': 'Old cleanup script - REDUNDANT',
        'fix_summary.py': 'Old fix summary - REDUNDANT', 
        'workspace_cleanup_tool.py': 'Cleanup tool - USED ONCE, CAN REMOVE',
        'workspace_organizer_fixed.py': 'Old organizer - REDUNDANT',
        'coverage_explanation.py': 'Old explanation - REDUNDANT',
        'drone_visualization.py': 'Old visualization - REDUNDANT',
        'supplementary_docs.py': 'Old supplementary docs - REDUNDANT'
    }
    
    # Old documentation (REMOVE - Outdated)
    old_docs = {
        '2D_SIMULATION_IMPLEMENTATION.md': 'Old implementation docs',
        'ITERATIONS_FIX_SUMMARY.md': 'Old fix summary',
        'MANUSCRIPT_SECTIONS.md': 'Old manuscript sections',
        'PAPER_SECTIONS_GUIDE.md': 'Old paper guide',
        'SOLUTION_SUMMARY.md': 'Old solution summary'
    }
    
    # Result directories (KEEP - Contains generated results)
    result_dirs = {
        'academic_paper_output_20250816_104310/': 'Academic paper output',
        'dashboard_documentation_20250822_120242/': 'Dashboard documentation',
        'updated_academic_paper_20250822_120013/': 'Updated academic paper',
        'REMOVED_FILES_BACKUP_20250822_120608/': 'Backup files',
        'REMOVED_FILES_BACKUP_20250822_134132/': 'Recent backup files'
    }
    
    return {
        'essential_core': essential_core,
        'active_files': active_files,
        'research_tools': research_tools,
        'analysis_tools': analysis_tools,
        'experimental_tools': experimental_tools,
        'documentation': documentation,
        'redundant_files': redundant_files,
        'old_docs': old_docs,
        'result_dirs': result_dirs
    }

def print_analysis():
    """Print the analysis results"""
    
    analysis = analyze_file_usage()
    
    print("🔍 FILE USAGE ANALYSIS")
    print("=" * 60)
    
    print("\n✅ ESSENTIAL CORE FILES (NEVER REMOVE):")
    for file, desc in analysis['essential_core'].items():
        if os.path.exists(file):
            print(f"   ✅ {file} - {desc}")
        else:
            print(f"   ❌ {file} - {desc} (MISSING!)")
    
    print(f"\n🔄 ACTIVE FILES (CURRENTLY USED):")
    for file, desc in analysis['active_files'].items():
        if os.path.exists(file):
            print(f"   ✅ {file} - {desc}")
        else:
            print(f"   ❌ {file} - {desc} (MISSING!)")
    
    print(f"\n📝 RESEARCH TOOLS (USEFUL FOR RESEARCH):")
    for file, desc in analysis['research_tools'].items():
        if os.path.exists(file):
            print(f"   📝 {file} - {desc}")
    
    print(f"\n📊 ANALYSIS TOOLS (USEFUL FOR ANALYSIS):")
    for file, desc in analysis['analysis_tools'].items():
        if os.path.exists(file):
            print(f"   📊 {file} - {desc}")
    
    print(f"\n🧪 EXPERIMENTAL TOOLS (USEFUL FOR EXPERIMENTS):")
    for file, desc in analysis['experimental_tools'].items():
        if os.path.exists(file):
            print(f"   🧪 {file} - {desc}")
    
    print(f"\n📋 DOCUMENTATION (KEEP FOR REFERENCE):")
    for file, desc in analysis['documentation'].items():
        if os.path.exists(file):
            print(f"   📋 {file} - {desc}")
    
    print(f"\n🗑️  REDUNDANT FILES (CAN BE REMOVED):")
    for file, desc in analysis['redundant_files'].items():
        if os.path.exists(file):
            print(f"   🗑️  {file} - {desc}")
    
    print(f"\n🗂️  OLD DOCUMENTATION (CAN BE REMOVED):")
    for file, desc in analysis['old_docs'].items():
        if os.path.exists(file):
            print(f"   🗂️  {file} - {desc}")
    
    print(f"\n📁 RESULT DIRECTORIES (KEEP - CONTAINS OUTPUTS):")
    for dir_name, desc in analysis['result_dirs'].items():
        if os.path.exists(dir_name):
            print(f"   📁 {dir_name} - {desc}")
    
    # Summary
    essential_count = len([f for f in analysis['essential_core'].keys() if os.path.exists(f)])
    active_count = len([f for f in analysis['active_files'].keys() if os.path.exists(f)])
    useful_count = (len([f for f in analysis['research_tools'].keys() if os.path.exists(f)]) +
                   len([f for f in analysis['analysis_tools'].keys() if os.path.exists(f)]) +
                   len([f for f in analysis['experimental_tools'].keys() if os.path.exists(f)]))
    doc_count = len([f for f in analysis['documentation'].keys() if os.path.exists(f)])
    redundant_count = len([f for f in analysis['redundant_files'].keys() if os.path.exists(f)])
    old_doc_count = len([f for f in analysis['old_docs'].keys() if os.path.exists(f)])
    
    print(f"\n📊 SUMMARY:")
    print(f"   Essential Core Files: {essential_count}")
    print(f"   Active Files: {active_count}")
    print(f"   Useful Tools: {useful_count}")
    print(f"   Documentation: {doc_count}")
    print(f"   Redundant Files: {redundant_count} (can remove)")
    print(f"   Old Documentation: {old_doc_count} (can remove)")
    
    total_keep = essential_count + active_count + useful_count + doc_count
    total_remove = redundant_count + old_doc_count
    
    print(f"\n🎯 RECOMMENDATION:")
    print(f"   KEEP: {total_keep} files")
    print(f"   CAN REMOVE: {total_remove} files")
    
    return analysis

if __name__ == "__main__":
    print_analysis()
