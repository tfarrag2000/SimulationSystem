import json
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import pickle
import logging

logger = logging.getLogger(__name__)

class ExperimentLogger:
    """
    Experiment logging and management system for drone optimization
    """
    
    def __init__(self, base_dir="experiments"):
        """Initialize experiment logger"""
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.base_dir / "raw_data").mkdir(exist_ok=True)
        (self.base_dir / "results").mkdir(exist_ok=True)
        (self.base_dir / "logs").mkdir(exist_ok=True)
        
        self.current_experiment = None
        
    def log_experiment(self, experiment_data):
        """
        Log a complete experiment
        
        Args:
            experiment_data: Dictionary containing experiment information
            
        Returns:
            str: Experiment ID
        """
        try:
            # Generate unique experiment ID
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            exp_id = f"exp_{timestamp}"
            
            # Add metadata
            experiment_data['metadata'] = {
                'experiment_id': exp_id,
                'timestamp': datetime.now().isoformat(),
                'version': '1.0'
            }
            
            # Save main experiment file
            exp_file = self.base_dir / "results" / f"{exp_id}.json"
            with open(exp_file, 'w') as f:
                json.dump(experiment_data, f, indent=2, default=self._json_serializer)
            
            # Save detailed results if available
            if 'detailed_result' in experiment_data:
                detail_file = self.base_dir / "raw_data" / f"{exp_id}_detail.pkl"
                with open(detail_file, 'wb') as f:
                    pickle.dump(experiment_data['detailed_result'], f)
            
            logger.info(f"Experiment {exp_id} logged successfully")
            return exp_id
            
        except Exception as e:
            logger.error(f"Failed to log experiment: {str(e)}")
            raise
    
    def load_experiment(self, exp_id):
        """
        Load experiment data
        
        Args:
            exp_id: Experiment ID
            
        Returns:
            dict: Experiment data
        """
        try:
            exp_file = self.base_dir / "results" / f"{exp_id}.json"
            if not exp_file.exists():
                raise FileNotFoundError(f"Experiment {exp_id} not found")
            
            with open(exp_file, 'r') as f:
                data = json.load(f)
            
            # Load detailed results if available
            detail_file = self.base_dir / "raw_data" / f"{exp_id}_detail.pkl"
            if detail_file.exists():
                with open(detail_file, 'rb') as f:
                    data['detailed_result'] = pickle.load(f)
            
            return data
            
        except Exception as e:
            logger.error(f"Failed to load experiment {exp_id}: {str(e)}")
            raise
    
    def list_experiments(self):
        """
        List all available experiments
        
        Returns:
            list: List of experiment information
        """
        experiments = []
        results_dir = self.base_dir / "results"
        
        for exp_file in results_dir.glob("exp_*.json"):
            try:
                with open(exp_file, 'r') as f:
                    data = json.load(f)
                
                exp_info = {
                    'experiment_id': data.get('metadata', {}).get('experiment_id', exp_file.stem),
                    'timestamp': data.get('metadata', {}).get('timestamp', 'Unknown'),
                    'algorithm': data.get('algorithm_results', {}).get('algorithm_name', 'Unknown'),
                    'coverage': data.get('algorithm_results', {}).get('coverage', 0),
                    'file': str(exp_file)
                }
                experiments.append(exp_info)
                
            except Exception as e:
                logger.warning(f"Could not read experiment file {exp_file}: {e}")
        
        return sorted(experiments, key=lambda x: x['timestamp'], reverse=True)
    
    def compare_experiments(self, exp_ids):
        """
        Compare multiple experiments
        
        Args:
            exp_ids: List of experiment IDs
            
        Returns:
            pandas.DataFrame: Comparison data
        """
        comparison_data = []
        
        for exp_id in exp_ids:
            try:
                data = self.load_experiment(exp_id)
                algo_results = data.get('algorithm_results', {})
                sim_params = data.get('simulation_parameters', {})
                
                comparison_row = {
                    'experiment_id': exp_id,
                    'algorithm': algo_results.get('algorithm_name', 'Unknown'),
                    'coverage': algo_results.get('coverage', 0),
                    'active_nodes': algo_results.get('active_nodes', 0),
                    'execution_time': algo_results.get('execution_time', 0),
                    'num_drones': sim_params.get('num_drones', 0),
                    'area_size': f"{sim_params.get('width', 0)}x{sim_params.get('height', 0)}",
                    'sensing_radius': sim_params.get('sensing_radius', 0),
                    'timestamp': data.get('metadata', {}).get('timestamp', 'Unknown')
                }
                
                # Calculate derived metrics
                if comparison_row['active_nodes'] > 0:
                    comparison_row['efficiency'] = comparison_row['coverage'] / comparison_row['active_nodes']
                    comparison_row['utilization'] = comparison_row['active_nodes'] / comparison_row['num_drones']
                else:
                    comparison_row['efficiency'] = 0
                    comparison_row['utilization'] = 0
                
                # Performance rating (simple scoring)
                coverage_score = min(comparison_row['coverage'], 100) / 100 * 40
                efficiency_score = min(comparison_row['efficiency'], 10) / 10 * 30
                utilization_score = comparison_row['utilization'] * 30
                comparison_row['performance_rating'] = coverage_score + efficiency_score + utilization_score
                
                comparison_data.append(comparison_row)
                
            except Exception as e:
                logger.warning(f"Could not load experiment {exp_id} for comparison: {e}")
        
        return pd.DataFrame(comparison_data)
    
    def delete_experiment(self, exp_id):
        """
        Delete an experiment
        
        Args:
            exp_id: Experiment ID to delete
            
        Returns:
            bool: Success status
        """
        try:
            # Delete main file
            exp_file = self.base_dir / "results" / f"{exp_id}.json"
            if exp_file.exists():
                exp_file.unlink()
            
            # Delete detailed results
            detail_file = self.base_dir / "raw_data" / f"{exp_id}_detail.pkl"
            if detail_file.exists():
                detail_file.unlink()
            
            logger.info(f"Experiment {exp_id} deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete experiment {exp_id}: {str(e)}")
            return False
    
    def get_algorithm_statistics(self):
        """
        Get statistics across all experiments grouped by algorithm
        
        Returns:
            dict: Algorithm performance statistics
        """
        experiments = self.list_experiments()
        
        if not experiments:
            return {}
        
        # Group by algorithm
        algorithm_stats = {}
        
        for exp in experiments:
            algorithm = exp['algorithm']
            if algorithm not in algorithm_stats:
                algorithm_stats[algorithm] = {
                    'count': 0,
                    'coverages': [],
                    'execution_times': [],
                    'avg_coverage': 0,
                    'avg_execution_time': 0,
                    'best_coverage': 0,
                    'worst_coverage': 100
                }
            
            stats = algorithm_stats[algorithm]
            stats['count'] += 1
            stats['coverages'].append(exp['coverage'])
            
            # Load full experiment for execution time
            try:
                full_data = self.load_experiment(exp['experiment_id'])
                exec_time = full_data.get('algorithm_results', {}).get('execution_time', 0)
                stats['execution_times'].append(exec_time)
            except:
                stats['execution_times'].append(0)
        
        # Calculate statistics
        for algorithm, stats in algorithm_stats.items():
            if stats['coverages']:
                stats['avg_coverage'] = np.mean(stats['coverages'])
                stats['std_coverage'] = np.std(stats['coverages'])
                stats['best_coverage'] = np.max(stats['coverages'])
                stats['worst_coverage'] = np.min(stats['coverages'])
            
            if stats['execution_times']:
                stats['avg_execution_time'] = np.mean(stats['execution_times'])
                stats['std_execution_time'] = np.std(stats['execution_times'])
        
        return algorithm_stats
    
    def export_summary_report(self):
        """
        Export a summary report of all experiments
        
        Returns:
            dict: Summary report
        """
        experiments = self.list_experiments()
        algorithm_stats = self.get_algorithm_statistics()
        
        report = {
            'summary': {
                'total_experiments': len(experiments),
                'algorithms_tested': len(algorithm_stats),
                'date_range': {
                    'earliest': min([exp['timestamp'] for exp in experiments]) if experiments else None,
                    'latest': max([exp['timestamp'] for exp in experiments]) if experiments else None
                }
            },
            'algorithm_performance': algorithm_stats,
            'recent_experiments': experiments[:10],  # Last 10 experiments
            'generated': datetime.now().isoformat()
        }
        
        return report
    
    def _json_serializer(self, obj):
        """JSON serializer for complex objects"""
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict('records')
        elif isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return str(obj)
    
    def start_experiment_session(self, experiment_config):
        """
        Start a new experiment session
        
        Args:
            experiment_config: Configuration for the experiment
            
        Returns:
            str: Session ID
        """
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.current_experiment = {
            'session_id': session_id,
            'config': experiment_config,
            'start_time': datetime.now(),
            'results': []
        }
        
        return session_id
    
    def log_step_result(self, step_data):
        """
        Log results from a simulation step
        
        Args:
            step_data: Data from simulation step
        """
        if self.current_experiment:
            self.current_experiment['results'].append({
                'timestamp': datetime.now().isoformat(),
                'data': step_data
            })
    
    def end_experiment_session(self):
        """
        End current experiment session and save results
        
        Returns:
            str: Experiment ID
        """
        if not self.current_experiment:
            raise ValueError("No active experiment session")
        
        # Prepare final experiment data
        experiment_data = {
            'session_id': self.current_experiment['session_id'],
            'configuration': self.current_experiment['config'],
            'start_time': self.current_experiment['start_time'].isoformat(),
            'end_time': datetime.now().isoformat(),
            'step_results': self.current_experiment['results'],
            'summary': self._generate_session_summary()
        }
        
        exp_id = self.log_experiment(experiment_data)
        self.current_experiment = None
        
        return exp_id
    
    def _generate_session_summary(self):
        """Generate summary for current session"""
        if not self.current_experiment or not self.current_experiment['results']:
            return {}
        
        results = self.current_experiment['results']
        
        return {
            'total_steps': len(results),
            'duration': (datetime.now() - self.current_experiment['start_time']).total_seconds(),
            'final_coverage': results[-1]['data'].get('coverage', 0) if results else 0,
            'avg_active_drones': np.mean([r['data'].get('active_drones', 0) for r in results]),
            'total_power_consumption': sum([r['data'].get('power_consumption', 0) for r in results])
        }