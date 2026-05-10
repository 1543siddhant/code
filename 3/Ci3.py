# 7 Implementation of Clonal selection algorithm using Python.


import numpy as np

# Objective function to minimize
def objective_function(x):
    return x ** 2


def clonal_selection_algorithm(
    population_size=20,
    num_selected=5,
    clone_factor=4,
    mutation_rate=0.2,
    num_generations=50,
    search_space=(-10, 10),
    seed=42
):
    """
    Clonal Selection Algorithm for minimization.

    Parameters:
    population_size  : number of antibodies in population
    num_selected     : number of best antibodies selected each generation
    clone_factor     : controls number of clones per selected antibody
    mutation_rate    : base mutation strength
    num_generations  : number of iterations
    search_space     : (min, max) range of x
    seed             : random seed for reproducibility
    """

    rng = np.random.default_rng(seed)

    # Initialize random population
    population = rng.uniform(search_space[0], search_space[1], population_size)

    best_solution = None
    best_fitness = float('inf')

    for generation in range(num_generations):
        # Evaluate fitness of current population
        fitness = np.array([objective_function(x) for x in population])

        # Sort population by fitness (ascending for minimization)
        sorted_indices = np.argsort(fitness)
        population = population[sorted_indices]
        fitness = fitness[sorted_indices]

        # Store global best solution
        if fitness[0] < best_fitness:
            best_fitness = fitness[0]
            best_solution = population[0]

        # Select best antibodies
        selected_antibodies = population[:num_selected]
        selected_fitness = fitness[:num_selected]

        # Cloning and hypermutation
        clones = []
        for i, antibody in enumerate(selected_antibodies):
            # Better antibodies get more clones
            num_clones = max(1, clone_factor * (num_selected - i))

            # Better antibodies mutate less, worse selected antibodies mutate more
            if len(selected_fitness) > 1:
                normalized_rank = (selected_fitness[i] - selected_fitness.min()) / (
                    selected_fitness.max() - selected_fitness.min() + 1e-12
                )
            else:
                normalized_rank = 0.0

            sigma = mutation_rate * (0.1 + normalized_rank)

            for _ in range(num_clones):
                clone = antibody + rng.normal(0, sigma)
                clone = np.clip(clone, search_space[0], search_space[1])
                clones.append(clone)

        clones = np.array(clones)

        # Evaluate clones
        clone_fitness = np.array([objective_function(x) for x in clones])

        # Create next generation:
        # keep the best clones and add random immigrants for diversity
        random_immigrants = rng.uniform(search_space[0], search_space[1], population_size)

        combined_population = np.concatenate((clones, random_immigrants))
        combined_fitness = np.array([objective_function(x) for x in combined_population])

        # Select best individuals for next generation
        next_indices = np.argsort(combined_fitness)[:population_size]
        population = combined_population[next_indices]

        print(f"Generation {generation + 1}: Best Fitness = {best_fitness:.6f}, Best Solution = {best_solution:.6f}")

    return best_solution, best_fitness


# Parameters
population_size = 20
num_selected = 5
clone_factor = 4
mutation_rate = 0.2
num_generations = 50
search_space = (-10, 10)

best_solution, best_fitness = clonal_selection_algorithm(
    population_size=population_size,
    num_selected=num_selected,
    clone_factor=clone_factor,
    mutation_rate=mutation_rate,
    num_generations=num_generations,
    search_space=search_space
)

print("\nFinal Result:")
print(f"Best Solution: {best_solution}")
print(f"Best Fitness: {best_fitness}")


# ### 🧬 Clonal Selection Algorithm (CSA) Theory

# **Definition:**
# CSA is an Artificial Immune System (AIS) inspired by the **Clonal Selection Theory** of acquired immunity. It mimics how the body’s immune system identifies antigens (problems) and produces specific antibodies (solutions) to neutralize them.

# **Core Principles:**

# * **Antibodies & Antigens:** In optimization, a **solution** is an antibody, and the **objective function** is the antigen.
# * **Affinity:** This represents the **fitness** of a solution. Higher affinity means a better solution.
# * **Cloning:** High-affinity antibodies are cloned (duplicated). The number of clones is proportional to affinity—the better the solution, the more offspring it produces.
# * **Hypermutation:** Clones undergo mutation. The mutation rate is **inversely proportional** to affinity:
# * *High-affinity solutions* mutate slightly (fine-tuning/exploitation).
# * *Low-affinity solutions* mutate significantly (broad searching/exploration).


# * **Receptor Editing:** A percentage of the population is replaced with random individuals to maintain diversity and avoid local optima.

# ---

# ### 🚀 Algorithm Flow (Step-by-Step)

# 1. **Initialize:** Generate a random population of antibodies.
# 2. **Evaluate:** Calculate the affinity (fitness) of each antibody against the antigen.
# 3. **Select:** Pick the $n$ best antibodies based on affinity.
# 4. **Clone:** Duplicate these antibodies (better solutions get more clones).
# 5. **Hypermutate:** Mutate clones based on their rank; the best stay relatively stable, the worst change drastically.
# 6. **Re-evaluate:** Check the fitness of the new clones.
# 7. **Reselect & Replace:** Keep the best clones for the next generation and introduce random "immigrants" to keep the population diverse.
# 8. **Repeat:** Continue until the maximum generations are reached.