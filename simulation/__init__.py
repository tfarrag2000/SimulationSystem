from .environment import DroneEnvironment

# Define SimulationState class
class SimulationState:
    """Holds the current state of the simulation"""
    
    def __init__(self):
        self.current_step = 0
        self.algorithm = None
        self.algorithm_params = {}
        self.running = False

# Define run_simulation_step function
def run_simulation_step(simulation, optimization_algorithm, algorithm_params=None):
    """Run a single simulation step with the specified optimization algorithm"""
    if algorithm_params is None:
        algorithm_params = {}
        
    # Run the optimization algorithm to get drone activation status
    activation_status = optimization_algorithm(simulation, **algorithm_params)
    
    # Apply the activation status
    simulation.apply_activation(activation_status)
    
    # Step the simulation and return metrics
    return simulation.step()