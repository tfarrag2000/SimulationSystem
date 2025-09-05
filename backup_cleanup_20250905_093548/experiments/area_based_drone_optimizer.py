#!/usr/bin/env python3
"""
AREA-BASED DRONE OPTIMIZATION
True area coverage optimization using geometric calculations
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import ListedColormap
import json
from datetime import datetime
import os
from scipy.optimize import differential_evolution
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
import warnings
warnings.filterwarnings('ignore')

class AreaBasedDroneOptimizer:
    def __init__(self, grid_width=100, grid_height=80):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.total_area = grid_width * grid_height
        self.drones = []
        self.target_coverage = 0.90  # Target 90% area coverage
        
    def add_drone(self, x, y, radius, status='active'):
        """Add a drone to the optimization"""
        self.drones.append({
            'x': x, 'y': y, 'radius': radius, 'status': status, 'id': len(self.drones)
        })
    
    def load_current_deployment(self):
        """Load current drone positions"""
        # Current positions from the visualization
        drone_positions = [
            # Active drones (green dots)
            (15, 65), (25, 65), (35, 65), (65, 65), (75, 65), (85, 65),
            (10, 57), (20, 41), (25, 22), (15, 15), (40, 25), (55, 19),
            (70, 36), (75, 15), (85, 20), (45, 39), (35, 57), (50, 55),
            (60, 45), (80, 59), (90, 36), (95, 15),
            # Sleeping drones (red dots) - can be repositioned
            (25, 67), (45, 67), (75, 67), (85, 67)
        ]
        
        # Add active drones
        for i, (x, y) in enumerate(drone_positions[:22]):
            self.add_drone(x, y, radius=12, status='active')
        
        # Add sleeping drones that can be repositioned
        for i, (x, y) in enumerate(drone_positions[22:]):
            self.add_drone(x, y, radius=12, status='repositionable')
    
    def calculate_actual_area_coverage(self, selected_drones=None):
        """Calculate actual area coverage using geometric intersection"""
        if selected_drones is None:
            selected_drones = [d for d in self.drones if d['status'] in ['active', 'repositioned']]
        
        if not selected_drones:
            return 0.0
        
        # Create area boundary
        area_boundary = Polygon([(0, 0), (self.grid_width, 0), 
                                (self.grid_width, self.grid_height), (0, self.grid_height)])
        
        # Create circles for each drone and find intersection with area
        coverage_circles = []
        for drone in selected_drones:
            # Create circle
            circle_center = Point(drone['x'], drone['y'])
            circle = circle_center.buffer(drone['radius'])
            
            # Intersect with area boundary
            intersection = circle.intersection(area_boundary)
            if intersection.area > 0:
                coverage_circles.append(intersection)
        
        if not coverage_circles:
            return 0.0
        
        # Calculate union of all coverage areas
        try:
            total_coverage = unary_union(coverage_circles)
            covered_area = total_coverage.area
            coverage_ratio = covered_area / self.total_area
            return coverage_ratio
        except Exception as e:
            print(f"Error in geometric calculation: {e}")
            # Fallback to grid-based calculation
            return self._fallback_grid_coverage(selected_drones)
    
    def _fallback_grid_coverage(self, selected_drones, resolution=100):
        """Fallback high-resolution grid-based coverage calculation"""
        grid_x = np.linspace(0, self.grid_width, resolution)
        grid_y = np.linspace(0, self.grid_height, resolution)
        covered_points = 0
        total_points = resolution * resolution
        
        for x in grid_x:
            for y in grid_y:
                for drone in selected_drones:
                    distance = np.sqrt((x - drone['x'])**2 + (y - drone['y'])**2)
                    if distance <= drone['radius']:
                        covered_points += 1
                        break
        
        return covered_points / total_points
    
    def calculate_overlap_area(self, selected_drones=None):
        """Calculate total overlap area between drones"""
        if selected_drones is None:
            selected_drones = [d for d in self.drones if d['status'] in ['active', 'repositioned']]
        
        if len(selected_drones) <= 1:
            return 0.0
        
        total_overlap = 0.0
        
        for i in range(len(selected_drones)):
            for j in range(i + 1, len(selected_drones)):
                drone1, drone2 = selected_drones[i], selected_drones[j]
                
                # Calculate distance between centers
                distance = np.sqrt((drone1['x'] - drone2['x'])**2 + (drone1['y'] - drone2['y'])**2)
                
                # Check if circles overlap
                if distance < (drone1['radius'] + drone2['radius']):
                    r1, r2 = drone1['radius'], drone2['radius']
                    
                    if distance <= abs(r1 - r2):
                        # One circle completely inside the other
                        overlap_area = np.pi * min(r1, r2)**2
                    else:
                        # Partial overlap - use lens area formula
                        alpha1 = 2 * np.arccos((distance**2 + r1**2 - r2**2) / (2 * distance * r1))
                        alpha2 = 2 * np.arccos((distance**2 + r2**2 - r1**2) / (2 * distance * r2))
                        overlap_area = 0.5 * (r1**2 * (alpha1 - np.sin(alpha1)) + 
                                             r2**2 * (alpha2 - np.sin(alpha2)))
                    
                    total_overlap += overlap_area
        
        return total_overlap
    
    def identify_redundant_drones_by_area(self):
        """Identify redundant drones based on actual area contribution"""
        active_drones = [d for d in self.drones if d['status'] == 'active']
        redundancy_analysis = []
        
        # Calculate current total coverage
        current_coverage = self.calculate_actual_area_coverage(active_drones)
        
        for i, drone in enumerate(active_drones):
            # Calculate coverage without this specific drone
            remaining_drones = [d for j, d in enumerate(active_drones) if j != i]
            coverage_without = self.calculate_actual_area_coverage(remaining_drones)
            
            # Calculate this drone's unique contribution
            area_contribution = current_coverage - coverage_without
            area_contribution_pct = (area_contribution * self.total_area)
            
            # Calculate overlap this drone creates
            drone_circle_area = np.pi * drone['radius']**2
            overlap_ratio = max(0, (drone_circle_area - area_contribution_pct) / drone_circle_area)
            
            redundancy_analysis.append({
                'drone_id': drone['id'],
                'position': (drone['x'], drone['y']),
                'area_contribution': area_contribution_pct,
                'coverage_contribution_pct': area_contribution * 100,
                'overlap_ratio': overlap_ratio,
                'efficiency_score': area_contribution_pct / drone_circle_area,
                'redundancy_score': overlap_ratio - (area_contribution * 5)  # Higher = more redundant
            })
        
        # Sort by redundancy score (higher = more redundant)
        redundancy_analysis.sort(key=lambda x: x['redundancy_score'], reverse=True)
        
        return redundancy_analysis
    
    def optimize_drone_removal_by_area(self):
        """Remove redundant drones based on area coverage analysis"""
        print("🔍 AREA-BASED DRONE REMOVAL ANALYSIS")
        print("=" * 50)
        
        # Get initial coverage
        initial_drones = [d for d in self.drones if d['status'] == 'active']
        initial_coverage = self.calculate_actual_area_coverage(initial_drones)
        initial_area = initial_coverage * self.total_area
        
        print(f"📊 Initial Analysis:")
        print(f"   • Total drones: {len(initial_drones)}")
        print(f"   • Coverage area: {initial_area:.1f} sq units ({initial_coverage*100:.1f}%)")
        print(f"   • Total area: {self.total_area:.1f} sq units")
        
        # Identify redundant drones
        redundancy_analysis = self.identify_redundant_drones_by_area()
        
        print(f"\n🎯 Area Redundancy Analysis:")
        for i, analysis in enumerate(redundancy_analysis[:5]):  # Show top 5 most redundant
            print(f"   • Drone {analysis['drone_id']}: "
                  f"Contributes {analysis['area_contribution']:.1f} sq units "
                  f"({analysis['coverage_contribution_pct']:.2f}%), "
                  f"Overlap: {analysis['overlap_ratio']:.2f}, "
                  f"Efficiency: {analysis['efficiency_score']:.3f}")
        
        # Try removing most redundant drones
        remaining_drones = initial_drones.copy()
        removed_drones = []
        removal_log = []
        
        for analysis in redundancy_analysis:
            if analysis['redundancy_score'] > 0:  # Only remove if truly redundant
                drone_id = analysis['drone_id']
                
                # Simulate removal
                test_drones = [d for d in remaining_drones if d['id'] != drone_id]
                test_coverage = self.calculate_actual_area_coverage(test_drones)
                
                if test_coverage >= self.target_coverage:
                    # Safe to remove
                    remaining_drones = test_drones
                    removed_drones.append(drone_id)
                    removal_log.append({
                        'drone_id': drone_id,
                        'area_contribution': analysis['area_contribution'],
                        'remaining_coverage': test_coverage * 100,
                        'remaining_drones': len(test_drones)
                    })
                    print(f"   ✅ Removed drone {drone_id} (contributed {analysis['area_contribution']:.1f} sq units)")
        
        # Final results
        final_coverage = self.calculate_actual_area_coverage(remaining_drones)
        final_area = final_coverage * self.total_area
        
        removal_summary = {
            'initial_drones': len(initial_drones),
            'final_drones': len(remaining_drones),
            'drones_removed': len(removed_drones),
            'initial_coverage_pct': initial_coverage * 100,
            'final_coverage_pct': final_coverage * 100,
            'initial_area': initial_area,
            'final_area': final_area,
            'area_lost': initial_area - final_area,
            'efficiency_gain': (len(removed_drones) / len(initial_drones)) * 100,
            'removed_drone_ids': removed_drones,
            'removal_log': removal_log
        }
        
        print(f"\n✅ Area-Based Removal Results:")
        print(f"   • Drones removed: {len(removed_drones)} ({removal_summary['efficiency_gain']:.1f}% reduction)")
        print(f"   • Coverage: {initial_area:.1f} → {final_area:.1f} sq units")
        print(f"   • Coverage %: {initial_coverage*100:.1f}% → {final_coverage*100:.1f}%")
        print(f"   • Area lost: {removal_summary['area_lost']:.1f} sq units")
        print(f"   • Target maintained: {'✅' if final_coverage >= self.target_coverage else '❌'}")
        
        return removal_summary, remaining_drones
    
    def optimize_repositioning_by_area(self):
        """Optimize drone positions based on area coverage"""
        print("\n🎯 AREA-BASED DRONE REPOSITIONING")
        print("=" * 50)
        
        # Get repositionable drones
        active_drones = [d for d in self.drones if d['status'] == 'active']
        repositionable_drones = [d for d in self.drones if d['status'] == 'repositionable']
        
        if not repositionable_drones:
            print("❌ No repositionable drones found!")
            return None
        
        initial_coverage = self.calculate_actual_area_coverage(active_drones + repositionable_drones)
        
        print(f"📊 Initial Analysis:")
        print(f"   • Active drones: {len(active_drones)}")
        print(f"   • Repositionable drones: {len(repositionable_drones)}")
        print(f"   • Initial area coverage: {initial_coverage*100:.1f}%")
        
        # Objective function for area coverage optimization
        def area_coverage_objective(positions):
            # Create new drone configuration
            test_drones = active_drones.copy()
            
            pos_idx = 0
            for d in repositionable_drones:
                new_drone = d.copy()
                new_drone['x'] = positions[pos_idx * 2]
                new_drone['y'] = positions[pos_idx * 2 + 1]
                new_drone['status'] = 'repositioned'
                test_drones.append(new_drone)
                pos_idx += 1
            
            # Calculate area coverage
            coverage = self.calculate_actual_area_coverage(test_drones)
            
            # Calculate overlap penalty
            overlap_area = self.calculate_overlap_area(test_drones)
            overlap_penalty = overlap_area / self.total_area
            
            # Boundary penalties
            boundary_penalty = 0
            for i in range(0, len(positions), 2):
                x, y = positions[i], positions[i+1]
                if x < 0 or x > self.grid_width or y < 0 or y > self.grid_height:
                    boundary_penalty += 1
            
            # Objective: maximize coverage, minimize overlap
            score = coverage - 0.1 * overlap_penalty - boundary_penalty
            return -score  # Negative for minimization
        
        # Set up bounds
        bounds = []
        for _ in range(len(repositionable_drones)):
            bounds.extend([(0, self.grid_width), (0, self.grid_height)])
        
        print(f"\n🔄 Optimizing positions for maximum area coverage...")
        
        # Run optimization
        result = differential_evolution(
            area_coverage_objective,
            bounds,
            maxiter=150,
            popsize=20,
            seed=42
        )
        
        # Create optimized configuration
        optimized_drones = active_drones.copy()
        pos_idx = 0
        repositioning_details = []
        
        for d in repositionable_drones:
            optimized_drone = d.copy()
            new_x = result.x[pos_idx * 2]
            new_y = result.x[pos_idx * 2 + 1]
            optimized_drone['x'] = new_x
            optimized_drone['y'] = new_y
            optimized_drone['status'] = 'repositioned'
            optimized_drones.append(optimized_drone)
            
            # Track movement
            distance_moved = np.sqrt((new_x - d['x'])**2 + (new_y - d['y'])**2)
            repositioning_details.append({
                'drone_id': d['id'],
                'original_position': (d['x'], d['y']),
                'new_position': (new_x, new_y),
                'distance_moved': distance_moved
            })
            pos_idx += 1
        
        # Calculate final results
        final_coverage = self.calculate_actual_area_coverage(optimized_drones)
        final_overlap = self.calculate_overlap_area(optimized_drones)
        
        repositioning_summary = {
            'initial_coverage_pct': initial_coverage * 100,
            'final_coverage_pct': final_coverage * 100,
            'coverage_improvement_pct': (final_coverage - initial_coverage) * 100,
            'initial_area': initial_coverage * self.total_area,
            'final_area': final_coverage * self.total_area,
            'area_gained': (final_coverage - initial_coverage) * self.total_area,
            'final_overlap_area': final_overlap,
            'repositioned_count': len(repositionable_drones),
            'optimization_success': result.success,
            'repositioning_details': repositioning_details
        }
        
        print(f"\n✅ Area-Based Repositioning Results:")
        print(f"   • Coverage improvement: +{repositioning_summary['coverage_improvement_pct']:.2f}%")
        print(f"   • Area gained: +{repositioning_summary['area_gained']:.1f} sq units")
        print(f"   • Final coverage: {final_coverage*100:.1f}%")
        print(f"   • Final overlap: {final_overlap:.1f} sq units")
        print(f"   • Optimization successful: {'✅' if result.success else '❌'}")
        
        print(f"\n📍 Repositioning Details:")
        for detail in repositioning_details:
            orig_x, orig_y = detail['original_position']
            new_x, new_y = detail['new_position']
            distance = detail['distance_moved']
            print(f"   • Drone {detail['drone_id']}: ({orig_x:.0f},{orig_y:.0f}) → ({new_x:.1f},{new_y:.1f}) [moved {distance:.1f} units]")
        
        return repositioning_summary, optimized_drones
    
    def visualize_area_optimization(self, before_drones, after_drones, title_suffix=""):
        """Visualize area-based optimization results"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"area_based_optimization_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
        
        # Before optimization
        before_coverage = self.calculate_actual_area_coverage(before_drones)
        before_area = before_coverage * self.total_area
        
        ax1.set_xlim(0, self.grid_width)
        ax1.set_ylim(0, self.grid_height)
        ax1.set_aspect('equal')
        ax1.set_title(f'Before {title_suffix}\nArea Coverage: {before_area:.1f} sq units ({before_coverage*100:.1f}%)', 
                     fontsize=14, fontweight='bold')
        
        # Draw coverage circles and drones for before
        for drone in before_drones:
            circle = patches.Circle((drone['x'], drone['y']), drone['radius'], 
                                  alpha=0.3, facecolor='green', edgecolor='darkgreen')
            ax1.add_patch(circle)
            ax1.plot(drone['x'], drone['y'], 'o', color='darkgreen', markersize=8)
        
        ax1.set_xlabel('X Coordinate (units)')
        ax1.set_ylabel('Y Coordinate (units)')
        ax1.grid(True, alpha=0.3)
        
        # After optimization
        after_coverage = self.calculate_actual_area_coverage(after_drones)
        after_area = after_coverage * self.total_area
        improvement = after_area - before_area
        
        ax2.set_xlim(0, self.grid_width)
        ax2.set_ylim(0, self.grid_height)
        ax2.set_aspect('equal')
        ax2.set_title(f'After {title_suffix}\nArea Coverage: {after_area:.1f} sq units ({after_coverage*100:.1f}%) [+{improvement:.1f}]', 
                     fontsize=14, fontweight='bold')
        
        # Draw coverage circles and drones for after
        for drone in after_drones:
            if drone['status'] == 'repositioned':
                circle = patches.Circle((drone['x'], drone['y']), drone['radius'], 
                                      alpha=0.3, facecolor='blue', edgecolor='darkblue')
                ax2.add_patch(circle)
                ax2.plot(drone['x'], drone['y'], 'o', color='darkblue', markersize=8)
            else:
                circle = patches.Circle((drone['x'], drone['y']), drone['radius'], 
                                      alpha=0.3, facecolor='green', edgecolor='darkgreen')
                ax2.add_patch(circle)
                ax2.plot(drone['x'], drone['y'], 'o', color='darkgreen', markersize=8)
        
        ax2.set_xlabel('X Coordinate (units)')
        ax2.set_ylabel('Y Coordinate (units)')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/area_based_{title_suffix.lower().replace(' ', '_')}_comparison.png", 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"\n📁 Visualization saved to: {output_dir}/")
        return output_dir

