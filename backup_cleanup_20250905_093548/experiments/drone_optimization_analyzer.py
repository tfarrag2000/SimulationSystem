#!/usr/bin/env python3
"""
DRONE OPTIMIZATION ANALYZER
Identifies redundant drones and optimizes deployment for minimal overlap
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import ListedColormap
import json
from datetime import datetime
import os

class DroneOptimizationAnalyzer:
    def __init__(self, grid_width=100, grid_height=80):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.drones = []
        self.coverage_threshold = 0.70  # 70% coverage requirement (more realistic)
        
    def add_drone(self, x, y, radius, status='active'):
        """Add a drone to the analysis"""
        self.drones.append({
            'x': x, 'y': y, 'radius': radius, 'status': status, 'id': len(self.drones)
        })
    
    def load_drones_from_image_analysis(self):
        """Load drone positions based on the provided visualization"""
        # Analyzing the attached image, I can see drone positions
        drone_positions = [
            # Active drones (green dots)
            (15, 65), (25, 65), (35, 65), (65, 65), (75, 65), (85, 65),
            (10, 57), (20, 41), (25, 22), (15, 15), (40, 25), (55, 19),
            (70, 36), (75, 15), (85, 20), (45, 39), (35, 57), (50, 55),
            (60, 45), (80, 59), (90, 36), (95, 15),
            # Sleeping drones (red dots with 'z')
            (25, 67), (45, 67), (75, 67), (85, 67)
        ]
        
        # Add drones with estimated coverage radius
        for i, (x, y) in enumerate(drone_positions[:22]):  # Active drones
            self.add_drone(x, y, radius=12, status='active')
        
        for i, (x, y) in enumerate(drone_positions[22:]):  # Sleeping drones
            self.add_drone(x, y, radius=12, status='sleeping')
    
    def calculate_coverage_grid(self, selected_drones=None):
        """Calculate coverage grid for given drones"""
        if selected_drones is None:
            selected_drones = [d for d in self.drones if d['status'] == 'active']
        
        # Create high-resolution grid for accurate coverage calculation
        resolution = 2  # points per unit
        grid_x = np.arange(0, self.grid_width, 1/resolution)
        grid_y = np.arange(0, self.grid_height, 1/resolution)
        coverage_grid = np.zeros((len(grid_y), len(grid_x)))
        
        # Calculate coverage for each point
        for i, y in enumerate(grid_y):
            for j, x in enumerate(grid_x):
                for drone in selected_drones:
                    distance = np.sqrt((x - drone['x'])**2 + (y - drone['y'])**2)
                    if distance <= drone['radius']:
                        coverage_grid[i, j] = 1
                        break
        
        return coverage_grid, grid_x, grid_y
    
    def calculate_overlap_matrix(self):
        """Calculate overlap between all drone pairs"""
        active_drones = [d for d in self.drones if d['status'] == 'active']
        n_drones = len(active_drones)
        overlap_matrix = np.zeros((n_drones, n_drones))
        
        for i in range(n_drones):
            for j in range(i+1, n_drones):
                drone1, drone2 = active_drones[i], active_drones[j]
                distance = np.sqrt((drone1['x'] - drone2['x'])**2 + (drone1['y'] - drone2['y'])**2)
                
                if distance < (drone1['radius'] + drone2['radius']):
                    # Calculate overlap area using circle intersection formula
                    r1, r2 = drone1['radius'], drone2['radius']
                    if distance <= abs(r1 - r2):
                        # One circle completely inside the other
                        overlap_area = np.pi * min(r1, r2)**2
                    else:
                        # Partial overlap
                        alpha1 = 2 * np.arccos((distance**2 + r1**2 - r2**2) / (2 * distance * r1))
                        alpha2 = 2 * np.arccos((distance**2 + r2**2 - r1**2) / (2 * distance * r2))
                        overlap_area = 0.5 * (r1**2 * (alpha1 - np.sin(alpha1)) + 
                                             r2**2 * (alpha2 - np.sin(alpha2)))
                    
                    # Normalize by smaller circle area
                    overlap_ratio = overlap_area / (np.pi * min(r1, r2)**2)
                    overlap_matrix[i, j] = overlap_matrix[j, i] = overlap_ratio
        
        return overlap_matrix, active_drones
    
    def identify_redundant_drones_advanced(self):
        """Advanced redundancy detection based on coverage contribution"""
        active_drones = [d for d in self.drones if d['status'] == 'active']
        redundancy_scores = []
        
        for i, drone in enumerate(active_drones):
            # Calculate coverage with and without this drone
            with_drone = active_drones.copy()
            without_drone = [d for j, d in enumerate(active_drones) if j != i]
            
            coverage_with, _, _ = self.calculate_coverage_grid(with_drone)
            coverage_without, _, _ = self.calculate_coverage_grid(without_drone)
            
            coverage_contribution = np.mean(coverage_with) - np.mean(coverage_without)
            
            # Calculate proximity to other drones
            min_distance = float('inf')
            for j, other_drone in enumerate(active_drones):
                if i != j:
                    distance = np.sqrt((drone['x'] - other_drone['x'])**2 + 
                                     (drone['y'] - other_drone['y'])**2)
                    min_distance = min(min_distance, distance)
            
            # Redundancy score: low contribution + close proximity = high redundancy
            proximity_factor = max(0, (30 - min_distance) / 30)  # Normalize to 0-1
            redundancy_score = proximity_factor - (coverage_contribution * 100)
            
            redundancy_scores.append({
                'drone_id': drone['id'],
                'drone_index': i,
                'position': (drone['x'], drone['y']),
                'coverage_contribution': coverage_contribution * 100,
                'min_distance_to_neighbor': min_distance,
                'redundancy_score': redundancy_score
            })
        
        # Sort by redundancy score (higher = more redundant)
        redundancy_scores.sort(key=lambda x: x['redundancy_score'], reverse=True)
        
        return redundancy_scores
    
    def identify_redundant_drones(self, max_overlap_threshold=0.4):
        """Identify drones that can be removed due to high overlap"""
        overlap_matrix, active_drones = self.calculate_overlap_matrix()
        redundant_candidates = []
        
        # Find drone pairs with high overlap
        n_drones = len(active_drones)
        for i in range(n_drones):
            for j in range(i+1, n_drones):
                if overlap_matrix[i, j] > max_overlap_threshold:
                    redundant_candidates.append({
                        'drone1_id': active_drones[i]['id'],
                        'drone2_id': active_drones[j]['id'],
                        'overlap_ratio': overlap_matrix[i, j],
                        'drone1_pos': (active_drones[i]['x'], active_drones[i]['y']),
                        'drone2_pos': (active_drones[j]['x'], active_drones[j]['y'])
                    })
        
        return redundant_candidates, overlap_matrix
    
    def optimize_drone_deployment(self):
        """Optimize drone deployment by removing redundant drones"""
        print("🔍 ANALYZING DRONE DEPLOYMENT OPTIMIZATION")
        print("=" * 50)
        
        # Calculate initial coverage
        initial_coverage, _, _ = self.calculate_coverage_grid()
        initial_coverage_percent = np.mean(initial_coverage) * 100
        
        print(f"📊 Initial Analysis:")
        print(f"   • Total drones: {len(self.drones)}")
        print(f"   • Active drones: {len([d for d in self.drones if d['status'] == 'active'])}")
        print(f"   • Coverage: {initial_coverage_percent:.1f}%")
        
        # Identify redundant drones using advanced analysis
        redundancy_scores = self.identify_redundant_drones_advanced()
        
        print(f"\n🎯 Redundancy Analysis:")
        print(f"   • Drones analyzed: {len(redundancy_scores)}")
        for i, score in enumerate(redundancy_scores[:5]):  # Show top 5 most redundant
            print(f"   • Drone {score['drone_id']}: Redundancy={score['redundancy_score']:.2f}, "
                  f"Contribution={score['coverage_contribution']:.2f}%, "
                  f"Distance={score['min_distance_to_neighbor']:.1f}")
        
        redundant_candidates, overlap_matrix = self.identify_redundant_drones()
        
        print(f"\n🎯 Overlap Analysis:")
        print(f"   • High overlap pairs found: {len(redundant_candidates)}")
        
        # Try removing drones based on redundancy scores
        active_drones = [d for d in self.drones if d['status'] == 'active']
        optimization_results = []
        
        # Advanced greedy removal approach
        drones_to_remove = set()
        remaining_drones = active_drones.copy()
        
        # Try removing most redundant drones first
        for score_info in redundancy_scores:
            drone_id = score_info['drone_id']
            if drone_id not in drones_to_remove and score_info['redundancy_score'] > 0:
                # Simulate removal
                test_drones = [d for d in remaining_drones if d['id'] != drone_id]
                test_coverage, _, _ = self.calculate_coverage_grid(test_drones)
                test_coverage_percent = np.mean(test_coverage) * 100
                
                if test_coverage_percent >= self.coverage_threshold * 100:
                    drones_to_remove.add(drone_id)
                    remaining_drones = test_drones
                    optimization_results.append({
                        'removed_drone_id': drone_id,
                        'redundancy_score': score_info['redundancy_score'],
                        'coverage_contribution': score_info['coverage_contribution'],
                        'remaining_coverage': test_coverage_percent,
                        'drones_remaining': len(test_drones)
                    })
                    print(f"   ✅ Removed drone {drone_id} (redundancy: {score_info['redundancy_score']:.2f})")
        
        # Also try overlap-based removal
        for candidate in sorted(redundant_candidates, key=lambda x: x['overlap_ratio'], reverse=True):
            drone1_id, drone2_id = candidate['drone1_id'], candidate['drone2_id']
            
            # Check if we can remove one of these drones
            for remove_id in [drone1_id, drone2_id]:
                if remove_id not in drones_to_remove:
                    # Simulate removal
                    test_drones = [d for d in remaining_drones if d['id'] != remove_id]
                    test_coverage, _, _ = self.calculate_coverage_grid(test_drones)
                    test_coverage_percent = np.mean(test_coverage) * 100
                    
                    if test_coverage_percent >= self.coverage_threshold * 100:
                        drones_to_remove.add(remove_id)
                        remaining_drones = test_drones
                        optimization_results.append({
                            'removed_drone_id': remove_id,
                            'overlap_ratio': candidate['overlap_ratio'],
                            'remaining_coverage': test_coverage_percent,
                            'drones_remaining': len(test_drones)
                        })
                        print(f"   ✅ Removed drone {remove_id} (overlap: {candidate['overlap_ratio']:.2f})")
                        break
        
        # Final optimization results
        final_coverage, grid_x, grid_y = self.calculate_coverage_grid(remaining_drones)
        final_coverage_percent = np.mean(final_coverage) * 100
        
        optimization_summary = {
            'initial_drones': len(active_drones),
            'final_drones': len(remaining_drones),
            'drones_removed': len(drones_to_remove),
            'initial_coverage': initial_coverage_percent,
            'final_coverage': final_coverage_percent,
            'efficiency_gain': (len(drones_to_remove) / len(active_drones)) * 100,
            'removed_drone_ids': list(drones_to_remove),
            'optimization_steps': optimization_results
        }
        
        print(f"\n✅ Optimization Results:")
        print(f"   • Drones removed: {len(drones_to_remove)} ({optimization_summary['efficiency_gain']:.1f}% reduction)")
        print(f"   • Final coverage: {final_coverage_percent:.1f}%")
        print(f"   • Coverage maintained: {'✅' if final_coverage_percent >= self.coverage_threshold * 100 else '❌'}")
        
        return optimization_summary, remaining_drones, final_coverage, grid_x, grid_y
    
    def visualize_optimization(self, optimization_summary, optimized_drones, coverage_grid, grid_x, grid_y):
        """Create visualization showing before/after optimization"""
        
        # Create output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"drone_optimization_analysis_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Figure 1: Before and After Comparison
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Before optimization
        ax1.set_xlim(0, self.grid_width)
        ax1.set_ylim(0, self.grid_height)
        ax1.set_aspect('equal')
        ax1.set_title('Before Optimization\n(Original Deployment)', fontsize=14, fontweight='bold')
        
        # Draw coverage areas and drones
        for drone in self.drones:
            if drone['status'] == 'active':
                circle = patches.Circle((drone['x'], drone['y']), drone['radius'], 
                                      alpha=0.3, facecolor='green', edgecolor='darkgreen')
                ax1.add_patch(circle)
                ax1.plot(drone['x'], drone['y'], 'o', color='darkgreen', markersize=8, label='Active Drone' if drone['id'] == 0 else "")
            elif drone['status'] == 'sleeping':
                ax1.plot(drone['x'], drone['y'], 'o', color='red', markersize=8, label='Sleeping Drone' if drone['id'] == len([d for d in self.drones if d['status'] == 'active']) else "")
                ax1.text(drone['x']+1, drone['y']+1, 'z', fontsize=8, color='red', fontweight='bold')
        
        ax1.set_xlabel('X Coordinate (units)')
        ax1.set_ylabel('Y Coordinate (units)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # After optimization
        ax2.set_xlim(0, self.grid_width)
        ax2.set_ylim(0, self.grid_height)
        ax2.set_aspect('equal')
        ax2.set_title('After Optimization\n(Redundant Drones Removed)', fontsize=14, fontweight='bold')
        
        # Draw optimized deployment
        removed_ids = set(optimization_summary['removed_drone_ids'])
        
        for drone in self.drones:
            if drone['status'] == 'active':
                if drone['id'] in removed_ids:
                    # Removed drone - show as faded
                    circle = patches.Circle((drone['x'], drone['y']), drone['radius'], 
                                          alpha=0.1, facecolor='gray', edgecolor='gray', linestyle='--')
                    ax2.add_patch(circle)
                    ax2.plot(drone['x'], drone['y'], 'x', color='red', markersize=10, label='Removed Drone' if len([d for d in self.drones[:drone['id']] if d['id'] in removed_ids]) == 0 else "")
                else:
                    # Remaining active drone
                    circle = patches.Circle((drone['x'], drone['y']), drone['radius'], 
                                          alpha=0.3, facecolor='green', edgecolor='darkgreen')
                    ax2.add_patch(circle)
                    ax2.plot(drone['x'], drone['y'], 'o', color='darkgreen', markersize=8, label='Active Drone' if len([d for d in self.drones[:drone['id']] if d['status'] == 'active' and d['id'] not in removed_ids]) == 0 else "")
            elif drone['status'] == 'sleeping':
                ax2.plot(drone['x'], drone['y'], 'o', color='red', markersize=8, label='Sleeping Drone' if len([d for d in self.drones[:drone['id']] if d['status'] == 'sleeping']) == 0 else "")
                ax2.text(drone['x']+1, drone['y']+1, 'z', fontsize=8, color='red', fontweight='bold')
        
        ax2.set_xlabel('X Coordinate (units)')
        ax2.set_ylabel('Y Coordinate (units)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/drone_optimization_comparison.png", dpi=300, bbox_inches='tight')
        plt.show()
        
        # Figure 2: Coverage Analysis
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        
        # Show coverage grid
        coverage_display = ax.imshow(coverage_grid, extent=[0, self.grid_width, 0, self.grid_height], 
                                   origin='lower', alpha=0.6, cmap='RdYlGn')
        
        # Draw optimized drones
        for drone in optimized_drones:
            circle = patches.Circle((drone['x'], drone['y']), drone['radius'], 
                                  alpha=0.3, facecolor='none', edgecolor='blue', linewidth=2)
            ax.add_patch(circle)
            ax.plot(drone['x'], drone['y'], 'o', color='blue', markersize=10)
        
        ax.set_xlim(0, self.grid_width)
        ax.set_ylim(0, self.grid_height)
        ax.set_title(f'Optimized Coverage Analysis\n{len(optimized_drones)} Drones - {optimization_summary["final_coverage"]:.1f}% Coverage', 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('X Coordinate (units)')
        ax.set_ylabel('Y Coordinate (units)')
        ax.grid(True, alpha=0.3)
        
        # Add colorbar
        cbar = plt.colorbar(coverage_display, ax=ax)
        cbar.set_label('Coverage Intensity', rotation=270, labelpad=20)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/optimized_coverage_analysis.png", dpi=300, bbox_inches='tight')
        plt.show()
        
        # Save optimization report
        with open(f"{output_dir}/optimization_report.json", 'w') as f:
            json.dump(optimization_summary, f, indent=2)
        
        print(f"\n📁 Analysis saved to: {output_dir}/")
        return output_dir

def main():
    """Run drone optimization analysis"""
    print("🚁 DRONE DEPLOYMENT OPTIMIZATION ANALYZER")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = DroneOptimizationAnalyzer(grid_width=100, grid_height=80)
    
    # Load drone positions from image analysis
    analyzer.load_drones_from_image_analysis()
    
    # Run optimization analysis
    optimization_summary, optimized_drones, coverage_grid, grid_x, grid_y = analyzer.optimize_drone_deployment()
    
    # Create visualizations
    output_dir = analyzer.visualize_optimization(optimization_summary, optimized_drones, coverage_grid, grid_x, grid_y)
    
    print("\n🎯 OPTIMIZATION SUMMARY:")
    print("=" * 40)
    print(f"Initial drones: {optimization_summary['initial_drones']}")
    print(f"Optimized drones: {optimization_summary['final_drones']}")
    print(f"Drones removed: {optimization_summary['drones_removed']}")
    print(f"Efficiency gain: {optimization_summary['efficiency_gain']:.1f}%")
    print(f"Coverage maintained: {optimization_summary['final_coverage']:.1f}%")
    print(f"Removed drone IDs: {optimization_summary['removed_drone_ids']}")
    
    return optimization_summary, output_dir

if __name__ == "__main__":
    main()
