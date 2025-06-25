import numpy as np
import pandas as pd
from scipy.spatial import distance

class DroneEnvironment:
    """Core simulation environment for drone coverage optimization"""
    
    def __init__(self, width=100, height=100, num_drones=20, sensing_radius=20, 
                 grid_resolution=5, num_parking_spots=100, num_disabled_spots=10):
        """Initialize the simulation environment"""
        # Environment parameters
        self.width = width
        self.height = height
        self.sensing_radius = sensing_radius
        self.grid_resolution = grid_resolution
        
        # Simulation state
        self.step_count = 0
        
        # Initialize metrics_history - THIS WAS MISSING!
        self.metrics_history = {
            'coverage': [],
            'active_drones': [],
            'power_consumption': [],
            'avg_overlap': [],
            'violations': []
        }
        
        # Generate grid points
        x = np.arange(0, width, grid_resolution)
        y = np.arange(0, height, grid_resolution)
        xx, yy = np.meshgrid(x, y)
        self.grid_points = np.column_stack([xx.ravel(), yy.ravel()])
        
        # Initialize drones with spread-out positions
        self.drones = self._generate_spread_positions(num_drones)
        
        # For parking scenario
        if num_parking_spots > 0:
            self.is_parking_scenario = True
            self.parking_spots = self._generate_parking_spots(num_parking_spots, num_disabled_spots)
            self.vehicles = self._initialize_vehicles(int(num_parking_spots * 0.3))  # 30% of spots have vehicles
            self.violations = []
        else:
            self.is_parking_scenario = False
            self.parking_spots = None
            self.vehicles = None
            self.violations = []
    
    def _generate_spread_positions(self, num_drones):
        """Generate well-distributed drone positions"""
        positions = []
        
        # Start with one random position
        if num_drones > 0:
            positions.append(np.random.uniform(0, [self.width, self.height]))
        
        # Generate remaining positions with good spacing
        while len(positions) < num_drones:
            # Generate candidate positions
            candidates = np.random.uniform(0, [self.width, self.height], (10, 2))
            
            # Find the candidate with maximum distance from existing positions
            if positions:
                min_dists = []
                for c in candidates:
                    dists = [np.linalg.norm(c - p) for p in positions]
                    min_dists.append(min(dists))
                
                best_idx = np.argmax(min_dists)
                positions.append(candidates[best_idx])
            else:
                positions.append(candidates[0])
        
        # Create DataFrame
        return pd.DataFrame({
            'id': range(num_drones),
            'x': [p[0] for p in positions],
            'y': [p[1] for p in positions],
            'active': [0] * num_drones,  # Initially all inactive
            'energy': [100.0] * num_drones
        })
    
    def _generate_parking_spots(self, num_spots, num_disabled):
        """Generate parking spot locations"""
        if num_spots <= 0:
            return pd.DataFrame()
            
        # Create a grid layout for parking spots
        spots_per_row = max(1, int(np.sqrt(num_spots) * 1.5))  # Make the layout rectangular
        rows = max(1, int(np.ceil(num_spots / spots_per_row)))
        
        x_spacing = self.width / (spots_per_row + 1)
        y_spacing = self.height / (rows + 1)
        
        parking_spots = []
        spot_id = 0
        
        for row in range(rows):
            for col in range(spots_per_row):
                if spot_id >= num_spots:
                    break
                    
                # Every nth spot is a disabled spot
                disabled_interval = max(1, num_spots // max(1, num_disabled))
                is_disabled = 1 if spot_id % disabled_interval == 0 and spot_id < num_disabled else 0
                
                parking_spots.append({
                    'id': spot_id,
                    'x': (col + 1) * x_spacing,
                    'y': (row + 1) * y_spacing,
                    'disabled': is_disabled,
                    'occupied': 0,
                    'vehicle_id': None
                })
                
                spot_id += 1
        
        return pd.DataFrame(parking_spots)
    
    def _initialize_vehicles(self, num_vehicles):
        """Initialize vehicles for parking scenario"""
        if num_vehicles <= 0:
            return pd.DataFrame()
            
        # About 10% of vehicles are disabled-permit vehicles
        num_disabled = max(1, int(num_vehicles * 0.1))
        
        return pd.DataFrame({
            'id': range(num_vehicles),
            'disabled': [1] * num_disabled + [0] * (num_vehicles - num_disabled),
            'rfid': [f"DIS-{i}" if i < num_disabled else f"CAR-{i}" for i in range(num_vehicles)],
            'license': [f"XYZ{i:03d}" for i in range(num_vehicles)],
            'parked': [0] * num_vehicles
        })
    
    def compute_coverage(self, activation_status=None):
        """Compute coverage percentage and overlap"""
        if activation_status is None:
            activation_status = self.drones['active'].values
            
        covered_points = set()
        overlap_count = np.zeros(len(self.grid_points))
        
        for i, active in enumerate(activation_status):
            if active and i < len(self.drones):
                drone_pos = np.array([self.drones.iloc[i]['x'], self.drones.iloc[i]['y']])
                distances = np.linalg.norm(self.grid_points - drone_pos, axis=1)
                covered_indices = np.where(distances <= self.sensing_radius)[0]
                
                for idx in covered_indices:
                    covered_points.add(idx)
                    overlap_count[idx] += 1
        
        coverage = len(covered_points) / len(self.grid_points) if len(self.grid_points) > 0 else 0
        avg_overlap = np.mean(overlap_count[overlap_count > 0]) if np.any(overlap_count > 0) else 0
        
        return coverage, avg_overlap
    
    def compute_power_consumption(self):
        """Calculate power consumption based on active drones"""
        # Simple model: each active drone consumes 1 unit of power per step
        active_count = np.sum(self.drones['active'])
        return float(active_count)
    
    def apply_activation(self, activation_status):
        """
        Apply the activation status to drones.

        Args:
            activation_status: Array/list of 0s and 1s indicating which drones should be active.
        Returns:
            tuple: (is_valid, warnings)
        """
        is_valid, corrected_activation, warnings = self.validate_activation(activation_status)
        self.drones['active'] = corrected_activation

        for i, active in enumerate(corrected_activation):
            if i < len(self.drones):
                if active:
                    current_energy = self.drones.loc[i, 'energy']
                    energy_consumption = np.random.uniform(0.5, 2.0)
                    new_energy = max(0, current_energy - energy_consumption)
                    self.drones.loc[i, 'energy'] = new_energy
                    if new_energy <= 5.0:
                        self.drones.loc[i, 'active'] = 0
                else:
                    current_energy = self.drones.loc[i, 'energy']
                    if 0 < current_energy < 100:
                        recovery_rate = np.random.uniform(0.1, 0.5)
                        new_energy = min(100, current_energy + recovery_rate)
                        self.drones.loc[i, 'energy'] = new_energy
        return is_valid, warnings
    
    def check_violations(self):
        """Check for parking violations in parking scenario"""
        if not self.is_parking_scenario or self.parking_spots is None or self.vehicles is None:
            return 0
            
        violation_count = 0
        
        # Reset parking occupancy
        self.parking_spots['occupied'] = 0
        self.parking_spots['vehicle_id'] = None
        
        # Randomly assign vehicles to spots (simplified model)
        available_spots = self.parking_spots.index.tolist()
        np.random.shuffle(available_spots)
        
        num_vehicles_to_park = min(len(self.vehicles), len(available_spots))
        
        for i in range(num_vehicles_to_park):
            vehicle = self.vehicles.iloc[i]
            spot_idx = available_spots[i]
            spot = self.parking_spots.loc[spot_idx]
            
            # Mark spot as occupied
            self.parking_spots.loc[spot_idx, 'occupied'] = 1
            self.parking_spots.loc[spot_idx, 'vehicle_id'] = vehicle['license']
            
            # Check for violations: non-disabled vehicle in disabled spot
            if spot['disabled'] == 1 and vehicle['disabled'] == 0:
                violation_count += 1
                self.violations.append({
                    'step': self.step_count,
                    'license': vehicle['license'],
                    'rfid': vehicle['rfid'],
                    'violation': 'Unauthorized disabled parking'
                })
        
        return violation_count
    
    def step(self):
        """Advance simulation by one step"""
        self.step_count += 1
        
        # Check for violations in parking scenario
        violations = self.check_violations()
        
        # Compute metrics
        coverage, avg_overlap = self.compute_coverage()
        power = self.compute_power_consumption()
        active_count = int(np.sum(self.drones['active']))
        
        # Ensure metrics_history exists
        if not hasattr(self, 'metrics_history'):
            self.metrics_history = {
                'coverage': [],
                'active_drones': [],
                'power_consumption': [],
                'avg_overlap': [],
                'violations': []
            }
        
        # Record metrics
        self.metrics_history['coverage'].append(float(coverage))
        self.metrics_history['active_drones'].append(int(active_count))
        self.metrics_history['power_consumption'].append(float(power))
        self.metrics_history['avg_overlap'].append(float(avg_overlap))
        self.metrics_history['violations'].append(int(violations))
        
        return {
            'step': self.step_count,
            'coverage': float(coverage),
            'active_drones': int(active_count),
            'power_consumption': float(power),
            'avg_overlap': float(avg_overlap),
            'violations': int(violations)
        }
    
    def get_drone_positions(self):
        """Get current drone positions as numpy array"""
        return self.drones[['x', 'y']].values
    
    def get_active_drones(self):
        """Get DataFrame of currently active drones"""
        return self.drones[self.drones['active'] == 1]
    
    def get_inactive_drones(self):
        """Get DataFrame of currently inactive drones"""
        return self.drones[self.drones['active'] == 0]
    
    def reset_simulation(self):
        """Reset simulation to initial state"""
        self.step_count = 0
        self.drones['active'] = 0
        self.drones['energy'] = 100.0
        
        # Reset metrics history
        self.metrics_history = {
            'coverage': [],
            'active_drones': [],
            'power_consumption': [],
            'avg_overlap': [],
            'violations': []
        }
        
        # Reset violations
        if hasattr(self, 'violations'):
            self.violations = []
    
    def get_simulation_state(self):
        """Get complete simulation state for saving/loading"""
        return {
            'step_count': self.step_count,
            'drones': self.drones.to_dict('records'),
            'metrics_history': self.metrics_history,
            'environment_params': {
                'width': self.width,
                'height': self.height,
                'sensing_radius': self.sensing_radius,
                'grid_resolution': self.grid_resolution
            }
        }
    
    def load_simulation_state(self, state):
        """Load simulation state from saved data"""
        self.step_count = state.get('step_count', 0)
        if 'drones' in state:
            self.drones = pd.DataFrame(state['drones'])
        if 'metrics_history' in state:
            self.metrics_history = state['metrics_history']
        # Environment params are read-only after initialization
    
    def get_coverage_map(self, resolution=50):
        """
        Generate detailed coverage map for visualization
        
        Args:
            resolution: Grid resolution for coverage map
            
        Returns:
            tuple: (x_coords, y_coords, coverage_matrix)
        """
        x = np.linspace(0, self.width, resolution)
        y = np.linspace(0, self.height, resolution)
        xx, yy = np.meshgrid(x, y)
        
        coverage_map = np.zeros((resolution, resolution))
        active_drones = self.get_active_drones()
        
        for i in range(resolution):
            for j in range(resolution):
                point = np.array([xx[i, j], yy[i, j]])
                
                # Check coverage by any active drone
                for _, drone in active_drones.iterrows():
                    drone_pos = np.array([drone['x'], drone['y']])
                    distance = np.linalg.norm(point - drone_pos)
                    if distance <= self.sensing_radius:
                        coverage_map[i, j] += 1
        
        return x, y, coverage_map
    
    def get_energy_statistics(self):
        """Get energy statistics for all drones"""
        energy_levels = self.drones['energy'].values
        return {
            'mean_energy': float(np.mean(energy_levels)),
            'std_energy': float(np.std(energy_levels)),
            'min_energy': float(np.min(energy_levels)),
            'max_energy': float(np.max(energy_levels)),
            'low_energy_count': int(np.sum(energy_levels < 20)),
            'critical_energy_count': int(np.sum(energy_levels < 5))
        }
    
    def get_coverage_statistics(self):
        """Get detailed coverage statistics"""
        coverage, overlap = self.compute_coverage()
        
        return {
            'total_coverage': float(coverage),
            'coverage_percentage': float(coverage * 100),
            'average_overlap': float(overlap),
            'active_drone_count': int(np.sum(self.drones['active'])),
            'total_drone_count': len(self.drones),
            'utilization_ratio': float(np.sum(self.drones['active']) / len(self.drones))
        }
    
    def validate_activation(self, activation_status):
        """
        Validate activation status before applying
        
        Args:
            activation_status: Proposed activation status
            
        Returns:
            tuple: (is_valid, corrected_activation, warnings)
        """
        warnings = []
        corrected_activation = list(activation_status)
        
        # Check length
        if len(activation_status) != len(self.drones):
            warnings.append(f"Activation length mismatch: got {len(activation_status)}, expected {len(self.drones)}")
            # Correct the length
            if len(activation_status) > len(self.drones):
                corrected_activation = activation_status[:len(self.drones)]
            else:
                corrected_activation.extend([0] * (len(self.drones) - len(activation_status)))
        
        # Check energy constraints
        for i, active in enumerate(corrected_activation):
            if i < len(self.drones) and active and self.drones.iloc[i]['energy'] <= 5.0:
                corrected_activation[i] = 0
                warnings.append(f"Drone {i} cannot be activated: insufficient energy ({self.drones.iloc[i]['energy']:.1f}%)")
        
        # Check if activation makes sense (at least one drone active if possible)
        total_activatable = sum(1 for i in range(len(self.drones)) if self.drones.iloc[i]['energy'] > 5.0)
        total_activated = sum(corrected_activation)
        
        if total_activated == 0 and total_activatable > 0:
            warnings.append("No drones activated despite having activatable drones available")
        
        is_valid = len(warnings) == 0
        return is_valid, corrected_activation, warnings
