#!/usr/bin/env python3
"""
Smart Coverage Distribution Enhancement
======================================

Implements intelligent drone placement logic that:
1. Prevents redundant placement - each drone must contribute meaningfully
2. Minimum grid point coverage rule - each drone covers at least 1 new grid point
3. Gap-filling priority - prioritize uncovered areas over overlap
4. Coverage efficiency optimization

Created: September 6, 2025
Author: GitHub Copilot for Drone Coverage Research
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Any
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

class SmartCoverageDistributor:
    """
    Smart coverage distribution system that ensures efficient drone placement.
    """
    
    def __init__(self, area_width: float, area_height: float, sensing_radius: float, 
                 grid_resolution: int = 85):
        self.area_width = area_width
        self.area_height = area_height
        self.sensing_radius = sensing_radius
        self.grid_resolution = grid_resolution
        
        # Create grid points for coverage calculation
        self.grid_points = self._create_grid_points()
        
        # Smart coverage parameters
        self.MIN_NEW_GRID_POINTS = 1  # Minimum new grid points per drone
        self.REDUNDANCY_THRESHOLD = 0.95  # 95% overlap threshold
        self.GAP_PRIORITY_WEIGHT = 2.0  # Priority multiplier for gap areas
        
    def _create_grid_points(self) -> np.ndarray:
        """
        Create grid points for coverage calculation.
        """
        x_points = np.linspace(0, self.area_width, self.grid_resolution)
        y_points = np.linspace(0, self.area_height, self.grid_resolution)
        
        grid_points = []
        for x in x_points:
            for y in y_points:
                grid_points.append([x, y])
        
        return np.array(grid_points)
    
    def calculate_coverage_contribution(self, candidate_position: np.ndarray, 
                                      existing_positions: List[np.ndarray]) -> Dict[str, Any]:
        """
        Calculate the coverage contribution of a candidate drone position.
        
        Returns:
            dict: Coverage metrics including new grid points, redundancy, and efficiency
        """
        candidate_pos = np.array(candidate_position)
        
        # Calculate distances from candidate to all grid points
        distances_to_candidate = cdist([candidate_pos], self.grid_points)[0]
        candidate_coverage = distances_to_candidate <= self.sensing_radius
        
        # Calculate existing coverage
        existing_coverage = np.zeros(len(self.grid_points), dtype=bool)
        for pos in existing_positions:
            distances = cdist([pos], self.grid_points)[0]
            pos_coverage = distances <= self.sensing_radius
            existing_coverage |= pos_coverage
        
        # Calculate new coverage contribution
        new_coverage = candidate_coverage & ~existing_coverage
        new_grid_points = np.sum(new_coverage)
        
        # Calculate redundancy (overlap with existing coverage)
        overlap = candidate_coverage & existing_coverage
        redundant_points = np.sum(overlap)
        total_candidate_points = np.sum(candidate_coverage)
        
        redundancy_ratio = redundant_points / total_candidate_points if total_candidate_points > 0 else 0
        
        # Calculate coverage efficiency
        efficiency = new_grid_points / total_candidate_points if total_candidate_points > 0 else 0
        
        # Calculate gap-filling priority (prioritize areas with fewer nearby drones)
        gap_priority = self._calculate_gap_priority(candidate_pos, existing_positions)
        
        return {
            'new_grid_points': new_grid_points,
            'redundant_points': redundant_points,
            'total_coverage_points': total_candidate_points,
            'redundancy_ratio': redundancy_ratio,
            'efficiency': efficiency,
            'gap_priority': gap_priority,
            'is_meaningful': new_grid_points >= self.MIN_NEW_GRID_POINTS,
            'is_redundant': redundancy_ratio >= self.REDUNDANCY_THRESHOLD
        }
    
    def _calculate_gap_priority(self, candidate_pos: np.ndarray, 
                               existing_positions: List[np.ndarray]) -> float:
        """
        Calculate gap-filling priority for a candidate position.
        Higher values indicate better gap-filling potential.
        """
        if not existing_positions:
            return 1.0
        
        # Calculate distance to nearest existing drone
        existing_array = np.array(existing_positions)
        distances_to_existing = cdist([candidate_pos], existing_array)[0]
        min_distance = np.min(distances_to_existing)
        
        # Normalize distance (higher distance = higher priority)
        max_possible_distance = np.sqrt(self.area_width**2 + self.area_height**2)
        normalized_distance = min_distance / max_possible_distance
        
        return normalized_distance * self.GAP_PRIORITY_WEIGHT
    
    def optimize_drone_placement(self, candidate_positions: List[np.ndarray], 
                                max_drones: int) -> Dict[str, Any]:
        """
        Optimize drone placement using smart coverage distribution.
        
        Args:
            candidate_positions: List of candidate drone positions
            max_drones: Maximum number of drones to place
            
        Returns:
            dict: Optimized placement with selected positions and metrics
        """
        selected_positions = []
        placement_metrics = []
        coverage_history = []
        
        # Create candidate position array
        candidates = np.array(candidate_positions)
        
        # Greedy selection with smart coverage optimization
        for drone_idx in range(min(max_drones, len(candidates))):
            best_candidate = None
            best_score = -1
            best_metrics = None
            
            for i, candidate in enumerate(candidates):
                if any(np.array_equal(candidate, selected) for selected in selected_positions):
                    continue  # Skip already selected positions
                
                # Calculate coverage contribution
                metrics = self.calculate_coverage_contribution(candidate, selected_positions)
                
                # Calculate smart placement score
                score = self._calculate_placement_score(metrics)
                
                if score > best_score and metrics['is_meaningful']:
                    best_score = score
                    best_candidate = candidate
                    best_metrics = metrics
            
            # Add best candidate if found
            if best_candidate is not None:
                selected_positions.append(best_candidate)
                placement_metrics.append(best_metrics)
                
                # Calculate current total coverage
                total_coverage = self._calculate_total_coverage(selected_positions)
                coverage_history.append(total_coverage)
            else:
                # No meaningful candidate found
                break
        
        # Calculate final metrics
        final_coverage = self._calculate_total_coverage(selected_positions)
        efficiency_per_drone = final_coverage / len(selected_positions) if selected_positions else 0
        
        return {
            'selected_positions': selected_positions,
            'num_drones_used': len(selected_positions),
            'final_coverage_percentage': final_coverage,
            'efficiency_per_drone': efficiency_per_drone,
            'placement_metrics': placement_metrics,
            'coverage_history': coverage_history,
            'smart_placement_applied': True
        }
    
    def _calculate_placement_score(self, metrics: Dict[str, Any]) -> float:
        """
        Calculate smart placement score based on multiple criteria.
        """
        if not metrics['is_meaningful']:
            return 0.0
        
        # Base score from new coverage contribution
        new_points_score = metrics['new_grid_points'] / 100.0  # Normalize
        
        # Efficiency bonus
        efficiency_bonus = metrics['efficiency'] * 0.5
        
        # Gap-filling bonus
        gap_bonus = metrics['gap_priority'] * 0.3
        
        # Redundancy penalty
        redundancy_penalty = metrics['redundancy_ratio'] * 0.4
        
        total_score = new_points_score + efficiency_bonus + gap_bonus - redundancy_penalty
        
        return max(total_score, 0.0)
    
    def _calculate_total_coverage(self, positions: List[np.ndarray]) -> float:
        """
        Calculate total coverage percentage for given positions.
        """
        if not positions:
            return 0.0
        
        total_coverage = np.zeros(len(self.grid_points), dtype=bool)
        
        for pos in positions:
            distances = cdist([pos], self.grid_points)[0]
            pos_coverage = distances <= self.sensing_radius
            total_coverage |= pos_coverage
        
        coverage_percentage = (np.sum(total_coverage) / len(self.grid_points)) * 100
        return coverage_percentage
    
    def analyze_coverage_distribution(self, positions: List[np.ndarray]) -> Dict[str, Any]:
        """
        Analyze the coverage distribution quality.
        """
        if not positions:
            return {'error': 'No positions provided'}
        
        # Calculate coverage metrics for each drone
        drone_metrics = []
        for i, pos in enumerate(positions):
            other_positions = positions[:i] + positions[i+1:]
            metrics = self.calculate_coverage_contribution(pos, other_positions)
            metrics['drone_id'] = i
            metrics['position'] = pos
            drone_metrics.append(metrics)
        
        # Calculate distribution quality metrics
        new_points_list = [m['new_grid_points'] for m in drone_metrics]
        efficiency_list = [m['efficiency'] for m in drone_metrics]
        redundancy_list = [m['redundancy_ratio'] for m in drone_metrics]
        
        return {
            'drone_metrics': drone_metrics,
            'total_coverage': self._calculate_total_coverage(positions),
            'average_new_points': np.mean(new_points_list),
            'average_efficiency': np.mean(efficiency_list),
            'average_redundancy': np.mean(redundancy_list),
            'drones_with_meaningful_contribution': sum(1 for m in drone_metrics if m['is_meaningful']),
            'drones_with_high_redundancy': sum(1 for m in drone_metrics if m['is_redundant']),
            'distribution_quality_score': self._calculate_distribution_quality(drone_metrics)
        }
    
    def _calculate_distribution_quality(self, drone_metrics: List[Dict]) -> float:
        """
        Calculate overall distribution quality score.
        """
        if not drone_metrics:
            return 0.0
        
        # Quality factors
        meaningful_ratio = sum(1 for m in drone_metrics if m['is_meaningful']) / len(drone_metrics)
        avg_efficiency = np.mean([m['efficiency'] for m in drone_metrics])
        low_redundancy_ratio = sum(1 for m in drone_metrics if not m['is_redundant']) / len(drone_metrics)
        
        # Combined quality score
        quality_score = (meaningful_ratio * 0.4 + avg_efficiency * 0.4 + low_redundancy_ratio * 0.2) * 100
        
        return quality_score


def enhance_algorithm_with_smart_coverage(algorithm_function):
    """
    Decorator to enhance algorithms with smart coverage distribution.
    """
    def enhanced_algorithm(simulation, **kwargs):
        # Run original algorithm
        result = algorithm_function(simulation, **kwargs)
        
        if result is None or 'best_solution' not in result:
            return result
        
        # Apply smart coverage enhancement
        smart_distributor = SmartCoverageDistributor(
            simulation.width, 
            simulation.height, 
            simulation.sensing_radius
        )
        
        # Extract drone positions from result
        if hasattr(result['best_solution'], 'ndim') and result['best_solution'].ndim == 2:
            # Position-based solution
            positions = []
            for drone_state in result['best_solution']:
                if drone_state[2] >= 0.5:  # Active drone
                    positions.append([drone_state[0], drone_state[1]])
        else:
            # Binary activation array
            positions = []
            for i, active in enumerate(result['best_solution']):
                if active >= 0.5:
                    drone_data = simulation.drones.iloc[i]
                    positions.append([drone_data['x'], drone_data['y']])
        
        # Analyze coverage distribution
        if positions:
            distribution_analysis = smart_distributor.analyze_coverage_distribution(positions)
            result['smart_coverage_analysis'] = distribution_analysis
            result['coverage_quality_score'] = distribution_analysis['distribution_quality_score']
            result['meaningful_drones'] = distribution_analysis['drones_with_meaningful_contribution']
            result['redundant_drones'] = distribution_analysis['drones_with_high_redundancy']
        
        return result
    
    return enhanced_algorithm


def main():
    """
    Test the smart coverage distribution system.
    """
    print("🧠 SMART COVERAGE DISTRIBUTION SYSTEM")
    print("=" * 60)
    
    # Test parameters
    area_width, area_height = 40, 40
    sensing_radius = 10
    
    # Create smart distributor
    distributor = SmartCoverageDistributor(area_width, area_height, sensing_radius)
    
    # Generate test candidate positions
    np.random.seed(42)
    num_candidates = 20
    candidates = []
    for _ in range(num_candidates):
        x = np.random.uniform(0, area_width)
        y = np.random.uniform(0, area_height)
        candidates.append([x, y])
    
    print(f"📊 Testing with {num_candidates} candidate positions")
    print(f"🎯 Area: {area_width}×{area_height}, Sensing radius: {sensing_radius}")
    
    # Test smart placement
    max_drones = 12
    optimization_result = distributor.optimize_drone_placement(candidates, max_drones)
    
    print(f"\n🚀 Smart Placement Results:")
    print(f"   Drones used: {optimization_result['num_drones_used']}/{max_drones}")
    print(f"   Final coverage: {optimization_result['final_coverage_percentage']:.1f}%")
    print(f"   Efficiency per drone: {optimization_result['efficiency_per_drone']:.1f}%")
    
    # Analyze distribution quality
    if optimization_result['selected_positions']:
        analysis = distributor.analyze_coverage_distribution(optimization_result['selected_positions'])
        
        print(f"\n📊 Coverage Distribution Analysis:")
        print(f"   Meaningful drones: {analysis['drones_with_meaningful_contribution']}/{len(optimization_result['selected_positions'])}")
        print(f"   High redundancy drones: {analysis['drones_with_high_redundancy']}")
        print(f"   Average efficiency: {analysis['average_efficiency']:.3f}")
        print(f"   Average redundancy: {analysis['average_redundancy']:.3f}")
        print(f"   Distribution quality: {analysis['distribution_quality_score']:.1f}/100")
    
    print(f"\n✅ Smart Coverage Distribution System Ready!")


if __name__ == "__main__":
    main()
