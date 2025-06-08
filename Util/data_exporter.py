import pandas as pd
import numpy as np
import json
import pickle
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import zipfile
import io
import base64

class DataExporter:
    """
    Advanced data export functionality for drone optimization experiments
    """
    
    def __init__(self, experiment_logger):
        self.logger = experiment_logger
        self.export_dir = experiment_logger.base_dir / "exports"
        self.export_dir.mkdir(exist_ok=True)
    
    def export_experiment_report(self, experiment_id, include_plots=True, format='html'):
        """
        Generate comprehensive experiment report
        
        Args:
            experiment_id: ID of experiment to export
            include_plots: Whether to include visualizations
            format: 'html', 'pdf', or 'markdown'
            
        Returns:
            str: Path to generated report
        """
        try:
            # Load experiment data
            exp_data = self.logger.load_experiment(experiment_id)
            
            # Generate report content
            report_content = self._generate_report_content(exp_data, include_plots)
            
            # Save in requested format
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"report_{experiment_id}_{timestamp}.{format}"
            output_path = self.export_dir / filename
            
            if format == 'html':
                self._save_html_report(report_content, output_path)
            elif format == 'markdown':
                self._save_markdown_report(report_content, output_path)
            elif format == 'pdf':
                self._save_pdf_report(report_content, output_path)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            return str(output_path)
            
        except Exception as e:
            raise Exception(f"Failed to export report: {str(e)}")
    
    def _generate_report_content(self, exp_data, include_plots=True):
        """Generate structured report content"""
        content = {
            'title': f"Drone Optimization Experiment Report",
            'experiment_id': exp_data['experiment_id'],
            'timestamp': exp_data['timestamp'],
            'summary': self._generate_summary_section(exp_data),
            'configuration': self._generate_config_section(exp_data),
            'results': self._generate_results_section(exp_data),
            'analysis': self._generate_analysis_section(exp_data),
            'plots': self._generate_plots_section(exp_data) if include_plots else None
        }
        
        return content
    
    def _generate_summary_section(self, exp_data):
        """Generate executive summary"""
        algo_results = exp_data['algorithm_results']
        sim_params = exp_data['simulation_parameters']
        
        return {
            'algorithm': algo_results['algorithm_name'],
            'coverage_achieved': f"{algo_results['coverage']:.2f}%",
            'active_drones': algo_results['active_nodes'],
            'total_drones': sim_params['num_drones'],
            'execution_time': f"{algo_results['execution_time']:.3f} seconds",
            'area_size': f"{sim_params['width']} x {sim_params['height']} meters",
            'sensing_radius': f"{sim_params['sensing_radius']} meters"
        }
    
    def _generate_config_section(self, exp_data):
        """Generate configuration details"""
        return {
            'algorithm_parameters': exp_data['algorithm_results']['parameters'],
            'simulation_parameters': exp_data['simulation_parameters'],
            'environment_config': exp_data['configuration']
        }
    
    def _generate_results_section(self, exp_data):
        """Generate detailed results"""
        results = exp_data['algorithm_results'].copy()
        
        # Add derived metrics
        sim_params = exp_data['simulation_parameters']
        results['drone_utilization'] = f"{(results['active_nodes'] / sim_params['num_drones'] * 100):.1f}%"
        results['coverage_per_drone'] = f"{(results['coverage'] / results['active_nodes']):.2f}%" if results['active_nodes'] > 0 else "N/A"
        
        return results
    
    def _generate_analysis_section(self, exp_data):
        """Generate analysis and insights"""
        analysis = exp_data.get('environment_analysis', {})
        
        # Performance assessment
        coverage = exp_data['algorithm_results']['coverage']
        efficiency = analysis.get('efficiency_score', 0)
        
        performance_level = "Excellent" if coverage > 90 else "Good" if coverage > 75 else "Fair" if coverage > 50 else "Poor"
        efficiency_level = "High" if efficiency > 0.8 else "Medium" if efficiency > 0.5 else "Low"
        
        insights = {
            'performance_assessment': performance_level,
            'efficiency_rating': efficiency_level,
            'recommendations': self._generate_recommendations(exp_data)
        }
        
        insights.update(analysis)
        return insights
    
    def _generate_recommendations(self, exp_data):
        """Generate optimization recommendations"""
        recommendations = []
        
        algo_results = exp_data['algorithm_results']
        coverage = algo_results['coverage']
        active_nodes = algo_results['active_nodes']
        total_nodes = exp_data['simulation_parameters']['num_drones']
        
        if coverage < 80:
            recommendations.append("Consider increasing population size or iterations for better coverage")
        
        if active_nodes / total_nodes > 0.8:
            recommendations.append("High drone utilization - consider optimizing for energy efficiency")
        
        if algo_results['execution_time'] > 10:
            recommendations.append("Consider enabling parallel processing for faster execution")
        
        if not recommendations:
            recommendations.append("Current configuration appears well-optimized")
        
        return recommendations
    
    def _generate_plots_section(self, exp_data):
        """Generate plot data for visualization"""
        plots = {}
        
        # Fitness evolution plot
        if exp_data['algorithm_results']['fitness_history']:
            plots['fitness_evolution'] = self._create_fitness_plot(exp_data['algorithm_results']['fitness_history'])
        
        # Coverage metrics plot
        if 'simulation_state' in exp_data and 'metrics_history' in exp_data['simulation_state']:
            plots['coverage_metrics'] = self._create_coverage_plot(exp_data['simulation_state']['metrics_history'])
        
        return plots
    
    def _create_fitness_plot(self, fitness_history):
        """Create fitness evolution plot"""
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(1, len(fitness_history) + 1)),
            y=fitness_history,
            mode='lines+markers',
            name='Fitness Score',
            line=dict(color='blue', width=2)
        ))
        
        fig.update_layout(
            title="Algorithm Fitness Evolution",
            xaxis_title="Iteration",
            yaxis_title="Fitness Score",
            showlegend=False
        )
        
        return fig.to_html(include_plotlyjs='cdn', div_id="fitness_plot")
    
    def _create_coverage_plot(self, metrics_history):
        """Create coverage metrics plot"""
        steps = list(range(1, len(metrics_history['coverage']) + 1))
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Coverage', 'Active Drones', 'Power Consumption', 'Overlap'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Coverage
        fig.add_trace(
            go.Scatter(x=steps, y=[c*100 for c in metrics_history['coverage']], 
                      mode='lines', name='Coverage %', line=dict(color='green')),
            row=1, col=1
        )
        
        # Active drones
        fig.add_trace(
            go.Scatter(x=steps, y=metrics_history['active_drones'], 
                      mode='lines', name='Active Drones', line=dict(color='blue')),
            row=1, col=2
        )
        
        # Power consumption
        fig.add_trace(
            go.Scatter(x=steps, y=metrics_history['power_consumption'], 
                      mode='lines', name='Power', line=dict(color='orange')),
            row=2, col=1
        )
        
        # Overlap
        fig.add_trace(
            go.Scatter(x=steps, y=metrics_history['avg_overlap'], 
                      mode='lines', name='Overlap', line=dict(color='red')),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Simulation Metrics Over Time",
            showlegend=False,
            height=600
        )
        
        return fig.to_html(include_plotlyjs='cdn', div_id="metrics_plot")
    
    def _save_html_report(self, content, output_path):
        """Save report as HTML"""
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{content['title']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .section {{ margin: 20px 0; padding: 15px; border-left: 3px solid #007bff; }}
                .metric {{ background-color: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 3px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .plot-container {{ margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{content['title']}</h1>
                <p><strong>Experiment ID:</strong> {content['experiment_id']}</p>
                <p><strong>Generated:</strong> {content['timestamp']}</p>
            </div>
            
            <div class="section">
                <h2>Executive Summary</h2>
                <div class="metric"><strong>Algorithm:</strong> {content['summary']['algorithm']}</div>
                <div class="metric"><strong>Coverage Achieved:</strong> {content['summary']['coverage_achieved']}</div>
                <div class="metric"><strong>Active Drones:</strong> {content['summary']['active_drones']} / {content['summary']['total_drones']}</div>
                <div class="metric"><strong>Execution Time:</strong> {content['summary']['execution_time']}</div>
                <div class="metric"><strong>Area Size:</strong> {content['summary']['area_size']}</div>
            </div>
            
            <div class="section">
                <h2>Configuration</h2>
                <h3>Algorithm Parameters</h3>
                <pre>{json.dumps(content['configuration']['algorithm_parameters'], indent=2)}</pre>
                <h3>Simulation Parameters</h3>
                <pre>{json.dumps(content['configuration']['simulation_parameters'], indent=2)}</pre>
            </div>
            
            <div class="section">
                <h2>Results & Analysis</h2>
                <div class="metric"><strong>Performance Assessment:</strong> {content['analysis'].get('performance_assessment', 'N/A')}</div>
                <div class="metric"><strong>Efficiency Rating:</strong> {content['analysis'].get('efficiency_rating', 'N/A')}</div>
                <h3>Recommendations</h3>
                <ul>
                    {''.join([f'<li>{rec}</li>' for rec in content['analysis'].get('recommendations', [])])}
                </ul>
            </div>
            
            {self._generate_plots_html(content.get('plots', {}))}
        </body>
        </html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
    
    def _generate_plots_html(self, plots):
        """Generate HTML for plots section"""
        if not plots:
            return ""
        
        plots_html = '<div class="section"><h2>Visualizations</h2>'
        
        for plot_name, plot_html in plots.items():
            plots_html += f'<div class="plot-container"><h3>{plot_name.replace("_", " ").title()}</h3>{plot_html}</div>'
        
        plots_html += '</div>'
        return plots_html
    
    def _save_markdown_report(self, content, output_path):
        """Save report as Markdown"""
        markdown_content = f"""# {content['title']}

**Experiment ID:** {content['experiment_id']}  
**Generated:** {content['timestamp']}

## Executive Summary

- **Algorithm:** {content['summary']['algorithm']}
- **Coverage Achieved:** {content['summary']['coverage_achieved']}
- **Active Drones:** {content['summary']['active_drones']} / {content['summary']['total_drones']}
- **Execution Time:** {content['summary']['execution_time']}
- **Area Size:** {content['summary']['area_size']}

## Configuration

### Algorithm Parameters
```json
{json.dumps(content['configuration']['algorithm_parameters'], indent=2)}
```

### Simulation Parameters
```json
{json.dumps(content['configuration']['simulation_parameters'], indent=2)}
```

## Results & Analysis

- **Performance Assessment:** {content['analysis'].get('performance_assessment', 'N/A')}
- **Efficiency Rating:** {content['analysis'].get('efficiency_rating', 'N/A')}

### Recommendations
{chr(10).join([f'- {rec}' for rec in content['analysis'].get('recommendations', [])])}

## Detailed Results
```json
{json.dumps(content['results'], indent=2)}
```
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    
    def export_comparison_report(self, experiment_ids, format='html'):
        """Export comparison report for multiple experiments"""
        try:
            comparison_data = self.logger.compare_experiments(experiment_ids)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"comparison_report_{timestamp}.{format}"
            output_path = self.export_dir / filename
            
            if format == 'html':
                self._save_comparison_html(comparison_data, output_path)
            elif format == 'csv':
                comparison_data.to_csv(output_path, index=False)
            else:
                raise ValueError(f"Unsupported format for comparison: {format}")
            
            return str(output_path)
            
        except Exception as e:
            raise Exception(f"Failed to export comparison report: {str(e)}")
    
    def _save_comparison_html(self, comparison_data, output_path):
        """Save comparison report as HTML"""
        # Create comparison visualizations
        comparison_plots = self._create_comparison_plots(comparison_data)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Algorithm Comparison Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .plot-container {{ margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Algorithm Comparison Report</h1>
                <p><strong>Generated:</strong> {datetime.now().isoformat()}</p>
                <p><strong>Experiments Compared:</strong> {len(comparison_data)}</p>
            </div>
            
            <h2>Comparison Table</h2>
            {comparison_data.to_html(classes='comparison-table', table_id='comparison', escape=False)}
            
            <h2>Visual Comparisons</h2>
            {comparison_plots}
        </body>
        </html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _create_comparison_plots(self, comparison_data):
        """Create comparison visualization plots"""
        if comparison_data.empty:
            return "<p>No data available for visualization.</p>"
        
        # Performance comparison plot
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Coverage Comparison', 'Active Nodes', 'Execution Time', 'Performance Rating'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        algorithms = comparison_data['algorithm'].tolist()
        
        # Coverage
        fig.add_trace(
            go.Bar(x=algorithms, y=comparison_data['coverage'], name='Coverage %', marker_color='green'),
            row=1, col=1
        )
        
        # Active nodes
        fig.add_trace(
            go.Bar(x=algorithms, y=comparison_data['active_nodes'], name='Active Nodes', marker_color='blue'),
            row=1, col=2
        )
        
        # Execution time
        fig.add_trace(
            go.Bar(x=algorithms, y=comparison_data['execution_time'], name='Time (s)', marker_color='orange'),
            row=2, col=1
        )
        
        # Performance rating
        fig.add_trace(
            go.Bar(x=algorithms, y=comparison_data['performance_rating'], name='Rating', marker_color='purple'),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Algorithm Performance Comparison",
            showlegend=False,
            height=600
        )
        
        return fig.to_html(include_plotlyjs='cdn', div_id="comparison_plot")
    
    def export_experiment_data(self, experiment_id, format='json'):
        """Export raw experiment data in various formats"""
        try:
            exp_data = self.logger.load_experiment(experiment_id)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"data_{experiment_id}_{timestamp}.{format}"
            output_path = self.export_dir / filename
            
            if format == 'json':
                with open(output_path, 'w') as f:
                    json.dump(exp_data, f, indent=2, default=self._json_serializer)
            elif format == 'pickle':
                with open(output_path, 'wb') as f:
                    pickle.dump(exp_data, f)
            elif format == 'csv':
                # Extract tabular data
                self._export_tabular_data(exp_data, output_path)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            return str(output_path)
            
        except Exception as e:
            raise Exception(f"Failed to export experiment data: {str(e)}")
    
    def _export_tabular_data(self, exp_data, output_path):
        """Export experiment data as CSV tables"""
        base_path = output_path.with_suffix('')
        
        # Drone positions
        if 'simulation_state' in exp_data and 'drone_positions' in exp_data['simulation_state']:
            drone_df = pd.DataFrame(exp_data['simulation_state']['drone_positions'])
            drone_df.to_csv(f"{base_path}_drones.csv", index=False)
        
        # Metrics history
        if 'simulation_state' in exp_data and 'metrics_history' in exp_data['simulation_state']:
            metrics = exp_data['simulation_state']['metrics_history']
            metrics_df = pd.DataFrame(metrics)
            metrics_df.to_csv(f"{base_path}_metrics.csv", index=False)
        
        # Algorithm results
        algo_results = exp_data['algorithm_results']
        results_df = pd.DataFrame([algo_results])
        results_df.to_csv(f"{base_path}_results.csv", index=False)
    
    def create_experiment_archive(self, experiment_ids, archive_name=None):
        """Create ZIP archive of multiple experiments"""
        if archive_name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            archive_name = f"experiments_archive_{timestamp}.zip"
        
        archive_path = self.export_dir / archive_name
        
        try:
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for exp_id in experiment_ids:
                    try:
                        # Add experiment files to archive
                        exp_data = self.logger.load_experiment(exp_id)
                        
                        # Add main experiment data
                        zipf.writestr(f"{exp_id}/experiment.json", 
                                     json.dumps(exp_data, indent=2, default=self._json_serializer))
                        
                        # Add detailed result if available
                        if 'detailed_result' in exp_data:
                            result_bytes = pickle.dumps(exp_data['detailed_result'])
                            zipf.writestr(f"{exp_id}/result.pkl", result_bytes)
                        
                        # Add report
                        report_path = self.export_experiment_report(exp_id, format='html')
                        with open(report_path, 'r', encoding='utf-8') as f:
                            zipf.writestr(f"{exp_id}/report.html", f.read())
                        
                        # Clean up temporary report
                        Path(report_path).unlink()
                        
                    except Exception as e:
                        print(f"Warning: Could not archive experiment {exp_id}: {e}")
            
            return str(archive_path)
            
        except Exception as e:
            raise Exception(f"Failed to create archive: {str(e)}")
    
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
    
    def export_algorithm_statistics(self):
        """Export comprehensive algorithm performance statistics"""
        stats = self.logger.get_algorithm_statistics()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"algorithm_statistics_{timestamp}.json"
        output_path = self.export_dir / filename
        
        with open(output_path, 'w') as f:
            json.dump(stats, f, indent=2, default=self._json_serializer)
        
        return str(output_path)