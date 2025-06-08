import numpy as np
import random
from multiprocessing import Pool, cpu_count
import concurrent.futures
import time

class AlgorithmResult:
    """Class to store algorithm results and metadata"""
    def __init__(self, best_solution, fitness_history, coverage, active_nodes, 
                 overlap, execution_time, algorithm_name, parameters):
        self.best_solution = best_solution
        self.fitness_history = fitness_history
        self.coverage = coverage
        self.active_nodes = active_nodes
        self.overlap = overlap
        self.execution_time = execution_time
        self.algorithm_name = algorithm_name
        self.parameters = parameters
        self.timestamp = time.time()

def convert_to_binary_activation(particle_solution, simulation):
    """Convert particle solution to binary activation array compatible with simulation"""
    activation = np.zeros(len(simulation.drones), dtype=int)
    
    # Update drone positions and activation status
    for i, particle in enumerate(particle_solution):
        if i < len(simulation.drones):
            simulation.drones.loc[i, 'x'] = np.clip(particle[0], 0, simulation.width)
            simulation.drones.loc[i, 'y'] = np.clip(particle[1], 0, simulation.height)
            activation[i] = int(particle[2]) if particle[2] > 0.5 else 0
    
    return activation

def parallel_fitness_evaluation(particles, fitness_func, num_processes=None):
    """Evaluate fitness of multiple particles in parallel"""
    if num_processes is None:
        num_processes = min(cpu_count(), len(particles))
    
    with Pool(num_processes) as pool:
        fitness_scores = pool.map(fitness_func, particles)
    
    return fitness_scores

def greedy_optimization(simulation, desired_coverage=0.95, overlap_weight=0.2, energy_weight=0.1):
    """Simple greedy algorithm for drone activation"""
    start_time = time.time()
    
    num_drones = len(simulation.drones)
    activation = np.zeros(num_drones, dtype=int)
    covered = set()
    
    # Pre-compute coverage sets for each drone
    coverage_sets = []
    for i in range(num_drones):
        drone_pos = np.array([simulation.drones.iloc[i]['x'], simulation.drones.iloc[i]['y']])
        dists = np.linalg.norm(simulation.grid_points - drone_pos, axis=1)
        coverage_sets.append(set(np.where(dists <= simulation.sensing_radius)[0]))
    
    # Activate drones one by one until desired coverage is reached
    while len(covered) / len(simulation.grid_points) < desired_coverage:
        best_idx = -1
        best_score = -np.inf
        
        for i in range(num_drones):
            if activation[i] == 1 or simulation.drones.iloc[i]['energy'] <= 5.0:
                continue
                
            new_cover = coverage_sets[i] - covered
            if not new_cover:
                continue
                
            overlap = coverage_sets[i] & covered
            energy_factor = simulation.drones.iloc[i]['energy'] / 100.0
            score = (len(new_cover) - overlap_weight * len(overlap)) * energy_factor
            
            if score > best_score:
                best_score = score
                best_idx = i
        
        if best_idx == -1:
            break
            
        activation[best_idx] = 1
        covered.update(coverage_sets[best_idx])
    
    execution_time = time.time() - start_time
    
    # Create a simple result object
    coverage_pct = len(covered) / len(simulation.grid_points) * 100
    result = AlgorithmResult(
        best_solution=None,
        fitness_history=[],
        coverage=coverage_pct,
        active_nodes=int(np.sum(activation)),
        overlap=0,
        execution_time=execution_time,
        algorithm_name="Greedy Algorithm",
        parameters={'desired_coverage': desired_coverage, 'overlap_weight': overlap_weight}
    )
    
    return activation, result

