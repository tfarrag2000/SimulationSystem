import os

file_path = r"d:\OneDrive_Personal\OneDrive\My Research\03_published\Taif only\Drones 2\Kitchen\SimulationSystem\SimulationSystem\automatic_academic_paper_generator.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Unified Professional Color Palette (Synced across all figures)
old_colors = """    academic_colors = [
        '#2E4057', '#048A81', '#54C6EB', '#F18F01', '#C73E1D', '#7B2D26', '#A4243B',
        '#1B365D', '#0F4C75', '#3282B8', '#BBE1FA', '#9B59B6', '#8E44AD', '#D63031'
    ]"""

new_colors = """    # Unified Professional Color Palette (Synced across all figures)
    academic_colors = [
        '#2C3E50', '#16A085', '#3498DB', '#F39C12', '#E67E22', '#C0392B', '#D35400',
        '#34495E', '#2980B9', '#5DADE2', '#AED6F1', '#9B59B6', '#A569BD', '#E74C3C'
    ]"""

# Try a more robust regex-free replacement
if "academic_colors = [" in content:
    # Find the start and end of the list
    start_idx = content.find("academic_colors = [")
    end_idx = content.find("]", start_idx) + 1
    
    # Check if there are values inside
    header_comment = "    # Professional color palette - Consistent for all figures\n"
    full_old_block = header_comment + content[start_idx:end_idx]
    
    # Perform replacement
    # We'll just replace the whole block if possible
    # Alternatively, find the indentation
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if "academic_colors = [" in line:
            indent = line[:line.find("academic_colors")]
            new_lines = [
                f"{indent}# Unified Professional Color Palette (Synced across all figures)",
                f"{indent}academic_colors = [",
                f"{indent}    '#2C3E50', '#16A085', '#3498DB', '#F39C12', '#E67E22', '#C0392B', '#D35400',",
                f"{indent}    '#34495E', '#2980B9', '#5DADE2', '#AED6F1', '#9B59B6', '#8E44AD', '#D63031'",
                f"{indent}]"
            ]
            # Replace the lines from i to i+3 (approx)
            # Find the line with the closing ]
            end_line = i
            for j in range(i, i+10):
                if "]" in lines[j]:
                    end_line = j
                    break
            
            lines[i-1:end_line+1] = new_lines
            updated_content = "\n".join(lines)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print("Successfully updated colors!")
            break
else:
    print("Could not find academic_colors definition.")
