#!/usr/bin/env python3
"""
Quick Start Example for Drone Optimization System

This example demonstrates how to use the system without the UI,
running a simple simulation with the Greedy optimization algorithm.

Usage:
    python quick_start_example.py
"""

import numpy as np
import matplotlib.pyplot as plt
from simulation import DroneEnvironment
from optimization import greedy_optimization

def main():
    """
    Run a simple example of drone optimization with the Greedy algorithm
    """
    print("Drone Optimization System - Quick Start Example")
    print("=" * 50)
    
    # Create a simulation environment
    print("\nInitializing simulation environment...")
    sim = DroneEnvironment(
        width=100,
        height=100,
        num_drones=20,
        sensing_radius=15,
        grid_resolution=5
    )
    
    print(f"Environment created with {len(sim.drones)} drones")
    print(f"Grid size: {sim.width} x {sim.height}")
    print(f"Number of grid points: {len(sim.grid_points)}")
    
    # Run the Greedy optimization algorithm
    print("\nRunning Greedy optimization algorithm...")
    activation = greedy_optimization(sim, desired_coverage=0.9, overlap_weight=0.2)
    
    # Apply the optimization results
    sim.apply_activation(activation)
    
    # Run a simulation step
    metrics = sim.step()
    
    # Display results
    print("\nOptimization Results:")
    print(f"Active Drones: {metrics['active_drones']} out of {len(sim.drones)}")
    print(f"Coverage: {metrics['coverage']*100:.2f}%")
    print(f"Average Overlap: {metrics['avg_overlap']:.2f}")
    print(f"Power Consumption: {metrics['power_consumption']} units")
    
    # Visualize the results
    print("\nCreating visualization...")
    visualize_results(sim)
    
    print("\nExample completed successfully!")
    print("To explore more features, run the full application with: python run.py")

def visualize_results(sim):
    """
    Create a simple matplotlib visualization of the optimization results
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot grid points
    ax.scatter(
        sim.grid_points[:, 0],
        sim.grid_points[:, 1],
        c='lightgray',
        s=10,
        alpha=0.3,
        label='Grid Points'
    )
    
    # Plot drones
    active_drones = sim.drones[sim.drones['active'] == 1]
    inactive_drones = sim.drones[sim.drones['active'] == 0]
    
    ax.scatter(
        active_drones['x'],
        active_drones['y'],
        c='green',
        s=100,
        marker='o',
        label='Active Drones'
    )
    
    ax.scatter(
        inactive_drones['x'],
        inactive_drones['y'],
        c='red',
        s=100,
        marker='o',
        label='Inactive Drones'
    )
    
    # Draw coverage circles
    for _, drone in active_drones.iterrows():
        circle = plt.Circle(
            (drone['x'], drone['y']),
            sim.sensing_radius,
            fill=False,
            color='green',
            alpha=0.3
        )
        ax.add_patch(circle)
    
    # Add labels and legend
    ax.set_xlim(0, sim.width)
    ax.set_ylim(0, sim.height)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Drone Optimization Results - Greedy Algorithm')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('optimization_result.png')
    plt.show()

if __name__ == "__main__":
    main()