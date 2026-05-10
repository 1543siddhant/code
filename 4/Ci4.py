# 2 Implement DEAP (Distributed Evolutionary Algorithms) using Python.


import random
import numpy as np
from deap import base, creator, tools, algorithms

# ---------------------------------------------------
# Problem: Minimize the sphere function
# f(x) = x1^2 + x2^2 + ... + xn^2
# ---------------------------------------------------
def evaluate(individual):
    return (sum(x ** 2 for x in individual),)

# ---------------------------------------------------
# Safe creation of DEAP classes
# (prevents error if code is run multiple times)
# ---------------------------------------------------
if not hasattr(creator, "FitnessMin"):
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

if not hasattr(creator, "Individual"):
    creator.create("Individual", list, fitness=creator.FitnessMin)

# ---------------------------------------------------
# Toolbox initialization
# ---------------------------------------------------
toolbox = base.Toolbox()

# Attribute generator: random float in [-5, 5]
toolbox.register("attr_float", random.uniform, -5, 5)

# Individual: 10-dimensional vector
toolbox.register(
    "individual",
    tools.initRepeat,
    creator.Individual,
    toolbox.attr_float,
    n=10
)

# Population: list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Genetic operators
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)

def main():
    random.seed(42)
    np.random.seed(42)

    # Create initial population
    pop = toolbox.population(n=50)

    # Statistics collection
    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    # Run evolutionary algorithm
    pop, logbook = algorithms.eaSimple(
        pop,
        toolbox,
        cxpb=0.5,
        mutpb=0.2,
        ngen=50,
        stats=stats,
        verbose=True
    )

    # Best individual
    best_ind = tools.selBest(pop, k=1)[0]
    print("\nBest individual:", best_ind)
    print("Best fitness:", best_ind.fitness.values[0])

    return pop, logbook

if __name__ == "__main__":
    main()

# ### 🧬 DEAP & Genetic Algorithms: Compressed Theory

# **DEAP (Distributed Evolutionary Algorithms in Python)** is a flexible framework used to solve optimization problems by mimicking biological evolution.

# **Core Evolutionary Concepts:**

# * **Individual:** A single candidate solution (e.g., a list of 10 numbers).
# * **Population:** A group of individuals evolving together.
# * **Fitness:** A score representing the quality of a solution. In the **Sphere Function** ($f(x) = \sum x_i^2$), the goal is **minimization** (lower is better, optimum is 0).
# * **Selection:** Choosing the "fittest" individuals to pass genes to the next generation (e.g., Tournament Selection).
# * **Crossover (Mating):** Combining two parents to create offspring (e.g., Blend Crossover).
# * **Mutation:** Introducing random changes (e.g., Gaussian Mutation) to maintain diversity and explore new solutions.

# ---

# ### 🔍 Code Logic Breakdown

# 1. **`creator.create`**: Defines the "blueprint." It creates a `FitnessMin` 
# class (with negative weight for minimization) and an `Individual` class (a list with a fitness attribute).
# 2. **`toolbox.register`**: The "setup phase." It stores functions for 
# generating random numbers, creating individuals, and defining genetic operators (Mate, Mutate, Select).
# 3. **`evaluate` function**: The "judge." It calculates the sum of squares. 
# It must return a **tuple** because DEAP supports multi-objective optimization.
# 4. **`algorithms.eaSimple`**: The "engine." This built-in loop handles the entire evolutionary cycle:
# * **Selection → Crossover → Mutation → Evaluation → Replacement.**


# 5. **`tools.Statistics`**: The "monitor." It tracks the `min`, `max`, and `avg` fitness across 
# generations to prove the algorithm is converging.

# ---

# ### 📊 Understanding the Output Results

# * **Gen 0:** High fitness values (avg ~84). The population is random and far from the target.
# * **Mid Generations:** Fitness drops rapidly (avg ~8). Crossover and Selection are
# successfully "breeding" better solutions.
# * **Final Generation:** Fitness is near zero (e.g., 0.02). The solution vector 
# contains values very close to zero, proving the GA successfully optimized the Sphere function.
# * **Standard Deviation (std):** High `std` at the start means high diversity;
# low `std` at the end means the population has **converged** on the optimal solution.

# ---

# ### ✅ Why This Approach Works

# The algorithm works because it balances **Exploration** 
# (mutation and initial randomness) with **Exploitation** 
# (selecting the best and crossing them). By removing "weak" 
# individuals and keeping "strong" ones, the population naturally 
# "rolls down the hill" of the Sphere Function toward the global minimum at zero.