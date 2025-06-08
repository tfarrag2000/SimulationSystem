# Optimization Algorithms Guide

This guide explains the different optimization algorithms implemented in the Drone Optimization Simulation System, how they work, and how to configure them for best results.

## Overview of the Optimization Problem

The drone optimization problem involves determining which drones to activate to achieve maximum coverage of an area while minimizing:
- Power consumption (by activating fewer drones)
- Sensor overlap (areas covered by multiple drones)

Each algorithm approaches this multi-objective optimization problem differently, with unique strengths and weaknesses.

## Greedy Algorithm

### How It Works

The Greedy Algorithm makes locally optimal choices at each step:

1. Start with all drones inactive
2. Calculate the potential coverage gain for activating each drone
3. Activate the drone that provides the best coverage-to-overlap ratio
4. Repeat until desired coverage is achieved
5. Post-pruning: Try to deactivate drones without reducing coverage below the threshold

### Key Parameters

- **Desired Coverage**: Target percentage of area to cover (0.5-1.0)
- **Overlap Weight**: How much to penalize sensor overlap (0.0-1.0)

### When to Use

- Quick solutions for simple scenarios
- When computation time is limited
- As a baseline for comparison with other algorithms

### Strengths and Weaknesses

**Strengths:**
- Fast computation time
- Simple to understand and implement
- Often finds reasonably good solutions

**Weaknesses:**
- Can get stuck in local optima
- May not find the global optimal solution
- Post-pruning may not remove all redundant drones

## Genetic Algorithm (GA)

### How It Works

The Genetic Algorithm uses principles of natural selection:

1. Initialize a population of random drone activation patterns
2. Evaluate fitness of each pattern based on coverage, active drones, and overlap
3. Select the fittest individuals to "reproduce"
4. Create "offspring" through crossover (combining patterns) and mutation (random changes)
5. Replace the old population with the new generation
6. Repeat for multiple generations to evolve better solutions

### Key Parameters

- **Population Size**: Number of candidate solutions per generation (30-100)
- **Number of Generations**: How many evolution cycles to run (50-500)
- **Mutation Rate**: Probability of random changes (0.01-0.2)
- **Crossover Rate**: Probability of combining solutions (0.6-0.9)
- **Elitism**: Number of best solutions to preserve unchanged (1-5)

### When to Use

- Complex scenarios with many drones
- When seeking high-quality solutions
- When computation time is not a major constraint

### Strengths and Weaknesses

**Strengths:**
- Can find near-optimal solutions
- Explores a wide range of possibilities
- Less likely to get stuck in local optima

**Weaknesses:**
- Slower computation time
- Results may vary between runs due to randomness
- Requires careful parameter tuning

## Particle Swarm Optimization (PSO)

### How It Works

PSO simulates a swarm of particles (potential solutions) moving through the solution space:

1. Initialize particles at random positions (continuous values between 0-1 for each drone)
2. Evaluate fitness of each particle
3. Update each particle's position based on:
   - Its own best-known position
   - The swarm's best-known position
   - Current velocity and inertia
4. Convert continuous positions to binary activation patterns (values >0.5 become active)
5. Repeat for multiple iterations as particles converge on optimal solutions

### Key Parameters

- **Swarm Size**: Number of particles (20-50)
- **Iterations**: Number of movement steps (50-200)
- **Inertia Weight**: How much particles maintain their trajectory (0.4-0.9)
- **Cognitive Factor**: How much particles are drawn to their personal best (1.0-2.0)
- **Social Factor**: How much particles are drawn to the global best (1.0-2.0)

### When to Use

- When seeking a balance between exploration and exploitation
- For problems with complex fitness landscapes
- When GA results are inconsistent

### Strengths and Weaknesses

**Strengths:**
- Often converges faster than GA
- Simple concept with few parameters
- Good balance of exploration and exploitation

**Weaknesses:**
- Can converge prematurely to local optima
- May struggle with highly constrained problems
- Discretization of continuous values can lose information

## Simulated Annealing (SA)

