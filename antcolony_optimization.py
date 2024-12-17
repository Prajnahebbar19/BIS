# -*- coding: utf-8 -*-
"""AntColony_Optimization.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12XLZ6roJvrOCN6yBgtNg9LnUhs6RXh7-
"""

import random
import math
import numpy as np

class AntColonyOptimization:
    def __init__(self, dist_matrix, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        self.dist_matrix = dist_matrix  # Distance matrix
        self.n_cities = len(dist_matrix)  # Number of cities
        self.n_ants = n_ants  # Number of ants
        self.n_best = n_best  # Number of best ants to update pheromone
        self.n_iterations = n_iterations  # Number of iterations
        self.decay = decay  # Pheromone decay rate
        self.alpha = alpha  # Influence of pheromone
        self.beta = beta  # Influence of distance

        # Initialize pheromone levels
        self.pheromone = np.ones((self.n_cities, self.n_cities))  # Initial pheromone levels
        self.heuristic = 1.0 / (dist_matrix + np.eye(self.n_cities))  # Inverse of distance matrix (heuristic)

    def _select_next_city(self, ant, visited):
        current_city = ant[-1]

        # Calculate probabilities of visiting each city
        pheromone = self.pheromone[current_city]
        heuristic = self.heuristic[current_city]

        # Apply pheromone and heuristic influence
        pheromone = pheromone ** self.alpha
        heuristic = heuristic ** self.beta

        # Zero out the cities already visited
        pheromone[visited] = 0
        heuristic[visited] = 0

        # Calculate probability distribution
        total = pheromone.dot(heuristic)
        if total == 0:
            return random.choice([i for i in range(self.n_cities) if not visited[i]])

        prob = (pheromone * heuristic) / total
        return np.random.choice(self.n_cities, p=prob)

    def _get_total_distance(self, ant):
        # Calculate total distance for the given ant's tour
        total_distance = 0
        for i in range(len(ant) - 1):
            total_distance += self.dist_matrix[ant[i]][ant[i + 1]]
        total_distance += self.dist_matrix[ant[-1]][ant[0]]  # Return to the start city
        return total_distance

    def _update_pheromone(self, all_ants):
        # Evaporate pheromone
        self.pheromone *= (1 - self.decay)

        # Deposit pheromone based on ants' solutions
        for ant in all_ants:
            total_distance = self._get_total_distance(ant)
            for i in range(len(ant) - 1):
                self.pheromone[ant[i]][ant[i + 1]] += 1.0 / total_distance
            self.pheromone[ant[-1]][ant[0]] += 1.0 / total_distance  # For the return path

    def _optimize(self):
        best_ant = None
        best_distance = float('inf')

        # Ant Colony Optimization iterations
        for iteration in range(self.n_iterations):
            all_ants = []

            for _ in range(self.n_ants):
                # Start from a random city
                start_city = random.randint(0, self.n_cities - 1)
                visited = [False] * self.n_cities
                visited[start_city] = True
                ant = [start_city]

                # Construct the solution for this ant
                for _ in range(self.n_cities - 1):
                    next_city = self._select_next_city(ant, visited)
                    visited[next_city] = True
                    ant.append(next_city)

                all_ants.append(ant)

                # Evaluate the tour
                total_distance = self._get_total_distance(ant)
                if total_distance < best_distance:
                    best_ant = ant
                    best_distance = total_distance

            # Update pheromone based on the best n_best ants
            self._update_pheromone(all_ants)

        return best_ant, best_distance

    def run(self):
        best_ant, best_distance = self._optimize()
        return best_ant, best_distance

# Example of how to use the ACO algorithm for the TSP
if __name__ == "__main__":
    # Define the distance matrix for the cities
    dist_matrix = np.array([
        [0, 2, 2, 5, 7],
        [2, 0, 4, 8, 2],
        [2, 4, 0, 1, 3],
        [5, 8, 1, 0, 6],
        [7, 2, 3, 6, 0]
    ])

    # Set the parameters for the ACO algorithm
    n_ants = 5
    n_best = 2
    n_iterations = 100
    decay = 0.95
    alpha = 1
    beta = 2

    # Initialize the ACO algorithm
    aco = AntColonyOptimization(dist_matrix, n_ants, n_best, n_iterations, decay, alpha, beta)

    # Run the algorithm
    best_ant, best_distance = aco.run()

    # Output the results
    print("Best tour:", best_ant)
    print("Total distance:", best_distance)

