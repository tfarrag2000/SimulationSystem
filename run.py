#!/usr/bin/env python3
"""
Drone Optimization Simulation System

This script is the main entry point for the drone optimization simulation system.
It sets up the Dash web application and connects all components.

Usage:
    python run.py

Example:
    python run.py --port 8080 --debug
"""

import argparse
import os
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