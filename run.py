import argparse
import sys
import importlib.util
import logging
import os
from datetime import datetime
from pathlib import Path

# Setup enhanced logging with compact format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S',
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
        logger.error(f"Missing dependencies: {', '.join(missing)}")
        logger.error(f"Install with: pip install {' '.join(missing)}")
        return False
    logger.info("Dependencies OK")
    return True

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Drone Optimization Simulation System')
    parser.add_argument('--port', type=int, default=8050, help='Port to run the web application on (default: 8050)')
    parser.add_argument('--debug', action='store_true', help='Run the app in debug mode')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host to bind the server to (default: 127.0.0.1)')
    return parser.parse_args()

def main():
    """Main entry point for the application"""
    if not check_dependencies():
        sys.exit(1)
    
    args = parse_arguments()
    
    try:
        # The app object is imported from app.py, which now contains all logic
        from app import app
        
        logger.info("=" * 45)
        logger.info("DRONE OPTIMIZATION SYSTEM")
        logger.info("=" * 45)
        logger.info(f"Server: http://{args.host}:{args.port}")
        logger.info(f"Debug: {'ON' if args.debug else 'OFF'}")
        logger.info("Ready to start...")
        
        # The server is run with the configuration from command-line arguments
        app.run_server(debug=args.debug, port=args.port, host=args.host)
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        logger.error("Check that app.py exists in current directory")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Startup error: {e}")
        sys.exit(1) 

if __name__ == '__main__':
    main()