def genetic_algorithm(simulation, 
                     population_size=50,
                     num_generations=200,
                     mutation_rate=0.1,
                     crossover_rate=0.8,
                     elitism=10,
                     desired_coverage=0.90,
                     parallel_processing=False,
                     w1=0.6, w2=0.2, w3=0.2):
    """Genetic Algorithm for drone optimization"""
    
    start_time = time.time()
    
    # Extract parameters from simulation
    AreaWidth, AreaHeight = simulation.width, simulation.height
    SensingRange = simulation.sensing_radius
    NumNodes = len(simulation.drones)
    GridPoints = simulation.grid_points
    NumGridPoints = len(GridPoints)

    # Initialize population using existing drone positions
    population = []
    for _ in range(population_size):
        particle = []
        for i in range(NumNodes):
            if len(population) == 0:  # First particle uses current positions
                x, y = simulation.drones.iloc[i]['x'], simulation.drones.iloc[i]['y']
            else:
                x, y = np.random.rand(2) * [AreaWidth, AreaHeight]
            activation = np.random.randint(0, 2)
            particle.append([x, y, activation])
        population.append(np.array(particle))

    def calculate_coverage(particle):
        covered = np.zeros(len(GridPoints), dtype=bool)
        for sensor in particle:
            if sensor[2] == 1:
                distances = np.linalg.norm(GridPoints - sensor[:2], axis=1)
                covered |= distances <= SensingRange
        return (np.sum(covered) / NumGridPoints) * 100

    def calculate_overlap(particle):
        overlap_penalty = 0
        active_nodes = particle[particle[:, 2] == 1]
        for i in range(len(active_nodes)):
            for j in range(i + 1, len(active_nodes)):
                d = np.linalg.norm(active_nodes[i, :2] - active_nodes[j, :2])
                if d < 2 * SensingRange:
                    overlap_penalty += 1 - (d / (2 * SensingRange))
        return overlap_penalty

    def fitness(particle):
        coverage = calculate_coverage(particle)
        active_nodes = np.sum(particle[:, 2])
        overlap = calculate_overlap(particle)
        return w1 * coverage - w2 * (active_nodes / NumNodes) * 100 - w3 * overlap

    def mutate(particle):
        particle = particle.copy()
        coord_mask = np.random.rand(NumNodes, 2) < mutation_rate
        particle[:, :2] += (np.random.randn(NumNodes, 2) * 2) * coord_mask
        particle[:, :2] = np.clip(particle[:, :2], 0, [AreaWidth, AreaHeight])
        flip_mask = np.random.rand(NumNodes) < mutation_rate
        particle[flip_mask, 2] = 1 - particle[flip_mask, 2]
        return particle

    def crossover(parent1, parent2):
        if np.random.rand() < crossover_rate:
            cut_point = np.random.randint(1, NumNodes - 1)
            child1 = np.vstack((parent1[:cut_point], parent2[cut_point:]))
            child2 = np.vstack((parent2[:cut_point], parent1[cut_point:]))
        else:
            child1, child2 = parent1.copy(), parent2.copy()
        return child1, child2

    best_particle = None
    fitness_history = []

    # Main GA loop
    for iteration in range(num_generations):
        # Parallel or sequential fitness evaluation
        if parallel_processing:
            try:
                fitness_scores = parallel_fitness_evaluation(population, fitness)
            except:
                # Fallback to sequential if parallel fails
                fitness_scores = [fitness(p) for p in population]
        else:
            fitness_scores = [fitness(p) for p in population]
        
        # Sort population by fitness
        sorted_indices = np.argsort(fitness_scores)[::-1]
        population = [population[i] for i in sorted_indices]
        fitness_scores = [fitness_scores[i] for i in sorted_indices]
        
        # Keep track of best
        if best_particle is None or fitness_scores[0] > fitness(best_particle):
            best_particle = population[0].copy()
        
        fitness_history.append(fitness_scores[0])
        
        # Create new population
        new_population = population[:elitism]  # Keep elite
        
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:min(30, len(population))], 2)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            if len(new_population) < population_size:
                new_population.append(mutate(child2))
        
        population = new_population[:population_size]
        
        if iteration % 10 == 0:  # Print every 10 iterations
            print(f"GA Iteration {iteration + 1}: Best Fitness = {fitness_scores[0]:.2f}, "
                  f"Coverage = {calculate_coverage(best_particle):.2f}%")
        
        if calculate_coverage(best_particle) >= desired_coverage * 100:
            print(f"Stopping early: Desired coverage reached.")
            break
    
    execution_time = time.time() - start_time
    
    # Create result object
    result = AlgorithmResult(
        best_solution=best_particle,
        fitness_history=fitness_history,
        coverage=calculate_coverage(best_particle),
        active_nodes=int(np.sum(best_particle[:, 2])),
        overlap=calculate_overlap(best_particle),
        execution_time=execution_time,
        algorithm_name="Genetic Algorithm",
        parameters={
            'population_size': population_size,
            'num_generations': num_generations,
            'mutation_rate': mutation_rate,
            'crossover_rate': crossover_rate,
            'parallel_processing': parallel_processing
        }
    )
    
    # Convert to binary activation for simulation compatibility
    activation = convert_to_binary_activation(best_particle, simulation)
    return activation, result

