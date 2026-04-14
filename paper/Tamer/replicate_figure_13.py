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
    'axes.titlesize': 18,
    'axes.labelsize': 16,
    'xtick.labelsize': 11,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'figure.dpi': 1000
})

# 2. Define Algorithms and Colors
std_algs = ['PSO', 'GA', 'SA', 'ACO', 'DE', 'ABC', 'Greedy']
stg_algs = [f"{a}_Staged" for a in std_algs]
all_algs = std_algs + stg_algs

PALETTE_14 = [
    '#2C3E50', '#16A085', '#3498DB', '#F39C12', '#E67E22', '#C0392B', '#D35400',
    '#34495E', '#2980B9', '#5DADE2', '#AED6F1', '#9B59B6', '#A569BD', '#E74C3C'
]

# Data for "High Precision" scenario
coverage_data = [83.1, 81.2, 79.4, 80.3, 78.1, 77.6, 69.7, 85.7, 83.4, 81.8, 82.5, 80.3, 79.8, 75.2]
drone_data = [14, 15, 16, 15, 16, 17, 21, 13, 14, 15, 14, 15, 16, 18]

def generate_replicated_figure_13():
    print("Generating Replicated Figure 13 (High Precision, PNG Only)...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 11))
    
    # --- Panel 1: Coverage Efficiency ---
    bars1 = ax1.bar(all_algs, coverage_data, color=PALETTE_14, edgecolor='maroon', linewidth=1.2)
    ax1.set_ylabel('Coverage Efficiency (%)', fontweight='bold')
    ax1.set_title('Coverage Performance - High Precision', fontweight='bold', pad=15)
    ax1.set_xticks(range(len(all_algs)))
    ax1.set_xticklabels(all_algs, rotation=90)
    ax1.set_ylim(50, 95)
    
    # Yellow "BEST" box over PSO_Staged (index 7)
    best_idx = 7
    best_val = coverage_data[best_idx]
    ax1.annotate(f'BEST: PSO Staged\n{best_val}%', 
                 xy=(best_idx, best_val), xytext=(0, 25), 
                 textcoords='offset points', ha='center',
                 bbox=dict(boxstyle='round,pad=0.5', fc='gold', alpha=0.9, ec='black'),
                 fontweight='bold', fontsize=11, 
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    # Value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.3, f'{height:.1f}%', 
                 ha='center', va='bottom', fontsize=9, weight='bold')

    # --- Panel 2: Drone Efficiency ---
    bars2 = ax2.bar(all_algs, drone_data, color=PALETTE_14, edgecolor='darkgreen', linewidth=1.0)
    ax2.set_ylabel('Number of Drones Required', fontweight='bold')
    ax2.set_title('Drone Efficiency - High Precision', fontweight='bold', pad=15)
    ax2.set_xticks(range(len(all_algs)))
    ax2.set_xticklabels(all_algs, rotation=90)
    ax2.set_ylim(10, 30)
    
    # Green "MOST EFFICIENT" box over PSO_Staged (index 7)
    eff_idx = 7
    eff_val = drone_data[eff_idx]
    ax2.annotate(f'MOST EFFICIENT: PSO Staged\n{eff_val} drones', 
                 xy=(eff_idx, eff_val), xytext=(30, -50), 
                 textcoords='offset points', ha='center',
                 bbox=dict(boxstyle='round,pad=0.5', fc='lightgreen', alpha=0.9, ec='darkgreen'),
                 fontweight='bold', fontsize=11, 
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    # Value labels
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.2, f'{height}', 
                 ha='center', va='bottom', fontsize=10, weight='bold')

    # Main Figure Title
    fig.suptitle('Test Case: High Precision - Algorithm Performance Analysis', fontsize=22, fontweight='bold', y=0.98)
    
    # Unified Two-Column Legend for Precise One-to-One Correspondence
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=PALETTE_14[i], label=all_algs[i]) for i in range(len(all_algs))]
    ax1.legend(handles=legend_elements, loc='lower center', ncol=2, frameon=True, fontsize=10, 
               title="Algorithms (Std/Staged)", title_fontsize=11)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Save PNG Only
    png_path = os.path.join(OUTPUT_DIR, "fig_13_FINAL_REPLICATED.png")
    plt.savefig(png_path, dpi=1000, bbox_inches='tight')
    plt.close()
    
    print(f"SUCCESS: Replicated Figure 13 (PNG) saved to:\n  {png_path}")

if __name__ == "__main__":
    generate_replicated_figure_13()
