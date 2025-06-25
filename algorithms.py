import numpy as np
import random
from multiprocessing import Pool, cpu_count
import concurrent.futures
import time

class AlgorithmResult:
    """Class to store algorithm results and metadata"""
    def __init__(self, best_solution, fitness_history, coverage, active_nodes, 
                 overlap, execution_time, algorithm_name, parameters,
                 coverage_history=None, overlap_history=None, active_nodes_history=None,
                 early_stop=False, stop_reason=None):
        self.best_solution = best_solution
        self.fitness_history = fitness_history
        self.coverage = coverage
        self.active_nodes = active_nodes
        self.overlap = overlap
        self.execution_time = execution_time
        self.algorithm_name = algorithm_name
        self.parameters = parameters
        self.timestamp = time.time()
        self.coverage_history = coverage_history or []
        self.overlap_history = overlap_history or []
        self.active_nodes_history = active_nodes_history or []
        self.early_stop = early_stop
        self.stop_reason = stop_reason

def convert_to_binary_activation(particle_solution, simulation):
    """Convert particle solution to binary activation array compatible with simulation"""
    activation = np.zeros(len(simulation.drones), dtype=int)
    # Ensure particle_solution is a 2D array before processing
    if particle_solution.ndim == 1:
        # Reshape if it's a flat array from GWO
        particle_solution = particle_solution.reshape((len(simulation.drones), 3))

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
    # Using a try-except block to handle potential issues with multiprocessing
    try:
        with Pool(num_processes) as pool:
            fitness_scores = pool.map(fitness_func, particles)
        return fitness_scores
    except Exception as e:
        print(f"Parallel evaluation failed: {e}. Falling back to serial evaluation.")
        return [fitness_func(p) for p in particles]


