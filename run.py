#!/usr/bin/env python3

import argparse
import sys
import sys
import sys
import importlib.util
import logging
from datetime import datetime
# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('drone_simulation')

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'dash', 'dash_bootstrap_components', 'plotly', 
        'numpy', 'pandas', 'scipy'
    ]
    
    missing = []
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing.append(package)
    
    if missing:
        logger.error(f"Missing dependencies: {', '.join(missing)}")
        logger.error("Please install the required packages using:")
        logger.error("pip install -r requirements.txt")
        return False
    
    return True

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Drone Optimization Simulation System')
    parser.add_argument('--port', type=int, default=8050,
                        help='Port to run the web application on (default: 8050)')
    parser.add_argument('--debug', action='store_true',
                        help='Run the app in debug mode')
    return parser.parse_args()

# Define allowed params for each algorithm
ALGORITHM_ALLOWED_PARAMS = {
    'greedy': ['desired_coverage', 'overlap_weight', 'energy_weight'],
    'ga': ['population_size', 'num_generations', 'mutation_rate', 'crossover_rate', 'elitism', 'desired_coverage', 'parallel_processing', 'w1', 'w2', 'w3'],
    'pso': ['swarm_size', 'iterations', 'inertia', 'cognitive_weight', 'social_weight', 'parallel_processing', 'w1', 'w2', 'w3', 'desired_coverage'],
    'sa': ['initial_temp', 'cooling_rate', 'iterations', 'min_temp', 'desired_coverage'],
    'ga_sa': ['population_size', 'num_generations', 'mutation_rate', 'crossover_rate', 'elitism_fraction', 'sa_temp', 'sa_cooling', 'sa_iters', 'desired_coverage', 'parallel_processing', 'w1', 'w2', 'w3'],
}

def filter_params(algorithm_key, params):
    allowed = ALGORITHM_ALLOWED_PARAMS.get(algorithm_key, [])
    return {k: v for k, v in params.items() if k in allowed}

def main():
    """Main entry point for the application"""
    # Check if dependencies are satisfied
    if not check_dependencies():
        sys.exit(1)
    
    args = parse_arguments()
    
    # Import app after checking dependencies
    try:
        from app import app
        
        logger.info(f"Starting Drone Optimization Simulation System on port {args.port}")
        logger.info(f"Debug mode: {'enabled' if args.debug else 'disabled'}")
        logger.info("Open your web browser and navigate to:")
        logger.info(f"http://127.0.0.1:{args.port}/")
        
        # Run the app
        app.run_server(debug=args.debug, port=args.port)
        
    except ImportError as e:
        logger.error(f"Error importing application: {e}")
        logger.error("Make sure the application files are in the correct location.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

# Example usage in your callback:
# if selected_algorithm == 'greedy':
#     filtered_params = filter_params('greedy', algorithm_params)
#     activation_status, result = greedy_optimization(simulation, **filtered_params)
# elif selected_algorithm == 'ga':
#     filtered_params = filter_params('ga', algorithm_params)
#     activation_status, result = genetic_algorithm(simulation, **filtered_params)
# ...and so on for other algorithms...