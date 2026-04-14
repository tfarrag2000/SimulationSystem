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
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'figure.dpi': 1000
})

# 2. Define Algorithms and Colors (Unified with Figures 9-15)
std_algs = ['PSO', 'GA', 'SA', 'ACO', 'DE', 'ABC', 'Greedy']
stg_algs = [f"{a}_Staged" for a in std_algs]
all_algs = std_algs + stg_algs

PALETTE_14 = [
    '#2C3E50', '#16A085', '#3498DB', '#F39C12', '#E67E22', '#C0392B', '#D35400',
    '#34495E', '#2980B9', '#5DADE2', '#AED6F1', '#9B59B6', '#A569BD', '#E74C3C'
]

from matplotlib.patches import Patch
legend_patches = [Patch(facecolor=PALETTE_14[i], label=all_algs[i]) for i in range(len(all_algs))]

# Data extraction (approximated from user reference image values)
energy_std = [1518.3, 1613.3, 1708.3, 1613.3, 1708.3, 1803.3, 2151.7]
energy_stg = [1423.3, 1518.3, 1613.3, 1518.3, 1613.3, 1708.3, 1898.3]
all_energy = energy_std + energy_stg

sleep_std = [41.3, 37.3, 33.3, 37.3, 33.3, 29.3, 14.7]
sleep_stg = [45.3, 41.3, 37.3, 41.3, 37.3, 33.3, 25.3]
all_sleep = sleep_std + sleep_stg

ratio_std = [0.056, 0.052, 0.048, 0.051, 0.047, 0.045, 0.034]
ratio_stg = [0.062, 0.057, 0.052, 0.056, 0.052, 0.048, 0.041]
all_ratio = ratio_std + ratio_stg

coverage_std = [85.1, 84.2, 82.5, 83.8, 81.3, 80.5, 72.1]
coverage_stg = [88.2, 86.1, 84.2, 85.1, 83.7, 81.9, 78.1]
all_coverage = coverage_std + coverage_stg

def generate_replicated_figure_6():
    print("Generating Replicated Figure 6 (PNG Only, 1000 DPI)...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(24, 18))
    
    colors = ['#FF9999']*7 + ['#66CCCC']*7 # Salmon for Standard, Teal for Staged
    x_range = range(len(all_algs))

    # --- Panel (a): Energy Consumption ---
    bars1 = ax1.bar(x_range, all_energy, color=PALETTE_14, edgecolor='black', linewidth=0.8)
    ax1.set_ylabel('Total Energy (Watts)', fontweight='bold')
    ax1.set_title('Energy Consumption Comparison', fontweight='bold', pad=15)
    ax1.set_xticks(x_range)
    ax1.set_xticklabels(all_algs, rotation=90)
    ax1.set_ylim(0, 2400)
    ax1.text(0.5, -0.3, '(a)', transform=ax1.transAxes, size=20, weight='bold', ha='center')
    
    # Legend for Panel A
    ax1.legend(handles=legend_patches, loc='upper left', ncol=2, fontsize=8, 
               title="Algorithms (Std/Staged)", title_fontsize=9)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 20, f'{height:.1f}W', ha='center', va='bottom', fontsize=10, weight='bold')

    # --- Panel (b): Sleep Drone Percentage ---
    bars2 = ax2.bar(x_range, all_sleep, color=PALETTE_14, edgecolor='black', linewidth=0.8)
    ax2.set_ylabel('Sleep Percentage (%)', fontweight='bold')
    ax2.set_title('Sleep Drone Percentage', fontweight='bold', pad=15)
    ax2.set_xticks(x_range)
    ax2.set_xticklabels(all_algs, rotation=90)
    ax2.axhline(y=50, color='red', linestyle='--', linewidth=1.5, label='50% Optimization Target', alpha=0.6)
    ax2.set_ylim(0, 60)
    ax2.text(0.5, -0.3, '(b)', transform=ax2.transAxes, size=20, weight='bold', ha='center')
    ax2.legend(loc='lower left', fontsize=9)
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1, f'{height:.1f}%', ha='center', va='bottom', fontsize=10, weight='bold')

    # --- Panel (c): Efficiency Ratio ---
    bars3 = ax3.bar(x_range, all_ratio, color=PALETTE_14, edgecolor='black', linewidth=0.8)
    ax3.set_ylabel('Efficiency Ratio', fontweight='bold')
    ax3.set_title('Energy Efficiency Ratio (Coverage/Energy)', fontweight='bold', pad=15)
    ax3.set_xticks(x_range)
    ax3.set_xticklabels(all_algs, rotation=90)
    ax3.set_ylim(0, 0.08)
    ax3.text(0.5, -0.3, '(c)', transform=ax3.transAxes, size=20, weight='bold', ha='center')
    
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.001, f'{height:.3f}', ha='center', va='bottom', fontsize=10, weight='bold')

    # --- Panel (d): Trade-off Scatter ---
    ax4.scatter(energy_std, coverage_std, color='#FF9999', s=150, edgecolor='black', label='Standard Algorithms', alpha=0.8)
    ax4.scatter(energy_stg, coverage_stg, color='#66CCCC', s=150, edgecolor='black', label='Staged Algorithms', alpha=1.0)
    
    # Panel (d) Custom Label Strategy to prevent overlapping "circles"
    offsets = {
        'PSO': (10, 10), 'GA': (10, -10), 'SA': (-15, -15), 'ACO': (10, 10), 
        'DE': (10, -10), 'ABC': (10, 5), 'Greedy': (10, 0),
        'PSO_Staged': (-20, 15), 'GA_Staged': (10, 15), 'SA_Staged': (10, -15), 
        'ACO_Staged': (-20, -15), 'DE_Staged': (10, 10), 'ABC_Staged': (-15, 10), 
        'Greedy_Staged': (-25, -15)
    }

    # Label each point with custom offsets to prevent overlap (The user's reported problem)
    for i, txt in enumerate(std_algs):
        off = offsets.get(txt, (7, 7))
        ax4.annotate(txt, (energy_std[i], coverage_std[i]), xytext=off, 
                     textcoords='offset points', fontsize=10, 
                     arrowprops=dict(arrowstyle='-', color='gray', alpha=0.3))
                     
    for i, txt in enumerate(stg_algs):
        off = offsets.get(txt, (-7, -15))
        ax4.annotate(txt, (energy_stg[i], coverage_stg[i]), xytext=off, 
                     textcoords='offset points', fontsize=10, weight='bold',
                     arrowprops=dict(arrowstyle='-', color='gray', alpha=0.3))

    ax4.set_xlabel('Total Energy (Watts)', fontweight='bold')
    ax4.set_ylabel('Coverage (%)', fontweight='bold')
    ax4.set_title('Coverage vs Energy Trade-off', fontweight='bold', pad=15)
    ax4.legend()
    ax4.grid(True, linestyle=':', alpha=0.4)
    ax4.text(0.5, -0.2, '(d)', transform=ax4.transAxes, size=20, weight='bold', ha='center')

    plt.tight_layout()
    
    # Save PNG Only
    png_path = os.path.join(OUTPUT_DIR, "fig_6_FINAL_REPLICATED.png")
    plt.savefig(png_path, dpi=1000, bbox_inches='tight')
    plt.close()
    
    print(f"SUCCESS: Replicated Figure 6 (PNG) saved to:\n  {png_path}")

if __name__ == "__main__":
    generate_replicated_figure_6()