def particle_swarm_optimization(simulation,
                               swarm_size=50,
                               iterations=300,
                               inertia=0.5,
                               cognitive_weight=1.5,
                               social_weight=1.5,
                               parallel_processing=False,
                               w1=0.7, w2=0.15, w3=0.15):
    """Particle Swarm Optimization for drone coverage"""
    
    start_time = time.time()
    
    # Extract parameters from simulation
    AreaWidth, AreaHeight = simulation.width, simulation.height
    SensingRange = simulation.sensing_radius
    NumNodes = len(simulation.drones)
    GridPoints = simulation.grid_points
    NumGridPoints = len(GridPoints)

    def calculate_coverage(particle):
        covered = np.zeros(len(GridPoints), dtype=bool)
        for sensor in particle:
            if sensor[2] == 1:
                distances = np.linalg.norm(GridPoints - sensor[:2], axis=1)
                covered |= distances <= SensingRange
        return (np.sum(covered) / NumGridPoints) * 100

    def calculate_overlap(particle):
        overlap_penalty = 0
        for i in range(len(particle)):
            for j in range(i + 1, len(particle)):
                if particle[i][2] == 1 and particle[j][2] == 1:
                    d = np.linalg.norm(particle[i][:2] - particle[j][:2])
                    if d < 2 * SensingRange:
                        overlap_penalty += 1 - (d / (2 * SensingRange))
        return overlap_penalty

    def fitness(particle):
        coverage = calculate_coverage(particle)
        active_nodes = np.sum(particle[:, 2])
        overlap = calculate_overlap(particle)
        if active_nodes < 3:
            return -float('inf')
        return w1 * coverage - w2 * (active_nodes / NumNodes) * 100 - w3 * overlap

    # Initialize particles and velocities
    particles = []
    for _ in range(swarm_size):
        particle = []
        for i in range(NumNodes):
            x, y = np.random.rand(2) * [AreaWidth, AreaHeight]
            activation = np.random.randint(0, 2)
            particle.append([x, y, activation])
        particles.append(np.array(particle))
    
    velocities = [np.random.rand(NumNodes, 3) - 0.5 for _ in range(swarm_size)]

    pbest = [p.copy() for p in particles]
    pbest_fitness = [fitness(p) for p in particles]
    gbest_idx = np.argmax(pbest_fitness)
    gbest = pbest[gbest_idx].copy()
    fitness_history = []

    for iteration in range(iterations):
        # Parallel or sequential fitness evaluation
        if parallel_processing:
            try:
                current_fitness = parallel_fitness_evaluation(particles, fitness)
            except:
                # Fallback to sequential if parallel fails
                current_fitness = [fitness(p) for p in particles]
        else:
            current_fitness = [fitness(p) for p in particles]
        
        for i in range(swarm_size):
            # Update velocity
            velocities[i] = (inertia * velocities[i] +
                           cognitive_weight * np.random.rand(NumNodes, 3) * (pbest[i] - particles[i]) +
                           social_weight * np.random.rand(NumNodes, 3) * (gbest - particles[i]))
            velocities[i] = np.clip(velocities[i], -5, 5)

            # Update position
            particles[i] += velocities[i]
            particles[i][:, 0:2] = np.clip(particles[i][:, 0:2], 0, [AreaWidth, AreaHeight])
            particles[i][:, 2] = np.where(particles[i][:, 2] > 0.5, 1, 0)

            # Update personal best
            if current_fitness[i] > pbest_fitness[i]:
                pbest[i] = particles[i].copy()
                pbest_fitness[i] = current_fitness[i]

        # Update global best
        best_idx = np.argmax(pbest_fitness)
        if pbest_fitness[best_idx] > fitness(gbest):
            gbest = pbest[best_idx].copy()

        fitness_history.append(fitness(gbest))
        
        if iteration % 20 == 0:  # Print every 20 iterations
            print(f"PSO Iteration {iteration + 1}: Best Fitness = {fitness(gbest):.2f}, "
                  f"Coverage = {calculate_coverage(gbest):.2f}%")

    execution_time = time.time() - start_time
    
    # Create result object
    result = AlgorithmResult(
        best_solution=gbest,
        fitness_history=fitness_history,
        coverage=calculate_coverage(gbest),
        active_nodes=int(np.sum(gbest[:, 2])),
        overlap=calculate_overlap(gbest),
        execution_time=execution_time,
        algorithm_name="Particle Swarm Optimization",
        parameters={
            'swarm_size': swarm_size,
            'iterations': iterations,
            'parallel_processing': parallel_processing
        }
    )
    
    activation = convert_to_binary_activation(gbest, simulation)
    return activation, result

