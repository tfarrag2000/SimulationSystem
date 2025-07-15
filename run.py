import argparse
import sys
import importlib.util
import logging
import os
from datetime import datetime
from pathlib import Path

# Setup enhanced logging
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
    required_packages = {
        'dash': 'dash', 'dash_bootstrap_components': 'dash-bootstrap-components',
        'plotly': 'plotly', 'numpy': 'numpy', 'pandas': 'pandas', 'scipy': 'scipy'
    }
    missing = [pip_name for package, pip_name in required_packages.items() if importlib.util.find_spec(package) is None]
    if missing:
        logger.error(f"🚨 Missing dependencies: {', '.join(missing)}")
        logger.error(f"📦 Please install them using: pip install {' '.join(missing)}")
        return False
    logger.info("✅ All dependencies satisfied.")
    return True

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Drone Optimization Simulation System')
    parser.add_argument('--port', type=int, default=8050, help='Port to run the web application on (default: 8050)')
    parser.add_argument('--debug', action='store_true', help='Run the app in debug mode')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host to bind the server to (default: 127.0.0.1)')
    return parser.parse_args()

# Define allowed params for each algorithm
ALGORITHM_ALLOWED_PARAMS = {
    'greedy': ['desired_coverage', 'overlap_weight', 'energy_weight', 'max_iterations', 'convergence_threshold'],
    'ga': ['population_size', 'num_generations', 'mutation_rate', 'crossover_rate', 'elitism', 'desired_coverage', 'parallel_processing', 'w1', 'w2', 'w3', 'convergence_threshold'],
    'pso': ['swarm_size', 'iterations', 'inertia', 'cognitive_weight', 'social_weight', 'w1', 'w2', 'w3', 'desired_coverage', 'parallel_processing', 'convergence_threshold'],
    'sa': ['num_iterations', 'initial_temp', 'cooling_rate', 'perturb_radius', 'desired_coverage', 'w1', 'w2', 'w3', 'convergence_threshold'],
    'ga_sa': ['population_size', 'num_generations', 'mutation_rate', 'crossover_rate', 'elitism_fraction', 'sa_temp', 'sa_cooling', 'sa_iters', 'desired_coverage', 'parallel_processing', 'w1', 'w2', 'w3', 'convergence_threshold'],
    'gwo': ['population_size', 'max_iterations', 'desired_coverage', 'parallel_processing', 'w1', 'w2', 'w3', 'convergence_threshold'],
    'mrfo': ['population_size', 'num_generations', 'desired_coverage', 'parallel_processing', 'w1', 'w2', 'w3', 'convergence_threshold'],
}

# Default parameters to FIX THE 5-ITERATION ISSUE
ALGORITHM_DEFAULT_PARAMS = {
    'greedy': {'max_iterations': 500, 'convergence_threshold': 0.000001},
    'ga': {'num_generations': 500, 'convergence_threshold': 0.000001},
    'pso': {'iterations': 500, 'convergence_threshold': 0.000001},
    'sa': {'num_iterations': 500, 'convergence_threshold': 0.000001},
    'ga_sa': {'num_generations': 250, 'convergence_threshold': 0.000001},
    'gwo': {'max_iterations': 500, 'convergence_threshold': 0.000001},
    'mrfo': {'num_generations': 500, 'convergence_threshold': 0.000001}
}

def get_default_params(algorithm_key):
    """Get default parameters for an algorithm"""
    return ALGORITHM_DEFAULT_PARAMS.get(algorithm_key, {}).copy()

def filter_params(algorithm_key, params):
    """Filter parameters and apply proper defaults to fix 5-iteration issue"""
    allowed = ALGORITHM_ALLOWED_PARAMS.get(algorithm_key, [])
    defaults = get_default_params(algorithm_key)
    filtered = {k: v for k, v in params.items() if k in allowed}
    
    # Merge: defaults first, then user overrides
    result = defaults.copy()
    result.update(filtered)
    
    logger.info(f"Running {algorithm_key.upper()} with parameters: {result}")
    return result

def main():
    """Main entry point for the application"""
    if not check_dependencies():
        sys.exit(1)
    
    args = parse_arguments()
    
    try:
        from app import app
        
        logger.info("="*60)
        logger.info("🚁 DRONE OPTIMIZATION SIMULATION SYSTEM")
        logger.info("="*60)
        logger.info(f"✅ 5-ITERATION FIX APPLIED: All algorithms will now run for extended iterations.")
        logger.info(f"🚀 Starting server at http://{args.host}:{args.port}")
        logger.info(f"🐛 Debug mode: {'enabled' if args.debug else 'disabled'}")
        
        app.run_server(debug=args.debug, port=args.port, host=args.host)
        
    except ImportError as e:
        logger.error(f"❌ Error importing application: {e}")
        logger.error("Ensure app.py and other required files are in the same directory.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"💥 Fatal error during application startup: {e}")
        sys.exit(1) 

if __name__ == '__main__':
    main()