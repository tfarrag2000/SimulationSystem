# Troubleshooting Guide

This guide helps resolve common issues encountered when using the Drone Optimization SimulationSystem.

## 🚨 Common Issues

### Installation Problems

#### ImportError: No module named 'algorithms'
**Problem**: Cannot import the algorithms module
```bash
ImportError: No module named 'algorithms'
```

**Solutions**:
```bash
# 1. Verify you're in the correct directory
cd /path/to/SimulationSystem

# 2. Check if algorithms.py exists
ls -la algorithms.py

# 3. Verify Python path
python -c "import sys; print(sys.path)"

# 4. Add current directory to path (if needed)
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### Missing Dependencies
**Problem**: Missing required packages
```bash
ModuleNotFoundError: No module named 'numpy'
```

**Solutions**:
```bash
# Install all requirements
pip install -r requirements.txt

# If requirements.txt is missing, install manually:
pip install numpy pandas matplotlib seaborn scipy

# For development dependencies:
pip install jupyter notebook ipython
```

#### Version Conflicts
**Problem**: Package version incompatibilities
```bash
ERROR: package has requirement numpy>=1.20.0, but you have numpy 1.19.0
```

**Solutions**:
```bash
# Update specific package
pip install --upgrade numpy

# Update all packages
pip install --upgrade -r requirements.txt

# Create fresh environment
python -m venv fresh_env
source fresh_env/bin/activate  # Linux/Mac
# fresh_env\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Runtime Errors

#### Memory Errors
**Problem**: Out of memory during large experiments
```bash
MemoryError: Unable to allocate array
```

**Solutions**:
```python
# 1. Reduce experiment scope
algorithms_subset = algorithms[:5]  # Test fewer algorithms
scenarios_subset = scenarios[:3]    # Test fewer scenarios

# 2. Reduce algorithm parameters
activation, result = standard_genetic(
    sim, 
    population_size=20,      # Reduced from 50
    num_generations=50       # Reduced from 200
)

# 3. Enable memory optimization
import gc
gc.collect()  # Force garbage collection

# 4. Process in batches
for i in range(0, len(algorithms), 3):  # Process 3 at a time
    batch = algorithms[i:i+3]
    # Process batch
    gc.collect()
```

#### Convergence Issues
**Problem**: Algorithms not converging
```bash
WARNING: Algorithm did not converge within 1000 iterations
```

**Solutions**:
```python
# 1. Increase iteration limits
activation, result = standard_genetic(
    sim, 
    num_generations=500,     # Increased from 200
    max_iterations=2000      # Increased limit
)

# 2. Adjust convergence tolerance
activation, result = smart_greedy_position_optimization(
    sim,
    tolerance=1e-4,          # Relaxed from 1e-6
    convergence_window=5     # Reduced from 10
)

# 3. Use staged optimization
activation, result = staged_genetic(sim, staged_mode=True)
```

#### Performance Issues
**Problem**: Slow algorithm execution
```bash
# Algorithm taking hours to complete
```

**Solutions**:
```python
# 1. Enable parallel processing
activation, result = standard_pso(
    sim, 
    parallel_processing=True,
    num_workers=4
)

# 2. Reduce problem complexity
sim = DroneSimulationEnvironment(
    area_width=30,           # Reduced from 100
    area_height=30,          # Reduced from 100
    num_drones=10,          # Reduced from 50
    drone_range=8.0
)

# 3. Use fast algorithms for initial testing
fast_algorithms = [
    'standard_greedy',
    'random_activation',
    'smart_greedy_position_optimization'
]
```

### Data and Results Issues

#### Missing Results Files
**Problem**: Results files not found
```bash
FileNotFoundError: No such file or directory: 'results/detailed_results.csv'
```

**Solutions**:
```python
# 1. Check results directory exists
import os
if not os.path.exists('results'):
    os.makedirs('results')

# 2. Verify experiment completed successfully
# Look for error messages in console output

# 3. Check for partial results
import glob
partial_results = glob.glob('results/**/detailed_results.csv', recursive=True)
print("Found results:", partial_results)

# 4. Re-run with error handling
try:
    # Run comprehensive experiment
    python comprehensive_experimental.py
except Exception as e:
    print(f"Error: {e}")
    # Check what was saved
```

#### Corrupted Results Data
**Problem**: Results data appears corrupted
```bash
pandas.errors.EmptyDataError: No columns to parse from file
```

