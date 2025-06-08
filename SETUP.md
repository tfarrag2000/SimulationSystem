# Drone Optimization Simulation System - Setup Guide

This guide will help you set up and run the Drone Optimization Simulation System on your local machine.

## System Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Step 1: Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/drone-optimization-system.git
cd drone-optimization-system
```

## Step 2: Set Up a Virtual Environment (Recommended)

It's recommended to use a virtual environment to keep dependencies isolated:

### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Step 4: Run the Application

Start the application:

```bash
python run.py
```

By default, the application will be available at `http://127.0.0.1:8050/` in your web browser.

### Command-line Options

- `--port PORT`: Change the port number (default: 8050)
- `--debug`: Run the app in debug mode

Example:
```bash
python run.py --port 8080 --debug
```

## Step 5: Using the Simulation System

1. **Initialize the Simulation**:
   - Configure the environment settings (area size, number of drones, etc.)
   - Select an optimization algorithm
   - Configure algorithm-specific parameters
   - Click "Initialize Simulation"

2. **Run the Simulation**:
   - Use the "Step" button to advance one step at a time
   - Use the "Run Continuous" button for continuous simulation
   - Use the "Pause" button to pause a continuous run

3. **Analyze Results**:
   - The main visualization shows drone positions and coverage
   - Performance metrics tabs show coverage, power usage, and other metrics
   - Logs provide additional information about the simulation

## Configuring Different Scenarios

### Basic Drone Coverage
- Set up a standard grid area
- Configure drones and sensing radius
- Compare different optimization algorithms

### Parking Lot Scenario
- Enable the parking scenario
- Configure parking spots and disabled spots
- Run the simulation to detect parking violations

### Algorithm Experimentation
- Try different parameters for each algorithm
- Compare the performance of different algorithms
- Analyze trade-offs between coverage and power consumption

## Troubleshooting

If you encounter any issues:

1. **Missing Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Port Already in Use**:
   ```bash
   python run.py --port 8051
   ```

3. **Application Crashes**:
   Run in debug mode to see detailed error messages:
   ```bash
   python run.py --debug
   ```

## Additional Resources

- Check the `examples/` directory for example scenarios
- Refer to `docs/` for detailed documentation of each component
- See `algorithm_guide.md` for information about optimization algorithms

## Next Steps

After setting up the system, you might want to:

- Experiment with different optimization algorithms
- Adjust parameters to optimize for different objectives
- Implement custom algorithms or scenarios
- Analyze the performance data for insights

For more detailed information, refer to the [README.md](README.md) file.