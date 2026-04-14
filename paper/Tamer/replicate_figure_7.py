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
    'font.size': 12,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 10,
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'figure.dpi': 1000
})

# 2. Define Algorithms and Colors (Matched to Reference Image)
std_algs = ['PSO', 'GA', 'SA', 'ACO', 'DE', 'ABC', 'Greedy']
stg_algs = [f"{a}_Staged" for a in std_algs]
all_algs = std_algs + stg_algs

# Paired Colors
PALETTE = [
    '#3498DB', # Blue (PSO)
    '#A9CCE3', # Light Blue (GA)
    '#F39C12', # Orange (SA)
    '#27AE60', # Green (ACO)
    '#E74C3C', # Red (DE)
    '#F5B7B1', # Pink (ABC)
    '#8E44AD', # Purple (Greedy)
]

def generate_replicated_figure_7():
    print("Generating Replicated Figure 7 (1000 DPI)...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 10))
    
    # --- Panel A: Convergence Curves ---
    iterations = np.arange(0, 101, 5)
    np.random.seed(42) # Pinned for scientific consistency
    
    # Data Simulation logic matching the reference curves
    # Staged algorithms (Solid) reach ~89-93%
    # Standard algorithms (Dashed) reach ~75-86%
    
    for i in range(len(std_algs)):
        color = PALETTE[i]
        
        # Standard Version (Simulated Trajectory)
        std_final = 82 + i if i < 6 else 78  # Greedy is lower
        std_rate = 0.06 if i < 6 else 0.08
        std_curve = std_final * (1 - np.exp(-std_rate * (iterations + 10))) + np.random.normal(0, 0.3, len(iterations))
        
        # Staged Version (Simulated Trajectory)
        stg_final = 91 + (i % 2)
        stg_rate = 0.11
        stg_curve = stg_final * (1 - np.exp(-stg_rate * (iterations + 10))) + np.random.normal(0, 0.3, len(iterations))

        ax1.plot(iterations, std_curve, linestyle='--', color=color, linewidth=1.8, alpha=0.7, label=std_algs[i])
        ax1.plot(iterations, stg_curve, linestyle='-', color=color, linewidth=2.8, alpha=0.9, label=stg_algs[i])

    ax1.set_xlabel('Iterations', fontweight='bold')
    ax1.set_ylabel('Coverage Efficiency (%)', fontweight='bold')
    ax1.set_title('Algorithm Convergence Analysis', fontweight='bold', pad=15)
    ax1.set_ylim(65, 95)
    ax1.grid(True, linestyle=':', alpha=0.6)
    
    # Legend placement between plots (as per reference)
    ax1.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), ncol=1, frameon=True, fancybox=True, shadow=True)

    # --- Panel B: Early Convergence Rate ---
    # Values extracted from reference image (approximated)
    rates = [3.3, 2.7, 3.0, 3.2, 3.4, 2.65, 3.72, 4.0, 3.8, 3.97, 3.98, 4.1, 3.98, 3.8] # Approximated heights
    labels = all_algs
    
    # Use paired colors for bars
    bar_colors = PALETTE + PALETTE
    
    bars = ax2.bar(range(len(labels)), rates, color=bar_colors, alpha=0.85, edgecolor='black', linewidth=0.8)
    
    # Match the "Staged" opacity from reference
    for i in range(7, 14):
        bars[i].set_alpha(1.0)
        bars[i].set_linewidth(1.2)

    ax2.set_ylabel('Convergence Rate (%/iteration)', fontweight='bold')
    ax2.set_xlabel('Optimization Algorithms', fontweight='bold')
    ax2.set_title('Early Convergence Rate Comparison', fontweight='bold', pad=15)
    ax2.set_xticks(range(len(labels)))
    
    # ENHANCEMENT: 90 Degree Rotation (Reviewer Correction)
    ax2.set_xticklabels(labels, rotation=90, ha='center') 
    
    ax2.set_ylim(0, 4.5)
    ax2.grid(axis='y', linestyle=':', alpha=0.5)

    plt.tight_layout()
    
    # Save Outputs
    png_path = os.path.join(OUTPUT_DIR, "fig_7_FINAL_REPLICATED.png")
    eps_path = os.path.join(OUTPUT_DIR, "fig_7_FINAL_REPLICATED.eps")
    
    plt.savefig(png_path, dpi=1000, bbox_inches='tight')
    plt.savefig(eps_path, bbox_inches='tight')
    plt.close()
    
    print(f"SUCCESS: Replicated Figure 7 saved to:\n  {png_path}\n  {eps_path}")

if __name__ == "__main__":
    generate_replicated_figure_7()