def greedy_optimization(simulation, desired_coverage=0.95, overlap_weight=0.2, energy_weight=0.1):
    """Simple greedy algorithm for drone activation"""
    start_time = time.time()
    num_drones = len(simulation.drones)
    activation = np.zeros(num_drones, dtype=int)
    covered = set()
    coverage_history = []
    active_nodes_history = []
    overlap_history = []
    
    # Pre-compute coverage sets for each drone
    coverage_sets = []
    for i in range(num_drones):
        drone_pos = np.array([simulation.drones.iloc[i]['x'], simulation.drones.iloc[i]['y']])
        dists = np.linalg.norm(simulation.grid_points - drone_pos, axis=1)
        coverage_sets.append(set(np.where(dists <= simulation.sensing_radius)[0]))
        
    # Activate drones one by one until desired coverage is reached
    early_stop = False
    stop_reason = None
    while len(covered) / len(simulation.grid_points) < desired_coverage:
        best_idx = -1
        best_score = -np.inf
        for i in range(num_drones):
            if activation[i] == 1 or simulation.drones.iloc[i]['energy'] <= 5.0:
                continue
            new_cover = coverage_sets[i] - covered
            if not new_cover:
                continue
            
            current_overlap = coverage_sets[i] & covered
            energy_factor = simulation.drones.iloc[i]['energy'] / 100.0
            score = (len(new_cover) - overlap_weight * len(current_overlap)) * energy_factor
            if score > best_score:
                best_score = score
                best_idx = i
        
        if best_idx == -1:
            stop_reason = "No more drones can improve coverage."
            break
        
        activation[best_idx] = 1
        covered.update(coverage_sets[best_idx])
        
        # Track metrics
        coverage_pct = len(covered) / len(simulation.grid_points) * 100
        coverage_history.append(coverage_pct)
        active_nodes_history.append(int(np.sum(activation)))
        # For greedy, overlap calculation is complex to track iteratively, so we set to 0
        overlap_history.append(0) 
        
        if coverage_pct >= desired_coverage * 100:
            early_stop = True
            stop_reason = "Desired coverage reached."
            break
            
    execution_time = time.time() - start_time
    final_coverage_pct = len(covered) / len(simulation.grid_points) * 100
    
    result = AlgorithmResult(
        best_solution=activation, # Greedy solution is an activation array
        fitness_history=[],
        coverage=final_coverage_pct,
        active_nodes=int(np.sum(activation)),
        overlap=0, # Simplified for greedy
        execution_time=execution_time,
        algorithm_name="Greedy Algorithm",
        parameters={'desired_coverage': desired_coverage, 'overlap_weight': overlap_weight},
        coverage_history=coverage_history,
        overlap_history=overlap_history,
        active_nodes_history=active_nodes_history,
        early_stop=early_stop,
        stop_reason=stop_reason
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
    AreaWidth, AreaHeight = simulation.width, simulation.height
    SensingRange = simulation.sensing_radius
    NumNodes = len(simulation.drones)
    GridPoints = simulation.grid_points
    NumGridPoints = len(GridPoints)
    
    def calculate_coverage(particle):
        covered = np.zeros(len(GridPoints), dtype=bool)
        for sensor in particle:
            if sensor[2] >= 0.5:
                distances = np.linalg.norm(GridPoints - sensor[:2], axis=1)
                covered |= distances <= SensingRange
        return (np.sum(covered) / NumGridPoints) * 100

    def calculate_overlap(particle):
        overlap_penalty = 0
        active_nodes = particle[particle[:, 2] >= 0.5]
        for i in range(len(active_nodes)):
            for j in range(i + 1, len(active_nodes)):
                d = np.linalg.norm(active_nodes[i, :2] - active_nodes[j, :2])
                if d < 2 * SensingRange:
                    overlap_penalty += 1 - (d / (2 * SensingRange))
        return overlap_penalty

    def fitness(particle):
        coverage = calculate_coverage(particle)
        active_nodes = np.sum(particle[:, 2] >= 0.5)
        overlap = calculate_overlap(particle)
        return w1 * coverage - w2 * (active_nodes / NumNodes) * 100 - w3 * overlap

    # Initialize Population
    population = []
    for _ in range(population_size):
        particle = np.random.rand(NumNodes, 3) * [AreaWidth, AreaHeight, 1]
        population.append(particle)
        
    def mutate(particle):
        particle = particle.copy()
        coord_mask = np.random.rand(NumNodes, 2) < mutation_rate
        particle[:, :2] += (np.random.randn(NumNodes, 2) * 2) * coord_mask
        particle[:, :2] = np.clip(particle[:, :2], 0, [AreaWidth, AreaHeight])
        flip_mask = np.random.rand(NumNodes) < mutation_rate
        particle[flip_mask, 2] = 1 - particle[flip_mask, 2] # Flip activation
        return particle

    def crossover(parent1, parent2):
        if np.random.rand() < crossover_rate:
            cut_point = np.random.randint(1, NumNodes - 1) if NumNodes > 1 else 0
            child1 = np.vstack((parent1[:cut_point], parent2[cut_point:]))
            child2 = np.vstack((parent2[:cut_point], parent1[cut_point:]))
        else:
            child1, child2 = parent1.copy(), parent2.copy()
        return child1, child2

    best_particle = None
    best_fitness = -np.inf
    fitness_history = []
    coverage_history = []
    overlap_history = []
    active_nodes_history = []
    early_stop = False
    stop_reason = None

    for iteration in range(num_generations):
        if parallel_processing:
            fitness_scores = parallel_fitness_evaluation(population, fitness)
        else:
            fitness_scores = [fitness(p) for p in population]
        
        sorted_indices = np.argsort(fitness_scores)[::-1]
        population = [population[i] for i in sorted_indices]
        fitness_scores = [fitness_scores[i] for i in sorted_indices]

        if fitness_scores[0] > best_fitness:
            best_fitness = fitness_scores[0]
            best_particle = population[0].copy()

        fitness_history.append(best_fitness)
        coverage_history.append(calculate_coverage(best_particle))
        overlap_history.append(calculate_overlap(best_particle))
        active_nodes_history.append(int(np.sum(best_particle[:, 2] >= 0.5)))
        
        new_population = population[:elitism]
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:min(30, len(population))], 2)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            if len(new_population) < population_size:
                new_population.append(mutate(child2))
        population = new_population[:population_size]
        
        if iteration % 10 == 0:
            print(f"GA Iteration {iteration + 1}: Best Fitness = {best_fitness:.2f}, "
                  f"Coverage = {coverage_history[-1]:.2f}%")
                  
        if coverage_history[-1] >= desired_coverage * 100:
            print(f"Stopping early: Desired coverage reached.")
            early_stop = True
            stop_reason = "Desired coverage reached."
            break
            
    execution_time = time.time() - start_time
    
    result = AlgorithmResult(
        best_solution=best_particle,
        fitness_history=fitness_history,
        coverage=calculate_coverage(best_particle),
        active_nodes=int(np.sum(best_particle[:, 2] >= 0.5)),
        overlap=calculate_overlap(best_particle),
        execution_time=execution_time,
        algorithm_name="Genetic Algorithm",
        parameters={
            'population_size': population_size,
            'num_generations': num_generations,
            'mutation_rate': mutation_rate,
            'crossover_rate': crossover_rate,
            'parallel_processing': parallel_processing
        },
        coverage_history=coverage_history,
        overlap_history=overlap_history,
        active_nodes_history=active_nodes_history,
        early_stop=early_stop,
        stop_reason=stop_reason
    )
    activation = convert_to_binary_activation(best_particle, simulation)
    return activation, result

