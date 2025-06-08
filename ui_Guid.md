# 🚀 Complete UI Usage Guide - Parallel Processing & Experiments

## 📋 **Table of Contents**
1. [Getting Started](#getting-started)
2. [Parallel Processing Setup](#parallel-processing-setup)
3. [Running Experiments](#running-experiments)
4. [Saving & Exporting Results](#saving--exporting-results)
5. [Step-by-Step Workflow](#step-by-step-workflow)
6. [Advanced Features](#advanced-features)

---

## 🏁 **Getting Started**

### **1. Launch the Application**
```bash
python run.py
```
- Open browser to: `http://127.0.0.1:8050`
- You'll see the enhanced interface with experiment management

### **2. Interface Overview**
- **🧪 Experiment Management** (Top panel)
- **⚙️ Optimization Settings** (Left sidebar)
- **🎯 Visualization Tabs** (Main area)
- **📝 Simulation Logs** (Bottom panel)

---

## ⚡ **Parallel Processing Setup**

### **Step 1: Choose a Supported Algorithm**
Only these algorithms support parallel processing:
- ✅ **Genetic Algorithm (GA)**
- ✅ **Particle Swarm Optimization (PSO)**
- ❌ Greedy Algorithm (sequential by nature)
- ❌ Simulated Annealing (single solution approach)

### **Step 2: Enable Parallel Processing**

1. **Select GA or PSO** from the algorithm dropdown
2. **Toggle the Parallel Processing Switch**:
   ```
   ⚡ Performance Options
   [✓] Enable parallel execution
   ```
3. **View CPU Detection**: 
   - Green alert shows: "✅ Parallel processing available (8 CPU cores detected)"
   - System automatically detects your CPU cores

### **Step 3: Configure Algorithm Parameters**

#### **For Genetic Algorithm:**
```
Population Size: 50-200     (larger = more parallel benefit)
Generations: 100-500        (more generations for better results)
Mutation Rate: 0.05-0.2     (recommended range)
Crossover Rate: 0.6-0.9     (recommended range)
Elite Count: 5-20           (best solutions to preserve)
```

#### **For PSO:**
```
Swarm Size: 30-100          (larger = more parallel benefit)
Iterations: 100-500         (more iterations for convergence)
Inertia Weight: 0.4-0.9     (exploration vs exploitation)
Cognitive Weight: 1.0-2.0   (personal best influence)
Social Weight: 1.0-2.0      (global best influence)
```

### **Step 4: Verify Parallel Status**
- Green badge shows: "⚡ Parallel processing: Enabled"
- Status logs will show "[Parallel]" during execution

---

## 🧪 **Running Experiments**

### **Step 1: Start an Experiment Session**

1. **Enter Experiment Name**:
   ```
   [Experiment Name Field] → "GA_Parallel_Test_100_Drones"
   ```

2. **Click "Start Experiment"**:
   - Green alert appears: "🧪 Experiment 'GA_Parallel_Test_100_Drones' started!"
   - Active experiment card shows session details

### **Step 2: Configure Simulation Environment**

```
🌍 Environment Settings:
Area Width: 100-1000        (larger areas need more drones)
Area Height: 100-1000       (rectangular areas supported)
Total Drones: 20-100        (more drones = harder optimization)
Sensing Radius: 10-50       (affects coverage overlap)

🅿️ Parking Scenario (optional):
Parking Spots: 100-1000     (if using parking violation detection)
Disabled Spots: 5-50        (for compliance monitoring)
```

### **Step 3: Initialize and Run Simulation**

1. **Click "Initialize"**: Creates the simulation environment
2. **Choose Execution Mode**:
   - **"Step"**: Manual single-step execution
   - **"Run"**: Continuous automatic execution
   - **"Pause"**: Stop continuous execution

### **Step 4: Monitor Real-time Results**

Watch the visualization tabs:
- **🎯 Simulation View**: Drone positions and coverage areas
- **📊 Performance Metrics**: Coverage, power, overlap charts
- **🧪 Experiment Results**: Detailed experiment data

---

## 💾 **Saving & Exporting Results**

### **Step 1: Save Experiment Results**

During or after simulation:
1. **Click "Save Results"**:
   - Saves current state to experiment database
   - Shows: "✅ Experiment saved successfully! ID: exp_20231215_143052"

### **Step 2: Export Complete Data**

1. **Click "Export Data"**:
   - Creates HTML report with visualizations
   - Exports raw data in JSON forma