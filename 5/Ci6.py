
# Implement Ant colony optimization by solving the Traveling salesman problem using python
# Problem statement- A salesman needs to visit a set of cities exactly once and return to the original
# city. The task is to find the shortest possible route that the salesman can take to visit all the cities
# and return to the starting city.


import numpy as np
import random

# ---------------------------------------------------
# Distance matrix (example with 5 cities)
# dist[i][j] = distance from city i to city j
# ---------------------------------------------------
dist = np.array([
    [0, 2, 2, 5, 7],
    [2, 0, 4, 8, 2],
    [2, 4, 0, 1, 3],
    [5, 8, 1, 0, 2],
    [7, 2, 3, 2, 0]
], dtype=float)

n_cities = len(dist)

# ---------------------------------------------------
# ACO parameters
# ---------------------------------------------------
alpha = 1.0        # pheromone importance
beta = 2.0         # heuristic importance
evaporation = 0.5  # pheromone evaporation rate
Q = 100.0          # pheromone deposit factor

num_iterations = 50
num_ants = 10

# Initial pheromone on each edge
pheromone = np.ones((n_cities, n_cities), dtype=float)


# ---------------------------------------------------
# Function to compute total tour length
# route = [0, 2, 3, 1, 4]
# adds distance from last city back to first city
# ---------------------------------------------------
def route_length(route, dist_matrix):
    total = 0.0
    for i in range(len(route) - 1):
        total += dist_matrix[route[i]][route[i + 1]]
    total += dist_matrix[route[-1]][route[0]]
    return total


# ---------------------------------------------------
# Roulette-wheel selection for next city
# ---------------------------------------------------
def choose_next_city(current_city, unvisited, pheromone, dist_matrix, alpha, beta):
    cities = list(unvisited)

    desirabilities = []
    for city in cities:
        tau = pheromone[current_city][city] ** alpha
        eta = (1.0 / dist_matrix[current_city][city]) ** beta if dist_matrix[current_city][city] != 0 else 0.0
        desirabilities.append(tau * eta)

    total = sum(desirabilities)

    # If all probabilities become zero, choose randomly
    if total == 0:
        return random.choice(cities)

    probabilities = [d / total for d in desirabilities]

    r = random.random()
    cumulative = 0.0
    for city, prob in zip(cities, probabilities):
        cumulative += prob
        if r <= cumulative:
            return city

    # Fallback due to floating point rounding
    return cities[-1]


# ---------------------------------------------------
# Construct a complete tour for one ant
# ---------------------------------------------------
def construct_solution(start_city, pheromone, dist_matrix, alpha, beta):
    route = [start_city]
    unvisited = set(range(len(dist_matrix)))
    unvisited.remove(start_city)

    current_city = start_city
    while unvisited:
        next_city = choose_next_city(current_city, unvisited, pheromone, dist_matrix, alpha, beta)
        route.append(next_city)
        unvisited.remove(next_city)
        current_city = next_city

    return route


# ---------------------------------------------------
# Main ACO algorithm
# ---------------------------------------------------
def ant_colony_optimization(dist_matrix, num_ants=10, num_iterations=50):
    global pheromone

    best_route = None
    best_length = float("inf")

    for iteration in range(num_iterations):
        all_routes = []
        all_lengths = []

        # Each ant builds one complete tour
        for _ in range(num_ants):
            start_city = random.randint(0, n_cities - 1)
            route = construct_solution(start_city, pheromone, dist_matrix, alpha, beta)
            length = route_length(route, dist_matrix)

            all_routes.append(route)
            all_lengths.append(length)

            if length < best_length:
                best_length = length
                best_route = route.copy()

        # Evaporation
        pheromone *= (1.0 - evaporation)

        # Pheromone deposit
        for route, length in zip(all_routes, all_lengths):
            deposit = Q / length

            # Deposit on all edges in the tour
            for i in range(len(route) - 1):
                a, b = route[i], route[i + 1]
                pheromone[a][b] += deposit
                pheromone[b][a] += deposit  # symmetric TSP

            # Deposit on return edge to start city
            a, b = route[-1], route[0]
            pheromone[a][b] += deposit
            pheromone[b][a] += deposit

        print(f"Iteration {iteration + 1}: Best Length = {best_length:.4f}, Best Route = {best_route}")

    return best_route, best_length

best_route, best_length = ant_colony_optimization(dist, num_ants=num_ants, num_iterations=num_iterations)

print("\nFinal Result:")
print("Best route:", best_route)
print("Shortest distance:", best_length)


# 🐜 Ant Colony Optimization (ACO) for TSP: Compressed TheoryDefinition:ACO 
# is a metaheuristic inspired by the foraging behavior of real ants. It is used to solve the Traveling Salesman Problem (TSP),
# where the goal is to find the shortest path that visits every city once and returns to the start.Biological Mechanism:Ants deposit a chemical 
# called pheromone on the ground. Shorter paths allow ants to travel faster and more frequently, leading to a higher pheromone concentration.
# Other ants follow this trail, reinforcing the path until the colony converges on the optimal route.Key Components:Ant (Agent): Builds a solution
# city-by-city.Pheromone ($\tau$): "Memory" of the colony; represents long-term attractiveness of an edge.Heuristic ($\eta$): "Visibility"; usually $1 / \text{distance}$,
# representing immediate attractiveness.Evaporation: Gradual reduction of pheromones to prevent the algorithm from getting stuck in a sub-optimal solution (local optima).
# 🔍 Code Logic & Line Breakdownroute_length(route, dist): Calculates total distance of a tour. It must include the return edge (last city back to the first) to complete the TSP cycle.choose_next_city(...): 
#     Uses Roulette-Wheel Selection. It calculates the probability of moving to an unvisited city based on:$\text{Pheromone}^\alpha \times \text{Heuristic}^\beta$.construct_solution(...): A loop that manages the "tabu list" 
#     (visited cities) for a single ant, ensuring it visits each city exactly once.pheromone *= (1.0 - evaporation): Simulates the passage of time by decreasing pheromone levels on all paths.pheromone[a][b] += Q / length: The Reinforcement step.
#     Shorter tours (smaller length) deposit a larger amount of pheromone ($Q$).Symmetric Update ([a][b] and [b][a]): Since TSP distance is usually the same both ways, pheromone is updated in both directions to speed up convergence.✅ Summary of 
#     ImprovementsThe corrected approach ensures probabilistic consistency (probabilities always sum to 1), route integrity (no cities are skipped or duplicated), and path reinforcement (best routes are properly highlighted for future ants).
#     The result is a robust optimization tool that "evolves" from random walking to finding the most efficient travel route through collective intelligence.