def particle_swarm_optimization(simulation,
                               swarm_size=50,
                               iterations=300,
                               inertia=0.5,
                               cognitive_weight=1.5,
                               social_weight=1.5,
                               w1=0.7, w2=0.15, w3=0.15,
                               desired_coverage=0.90,
                               parallel_processing=False):
    """Particle Swarm Optimization for drone coverage"""
    start_time = time.time()
    AreaWidth, AreaHeight = simulation.width, simulation.height
    SensingRange = simulation.sensing_radius
    NumNodes = len(simulation.drones)
    GridPoints = simulation.grid_points
    NumGridPoints = len(GridPoints)
    
    def calculate_coverage(particle):
        covered = np.zeros(len(GridPoints), dtype=bool)
        for sensor in particle:
            if sensor[2] >= 0.5:
                distances = np.linalg.norm(GridPoints - sensor[:2], axis=1)
                covered |= distances <= SensingRange
        return (np.sum(covered) / NumGridPoints) * 100

    def calculate_overlap(particle):
        overlap_penalty = 0
        active_nodes = particle[particle[:, 2] >= 0.5]
        for i in range(len(active_nodes)):
            for j in range(i + 1, len(active_nodes)):
                d = np.linalg.norm(active_nodes[i, :2] - active_nodes[j, :2])
                if d < 2 * SensingRange:
                    overlap_penalty += 1 - (d / (2 * SensingRange))
        return overlap_penalty

    def fitness(particle):
        coverage = calculate_coverage(particle)
        active_nodes = np.sum(particle[:, 2] >= 0.5)
        overlap = calculate_overlap(particle)
        return w1 * coverage - w2 * (active_nodes / NumNodes) * 100 - w3 * overlap

    # Initialize particles
    particles = [np.random.rand(NumNodes, 3) * [AreaWidth, AreaHeight, 1] for _ in range(swarm_size)]
    velocities = [np.random.rand(NumNodes, 3) * 0.1 for _ in range(swarm_size)]
    
    if parallel_processing:
        pbest_fitness = parallel_fitness_evaluation(particles, fitness)
    else:
        pbest_fitness = [fitness(p) for p in particles]
        
    pbest = [p.copy() for p in particles]
    
    gbest_idx = np.argmax(pbest_fitness)
    gbest = pbest[gbest_idx].copy()
    gbest_fitness = pbest_fitness[gbest_idx]
    
    fitness_history = []
    coverage_history = []
    overlap_history = []
    active_nodes_history = []
    early_stop = False
    stop_reason = None
    
    for iteration in range(iterations):
        for i in range(swarm_size):
            # Update velocity
            velocities[i] = (inertia * velocities[i] +
                           cognitive_weight * np.random.rand() * (pbest[i] - particles[i]) +
                           social_weight * np.random.rand() * (gbest - particles[i]))
            
            # Update position
            particles[i] += velocities[i]
            
            # Apply bounds
            particles[i][:, :2] = np.clip(particles[i][:, :2], 0, [AreaWidth, AreaHeight])
            particles[i][:, 2] = np.clip(particles[i][:, 2], 0, 1)

        # Update personal best
        if parallel_processing:
            current_fitness_scores = parallel_fitness_evaluation(particles, fitness)
        else:
            current_fitness_scores = [fitness(p) for p in particles]

        for i in range(swarm_size):
            if current_fitness_scores[i] > pbest_fitness[i]:
                pbest[i] = particles[i].copy()
                pbest_fitness[i] = current_fitness_scores[i]

        # Update global best
        current_gbest_idx = np.argmax(pbest_fitness)
        if pbest_fitness[current_gbest_idx] > gbest_fitness:
            gbest = pbest[current_gbest_idx].copy()
            gbest_fitness = pbest_fitness[current_gbest_idx]
        
        fitness_history.append(gbest_fitness)
        coverage_history.append(calculate_coverage(gbest))
        overlap_history.append(calculate_overlap(gbest))
        active_nodes_history.append(int(np.sum(gbest[:, 2] >= 0.5)))
        
        if iteration % 20 == 0:
            print(f"PSO Iteration {iteration + 1}: Best Fitness = {gbest_fitness:.2f}, "
                  f"Coverage = {coverage_history[-1]:.2f}%")
                  
        if coverage_history[-1] >= desired_coverage * 100:
            print(f"Stopping early: Desired coverage reached.")
            early_stop = True
            stop_reason = "Desired coverage reached."
            break

    execution_time = time.time() - start_time
    
    result = AlgorithmResult(
        best_solution=gbest,
        fitness_history=fitness_history,
        coverage=calculate_coverage(gbest),
        active_nodes=int(np.sum(gbest[:, 2] >= 0.5)),
        overlap=calculate_overlap(gbest),
        execution_time=execution_time,
        algorithm_name="Particle Swarm Optimization",
        parameters={
            'swarm_size': swarm_size,
            'iterations': iterations,
            'inertia': inertia,
            'cognitive_weight': cognitive_weight,
            'social_weight': social_weight,
            'parallel_processing': parallel_processing
        },
        coverage_history=coverage_history,
        overlap_history=overlap_history,
        active_nodes_history=active_nodes_history,
        early_stop=early_stop,
        stop_reason=stop_reason
    )
    activation = convert_to_binary_activation(gbest, simulation)
    return activation, result

