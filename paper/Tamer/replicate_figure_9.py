import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Configuration
OUTPUT_DIR = r"d:\OneDrive_Personal\OneDrive\My Research\03_published\Taif only\Drones 2\Kitchen\SimulationSystem\SimulationSystem\paper\Tamer\figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Setup Academic Styling
plt.rcParams.update({
    'font.size': 14,
    'axes.titlesize': 20,
    'axes.labelsize': 18,
    'xtick.labelsize': 13,
    'ytick.labelsize': 13,
    'legend.fontsize': 11,
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'figure.dpi': 1000
})

# 2. Define Algorithms and Colors (Matched to Reference Image Gradient)
std_algs = ['PSO', 'GA', 'SA', 'ACO', 'DE', 'ABC', 'Greedy']
stg_algs = [f"{a}_Staged" for a in std_algs]
all_algs = std_algs + stg_algs

PALETTE_14 = [
    '#2C3E50', # PSO (Dark Blue)
    '#16A085', # GA (Greenish)
    '#3498DB', # SA (Sky Blue)
    '#F39C12', # ACO (Orange)
    '#E67E22', # DE (Carrot)
    '#C0392B', # ABC (Dark Red)
    '#D35400', # Greedy (Pumpkin)
    '#34495E', # PSO_Staged (Slate)
    '#2980B9', # GA_Staged (Belize)
    '#5DADE2', # SA_Staged (Blue)
    '#AED6F1', # ACO_Staged (Light Blue)
    '#9B59B6', # DE_Staged (Amethyst)
    '#A569BD', # ABC_Staged (Light Purple)
    '#E74C3C'  # Greedy_Staged (Red)
]

# 3. Define Scenarios and Performance Data (Extracted from Reference Image)
scenarios = [
    'Dense Coverage', 'Wide Area', 'Energy Constrained', 
    'High Precision', 'Mixed Terrain', 'Emergency Response'
]

# Rows are Algorithms, Columns are Scenarios
data = {
    'PSO': [89.5, 87.2, 85.8, 83.1, 80.7, 88.4],
    'GA': [87.8, 85.9, 83.4, 81.2, 78.9, 86.1],
    'SA': [85.1, 83.7, 81.9, 79.4, 77.1, 84.8],
    'ACO': [86.4, 84.5, 82.7, 80.3, 78.8, 85.5],
    'DE': [84.6, 82.8, 80.5, 78.1, 76.4, 83.1],
    'ABC': [83.9, 82.1, 79.8, 77.6, 75.8, 82.9],
    'Greedy': [75.2, 73.8, 71.5, 69.8, 68.1, 74.4],
    'PSO_Staged': [91.2, 89.4, 87.9, 85.7, 83.1, 90.8],
    'GA_Staged': [89.9, 88.1, 85.6, 83.4, 81.2, 88.7],
    'SA_Staged': [87.3, 85.9, 84.1, 81.8, 79.6, 86.4],
    'ACO_Staged': [88.6, 86.7, 84.9, 82.5, 80.9, 87.3],
    'DE_Staged': [86.9, 85.0, 82.7, 80.3, 78.7, 85.6],
    'ABC_Staged': [86.1, 84.3, 82.0, 79.8, 78.0, 84.8],
    'Greedy_Staged': [81.4, 79.8, 77.5, 75.2, 73.8, 80.9]
}

def generate_replicated_figure_9():
    print("Generating Replicated Figure 9 (Summary Comparison, PNG Only)...")
    
    fig, ax = plt.subplots(figsize=(26, 12))
    
    n_scenarios = len(scenarios)
    n_algs = len(all_algs)
    
    bar_width = 0.05
    indices = np.arange(n_scenarios)
    
    # Plot each algorithm's bar across all scenarios
    for i, alg in enumerate(all_algs):
        color = PALETTE_14[i]
        pos = indices + (i - n_algs/2) * bar_width
        bars = ax.bar(pos, data[alg], bar_width, label=alg, color=color, edgecolor='white', linewidth=0.3)
        
        # Add peak value labels ONLY on the highest bars to prevent massive overlap
        if alg == 'PSO_Staged':
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5, f'{height:.1f}', 
                        ha='center', va='bottom', fontsize=10, weight='bold')

    # Formatting
    ax.set_ylabel('Coverage Efficiency (%)', fontweight='bold', labelpad=15)
    ax.set_xlabel('Test Cases', fontweight='bold', labelpad=15)
    ax.set_title('Summary: Coverage Performance Comparison Across All Test Cases', fontweight='bold', pad=30)
    
    ax.set_xticks(indices)
    ax.set_xticklabels(scenarios, rotation=45, ha='right')
    
    ax.set_ylim(50, 95)
    ax.grid(axis='y', linestyle=':', alpha=0.5)
    
    # Unified Two-Column Legend for Precise One-to-One Correspondence
    ax.legend(loc='upper right', ncol=2, frameon=True, fancybox=True, 
              title="Algorithms (Column 1: Standard / Column 2: Staged)", 
              title_fontsize=12, handletextpad=0.5, columnspacing=1.0)

    plt.tight_layout()
    
    # Save PNG Only
    png_path = os.path.join(OUTPUT_DIR, "fig_9_FINAL_REPLICATED.png")
    plt.savefig(png_path, dpi=1000, bbox_inches='tight')
    plt.close()
    
    print(f"SUCCESS: Replicated Figure 9 (PNG) saved to:\n  {png_path}")

if __name__ == "__main__":
    generate_replicated_figure_9()
