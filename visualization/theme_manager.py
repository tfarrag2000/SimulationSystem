import plotly.graph_objs as go
import plotly.express as px
from typing import Dict, List, Optional

class ThemeManager:
    """
    Manages visual themes and styling for drone optimization visualizations
    """
    
    def __init__(self):
        self.themes = {
            'default': self._get_default_theme(),
            'dark': self._get_dark_theme(),
            'professional': self._get_professional_theme(),
            'colorblind': self._get_colorblind_theme(),
            'high_contrast': self._get_high_contrast_theme(),
            'research': self._get_research_theme()
        }
        
        self.current_theme = 'default'
    
    def _get_default_theme(self) -> Dict:
        """Default bright and colorful theme"""
        return {
            'name': 'default',
            'template': 'plotly_white',
            'colors': {
                'primary': '#1f77b4',
                'secondary': '#ff7f0e',
                'success': '#2ca02c',
                'danger': '#d62728',
                'warning': '#ff7f0e',
                'info': '#17a2b8',
                'background': '#ffffff',
                'text': '#212529',
                'grid': '#e0e0e0'
            },
            'drone_colors': {
                'active': '#2ca02c',
                'inactive': '#d62728',
                'low_energy': '#ff7f0e',
                'critical_energy': '#d62728'
            },
            'coverage_colors': {
                'covered': 'rgba(44, 160, 44, 0.3)',
                'uncovered': 'rgba(214, 39, 40, 0.1)',
                'overlap': 'rgba(255, 127, 14, 0.2)'
            },
            'font': {
                'family': 'Arial, sans-serif',
                'size': 12,
                'color': '#212529'
            }
        }
    
    def _get_dark_theme(self) -> Dict:
        """Dark theme for low-light environments"""
        return {
            'name': 'dark',
            'template': 'plotly_dark',
            'colors': {
                'primary': '#60a5fa',
                'secondary': '#f59e0b',
                'success': '#10b981',
                'danger': '#ef4444',
                'warning': '#f59e0b',
                'info': '#06b6d4',
                'background': '#1f2937',
                'text': '#f9fafb',
                'grid': '#374151'
            },
            'drone_colors': {
                'active': '#10b981',
                'inactive': '#ef4444',
                'low_energy': '#f59e0b',
                'critical_energy': '#ef4444'
            },
            'coverage_colors': {
                'covered': 'rgba(16, 185, 129, 0.3)',
                'uncovered': 'rgba(239, 68, 68, 0.1)',
                'overlap': 'rgba(245, 158, 11, 0.2)'
            },
            'font': {
                'family': 'Arial, sans-serif',
                'size': 12,
                'color': '#f9fafb'
            }
        }
    
    def _get_professional_theme(self) -> Dict:
        """Professional theme for presentations and reports"""
        return {
            'name': 'professional',
            'template': 'simple_white',
            'colors': {
                'primary': '#2563eb',
                'secondary': '#64748b',
                'success': '#059669',
                'danger': '#dc2626',
                'warning': '#d97706',
                'info': '#0891b2',
                'background': '#ffffff',
                'text': '#1e293b',
                'grid': '#e2e8f0'
            },
            'drone_colors': {
                'active': '#059669',
                'inactive': '#64748b',
                'low_energy': '#d97706',
                'critical_energy': '#dc2626'
            },
            'coverage_colors': {
                'covered': 'rgba(5, 150, 105, 0.25)',
                'uncovered': 'rgba(220, 38, 38, 0.1)',
                'overlap': 'rgba(217, 119, 6, 0.2)'
            },
            'font': {
                'family': 'Helvetica, Arial, sans-serif',
                'size': 11,
                'color': '#1e293b'
            }
        }
    
    def _get_colorblind_theme(self) -> Dict:
        """Colorblind-friendly theme using distinguishable colors"""
        return {
            'name': 'colorblind',
            'template': 'plotly_white',
            'colors': {
                'primary': '#1f77b4',  # Blue
                'secondary': '#ff7f0e',  # Orange
                'success': '#2ca02c',  # Green
                'danger': '#d62728',  # Red
                'warning': '#9467bd',  # Purple
                'info': '#8c564b',  # Brown
                'background': '#ffffff',
                'text': '#212529',
                'grid': '#e0e0e0'
            },
            'drone_colors': {
                'active': '#1f77b4',  # Blue for active
                'inactive': '#7f7f7f',  # Gray for inactive
                'low_energy': '#ff7f0e',  # Orange for low energy
                'critical_energy': '#d62728'  # Red for critical
            },
            'coverage_colors': {
                'covered': 'rgba(31, 119, 180, 0.3)',
                'uncovered': 'rgba(127, 127, 127, 0.1)',
                'overlap': 'rgba(255, 127, 14, 0.2)'
            },
            'font': {
                'family': 'Arial, sans-serif',
                'size': 12,
                'color': '#212529'
            }
        }
    
    def _get_high_contrast_theme(self) -> Dict:
        """High contrast theme for accessibility"""
        return {
            'name': 'high_contrast',
            'template': 'plotly_white',
            'colors': {
                'primary': '#000000',
                'secondary': '#ffffff',
                'success': '#00ff00',
                'danger': '#ff0000',
                'warning': '#ffff00',
                'info': '#0000ff',
                'background': '#ffffff',
                'text': '#000000',
                'grid': '#808080'
            },
            'drone_colors': {
                'active': '#00ff00',
                'inactive': '#ff0000',
                'low_energy': '#ffff00',
                'critical_energy': '#ff0000'
            },
            'coverage_colors': {
                'covered': 'rgba(0, 255, 0, 0.5)',
                'uncovered': 'rgba(255, 0, 0, 0.2)',
                'overlap': 'rgba(255, 255, 0, 0.3)'
            },
            'font': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': '#000000'
            }
        }
    
    def _get_research_theme(self) -> Dict:
        """Research/academic theme with muted colors"""
        return {
            'name': 'research',
            'template': 'plotly_white',
            'colors': {
                'primary': '#3366cc',
                'secondary': '#dc3912',
                'success': '#109618',
                'danger': '#990099',
                'warning': '#ff9900',
                'info': '#0099c6',
                'background': '#ffffff',
                'text': '#333333',
                'grid': '#cccccc'
            },
            'drone_colors': {
                'active': '#109618',
                'inactive': '#dc3912',
                'low_energy': '#ff9900',
                'critical_energy': '#990099'
            },
            'coverage_colors': {
                'covered': 'rgba(16, 150, 24, 0.2)',
                'uncovered': 'rgba(220, 57, 18, 0.1)',
                'overlap': 'rgba(255, 153, 0, 0.15)'
            },
            'font': {
                'family': 'Times New Roman, serif',
                'size': 11,
                'color': '#333333'
            }
        }
    
    def set_theme(self, theme_name: str):
        """Set the current theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
        else:
            raise ValueError(f"Unknown theme: {theme_name}")
    
    def get_current_theme(self) -> Dict:
        """Get the current theme configuration"""
        return self.themes[self.current_theme]
    
    def get_available_themes(self) -> List[str]:
        """Get list of available theme names"""
        return list(self.themes.keys())
    
    def apply_theme_to_figure(self, fig: go.Figure, theme_name: Optional[str] = None) -> go.Figure:
        """
        Apply theme styling to a plotly figure
        
        Args:
            fig: Plotly figure to style
            theme_name: Theme to apply (uses current theme if None)
            
        Returns:
            Styled figure
        """
        if theme_name is None:
            theme_name = self.current_theme
        
        if theme_name not in self.themes:
            theme_name = 'default'
        
        theme = self.themes[theme_name]
        
        # Apply template
        fig.update_layout(template=theme['template'])
        
        # Apply fonts
        fig.update_layout(
            font=theme['font'],
            title_font=dict(
                family=theme['font']['family'],
                size=theme['font']['size'] + 2,
                color=theme['font']['color']
            )
        )
        
        # Apply background colors
        fig.update_layout(
            plot_bgcolor=theme['colors']['background'],
            paper_bgcolor=theme['colors']['background']
        )
        
        # Apply grid colors
        fig.update_xaxes(gridcolor=theme['colors']['grid'])
        fig.update_yaxes(gridcolor=theme['colors']['grid'])
        
        return fig
    
    def get_color_palette(self, palette_name: str = 'default') -> List[str]:
        """
        Get a color palette for consistent coloring
        
        Args:
            palette_name: Name of the palette to get
            
        Returns:
            List of color codes
        """
        theme = self.themes.get(self.current_theme, self.themes['default'])
        
        if palette_name == 'algorithm_comparison':
            return [
                theme['colors']['primary'],
                theme['colors']['secondary'],
                theme['colors']['success'],
                theme['colors']['danger'],
                theme['colors']['warning'],
                theme['colors']['info']
            ]
        elif palette_name == 'energy_levels':
            return [
                theme['drone_colors']['active'],      # High energy
                theme['drone_colors']['low_energy'],  # Medium energy
                theme['drone_colors']['critical_energy']  # Low energy
            ]
        elif palette_name == 'performance':
            return [
                theme['colors']['success'],  # Good
                theme['colors']['warning'],  # Average
                theme['colors']['danger']    # Poor
            ]
        else:
            # Default palette
            return [
                theme['colors']['primary'],
                theme['colors']['secondary'],
                theme['colors']['success'],
                theme['colors']['danger']
            ]
    
    def create_custom_colorscale(self, scale_type: str = 'coverage') -> List:
        """
        Create custom colorscale for heatmaps and continuous data
        
        Args:
            scale_type: Type of colorscale ('coverage', 'energy', 'overlap')
            
        Returns:
            Plotly colorscale list
        """
        theme = self.themes[self.current_theme]
        
        if scale_type == 'coverage':
            return [
                [0.0, 'rgba(255, 255, 255, 0.8)'],  # No coverage
                [0.5, theme['coverage_colors']['covered']],  # Some coverage
                [1.0, theme['drone_colors']['active']]  # Full coverage
            ]
        elif scale_type == 'energy':
            return [
                [0.0, theme['drone_colors']['critical_energy']],  # No energy
                [0.3, theme['drone_colors']['low_energy']],       # Low energy
                [1.0, theme['drone_colors']['active']]            # Full energy
            ]
        elif scale_type == 'overlap':
            return [
                [0.0, 'rgba(255, 255, 255, 0.8)'],  # No overlap
                [0.5, theme['coverage_colors']['overlap']],  # Some overlap
                [1.0, theme['colors']['danger']]  # High overlap
            ]
        else:
            # Default viridis-like scale
            return 'Viridis'
    
    def get_drone_marker_style(self, active: bool, energy_level: float) -> Dict:
        """
        Get marker style for drone visualization based on status
        
        Args:
            active: Whether drone is active
            energy_level: Energy level (0-100)
            
        Returns:
            Dictionary with marker styling
        """
        theme = self.themes[self.current_theme]
        
        if not active:
            return {
                'size': 8,
                'color': theme['drone_colors']['inactive'],
                'symbol': 'circle',
                'opacity': 0.6,
                'line': dict(width=1, color=theme['colors']['text'])
            }
        
        # Active drone styling based on energy
        if energy_level > 75:
            color = theme['drone_colors']['active']
            size = 12
        elif energy_level > 25:
            color = theme['drone_colors']['low_energy']
            size = 10
        else:
            color = theme['drone_colors']['critical_energy']
            size = 8
        
        return {
            'size': size,
            'color': color,
            'symbol': 'triangle-up',
            'opacity': 1.0,
            'line': dict(width=2, color=theme['colors']['text'])
        }
    
    def export_theme_config(self, theme_name: str) -> Dict:
        """Export theme configuration for external use"""
        if theme_name not in self.themes:
            raise ValueError(f"Unknown theme: {theme_name}")
        
        return self.themes[theme_name].copy()
    
    def import_custom_theme(self, theme_name: str, theme_config: Dict):
        """Import a custom theme configuration"""
        # Validate required keys
        required_keys = ['colors', 'drone_colors', 'coverage_colors', 'font']
        for key in required_keys:
            if key not in theme_config:
                raise ValueError(f"Theme configuration missing required key: {key}")
        
        # Set default template if not specified
        if 'template' not in theme_config:
            theme_config['template'] = 'plotly_white'
        
        self.themes[theme_name] = theme_config

# Convenience functions for quick theme access
def get_color_palette(theme_name: str = 'default', palette_type: str = 'default') -> List[str]:
    """Get color palette for a specific theme"""
    theme_manager = ThemeManager()
    theme_manager.set_theme(theme_name)
    return theme_manager.get_color_palette(palette_type)

def apply_theme_to_figure(fig: go.Figure, theme_name: str = 'default') -> go.Figure:
    """Apply theme to figure"""
    theme_manager = ThemeManager()
    return theme_manager.apply_theme_to_figure(fig, theme_name)

def get_drone_colors(theme_name: str = 'default') -> Dict[str, str]:
    """Get drone-specific colors for a theme"""
    theme_manager = ThemeManager()
    theme = theme_manager.themes[theme_name]
    return theme['drone_colors']