def genetic_algorithm_with_sa(simulation,
                              population_size=50,
                              num_generations=100,
                              mutation_rate=0.1,
                              crossover_rate=0.8,
                              elitism_fraction=0.2,
                              sa_temp=100,
                              sa_cooling=0.95,
                              sa_iters=30,
                              desired_coverage=0.95,
                              parallel_processing=False,
                              w1=0.6, w2=0.2, w3=0.2):
    """Genetic Algorithm with Simulated Annealing refinement for drone optimization"""
    start_time = time.time()
    AreaWidth, AreaHeight = simulation.width, simulation.height
    SensingRange = simulation.sensing_radius
    NumNodes = len(simulation.drones)
    GridPoints = simulation.grid_points
    NumGridPoints = len(GridPoints)

    def calculate_coverage(particle):
        covered = np.zeros(len(GridPoints), dtype=bool)
        for sensor in particle:
            if sensor[2] >= 0.5:
                distances = np.linalg.norm(GridPoints - sensor[:2], axis=1)
                covered |= distances <= SensingRange
        return (np.sum(covered) / NumGridPoints) * 100

    def calculate_overlap(particle):
        overlap_penalty = 0
        active_nodes = particle[particle[:, 2] >= 0.5]
        for i in range(len(active_nodes)):
            for j in range(i + 1, len(active_nodes)):
                d = np.linalg.norm(active_nodes[i, :2] - active_nodes[j, :2])
                if d < 2 * SensingRange:
                    overlap_penalty += 1 - (d / (2 * SensingRange))
        return overlap_penalty

    def fitness(particle):
        coverage = calculate_coverage(particle)
        active_nodes = np.sum(particle[:, 2] >= 0.5)
        overlap = calculate_overlap(particle)
        return w1 * coverage - w2 * (active_nodes / NumNodes) * 100 - w3 * overlap

    def crossover(parent1, parent2):
        if np.random.rand() < crossover_rate:
            point = np.random.randint(1, NumNodes -1) if NumNodes > 1 else 0
            child1 = np.vstack((parent1[:point], parent2[point:]))
            child2 = np.vstack((parent2[:point], parent1[point:]))
            return child1, child2
        else:
            return parent1.copy(), parent2.copy()

    def mutate(particle):
        mutated_particle = particle.copy()
        for i in range(NumNodes):
            if np.random.rand() < mutation_rate:
                mutated_particle[i, 0:2] = np.random.rand(2) * [AreaWidth, AreaHeight]
                mutated_particle[i, 2] = 1 - mutated_particle[i, 2] # Flip activation
        return mutated_particle
        
    def sa_refinement(particle):
        current_sol = particle.copy()
        best_sol = particle.copy()
        current_fitness = fitness(current_sol)
        best_fitness = current_fitness
        temp = sa_temp

        for _ in range(sa_iters):
            neighbor = current_sol.copy()
            # Tweak a random drone
            idx_to_tweak = np.random.randint(0, NumNodes)
            neighbor[idx_to_tweak, 0:2] += (np.random.rand(2) - 0.5) * 5 # Small position change
            neighbor[idx_to_tweak, 0:2] = np.clip(neighbor[idx_to_tweak, 0:2], 0, [AreaWidth, AreaHeight])
            if np.random.rand() < 0.2: # Chance to flip activation
                neighbor[idx_to_tweak, 2] = 1 - neighbor[idx_to_tweak, 2]

            neighbor_fitness = fitness(neighbor)
            delta = neighbor_fitness - current_fitness
            
            if delta > 0 or np.random.rand() < np.exp(delta / temp):
                current_sol = neighbor
                current_fitness = neighbor_fitness
                if current_fitness > best_fitness:
                    best_sol = current_sol
                    best_fitness = current_fitness
            
            temp *= sa_cooling
        return best_sol

    # GA Main Loop
    population = [np.random.rand(NumNodes, 3) * [AreaWidth, AreaHeight, 1] for _ in range(population_size)]
    
    best_particle = None
    best_fitness = -np.inf
    fitness_history = []
    coverage_history = []
    overlap_history = []
    active_nodes_history = []
    early_stop = False
    stop_reason = None
    
    for generation in range(num_generations):
        if parallel_processing:
            fitness_scores = parallel_fitness_evaluation(population, fitness)
        else:
            fitness_scores = [fitness(p) for p in population]

        sorted_indices = np.argsort(fitness_scores)[::-1]
        population = [population[i] for i in sorted_indices]
        fitness_scores = [fitness_scores[i] for i in sorted_indices]

        if fitness_scores[0] > best_fitness:
            best_fitness = fitness_scores[0]
            best_particle = population[0].copy()

        fitness_history.append(best_fitness)
        coverage_history.append(calculate_coverage(best_particle))
        overlap_history.append(calculate_overlap(best_particle))
        active_nodes_history.append(int(np.sum(best_particle[:, 2] >= 0.5)))

        elite_count = int(elitism_fraction * population_size)
        elites = population[:elite_count]

        # Apply SA refinement to elites
        if parallel_processing:
            refined_elites = parallel_fitness_evaluation(elites, sa_refinement)
        else:
            refined_elites = [sa_refinement(elite) for elite in elites]
        
        new_population = refined_elites
        
        # Generate new individuals
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            if len(new_population) < population_size:
                new_population.append(mutate(child2))
        
        population = new_population[:population_size]

        if generation % 10 == 0:
            print(f"GA+SA Gen {generation + 1}: Best Fitness = {best_fitness:.2f}, "
                  f"Coverage = {coverage_history[-1]:.2f}%")

        if coverage_history[-1] >= desired_coverage * 100:
            print("Stopping early: Desired coverage reached.")
            early_stop = True
            stop_reason = "Desired coverage reached."
            break

    execution_time = time.time() - start_time
    
    result = AlgorithmResult(
        best_solution=best_particle,
        fitness_history=fitness_history,
        coverage=calculate_coverage(best_particle),
        active_nodes=int(np.sum(best_particle[:, 2] >= 0.5)),
        overlap=calculate_overlap(best_particle),
        execution_time=execution_time,
        algorithm_name="Genetic Algorithm with SA",
        parameters={
            'population_size': population_size,
            'num_generations': num_generations,
            'mutation_rate': mutation_rate,
            'crossover_rate': crossover_rate,
            'elitism_fraction': elitism_fraction,
            'sa_temp': sa_temp,
            'sa_cooling': sa_cooling,
            'sa_iters': sa_iters,
            'parallel_processing': parallel_processing
        },
        coverage_history=coverage_history,
        overlap_history=overlap_history,
        active_nodes_history=active_nodes_history,
        early_stop=early_stop,
        stop_reason=stop_reason
    )

    activation = convert_to_binary_activation(best_particle, simulation)
    return activation, result

