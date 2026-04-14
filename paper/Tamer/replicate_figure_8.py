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

# 2. Define Algorithms and Colors (Matched to Reference Image)
std_algs = ['PSO', 'GA', 'SA', 'ACO', 'DE', 'ABC', 'Greedy']
stg_algs = [f"{a}_Staged" for a in std_algs]

# Approximated Data points from Reference Image
# (X: Average Drone Count, Y: Average Coverage Efficiency)
drones_std = [14.7, 15.7, 16.7, 15.7, 16.7, 17.7, 21.3]
cov_std = [85.8, 83.9, 82.0, 83.0, 81.0, 80.3, 72.1]

drones_stg = [14.3, 14.7, 15.7, 14.7, 15.7, 16.7, 18.7]
cov_stg = [88.1, 86.1, 84.1, 85.1, 83.2, 82.5, 78.1]

def generate_replicated_figure_8():
    print("Generating Replicated Figure 8 (PNG Only, 1000 DPI)...")
    
    fig, ax = plt.subplots(figsize=(16, 11))
    
    # --- Scatter Plots ---
    ax.scatter(drones_std, cov_std, color='#3498DB', s=150, edgecolor='black', alpha=0.7, label='Standard Algorithms')
    ax.scatter(drones_stg, cov_stg, color='#E67E22', s=150, edgecolor='black', alpha=0.9, label='Staged Algorithms')

    # --- Regression Trend Line ---
    x_trend = np.linspace(min(min(drones_std), min(drones_stg)), max(max(drones_std), max(drones_stg)), 100)
    y_trend = -2.00 * x_trend + 115.0
    ax.plot(x_trend, y_trend, color='red', linestyle='--', linewidth=2.5, label='Trend: y=-2.00x+115.0')
    
    # --- Quadrant Dotted Lines ---
    # These represent the overall mean performance markers
    ax.axhline(y=82.5, color='gray', linestyle=':', linewidth=1.5, label='Mean Baselines')
    ax.axvline(x=16.3, color='gray', linestyle=':', linewidth=1.5)

    # --- Smart Annotation Strategy to Fix Overlaps ---
    # Legend: (x_offset, y_offset)
    offsets = {
        'PSO': (15, -15), 'GA': (15, -15), 'SA': (15, -15), 'ACO': (-25, -25), 
        'DE': (15, -15), 'ABC': (15, 10), 'Greedy': (15, 10),
        'PSO_Staged': (-20, 15), 'GA_Staged': (15, 15), 'SA_Staged': (15, 15), 
        'ACO_Staged': (-35, -10), 'DE_Staged': (-25, -25), 'ABC_Staged': (15, 15), 
        'Greedy_Staged': (15, 15)
    }

    # Label Standard Algorithms
    for i, txt in enumerate(std_algs):
        off = offsets.get(txt, (10, 10))
        ax.annotate(txt, (drones_std[i], cov_std[i]), xytext=off,
                    textcoords='offset points', fontsize=11,
                    arrowprops=dict(arrowstyle='->', color='gray', alpha=0.4))

    # Label Staged Algorithms
    for i, txt in enumerate(stg_algs):
        off = offsets.get(txt, (-10, -10))
        ax.annotate(txt, (drones_stg[i], cov_stg[i]), xytext=off,
                    textcoords='offset points', fontsize=11, weight='bold',
                    arrowprops=dict(arrowstyle='->', color='gray', alpha=0.4))

    # --- Optimality Box ---
    ax.text(13.5, 87.5, "High Coverage\nLow Drones\n(OPTIMAL)", 
            bbox=dict(facecolor='lightgreen', alpha=0.5, boxstyle='round,pad=0.5'),
            fontweight='bold', fontsize=12)

    # --- Styling ---
    ax.set_xlabel('Average Drone Count (Lower is Better)', fontweight='bold')
    ax.set_ylabel('Average Coverage Efficiency (%)', fontweight='bold')
    ax.set_title('Global Performance Trade-off Analysis', fontweight='bold', pad=25)
    ax.grid(True, linestyle='-', alpha=0.15)
    ax.legend(loc='upper right', frameon=True, shadow=True)
    
    ax.set_xlim(min(min(drones_std), min(drones_stg)) - 1, max(max(drones_std), max(drones_stg)) + 1)
    ax.set_ylim(min(min(cov_std), min(cov_stg)) - 1, max(max(cov_std), max(cov_stg)) + 1)

    plt.tight_layout()
    
    # Save PNG Only
    png_path = os.path.join(OUTPUT_DIR, "fig_8_FINAL_REPLICATED.png")
    plt.savefig(png_path, dpi=1000, bbox_inches='tight')
    plt.close()
    
    print(f"SUCCESS: Replicated Figure 8 (PNG) saved to:\n  {png_path}")

if __name__ == "__main__":
    generate_replicated_figure_8()
