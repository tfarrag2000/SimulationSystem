#!/usr/bin/env python3
"""
The Paper Folder Organization and Cleanup
Removes redundancy and organizes content properly
"""

import os
import shutil
from pathlib import Path

def organize_paper_folder():
    """Organize The Paper folder and remove redundancy"""
    print("🗂️ ORGANIZING THE PAPER FOLDER")
    print("=" * 50)
    
    paper_dir = Path("The Paper")
    
    # Create organized structure
    print("\n📁 Creating organized folder structure...")
    
    # Main directories
    directories = [
        "Data/Current",
        "Data/Archive", 
        "Figures/PNG/Current",
        "Figures/PNG/Archive",
        "Figures/EPS/Current",
        "Figures/Raw/Archive",
        "Tables/LaTeX",
        "Tables/CSV",
        "Documents/Final",
        "Documents/Drafts",
        "Experiments/Results/Current",
        "Experiments/Results/Archive",
        "Experiments/Scripts"
    ]
    
    for directory in directories:
        os.makedirs(paper_dir / directory, exist_ok=True)
        print(f"   ✅ Created: {directory}")
    
    # Move and organize existing files
    print("\n📄 Organizing existing files...")
    
    # Move data files to organized structure
    data_files = [
        "algorithm_ranking.csv",
        "all_experimental_data.csv", 
        "comprehensive_results.json",
        "coverage_statistics.csv",
        "efficiency_statistics.csv",
        "time_statistics.csv"
    ]
    
    for file in data_files:
        src = paper_dir / "Data" / file
        dst = paper_dir / "Data" / "Current" / file
        if src.exists():
            shutil.move(str(src), str(dst))
            print(f"   📊 Moved: {file} → Data/Current/")
    
    # Move main document to Final documents
    main_docs = [
        "Enhanced_IEEE_Paper_Staged_Optimization_FINAL.docx",
        "Enhanced_IEEE_Paper_Staged_Optimization.tex"
    ]
    
    for doc in main_docs:
        src = paper_dir / doc
        dst = paper_dir / "Documents" / "Final" / doc
        if src.exists():
            shutil.move(str(src), str(dst))
            print(f"   📄 Moved: {doc} → Documents/Final/")
    
    # Archive old drone paper
    old_paper = paper_dir / "Drone paper.docx"
    if old_paper.exists():
        shutil.move(str(old_paper), str(paper_dir / "Documents" / "Archive" / "Drone paper.docx"))
        print("   📄 Archived: Drone paper.docx → Documents/Archive/")
    
    # Move figures to current
    png_files = list((paper_dir / "Figures" / "PNG").glob("*.png"))
    for png_file in png_files:
        if png_file.name not in ["dashboard_screenshot.png"]:  # Keep main screenshot in root
            dst = paper_dir / "Figures" / "PNG" / "Current" / png_file.name
            shutil.move(str(png_file), str(dst))
            print(f"   🖼️ Moved: {png_file.name} → Figures/PNG/Current/")
    
    # Create summary files
    print("\n📋 Creating organization summary...")
    
    # Create README for folder structure
    readme_content = """
# THE PAPER FOLDER ORGANIZATION

## 📁 FOLDER STRUCTURE

### Data/
- **Current/**: Latest experimental data and results
- **Archive/**: Previous experimental data versions

### Figures/
- **PNG/Current/**: Publication-ready PNG figures
- **PNG/Archive/**: Previous figure versions
- **EPS/Current/**: Vector format figures for journals
- **Raw/Archive/**: Original/raw figure files

### Tables/
- **LaTeX/**: LaTeX formatted tables for paper
- **CSV/**: Raw table data in CSV format

### Documents/
- **Final/**: Final paper versions (Word + LaTeX)
- **Drafts/**: Draft versions and working documents
- **Archive/**: Older paper versions

### Experiments/
- **Results/Current/**: Latest experimental results
- **Results/Archive/**: Previous experimental runs
- **Scripts/**: Experimental execution scripts

## 📊 CURRENT MAIN FILES

### Final Documents:
- `Documents/Final/Enhanced_IEEE_Paper_Staged_Optimization_FINAL.docx`
- `Documents/Final/Enhanced_IEEE_Paper_Staged_Optimization.tex`

### Current Data:
- `Data/Current/algorithm_ranking.csv`
- `Data/Current/comprehensive_results.json`
- `Data/Current/coverage_statistics.csv`

### Current Figures:
- `Figures/PNG/Current/staged_vs_original_comparison.png`
- `Figures/PNG/Current/energy_savings_analysis.png`
- `Figures/dashboard_screenshot.png` (main screenshot)

## 🎯 USAGE GUIDE

1. **Adding new figures**: Place in `Figures/PNG/Current/`
2. **Adding new data**: Place in `Data/Current/`
3. **Paper revisions**: Work in `Documents/Final/`
4. **Experimental data**: Store in `Experiments/Results/Current/`

## 🧹 MAINTENANCE

- Archive old files regularly to Archive folders
- Keep Current folders clean with only latest versions
- Update this README when structure changes
"""
    
    with open(paper_dir / "README.md", 'w') as f:
        f.write(readme_content.strip())
    
    print("   ✅ Created: README.md with folder guide")
    
    # Create file index
    print("\n📑 Creating file index...")
    
    file_index = []
    for root, dirs, files in os.walk(paper_dir):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), paper_dir)
            file_size = os.path.getsize(os.path.join(root, file))
            file_index.append((rel_path, file_size))
    
    # Sort by size (largest first)
    file_index.sort(key=lambda x: x[1], reverse=True)
    
    index_content = "# THE PAPER FOLDER FILE INDEX\n\n"
    index_content += "| File Path | Size | Type |\n"
    index_content += "|-----------|------|------|\n"
    
    for file_path, size in file_index:
        size_mb = size / (1024 * 1024)
        file_ext = Path(file_path).suffix
        index_content += f"| {file_path} | {size_mb:.2f} MB | {file_ext} |\n"
    
    with open(paper_dir / "FILE_INDEX.md", 'w') as f:
        f.write(index_content)
    
    print("   ✅ Created: FILE_INDEX.md with complete file listing")
    
    print("\n" + "=" * 50)
    print("🎉 THE PAPER FOLDER ORGANIZATION COMPLETE!")
    print("\n📊 Organization Summary:")
    print(f"   📁 Created: {len(directories)} organized directories")
    print(f"   📄 Organized: {len(data_files)} data files")
    print(f"   📄 Organized: {len(main_docs)} main documents")
    print("   📋 Created: README.md and FILE_INDEX.md")
    print("\n🎯 Next Steps:")
    print("   1. Review organized structure in The Paper folder")
    print("   2. Check Documents/Final/ for enhanced paper")
    print("   3. Verify Figures/PNG/Current/ for latest figures")
    print("   4. Use README.md as guide for future organization")

if __name__ == "__main__":
    organize_paper_folder()