def grey_wolf_optimizer(simulation,
                        population_size=30,
                        max_iterations=100,
                        desired_coverage=0.90,
                        parallel_processing=False,
                        w1=0.6, w2=0.2, w3=0.2):
    """Grey Wolf Optimizer for drone optimization"""
    start_time = time.time()
    AreaWidth, AreaHeight = simulation.width, simulation.height
    SensingRange = simulation.sensing_radius
    NumNodes = len(simulation.drones)
    GridPoints = simulation.grid_points
    NumGridPoints = len(GridPoints)

    def calculate_coverage(particle):
        # Reshape to 2D if flat
        if particle.ndim == 1:
            particle = particle.reshape((NumNodes, 3))
        covered = np.zeros(len(GridPoints), dtype=bool)
        for sensor in particle:
            if sensor[2] >= 0.5:
                distances = np.linalg.norm(GridPoints - sensor[:2], axis=1)
                covered |= distances <= SensingRange
        return (np.sum(covered) / NumGridPoints) * 100

    def calculate_overlap(particle):
        # Reshape to 2D if flat
        if particle.ndim == 1:
            particle = particle.reshape((NumNodes, 3))
        overlap_penalty = 0
        active_nodes = particle[particle[:, 2] >= 0.5]
        for i in range(len(active_nodes)):
            for j in range(i + 1, len(active_nodes)):
                d = np.linalg.norm(active_nodes[i, :2] - active_nodes[j, :2])
                if d < 2 * SensingRange:
                    overlap_penalty += 1 - (d / (2 * SensingRange))
        return overlap_penalty
    
    def fitness(position):
        # GWO minimizes, so we negate the objective function
        coverage = calculate_coverage(position)
        active_nodes = np.sum(position.reshape(NumNodes, 3)[:, 2] >= 0.5)
        overlap = calculate_overlap(position)
        return -(w1 * coverage - w2 * (active_nodes / NumNodes) * 100 - w3 * overlap)

    # Initialize wolves
    dim = NumNodes * 3
    lb = np.tile([0, 0, 0], NumNodes)
    ub = np.tile([AreaWidth, AreaHeight, 1], NumNodes)
    wolves = np.random.uniform(0, 1, (population_size, dim)) * (ub - lb) + lb

    alpha_pos = np.zeros(dim)
    alpha_score = float("inf")
    beta_pos = np.zeros(dim)
    beta_score = float("inf")
    delta_pos = np.zeros(dim)
    delta_score = float("inf")
    
    fitness_history = []
    coverage_history = []
    overlap_history = []
    active_nodes_history = []
    early_stop = False
    stop_reason = None

    for iteration in range(max_iterations):
        if parallel_processing:
            scores = parallel_fitness_evaluation(wolves, fitness)
        else:
            scores = [fitness(w) for w in wolves]

        for i in range(population_size):
            wolves[i] = np.clip(wolves[i], lb, ub)
            score = scores[i]
            if score < alpha_score:
                alpha_score, alpha_pos = score, wolves[i].copy()
            elif score < beta_score:
                beta_score, beta_pos = score, wolves[i].copy()
            elif score < delta_score:
                delta_score, delta_pos = score, wolves[i].copy()

        a = 2 - iteration * (2 / max_iterations)

        for i in range(population_size):
            r1, r2 = np.random.rand(dim), np.random.rand(dim)
            A1, C1 = 2 * a * r1 - a, 2 * r2
            D_alpha = np.abs(C1 * alpha_pos - wolves[i])
            X1 = alpha_pos - A1 * D_alpha

            r1, r2 = np.random.rand(dim), np.random.rand(dim)
            A2, C2 = 2 * a * r1 - a, 2 * r2
            D_beta = np.abs(C2 * beta_pos - wolves[i])
            X2 = beta_pos - A2 * D_beta

            r1, r2 = np.random.rand(dim), np.random.rand(dim)
            A3, C3 = 2 * a * r1 - a, 2 * r2
            D_delta = np.abs(C3 * delta_pos - wolves[i])
            X3 = delta_pos - A3 * D_delta

            wolves[i] = (X1 + X2 + X3) / 3.0

        best_solution_2d = alpha_pos.reshape(NumNodes, 3)
        fitness_history.append(-alpha_score) # Store maximizing fitness
        coverage_history.append(calculate_coverage(best_solution_2d))
        overlap_history.append(calculate_overlap(best_solution_2d))
        active_nodes_history.append(int(np.sum(best_solution_2d[:, 2] >= 0.5)))

        if iteration % 10 == 0:
            print(f"GWO Iteration {iteration + 1}: Best Fitness = {-alpha_score:.2f}, "
                  f"Coverage = {coverage_history[-1]:.2f}%")

        if coverage_history[-1] >= desired_coverage * 100:
            print(f"Stopping early: Desired coverage reached.")
            early_stop = True
            stop_reason = "Desired coverage reached."
            break

    execution_time = time.time() - start_time
    best_solution = alpha_pos.reshape(NumNodes, 3)
    
    result = AlgorithmResult(
        best_solution=best_solution,
        fitness_history=fitness_history,
        coverage=calculate_coverage(best_solution),
        active_nodes=int(np.sum(best_solution[:, 2] >= 0.5)),
        overlap=calculate_overlap(best_solution),
        execution_time=execution_time,
        algorithm_name="Grey Wolf Optimizer",
        parameters={
            'population_size': population_size,
            'max_iterations': max_iterations,
            'parallel_processing': parallel_processing
        },
        coverage_history=coverage_history,
        overlap_history=overlap_history,
        active_nodes_history=active_nodes_history,
        early_stop=early_stop,
        stop_reason=stop_reason
    )
    activation = convert_to_binary_activation(best_solution, simulation)
    return activation, result