def main():
    """Run area-based drone optimization"""
    print("🚁 AREA-BASED DRONE OPTIMIZATION")
    print("=" * 60)
    
    # Initialize optimizer
    optimizer = AreaBasedDroneOptimizer(grid_width=100, grid_height=80)
    
    # Load current deployment
    optimizer.load_current_deployment()
    
    print("🔸 TESTING: Drone Removal Based on Area Coverage")
    # Test drone removal
    removal_summary, remaining_drones = optimizer.optimize_drone_removal_by_area()
    
    print("\n🔸 TESTING: Drone Repositioning Based on Area Coverage")
    # Test repositioning
    repositioning_summary, optimized_drones = optimizer.optimize_repositioning_by_area()
    
    if repositioning_summary:
        # Visualize repositioning results
        before_drones = [d for d in optimizer.drones if d['status'] in ['active', 'repositionable']]
        optimizer.visualize_area_optimization(before_drones, optimized_drones, "Repositioning")
        
        print("\n🎯 AREA-BASED OPTIMIZATION SUMMARY:")
        print("=" * 50)
        print(f"Repositioning Results:")
        print(f"  • Area gained: +{repositioning_summary['area_gained']:.1f} sq units")
        print(f"  • Coverage improvement: +{repositioning_summary['coverage_improvement_pct']:.2f}%")
        print(f"  • Final coverage: {repositioning_summary['final_coverage_pct']:.1f}%")
        
        if removal_summary:
            print(f"\nRemoval Analysis:")
            print(f"  • Drones removable: {removal_summary['drones_removed']}")
            print(f"  • Area that would be lost: {removal_summary['area_lost']:.1f} sq units")
        
        print(f"\n💡 RECOMMENDATION:")
        print(f"   ✅ Use REPOSITIONING for +{repositioning_summary['area_gained']:.1f} sq units gain")
        print(f"   ❌ Avoid removal (loses {removal_summary.get('area_lost', 0):.1f} sq units)")

if __name__ == "__main__":
    main()
