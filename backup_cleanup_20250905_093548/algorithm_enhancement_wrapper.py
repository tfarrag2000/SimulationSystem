#!/usr/bin/env python3
"""
RAPID ALGORITHM ENHANCEMENT WRAPPER
This module provides enhanced versions of all 14 algorithms using the same core approach
"""

import numpy as np
import time

def enhance_algorithm_wrapper(original_algorithm_func, algorithm_name):
    """
    Wrapper that enhances any algorithm with position and activation optimization
    
    Args:
        original_algorithm_func: Original algorithm function
        algorithm_name: Name of the algorithm
    
    Returns:
        enhanced_algorithm_func: Enhanced version of the algorithm
    """
    
    def enhanced_algorithm(simulation, **kwargs):
        """Enhanced version of the algorithm"""
        start_time = time.time()
        
        try:
            # Import enhanced core functions
            from enhanced_algorithm_core import (
                enhanced_position_optimizer, 
                smart_activation_optimization,
                create_algorithm_result
            )
            
            # Phase 1: Position Optimization
            optimized_positions, best_technique = enhanced_position_optimizer(simulation, max_iterations=20)
            
            # Update drone positions
            for i, pos in enumerate(optimized_positions):
                if i < len(simulation.drones):
                    simulation.drones.iloc[i, simulation.drones.columns.get_loc('x')] = pos[0]
                    simulation.drones.iloc[i, simulation.drones.columns.get_loc('y')] = pos[1]
            
            # Phase 2: Smart Activation Optimization  
            desired_coverage = kwargs.get('desired_coverage', kwargs.get('target_coverage', 0.85))
            activation = smart_activation_optimization(simulation, optimized_positions, desired_coverage)
            
            # Apply activation and calculate final coverage
            simulation.set_active_drones(activation)
            final_coverage = simulation.calculate_coverage_percentage()
            active_count = np.sum(activation)
            
            execution_time = time.time() - start_time
            
            # Create enhanced result
            result = create_algorithm_result(
                coverage=final_coverage,
                active_drones=active_count,
                execution_time=execution_time,
                algorithm_name=f'Enhanced {algorithm_name}',
                enhancement_used='position_activation_optimization',
                optimal_technique=best_technique
            )
            
            return activation, result
            
        except Exception as e:
            print(f"⚠️ Enhanced {algorithm_name} failed, using original: {e}")
            # Fall back to original algorithm
            return original_algorithm_func(simulation, **kwargs)
    
    return enhanced_algorithm

def create_staged_algorithm_wrapper(enhanced_algorithm_func, algorithm_name):
    """
    Create staged version that uses enhanced algorithm in two phases
    
    Args:
        enhanced_algorithm_func: Enhanced algorithm function
        algorithm_name: Name of the algorithm
    
    Returns:
        staged_algorithm_func: Staged version of the enhanced algorithm
    """
    
    def staged_algorithm(simulation, **kwargs):
        """Staged version of the enhanced algorithm"""
        start_time = time.time()
        
        try:
            # Phase 1: Position optimization with coverage focus
            print(f"🎯 Staged {algorithm_name} - Phase 1: Position Optimization")
            phase1_kwargs = kwargs.copy()
            phase1_kwargs['desired_coverage'] = kwargs.get('desired_coverage', 0.85)
            
            # Run enhanced algorithm for position optimization
            phase1_activation, phase1_result = enhanced_algorithm_func(simulation, **phase1_kwargs)
            phase1_coverage = phase1_result.coverage
            
            print(f"✅ Phase 1 Complete: {phase1_coverage:.1f}% coverage")
            
            # Phase 2: Activation refinement
            print(f"⚡ Staged {algorithm_name} - Phase 2: Activation Refinement")
            
            from enhanced_algorithm_core import smart_activation_optimization
            
            # Get current positions
            current_positions = np.array([[
                simulation.drones.iloc[i]['x'], 
                simulation.drones.iloc[i]['y']
            ] for i in range(len(simulation.drones))])
            
            # Refine activation with higher target coverage
            target_coverage = min(0.98, phase1_coverage / 100 + 0.1)  # Push for higher coverage
            refined_activation = smart_activation_optimization(simulation, current_positions, target_coverage)
            
            # Apply refined activation
            simulation.set_active_drones(refined_activation)
            final_coverage = simulation.calculate_coverage_percentage()
            active_count = np.sum(refined_activation)
            
            execution_time = time.time() - start_time
            
            # Create staged result
            from enhanced_algorithm_core import create_algorithm_result
            result = create_algorithm_result(
                coverage=final_coverage,
                active_drones=active_count,
                execution_time=execution_time,
                algorithm_name=f'Staged Enhanced {algorithm_name}',
                enhancement_used='two_phase_staged_optimization',
                optimal_technique='staged_refinement'
            )
            
            print(f"✅ Staged Complete: {final_coverage:.1f}% coverage with {active_count} drones")
            
            return refined_activation, result
            
        except Exception as e:
            print(f"⚠️ Staged {algorithm_name} failed, using enhanced version: {e}")
            # Fall back to enhanced version
            return enhanced_algorithm_func(simulation, **kwargs)
    
    return staged_algorithm