def manta_ray_foraging_optimization(simulation,
                                      population_size=50,
                                      num_generations=200,
                                      desired_coverage=0.95,
                                      parallel_processing=False,
                                      w1=0.6, w2=0.2, w3=0.2):
    """Manta Ray Foraging Optimization for drone optimization"""
    start_time = time.time()
    AreaWidth, AreaHeight = simulation.width, simulation.height
    SensingRange = simulation.sensing_radius
    NumNodes = len(simulation.drones)
    GridPoints = simulation.grid_points
    NumGridPoints = len(GridPoints)

    def calculate_coverage(particle):
        covered = np.zeros(len(GridPoints), dtype=bool)
        for sensor in particle:
            if sensor[2] >= 0.5:
                distances = np.linalg.norm(GridPoints - sensor[:2], axis=1)
                covered |= distances <= SensingRange
        return (np.sum(covered) / NumGridPoints) * 100

    def calculate_overlap(particle):
        overlap_penalty = 0
        active_nodes = particle[particle[:, 2] >= 0.5]
        for i in range(len(active_nodes)):
            for j in range(i + 1, len(active_nodes)):
                d = np.linalg.norm(active_nodes[i, :2] - active_nodes[j, :2])
                if d < 2 * SensingRange:
                    overlap_penalty += 1 - (d / (2 * SensingRange))
        return overlap_penalty

    def fitness(particle):
        coverage = calculate_coverage(particle)
        active_nodes = np.sum(particle[:, 2] >= 0.5)
        overlap = calculate_overlap(particle)
        return w1 * coverage - w2 * (active_nodes / NumNodes) * 100 - w3 * overlap

    def bound_particle(particle):
        particle[:, :2] = np.clip(particle[:, :2], 0, [AreaWidth, AreaHeight])
        particle[:, 2] = np.clip(particle[:, 2], 0, 1)
        return particle

    # Initialize population
    population = [bound_particle(np.random.rand(NumNodes, 3) * [AreaWidth, AreaHeight, 1]) for _ in range(population_size)]
    
    if parallel_processing:
        fitness_scores = parallel_fitness_evaluation(population, fitness)
    else:
        fitness_scores = [fitness(p) for p in population]
        
    best_particle = population[np.argmax(fitness_scores)].copy()
    best_fitness = max(fitness_scores)
    
    fitness_history = []
    coverage_history = []
    overlap_history = []
    active_nodes_history = []
    early_stop = False
    stop_reason = None
    
    # Main MRFO loop
    for t in range(num_generations):
        for i in range(population_size):
            if t / num_generations < np.random.rand():
                # Cyclone foraging (exploration)
                r = np.random.rand()
                beta = 2 * np.exp(r * (num_generations - t) / num_generations) * np.sin(2 * np.pi * r)
                if (t / num_generations) < 0.5:
                    rand_pos = np.random.rand(NumNodes, 3) * [AreaWidth, AreaHeight, 1]
                    population[i] = rand_pos + r * (rand_pos - population[i]) + beta * (rand_pos - population[i])
                else:
                    population[i] = best_particle + r * (best_particle - population[i]) + beta * (best_particle - population[i])
            else:
                # Chain foraging (exploitation)
                r = np.random.rand()
                alpha = 2 * r * np.sqrt(abs(np.log(r)))
                if i == 0:
                   population[i] = population[i] + r * (best_particle - population[i]) + alpha * (best_particle - population[i])
                else:
                   population[i] = population[i] + r * (population[i-1] - population[i]) + alpha * (best_particle - population[i])

            population[i] = bound_particle(population[i])
        
        # Somersault foraging
        for i in range(population_size):
            r1 = np.random.rand()
            r2 = np.random.rand(NumNodes, 3)
            population[i] = population[i] + (2 * r1 - 1) * best_particle - (r1 * population[i])

            population[i] = bound_particle(population[i])

        # Update fitness and best solution
        if parallel_processing:
            current_fitness_scores = parallel_fitness_evaluation(population, fitness)
        else:
            current_fitness_scores = [fitness(p) for p in population]

        for i in range(population_size):
            if current_fitness_scores[i] > best_fitness:
                 best_particle = population[i].copy()
                 best_fitness = current_fitness_scores[i]
        
        fitness_history.append(best_fitness)
        coverage_history.append(calculate_coverage(best_particle))
        overlap_history.append(calculate_overlap(best_particle))
        active_nodes_history.append(int(np.sum(best_particle[:, 2] >= 0.5)))
        
        print(f"MRFO Iteration {t + 1}: Best Fitness = {best_fitness:.2f}, "
              f"Coverage = {coverage_history[-1]:.2f}%")

        if coverage_history[-1] >= desired_coverage * 100:
            print(f"Stopping early: Desired coverage reached.")
            early_stop = True
            stop_reason = "Desired coverage reached."
            break
            
    execution_time = time.time() - start_time

    result = AlgorithmResult(
        best_solution=best_particle,
        fitness_history=fitness_history,
        coverage=calculate_coverage(best_particle),
        active_nodes=int(np.sum(best_particle[:, 2] >= 0.5)),
        overlap=calculate_overlap(best_particle),
        execution_time=execution_time,
        algorithm_name="Manta Ray Foraging Optimization",
        parameters={
            'population_size': population_size,
            'num_generations': num_generations,
            'parallel_processing': parallel_processing
        },
        coverage_history=coverage_history,
        overlap_history=overlap_history,
        active_nodes_history=active_nodes_history,
        early_stop=early_stop,
        stop_reason=stop_reason
    )
    activation = convert_to_binary_activation(best_particle, simulation)
    return activation, result