def simulated_annealing(simulation, initial_temp=100, cooling_rate=0.95, 
                       iterations=100, min_temp=0.01, desired_coverage=0.90):
    """Simulated Annealing algorithm for drone optimization"""
    start_time = time.time()
    
    num_drones = len(simulation.drones)
    current_solution = np.ones(num_drones, dtype=int)
    
    # Ensure drones with no energy are not activated
    for i in range(num_drones):
        if simulation.drones.iloc[i]['energy'] <= 5.0:
            current_solution[i] = 0
    
    def fitness(activation):
        coverage, avg_overlap = simulation.compute_coverage(activation)
        active_count = np.sum(activation)
        
        coverage_score = coverage * 10
        drone_penalty = 0.2 * (active_count / num_drones)
        overlap_penalty = 0.1 * avg_overlap
        
        if coverage < desired_coverage:
            return 0
            
        return coverage_score - drone_penalty - overlap_penalty
    
    current_fitness = fitness(current_solution)
    best_solution = current_solution.copy()
    best_fitness = current_fitness
    fitness_history = []
    temp = initial_temp
    
    for iteration in range(iterations):
        neighbor = current_solution.copy()
        flip_indices = np.random.choice(num_drones, size=max(1, int(num_drones * 0.1)), replace=False)
        for idx in flip_indices:
            if simulation.drones.iloc[idx]['energy'] > 5.0:
                neighbor[idx] = 1 - neighbor[idx]
        
        neighbor_fitness = fitness(neighbor)
        delta_fitness = neighbor_fitness - current_fitness
        
        if delta_fitness > 0:
            current_solution = neighbor
            current_fitness = neighbor_fitness
        else:
            probability = np.exp(delta_fitness / temp) if temp > 0 else 0
            if np.random.random() < probability:
                current_solution = neighbor
                current_fitness = neighbor_fitness
        
        if current_fitness > best_fitness:
            best_solution = current_solution.copy()
            best_fitness = current_fitness
            
        fitness_history.append(best_fitness)
        temp = max(min_temp, temp * cooling_rate)
        
        if iteration % 20 == 0:
            coverage, _ = simulation.compute_coverage(best_solution)
            print(f"SA Iteration {iteration + 1}: Best Fitness = {best_fitness:.2f}, Coverage = {coverage*100:.2f}%")
    
    execution_time = time.time() - start_time
    coverage, _ = simulation.compute_coverage(best_solution)
    
    result = AlgorithmResult(
        best_solution=best_solution,
        fitness_history=fitness_history,
        coverage=coverage * 100,
        active_nodes=int(np.sum(best_solution)),
        overlap=0,
        execution_time=execution_time,
        algorithm_name="Simulated Annealing",
        parameters={'initial_temp': initial_temp, 'cooling_rate': cooling_rate, 'iterations': iterations}
    )
    
    return best_solution, result