### How It Works

Simulated Annealing mimics the physical process of annealing in metallurgy:

1. Start with an initial solution (often all drones active)
2. Generate a neighboring solution by randomly flipping activation status of some drones
3. If the neighbor is better, accept it
4. If the neighbor is worse, accept it with a probability that decreases over time
5. Gradually "cool" the system by reducing the probability of accepting worse solutions
6. Continue until a stopping criterion is reached

### Key Parameters

- **Initial Temperature**: Starting temperature (higher = more exploration) (50-200)
- **Cooling Rate**: How quickly temperature decreases (0.8-0.99)
- **Iterations**: Number of cooling steps (100-500)

### When to Use

- When solutions might be trapped in local optima
- For problems with many constraints
- When other methods produce inconsistent results

### Strengths and Weaknesses

**Strengths:**
- Can escape local optima
- Relatively simple implementation
- Works well for combinatorial problems

**Weaknesses:**
- May require many iterations to converge
- Performance depends heavily on cooling schedule
- Can be sensitive to initial solution

## Parameter Tuning Recommendations

### General Approach

1. Start with default parameters
2. Run multiple simulations and observe trends
3. Adjust one parameter at a time and note the effect
4. Focus on parameters with the most significant impact

### Specific Recommendations

#### For Greedy Algorithm:
- If coverage is too low: Decrease overlap weight
- If too many drones are active: Increase overlap weight
- Balance between coverage and efficiency: Try overlap weights between 0.1-0.3

#### For Genetic Algorithm:
- For more reliable results: Increase population size
- For better solutions: Increase number of generations
- For more diversity: Increase mutation rate
- For faster convergence: Increase elitism

#### For PSO:
- For more exploration: Decrease inertia, increase cognitive factor
- For faster convergence: Increase inertia, increase social factor
- For better balance: Try inertia around 0.5, cognitive and social factors around 1.5

#### For Simulated Annealing:
- For more exploration: Increase initial temperature, increase cooling rate
- For faster convergence: Decrease initial temperature, decrease cooling rate
- For better solutions: Increase number of iterations

## Advanced Usage: Algorithm Comparison

When comparing algorithms, consider:

1. **Coverage Achieved**: Primary objective (higher is better)
2. **Number of Active Drones**: Measure of power efficiency (lower is better)
3. **Sensor Overlap**: Measure of redundancy (lower is better)
4. **Computation Time**: Practical consideration (faster is better)
5. **Consistency**: How results vary between runs (more consistent is better)

The best algorithm often depends on the specific scenario and constraints. It's recommended to experiment with all algorithms and choose based on your specific priorities.

## Example Scenarios

### Scenario 1: Maximum Coverage with Limited Drones
- **Best Algorithm**: Genetic Algorithm or PSO
- **Key Parameters**: Higher generations/iterations, focus on coverage

### Scenario 2: Balanced Coverage and Power Efficiency
- **Best Algorithm**: Simulated Annealing or PSO
- **Key Parameters**: Moderate temperature/cooling or balanced cognitive/social factors

### Scenario 3: Minimal Power Usage with Acceptable Coverage
- **Best Algorithm**: Greedy with Post-Pruning
- **Key Parameters**: Higher overlap weight, lower desired coverage

### Scenario 4: Real-time Optimization with Moving Targets
- **Best Algorithm**: Greedy (fastest) or PSO with small swarm size
- **Key Parameters**: Focus on speed rather than perfect optimization

## Implementing Custom Algorithms

The system architecture allows for adding custom optimization algorithms. To implement a new algorithm:

1. Create a new function in the optimization module
2. Ensure it accepts a simulation environment and relevant parameters
3. Return a binary array of drone activation states
4. Update the UI to include the new algorithm and its parameters

## Performance Considerations

- **GA and PSO** are more computationally intensive but generally produce better results
- **Greedy Algorithm** is fastest but may produce sub-optimal solutions
- **Simulated Annealing** offers a good balance of quality and speed
- For large areas or many drones, consider increasing iterations gradually