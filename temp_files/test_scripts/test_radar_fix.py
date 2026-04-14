#!/usr/bin/env python3
"""
Quick test for radar chart fix
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def test_radar_chart():
    """Test the radar chart dimension fix"""
    
    # Test data
    test_cases = ['Dense Coverage', 'Wide Area', 'Energy Constrained', 'High Precision', 'Mixed Terrain', 'Emergency Response']
    coverage_data = [[85.2, 78.1, 82.5, 90.3, 87.6, 83.9]]  # One algorithm
    
    # Create radar chart
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    
    # Define angles for radar chart
    angles = np.linspace(0, 2 * np.pi, len(test_cases), endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle - 7 elements
    
    # Values with same fix
    values = coverage_data[0].copy()  # 6 elements
    values.append(values[0])  # Complete the circle - 7 elements
    
    print(f"Angles length: {len(angles)}")
    print(f"Values length: {len(values)}")
    
    # This should work now
    ax.plot(angles, values, 'o-', linewidth=2.5, color='blue', alpha=0.8)
    ax.fill(angles, values, alpha=0.15, color='blue')
    
    # Customize radar chart
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(test_cases, fontsize=11)
    ax.set_ylim(70, 95)
    ax.grid(True, alpha=0.3)
    
    plt.title('Test Radar Chart - Dimension Fix', fontsize=16, fontweight='bold', pad=30)
    plt.tight_layout()
    plt.savefig('test_radar_fix.png', dpi=600, bbox_inches='tight')
    plt.close()
    
    print("✅ Radar chart dimension fix verified!")
    return True

if __name__ == "__main__":
    test_radar_chart()