**Solutions**:
```python
# 1. Validate CSV file
import pandas as pd
try:
    df = pd.read_csv('results/detailed_results.csv')
    print(f"Loaded {len(df)} rows successfully")
except Exception as e:
    print(f"File corruption: {e}")

# 2. Check file size
import os
file_size = os.path.getsize('results/detailed_results.csv')
if file_size == 0:
    print("File is empty - experiment may have failed")

# 3. Use backup results
backup_files = glob.glob('results/*/detailed_results.csv')
if backup_files:
    latest_backup = max(backup_files, key=os.path.getctime)
    df = pd.read_csv(latest_backup)
```

#### Inconsistent Results
**Problem**: Results vary significantly between runs
```bash
# Coverage ranges from 45% to 85% for same algorithm
```

**Solutions**:
```python
# 1. Set random seed for reproducibility
import numpy as np
np.random.seed(42)

# Run algorithm
activation, result = standard_genetic(sim, random_seed=42)

# 2. Increase number of runs for statistical validity
results = []
for run in range(10):  # Multiple runs
    activation, result = algorithm(sim)
    results.append(result.coverage)

mean_coverage = np.mean(results)
std_coverage = np.std(results)
print(f"Coverage: {mean_coverage:.1f}% ± {std_coverage:.1f}%")

# 3. Check for implementation bugs
# Review algorithm code for randomness sources
```

### Figure Generation Issues

#### Matplotlib Display Problems
**Problem**: Figures not displaying properly
```bash
UserWarning: Matplotlib is currently using agg, which is a non-GUI backend
```

**Solutions**:
```python
# 1. Set appropriate backend
import matplotlib
matplotlib.use('TkAgg')  # For GUI display
# matplotlib.use('Agg')  # For headless systems

import matplotlib.pyplot as plt

# 2. For Jupyter notebooks
%matplotlib inline

# 3. For headless servers
import matplotlib
matplotlib.use('Agg')
plt.ioff()  # Turn off interactive mode
```

#### Figure Quality Issues
**Problem**: Low-quality or blurry figures
```python
# Poor resolution figures
```

**Solutions**:
```python
# 1. Set high DPI
plt.figure(figsize=(12, 8), dpi=300)

# 2. Use vector formats
plt.savefig('figure.svg', format='svg', dpi=300, bbox_inches='tight')

# 3. Configure for publication quality
import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 12
plt.rcParams['axes.linewidth'] = 1.2
```

#### Missing Figures
**Problem**: Academic figures not generated
```bash
# No figures found in paper/figures/ directory
```

**Solutions**:
```python
# 1. Check figure generation manually
from paper_generation.generate_enhanced_figures import generate_all_academic_figures

try:
    figure_paths = generate_all_academic_figures('results/latest_experiment/')
    print("Generated figures:", figure_paths)
except Exception as e:
    print(f"Figure generation error: {e}")

# 2. Verify results data exists
import os
results_folder = 'results/comprehensive_experiment_*'
if not glob.glob(results_folder):
    print("No results data found - run experiments first")

# 3. Create figures manually
import matplotlib.pyplot as plt
# Create basic figures as fallback
```

### Paper Generation Issues

#### Document Creation Errors
**Problem**: Academic paper not generated
```bash
# automatic_academic_paper_generator.py fails
```

**Solutions**:
```python
# 1. Check dependencies
try:
    import docx
    print("python-docx installed")
except ImportError:
    print("Installing python-docx...")
    # pip install python-docx

# 2. Verify results data
from automatic_academic_paper_generator import AutomaticAcademicPaperGenerator

generator = AutomaticAcademicPaperGenerator()
try:
    paper_path = generator.generate_complete_paper()
    print(f"Paper generated: {paper_path}")
except Exception as e:
    print(f"Paper generation error: {e}")

# 3. Check permissions
import os
paper_dir = 'paper'
if not os.access(paper_dir, os.W_OK):
    print("No write permission to paper directory")
```

#### Template Errors
**Problem**: Document template issues
```bash
# Template formatting errors
```

**Solutions**:
```python
# 1. Use minimal template
generator = AutomaticAcademicPaperGenerator()
generator.use_minimal_template = True

# 2. Check template files
template_files = glob.glob('paper_generation/templates/*')
print("Available templates:", template_files)

# 3. Create basic document
from docx import Document
doc = Document()
doc.add_heading('Drone Optimization Results', 0)
doc.save('paper/basic_paper.docx')
```

