#!/usr/bin/env python3
"""
DRONE REPOSITIONING OPTIMIZER
Improves coverage by repositioning drones rather than removing them
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import ListedColormap
import json
from datetime import datetime
import os
from scipy.optimize import differential_evolution

class DroneRepositioningOptimizer:
    def __init__(self, grid_width=100, grid_height=80):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.drones = []
        self.target_coverage = 0.95  # Target 95% coverage
        
    def add_drone(self, x, y, radius, status='active'):
        """Add a drone to the optimization"""
        self.drones.append({
            'x': x, 'y': y, 'radius': radius, 'status': status, 'id': len(self.drones)
        })
    
    def load_current_deployment(self):
        """Load current drone positions from image analysis"""
        # Current positions from the visualization
        drone_positions = [
            # Active drones (green dots)
            (15, 65), (25, 65), (35, 65), (65, 65), (75, 65), (85, 65),
            (10, 57), (20, 41), (25, 22), (15, 15), (40, 25), (55, 19),
            (70, 36), (75, 15), (85, 20), (45, 39), (35, 57), (50, 55),
            (60, 45), (80, 59), (90, 36), (95, 15),
            # Sleeping drones (red dots) - will be repositioned
            (25, 67), (45, 67), (75, 67), (85, 67)
        ]
        
        # Add active drones
        for i, (x, y) in enumerate(drone_positions[:22]):
            self.add_drone(x, y, radius=12, status='active')
        
        # Add sleeping drones that can be repositioned
        for i, (x, y) in enumerate(drone_positions[22:]):
            self.add_drone(x, y, radius=12, status='repositionable')
    
    def calculate_coverage_score(self, positions=None):
        """Calculate coverage score for given drone positions"""
        if positions is None:
            active_drones = [d for d in self.drones if d['status'] == 'active']
            repositionable_drones = [d for d in self.drones if d['status'] == 'repositionable']
        else:
            # Use provided positions for repositionable drones
            active_drones = [d for d in self.drones if d['status'] == 'active']
            repositionable_drones = []
            
            # Create new positions for repositionable drones
            pos_idx = 0
            for d in self.drones:
                if d['status'] == 'repositionable':
                    new_drone = d.copy()
                    new_drone['x'] = positions[pos_idx * 2]
                    new_drone['y'] = positions[pos_idx * 2 + 1]
                    repositionable_drones.append(new_drone)
                    pos_idx += 1
        
        all_drones = active_drones + repositionable_drones
        
        # Calculate coverage on a grid
        resolution = 1
        grid_x = np.arange(0, self.grid_width, resolution)
        grid_y = np.arange(0, self.grid_height, resolution)
        coverage_points = 0
        total_points = len(grid_x) * len(grid_y)
        
        for x in grid_x:
            for y in grid_y:
                covered = False
                for drone in all_drones:
                    distance = np.sqrt((x - drone['x'])**2 + (y - drone['y'])**2)
                    if distance <= drone['radius']:
                        covered = True
                        break
                if covered:
                    coverage_points += 1
        
        coverage_ratio = coverage_points / total_points
        
        # Add penalty for drones going outside bounds
        bounds_penalty = 0
        for drone in repositionable_drones:
            if drone['x'] < 0 or drone['x'] > self.grid_width:
                bounds_penalty += 100
            if drone['y'] < 0 or drone['y'] > self.grid_height:
                bounds_penalty += 100
        
        # Add penalty for drones being too close to each other
        collision_penalty = 0
        for i, drone1 in enumerate(all_drones):
            for j, drone2 in enumerate(all_drones[i+1:], i+1):
                distance = np.sqrt((drone1['x'] - drone2['x'])**2 + (drone1['y'] - drone2['y'])**2)
                if distance < 5:  # Minimum separation
                    collision_penalty += (5 - distance) * 10
        
        # Objective: maximize coverage, minimize penalties
        score = coverage_ratio - (bounds_penalty + collision_penalty) / 1000
        return score
    
    def objective_function(self, positions):
        """Objective function for optimization (to be minimized)"""
        coverage_score = self.calculate_coverage_score(positions)
        return -coverage_score  # Negative because we want to maximize coverage
    
    def optimize_repositioning(self):
        """Optimize drone positions using differential evolution"""
        print("🎯 DRONE REPOSITIONING OPTIMIZATION")
        print("=" * 50)
        
        # Calculate initial coverage
        initial_coverage = self.calculate_coverage_score()
        repositionable_count = len([d for d in self.drones if d['status'] == 'repositionable'])
        
        print(f"📊 Initial Analysis:")
        print(f"   • Total drones: {len(self.drones)}")
        print(f"   • Active drones: {len([d for d in self.drones if d['status'] == 'active'])}")
        print(f"   • Repositionable drones: {repositionable_count}")
        print(f"   • Initial coverage: {initial_coverage * 100:.1f}%")
        
        if repositionable_count == 0:
            print("❌ No repositionable drones found!")
            return None
        
        # Set up optimization bounds (x, y for each repositionable drone)
        bounds = []
        for _ in range(repositionable_count):
            bounds.extend([(0, self.grid_width), (0, self.grid_height)])  # x, y bounds
        
        print(f"\n🔄 Optimizing positions...")
        
        # Run differential evolution optimization
        result = differential_evolution(
            self.objective_function,
            bounds,
            maxiter=100,
            popsize=15,
            seed=42,
            atol=1e-4,
            tol=1e-4
        )
        
        # Calculate final coverage with optimized positions
        final_coverage = self.calculate_coverage_score(result.x)
        
        # Create optimized drone configuration
        optimized_drones = [d for d in self.drones if d['status'] == 'active']
        pos_idx = 0
        for d in self.drones:
            if d['status'] == 'repositionable':
                optimized_drone = d.copy()
                optimized_drone['x'] = result.x[pos_idx * 2]
                optimized_drone['y'] = result.x[pos_idx * 2 + 1]
                optimized_drone['status'] = 'repositioned'
                optimized_drones.append(optimized_drone)
                pos_idx += 1
        
        optimization_summary = {
            'initial_coverage': initial_coverage * 100,
            'final_coverage': final_coverage * 100,
            'coverage_improvement': (final_coverage - initial_coverage) * 100,
            'total_drones': len(self.drones),
            'repositioned_count': repositionable_count,
            'optimization_success': result.success,
            'optimization_iterations': result.nit,
            'repositioned_positions': []
        }
        
        # Record new positions
        pos_idx = 0
        for d in self.drones:
            if d['status'] == 'repositionable':
                optimization_summary['repositioned_positions'].append({
                    'drone_id': d['id'],
                    'original_position': (d['x'], d['y']),
                    'new_position': (result.x[pos_idx * 2], result.x[pos_idx * 2 + 1]),
                    'movement_distance': np.sqrt(
                        (result.x[pos_idx * 2] - d['x'])**2 + 
                        (result.x[pos_idx * 2 + 1] - d['y'])**2
                    )
                })
                pos_idx += 1
        
        print(f"\n✅ Optimization Results:")
        print(f"   • Coverage improvement: {optimization_summary['coverage_improvement']:.2f}%")
        print(f"   • Final coverage: {final_coverage * 100:.1f}%")
        print(f"   • Optimization successful: {'✅' if result.success else '❌'}")
        print(f"   • Iterations: {result.nit}")
        
        print(f"\n📍 Repositioning Details:")
        for pos_info in optimization_summary['repositioned_positions']:
            orig_x, orig_y = pos_info['original_position']
            new_x, new_y = pos_info['new_position']
            distance = pos_info['movement_distance']
            print(f"   • Drone {pos_info['drone_id']}: ({orig_x:.0f},{orig_y:.0f}) → ({new_x:.1f},{new_y:.1f}) [moved {distance:.1f} units]")
        
        return optimization_summary, optimized_drones
    
    def visualize_repositioning(self, optimization_summary, optimized_drones):
        """Create visualization showing before/after repositioning"""
        
        # Create output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"drone_repositioning_analysis_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Figure 1: Before and After Comparison
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
        
        # Before repositioning
        ax1.set_xlim(0, self.grid_width)
        ax1.set_ylim(0, self.grid_height)
        ax1.set_aspect('equal')
        ax1.set_title(f'Before Repositioning\nCoverage: {optimization_summary["initial_coverage"]:.1f}%', 
                     fontsize=14, fontweight='bold')
        
        # Draw original deployment
        for drone in self.drones:
            if drone['status'] == 'active':
                circle = patches.Circle((drone['x'], drone['y']), drone['radius'], 
                                      alpha=0.3, facecolor='green', edgecolor='darkgreen')
                ax1.add_patch(circle)
                ax1.plot(drone['x'], drone['y'], 'o', color='darkgreen', markersize=8)
            elif drone['status'] == 'repositionable':
                circle = patches.Circle((drone['x'], drone['y']), drone['radius'], 
                                      alpha=0.2, facecolor='red', edgecolor='red')
                ax1.add_patch(circle)
                ax1.plot(drone['x'], drone['y'], 'o', color='red', markersize=8)
                ax1.text(drone['x']+1, drone['y']+1, 'z', fontsize=8, color='red', fontweight='bold')
        
        ax1.set_xlabel('X Coordinate (units)')
        ax1.set_ylabel('Y Coordinate (units)')
        ax1.grid(True, alpha=0.3)
        
        # After repositioning
        ax2.set_xlim(0, self.grid_width)
        ax2.set_ylim(0, self.grid_height)
        ax2.set_aspect('equal')
        ax2.set_title(f'After Repositioning\nCoverage: {optimization_summary["final_coverage"]:.1f}% (+{optimization_summary["coverage_improvement"]:.1f}%)', 
                     fontsize=14, fontweight='bold')
        
        # Draw optimized deployment
        for drone in optimized_drones:
            if drone['status'] == 'active':
                circle = patches.Circle((drone['x'], drone['y']), drone['radius'], 
                                      alpha=0.3, facecolor='green', edgecolor='darkgreen')
                ax2.add_patch(circle)
                ax2.plot(drone['x'], drone['y'], 'o', color='darkgreen', markersize=8)
            elif drone['status'] == 'repositioned':
                circle = patches.Circle((drone['x'], drone['y']), drone['radius'], 
                                      alpha=0.3, facecolor='blue', edgecolor='darkblue')
                ax2.add_patch(circle)
                ax2.plot(drone['x'], drone['y'], 'o', color='darkblue', markersize=8)
        
        # Draw movement arrows
        for pos_info in optimization_summary['repositioned_positions']:
            orig_x, orig_y = pos_info['original_position']
            new_x, new_y = pos_info['new_position']
            ax2.annotate('', xy=(new_x, new_y), xytext=(orig_x, orig_y),
                        arrowprops=dict(arrowstyle='->', color='orange', lw=2, alpha=0.7))
        
        ax2.set_xlabel('X Coordinate (units)')
        ax2.set_ylabel('Y Coordinate (units)')
        ax2.grid(True, alpha=0.3)
        
        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='darkgreen', markersize=10, label='Active Drones'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='darkblue', markersize=10, label='Repositioned Drones'),
            plt.Line2D([0], [0], color='orange', lw=2, label='Movement Path')
        ]
        ax2.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/drone_repositioning_comparison.png", dpi=300, bbox_inches='tight')
        plt.show()
        
        # Figure 2: Coverage Heat Map
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        
        # Calculate coverage grid for visualization
        resolution = 2
        grid_x = np.arange(0, self.grid_width, resolution)
        grid_y = np.arange(0, self.grid_height, resolution)
        coverage_grid = np.zeros((len(grid_y), len(grid_x)))
        
        for i, y in enumerate(grid_y):
            for j, x in enumerate(grid_x):
                for drone in optimized_drones:
                    distance = np.sqrt((x - drone['x'])**2 + (y - drone['y'])**2)
                    if distance <= drone['radius']:
                        coverage_grid[i, j] = 1
                        break
        
        # Display coverage
        coverage_display = ax.imshow(coverage_grid, extent=[0, self.grid_width, 0, self.grid_height], 
                                   origin='lower', alpha=0.8, cmap='RdYlGn')
        
        # Draw optimized drones
        for drone in optimized_drones:
            if drone['status'] == 'active':
                circle = patches.Circle((drone['x'], drone['y']), drone['radius'], 
                                      alpha=0.2, facecolor='none', edgecolor='darkgreen', linewidth=2)
                ax.add_patch(circle)
                ax.plot(drone['x'], drone['y'], 'o', color='darkgreen', markersize=10)
            elif drone['status'] == 'repositioned':
                circle = patches.Circle((drone['x'], drone['y']), drone['radius'], 
                                      alpha=0.2, facecolor='none', edgecolor='darkblue', linewidth=2)
                ax.add_patch(circle)
                ax.plot(drone['x'], drone['y'], 'o', color='darkblue', markersize=10)
        
        ax.set_xlim(0, self.grid_width)
        ax.set_ylim(0, self.grid_height)
        ax.set_title(f'Optimized Coverage Map\nFinal Coverage: {optimization_summary["final_coverage"]:.1f}% (Improvement: +{optimization_summary["coverage_improvement"]:.1f}%)', 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('X Coordinate (units)')
        ax.set_ylabel('Y Coordinate (units)')
        ax.grid(True, alpha=0.3)
        
        # Add colorbar
        cbar = plt.colorbar(coverage_display, ax=ax)
        cbar.set_label('Coverage Status', rotation=270, labelpad=20)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/optimized_coverage_heatmap.png", dpi=300, bbox_inches='tight')
        plt.show()
        
        # Save optimization report
        with open(f"{output_dir}/repositioning_report.json", 'w') as f:
            json.dump(optimization_summary, f, indent=2)
        
        print(f"\n📁 Analysis saved to: {output_dir}/")
        return output_dir

def main():
    """Run drone repositioning optimization"""
    print("🚁 DRONE REPOSITIONING OPTIMIZATION")
    print("=" * 60)
    
    # Initialize optimizer
    optimizer = DroneRepositioningOptimizer(grid_width=100, grid_height=80)
    
    # Load current deployment
    optimizer.load_current_deployment()
    
    # Run repositioning optimization
    result = optimizer.optimize_repositioning()
    
    if result is not None:
        optimization_summary, optimized_drones = result
        
        # Create visualizations
        output_dir = optimizer.visualize_repositioning(optimization_summary, optimized_drones)
        
        print("\n🎯 REPOSITIONING SUMMARY:")
        print("=" * 40)
        print(f"Initial coverage: {optimization_summary['initial_coverage']:.1f}%")
        print(f"Final coverage: {optimization_summary['final_coverage']:.1f}%")
        print(f"Coverage improvement: +{optimization_summary['coverage_improvement']:.1f}%")
        print(f"Drones repositioned: {optimization_summary['repositioned_count']}")
        print(f"Total drones: {optimization_summary['total_drones']}")
        
        print(f"\n💡 BENEFITS OF REPOSITIONING:")
        print("   • Maintains all drones in operation")
        print("   • Improves coverage without adding hardware")
        print("   • Optimizes spatial distribution")
        print("   • Reduces coverage gaps")
        print("   • Better resource utilization")
        
        return optimization_summary, output_dir
    else:
        print("❌ Optimization failed")
        return None, None

if __name__ == "__main__":
    main()
