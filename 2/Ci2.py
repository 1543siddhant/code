# Optimization of genetic algorithm parameter in hybrid genetic algorithm-neural network
# modelling: Application to spray drying of coconut milk.

import numpy as np
import pandas as pd
import random
import warnings

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

warnings.filterwarnings("ignore")

# ---------------------------------------------------
# 1. LOAD DATASET
# ---------------------------------------------------
# If your file has no header, this code works directly.
# If your file has a header, it will still handle it by converting
# numeric feature columns safely.

df = pd.read_csv("iris.data.csv", header=None)
df = df.dropna()

# Standard Iris dataset has 5 columns:
# 4 features + 1 target label
df.columns = ["sepal_length", "sepal_width", "petal_length", "petal_width", "class"]

# Convert feature columns to numeric
for col in ["sepal_length", "sepal_width", "petal_length", "petal_width"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows that became NaN after conversion
df = df.dropna()

# Encode target labels
le = LabelEncoder()
df["class"] = le.fit_transform(df["class"])

X = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]].values
y = df["class"].values

# ---------------------------------------------------
# 2. DATA PREPROCESSING
# ---------------------------------------------------
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split into train, validation, and test sets
X_train_full, X_test, y_train_full, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

X_train, X_val, y_train, y_val = train_test_split(
    X_train_full, y_train_full, test_size=0.25, random_state=42, stratify=y_train_full
)

# ---------------------------------------------------
# 3. GENETIC ALGORITHM SETTINGS
# ---------------------------------------------------
random.seed(42)
np.random.seed(42)

POPULATION_SIZE = 8
GENERATIONS = 8
MUTATION_RATE = 0.3

# Gene representation:
# [hidden_neurons, learning_rate, activation_index]
# activation_index: 0 -> relu, 1 -> tanh, 2 -> logistic

activation_map = {
    0: "relu",
    1: "tanh",
    2: "logistic"
}

def create_individual():
    hidden_neurons = random.randint(2, 20)
    learning_rate = round(random.uniform(0.001, 0.1), 4)
    activation_index = random.randint(0, 2)
    return [hidden_neurons, learning_rate, activation_index]

# ---------------------------------------------------
# 4. FITNESS FUNCTION
# ---------------------------------------------------
# Fitness = validation accuracy
# Higher accuracy means better individual.

def fitness(individual):
    hidden_neurons = int(individual[0])
    learning_rate = float(individual[1])
    activation_index = int(individual[2])

    activation = activation_map[activation_index]

    model = MLPClassifier(
        hidden_layer_sizes=(hidden_neurons,),
        activation=activation,
        solver="adam",
        learning_rate_init=learning_rate,
        max_iter=2000,
        random_state=42
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_val)
    acc = accuracy_score(y_val, predictions)
    return acc

# ---------------------------------------------------
# 5. SELECTION: TOURNAMENT SELECTION
# ---------------------------------------------------
def tournament_selection(scored_population, k=3):
    participants = random.sample(scored_population, k)
    participants.sort(key=lambda x: x[1], reverse=True)
    return participants[0][0]

# ---------------------------------------------------
# 6. CROSSOVER
# ---------------------------------------------------
def crossover(parent1, parent2):
    point = random.randint(1, 2)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# ---------------------------------------------------
# 7. MUTATION
# ---------------------------------------------------
def mutate(individual):
    # Mutate hidden neurons
    if random.random() < MUTATION_RATE:
        individual[0] = random.randint(2, 20)

    # Mutate learning rate
    if random.random() < MUTATION_RATE:
        individual[1] = round(random.uniform(0.001, 0.1), 4)

    # Mutate activation function
    if random.random() < MUTATION_RATE:
        individual[2] = random.randint(0, 2)

    return individual

# ---------------------------------------------------
# 8. INITIAL POPULATION
# ---------------------------------------------------
population = [create_individual() for _ in range(POPULATION_SIZE)]

best_individual = None
best_fitness = -1

# ---------------------------------------------------
# 9. GENETIC ALGORITHM LOOP
# ---------------------------------------------------
for generation in range(GENERATIONS):
    scored_population = []

    for individual in population:
        score = fitness(individual)
        scored_population.append((individual, score))

        if score > best_fitness:
            best_fitness = score
            best_individual = individual.copy()

    scored_population.sort(key=lambda x: x[1], reverse=True)

    print(f"Generation {generation + 1}")
    print(f"Best Individual: {scored_population[0][0]}")
    print(f"Validation Accuracy: {scored_population[0][1]:.4f}")
    print("-" * 50)

    # Elitism: keep the best 2 individuals
    new_population = [
        scored_population[0][0].copy(),
        scored_population[1][0].copy()
    ]

    # Generate rest of the population
    while len(new_population) < POPULATION_SIZE:
        parent1 = tournament_selection(scored_population)
        parent2 = tournament_selection(scored_population)

        child1, child2 = crossover(parent1, parent2)
        child1 = mutate(child1)
        child2 = mutate(child2)

        new_population.append(child1)
        if len(new_population) < POPULATION_SIZE:
            new_population.append(child2)

    population = new_population

# ---------------------------------------------------
# 10. FINAL MODEL USING BEST GA PARAMETERS
# ---------------------------------------------------
best_hidden_neurons = int(best_individual[0])
best_learning_rate = float(best_individual[1])
best_activation = activation_map[int(best_individual[2])]