## 🔧 Environment-Specific Issues

### Windows Issues

#### Path Separator Problems
**Problem**: File path issues on Windows
```bash
FileNotFoundError: [Errno 2] No such file or directory: 'results/experiment\data.csv'
```

**Solutions**:
```python
# Use os.path.join for cross-platform paths
import os
results_path = os.path.join('results', 'experiment', 'data.csv')

# Or use pathlib (recommended)
from pathlib import Path
results_path = Path('results') / 'experiment' / 'data.csv'
```

#### PowerShell Execution Policy
**Problem**: Cannot run Python scripts
```bash
execution of scripts is disabled on this system
```

**Solutions**:
```powershell
# Set execution policy for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run directly
python comprehensive_experimental.py
```

### Linux/Mac Issues

#### Permission Errors
**Problem**: Permission denied when saving files
```bash
PermissionError: [Errno 13] Permission denied: 'results/data.csv'
```

**Solutions**:
```bash
# Check directory permissions
ls -la results/

# Change permissions if needed
chmod 755 results/
chmod 644 results/*.csv

# Or create results directory with proper permissions
mkdir -p results
chmod 755 results
```

#### Display Issues on Headless Systems
**Problem**: No GUI backend available
```bash
# Running on server without display
```

**Solutions**:
```python
# Set headless backend before importing matplotlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Disable interactive mode
plt.ioff()

# Save figures instead of displaying
plt.savefig('output.png')
plt.close()
```

## 🧪 Testing and Validation

### Validate Installation
```python
# comprehensive_test.py
def test_installation():
    """Test that everything is properly installed"""
    try:
        # Test imports
        import algorithms
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        print("✅ All imports successful")
        
        # Test algorithm loading
        from algorithms import standard_greedy
        print("✅ Algorithm import successful")
        
        # Test simulation environment
        from app import DroneSimulationEnvironment
        sim = DroneSimulationEnvironment(20, 20, 5, 6.0)
        print("✅ Simulation environment created")
        
        # Test algorithm execution
        activation, result = standard_greedy(sim)
        print(f"✅ Algorithm executed: {result.coverage:.1f}% coverage")
        
        print("🎉 Installation validation complete!")
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_installation()
```

### Quick Diagnostic Script
```python
# diagnostic.py
import sys
import os
import importlib
import numpy as np

def run_diagnostics():
    """Run comprehensive system diagnostics"""
    print("🔍 System Diagnostics")
    print("=" * 50)
    
    # Python version
    print(f"Python version: {sys.version}")
    
    # Working directory
    print(f"Working directory: {os.getcwd()}")
    
    # Check key files
    key_files = ['algorithms.py', 'app.py', 'requirements.txt']
    for file in key_files:
        exists = "✅" if os.path.exists(file) else "❌"
        print(f"{exists} {file}")
    
    # Check imports
    modules = ['numpy', 'pandas', 'matplotlib', 'seaborn', 'scipy']
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - Not installed")
    
    # Memory check
    try:
        # Test memory allocation
        test_array = np.random.random((1000, 1000))
        print(f"✅ Memory allocation test passed")
        del test_array
    except MemoryError:
        print("❌ Memory allocation failed")
    
    print("=" * 50)

if __name__ == "__main__":
    run_diagnostics()
```

## 🆘 Getting Help

### Debug Mode
```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug mode
python comprehensive_experimental.py --debug
```

### Minimal Test Case
```python
# minimal_test.py - Simplest possible test
from algorithms import standard_greedy
from app import DroneSimulationEnvironment

# Minimal simulation
sim = DroneSimulationEnvironment(10, 10, 3, 4.0)
activation, result = standard_greedy(sim)
print(f"Test passed: {result.coverage:.1f}% coverage")
```

### Contact Information
When reporting issues, include:
1. **Python version**: `python --version`
2. **Operating system**: Windows/Linux/Mac
3. **Error message**: Full error traceback
4. **Code that caused the error**
5. **Expected vs. actual behavior**

### Useful Commands
```bash
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# List installed packages
pip list

# Check memory usage
python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"

# Test file permissions
python -c "import os; print('Write access:', os.access('.', os.W_OK))"
```

---
*For additional support, see [API Documentation](../api/) or [System Architecture](./system-architecture.md)*
