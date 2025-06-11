import json
import yaml
import pickle
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    """
    Configuration management system for drone optimization experiments
    """
    
    def __init__(self, config_dir: str = "configs"):
        """
        Initialize configuration manager
        
        Args:
            config_dir: Directory to store configuration files
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        # Default configuration templates
        self.default_configs = {
            'simulation': self._get_default_simulation_config(),
            'algorithms': self._get_default_algorithm_configs(),
            'visualization': self._get_default_visualization_config(),
            'experiment': self._get_default_experiment_config()
        }
        
        # Current active configuration
        self.current_config = self._merge_configs(self.default_configs)
    
    def _get_default_simulation_config(self) -> Dict[str, Any]:
        """Get default simulation configuration"""
        return {
            'environment': {
                'width': 100,
                'height': 100,
                'grid_resolution': 5,
                'sensing_radius': 20
            },
            'drones': {
                'num_drones': 20,
                'initial_energy': 100.0,
                'energy_consumption_rate': 1.0,
                'min_energy_threshold': 10.0
            },
            'parking_scenario': {
                'enabled': False,
                'num_parking_spots': 100,
                'num_disabled_spots': 10,
                'vehicle_density': 0.3
            },
            'physics': {
                'max_speed': 10.0,
                'acceleration': 2.0,
                'collision_radius': 2.0
            }
        }
    
    def _get_default_algorithm_configs(self) -> Dict[str, Any]:
        """Get default algorithm configurations"""
        return {
            'greedy': {
                'desired_coverage': 0.95,
                'overlap_weight': 0.2,
                'energy_weight': 0.1
            },
            'genetic_algorithm': {
                'population_size': 50,
                'num_generations': 200,
                'mutation_rate': 0.1,
                'crossover_rate': 0.8,
                'elitism': 10,
                'parallel_processing': False,
                'fitness_weights': {
                    'coverage': 0.6,
                    'energy': 0.2,
                    'overlap': 0.2
                }
            },
            'particle_swarm_optimization': {
                'swarm_size': 50,
                'iterations': 300,
                'inertia_weight': 0.5,
                'cognitive_weight': 1.5,
                'social_weight': 1.5,
                'parallel_processing': False,
                'fitness_weights': {
                    'coverage': 0.7,
                    'energy': 0.15,
                    'overlap': 0.15
                }
            },
            'simulated_annealing': {
                'initial_temp': 100,
                'cooling_rate': 0.95,
                'iterations': 100,
                'min_temp': 0.01,
                'neighborhood_size': 0.1
            },
            'hybrid_ga_sa': {
                'ga_generations': 100,
                'sa_temp': 50,
                'sa_cooling': 0.9,
                'sa_iterations': 30,
                'population_size': 30,
                'parallel_processing': True
            }
        }
    
    def _get_default_visualization_config(self) -> Dict[str, Any]:
        """Get default visualization configuration"""
        return {
            'theme': 'default',
            'animation': {
                'enabled': True,
                'interval': 1000,
                'trail_length': 5,
                'show_trails': True
            },
            'charts': {
                'update_interval': 500,
                'max_history_points': 1000,
                'show_trends': True
            },
            'export': {
                'default_format': 'png',
                'resolution': {'width': 1200, 'height': 800},
                'include_metadata': True
            }
        }
    
    def _get_default_experiment_config(self) -> Dict[str, Any]:
        """Get default experiment configuration"""
        return {
            'logging': {
                'enabled': True,
                'level': 'INFO',
                'save_detailed_results': True,
                'auto_save_interval': 10
            },
            'comparison': {
                'run_multiple_algorithms': False,
                'algorithms_to_compare': ['greedy', 'genetic_algorithm'],
                'num_runs_per_algorithm': 5,
                'statistical_analysis': True
            },
            'performance': {
                'enable_profiling': False,
                'memory_monitoring': False,
                'execution_time_limit': 300
            }
        }
    
    def _merge_configs(self, configs: Dict[str, Any]) -> Dict[str, Any]:
        """Merge multiple configuration dictionaries"""
        merged = {}
        for config_type, config_data in configs.items():
            merged.update(config_data)
        return merged
    
    def save_config(self, config_name: str, config_data: Optional[Dict[str, Any]] = None, 
                   config_type: str = 'custom') -> str:
        """
        Save configuration to file
        
        Args:
            config_name: Name for the configuration
            config_data: Configuration data (uses current config if None)
            config_type: Type of configuration ('json', 'yaml', 'pickle')
            
        Returns:
            Path to saved configuration file
        """
        if config_data is None:
            config_data = self.current_config
        
        # Add metadata
        config_with_metadata = {
            'metadata': {
                'name': config_name,
                'created': datetime.now().isoformat(),
                'version': '1.0',
                'description': f'Drone optimization configuration: {config_name}'
            },
            'configuration': config_data
        }
        
        # Determine file extension and save method
        if config_type == 'yaml':
            filename = f"{config_name}.yaml"
            filepath = self.config_dir / filename
            with open(filepath, 'w') as f:
                yaml.dump(config_with_metadata, f, default_flow_style=False, indent=2)
        elif config_type == 'pickle':
            filename = f"{config_name}.pkl"
            filepath = self.config_dir / filename
            with open(filepath, 'wb') as f:
                pickle.dump(config_with_metadata, f)
        else:  # default to json
            filename = f"{config_name}.json"
            filepath = self.config_dir / filename
            with open(filepath, 'w') as f:
                json.dump(config_with_metadata, f, indent=2, default=str)
        
        logger.info(f"Configuration saved to {filepath}")
        return str(filepath)
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from file
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Loaded configuration data
        """
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        # Determine file type and load accordingly
        if config_path.suffix == '.yaml' or config_path.suffix == '.yml':
            with open(config_path, 'r') as f:
                config_with_metadata = yaml.safe_load(f)
        elif config_path.suffix == '.pkl':
            with open(config_path, 'rb') as f:
                config_with_metadata = pickle.load(f)
        else:  # assume json
            with open(config_path, 'r') as f:
                config_with_metadata = json.load(f)
        
        # Extract configuration data
        if 'configuration' in config_with_metadata:
            config_data = config_with_metadata['configuration']
        else:
            config_data = config_with_metadata  # backwards compatibility
        
        logger.info(f"Configuration loaded from {config_path}")
        return config_data
    
    def apply_config(self, config_data: Dict[str, Any]):
        """Apply configuration to current settings"""
        self.current_config = self._merge_configs({'custom': config_data})
        logger.info("Configuration applied successfully")
    
    def get_config(self, section: Optional[str] = None) -> Dict[str, Any]:
        """
        Get current configuration or specific section
        
        Args:
            section: Specific section to retrieve (None for full config)
            
        Returns:
            Configuration data
        """
        if section is None:
            return self.current_config.copy()
        
        if section in self.current_config:
            return self.current_config[section].copy()
        else:
            raise KeyError(f"Configuration section '{section}' not found")
    
    def update_config(self, section: str, updates: Dict[str, Any]):
        """
        Update specific section of configuration
        
        Args:
            section: Section to update
            updates: Updates to apply
        """
        if section not in self.current_config:
            self.current_config[section] = {}
        
        self.current_config[section].update(updates)
        logger.info(f"Configuration section '{section}' updated")
    
    def list_saved_configs(self) -> List[Dict[str, Any]]:
        """List all saved configuration files"""
        configs = []
        
        for config_file in self.config_dir.glob("*"):
            if config_file.suffix in ['.json', '.yaml', '.yml', '.pkl']:
                try:
                    # Try to load metadata
                    if config_file.suffix == '.yaml' or config_file.suffix == '.yml':
                        with open(config_file, 'r') as f:
                            data = yaml.safe_load(f)
                    elif config_file.suffix == '.pkl':
                        with open(config_file, 'rb') as f:
                            data = pickle.load(f)
                    else:
                        with open(config_file, 'r') as f:
                            data = json.load(f)
                    
                    config_info = {
                        'filename': config_file.name,
                        'path': str(config_file),
                        'modified': datetime.fromtimestamp(config_file.stat().st_mtime).isoformat(),
                        'size': config_file.stat().st_size
                    }
                    
                    # Add metadata if available
                    if 'metadata' in data:
                        config_info.update(data['metadata'])
                    
                    configs.append(config_info)
                    
                except Exception as e:
                    logger.warning(f"Could not read config file {config_file}: {e}")
        
        return sorted(configs, key=lambda x: x['modified'], reverse=True)
    
    def delete_config(self, config_name: str) -> bool:
        """
        Delete a saved configuration
        
        Args:
            config_name: Name of configuration to delete
            
        Returns:
            True if deleted successfully
        """
        # Try different file extensions
        for ext in ['.json', '.yaml', '.yml', '.pkl']:
            config_path = self.config_dir / f"{config_name}{ext}"
            if config_path.exists():
                config_path.unlink()
                logger.info(f"Configuration '{config_name}' deleted")
                return True
        
        logger.warning(f"Configuration '{config_name}' not found")
        return False
    
    def export_config_template(self, template_type: str = 'complete') -> Dict[str, Any]:
        """
        Export configuration template for external use
        
        Args:
            template_type: Type of template ('basic', 'complete', 'minimal')
            
        Returns:
            Configuration template
        """
        if template_type == 'minimal':
            return {
                'environment': {
                    'width': 100,
                    'height': 100,
                    'num_drones': 20
                },
                'algorithm': 'greedy',
                'algorithm_params': {}
            }
        elif template_type == 'basic':
            return {
                'simulation': self.default_configs['simulation'],
                'algorithm': 'genetic_algorithm',
                'algorithm_params': self.default_configs['algorithms']['genetic_algorithm']
            }
        else:  # complete
            return self.default_configs.copy()
    
    def validate_config(self, config_data: Dict[str, Any]) -> List[str]:
        """
        Validate configuration data
        
        Args:
            config_data: Configuration to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check required fields
        if 'environment' in config_data:
            env = config_data['environment']
            if 'width' not in env or env['width'] <= 0:
                errors.append("Environment width must be positive")
            if 'height' not in env or env['height'] <= 0:
                errors.append("Environment height must be positive")
            if 'sensing_radius' not in env or env['sensing_radius'] <= 0:
                errors.append("Sensing radius must be positive")
        
        if 'drones' in config_data:
            drones = config_data['drones']
            if 'num_drones' not in drones or drones['num_drones'] <= 0:
                errors.append("Number of drones must be positive")
        
        # Validate algorithm parameters
        for algo_name, algo_config in config_data.get('algorithms', {}).items():
            if algo_name == 'genetic_algorithm':
                if algo_config.get('population_size', 0) <= 0:
                    errors.append(f"GA population size must be positive")
                if not 0 <= algo_config.get('mutation_rate', 0.1) <= 1:
                    errors.append(f"GA mutation rate must be between 0 and 1")
        
        return errors
    
    def create_experiment_config(self, base_config: str, 
                               variations: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
        """
        Create multiple experiment configurations with parameter variations
        
        Args:
            base_config: Base configuration name or data
            variations: Parameter variations to test
            
        Returns:
            List of experiment configurations
        """
        if isinstance(base_config, str):
            base_data = self.load_config(base_config)
        else:
            base_data = base_config
        
        import itertools
        
        # Generate all combinations of variations
        param_names = list(variations.keys())
        param_values = list(variations.values())
        
        experiment_configs = []
        for combination in itertools.product(*param_values):
            config = base_data.copy()
            
            # Apply parameter variations
            for param_name, param_value in zip(param_names, combination):
                # Handle nested parameters (e.g., 'drones.num_drones')
                if '.' in param_name:
                    section, key = param_name.split('.', 1)
                    if section not in config:
                        config[section] = {}
                    config[section][key] = param_value
                else:
                    config[param_name] = param_value
            
            # Add experiment metadata
            config['experiment_metadata'] = {
                'base_config': base_config if isinstance(base_config, str) else 'custom',
                'variations': dict(zip(param_names, combination)),
                'created': datetime.now().isoformat()
            }
            
            experiment_configs.append(config)
        
        return experiment_configs