print("\nBest Optimized Parameters")
print("Hidden Neurons:", best_hidden_neurons)
print("Learning Rate:", best_learning_rate)
print("Activation:", best_activation)

# Train final model on train + validation data
X_final_train = np.vstack((X_train, X_val))
y_final_train = np.hstack((y_train, y_val))

final_model = MLPClassifier(
    hidden_layer_sizes=(best_hidden_neurons,),
    activation=best_activation,
    solver="adam",
    learning_rate_init=best_learning_rate,
    max_iter=2000,
    random_state=42
)

final_model.fit(X_final_train, y_final_train)

# Test prediction
y_pred = final_model.predict(X_test)

test_acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=le.classes_)

print("\nFinal Test Accuracy:", round(test_acc, 4))
print("\nConfusion Matrix:\n", cm)
print("\nClassification Report:\n", report) 



#Actually coconut milk
# import numpy as np
# import random
# from sklearn.model_selection import train_test_split
# from sklearn.neural_network import MLPRegressor
# from sklearn.metrics import mean_squared_error
# from sklearn.preprocessing import StandardScaler

# # ---------------------------------------------------
# # SAMPLE DATASET
# # ---------------------------------------------------
# # Features:
# # [Inlet Temp, Feed Flow Rate, Maltodextrin %]

# X = np.array([
#     [150, 20, 10],
#     [160, 25, 12],
#     [170, 30, 14],
#     [180, 35, 16],
#     [190, 40, 18],
#     [200, 45, 20],
#     [210, 50, 22],
#     [220, 55, 24]
# ])

# # Output:
# # Powder Yield (%)

# y = np.array([55, 60, 64, 68, 72, 75, 78, 82])

# # ---------------------------------------------------
# # DATA PREPROCESSING
# # ---------------------------------------------------

# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)

# X_train, X_test, y_train, y_test = train_test_split(
#     X_scaled, y, test_size=0.2, random_state=42
# )

# # ---------------------------------------------------
# # GENETIC ALGORITHM PARAMETERS
# # ---------------------------------------------------

# POPULATION_SIZE = 6
# GENERATIONS = 5

# # Individual structure:
# # [hidden_neurons, learning_rate]

# def create_individual():
#     hidden_neurons = random.randint(2, 20)
#     learning_rate = round(random.uniform(0.001, 0.1), 3)
#     return [hidden_neurons, learning_rate]

# # ---------------------------------------------------
# # FITNESS FUNCTION
# # ---------------------------------------------------

# def fitness(individual):

#     hidden_neurons = individual[0]
#     learning_rate = individual[1]

#     # Create ANN model
#     model = MLPRegressor(
#         hidden_layer_sizes=(hidden_neurons,),
#         learning_rate_init=learning_rate,
#         max_iter=1000,
#         random_state=42
#     )

#     # Train ANN
#     model.fit(X_train, y_train)

#     # Prediction
#     predictions = model.predict(X_test)

#     # Error calculation
#     mse = mean_squared_error(y_test, predictions)

#     return mse

# # ---------------------------------------------------
# # INITIAL POPULATION
# # ---------------------------------------------------

# population = [create_individual() for _ in range(POPULATION_SIZE)]

# # ---------------------------------------------------
# # GENETIC ALGORITHM
# # ---------------------------------------------------

# for generation in range(GENERATIONS):

#     print("\nGeneration:", generation + 1)

#     # Evaluate fitness
#     scored_population = []

#     for individual in population:
#         mse = fitness(individual)
#         scored_population.append((individual, mse))

#     # Sort by fitness (lower MSE is better)
#     scored_population.sort(key=lambda x: x[1])

#     print("Best Individual:", scored_population[0])

#     # Select top 2 individuals
#     parent1 = scored_population[0][0]
#     parent2 = scored_population[1][0]

#     # ---------------------------------------------------
#     # CROSSOVER
#     # ---------------------------------------------------

#     new_population = [parent1, parent2]

#     while len(new_population) < POPULATION_SIZE:

#         child_hidden = random.choice(
#             [parent1[0], parent2[0]]
#         )

#         child_lr = random.choice(
#             [parent1[1], parent2[1]]
#         )

#         child = [child_hidden, child_lr]

#         # ---------------------------------------------------
#         # MUTATION
#         # ---------------------------------------------------

#         if random.random() < 0.3:
#             child[0] = random.randint(2, 20)

#         if random.random() < 0.3:
#             child[1] = round(random.uniform(0.001, 0.1), 3)

#         new_population.append(child)

#     population = new_population

# # ---------------------------------------------------
# # FINAL BEST MODEL
# # ---------------------------------------------------

# best_individual = scored_population[0][0]

# print("\nBest Optimized Parameters")
# print("Hidden Neurons:", best_individual[0])
# print("Learning Rate:", best_individual[1])

# # Train final ANN
# final_model = MLPRegressor(
#     hidden_layer_sizes=(best_individual[0],),
#     learning_rate_init=best_individual[1],
#     max_iter=1000,
#     random_state=42
# )

# final_model.fit(X_train, y_train)

# # Final prediction
# final_predictions = final_model.predict(X_test)

# print("\nActual Values:")
# print(y_test)

# print("\nPredicted Values:")
# print(final_predictions)

# final_mse = mean_squared_error(y_test, final_predictions)

# print("\nFinal Mean Squared Error:", final_mse)