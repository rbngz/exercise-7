import numpy as np

from environment import Environment
from ant import Ant
import random
import matplotlib.pyplot as plt
import networkx as nx

# Class representing the ant colony
"""
    ant_population: the number of ants in the ant colony
    iterations: the number of iterations 
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
    rho: pheromone evaporation rate
"""


class AntColony:
    def __init__(
        self,
        ant_population: int,
        iterations: int,
        alpha: float,
        beta: float,
        rho: float,
    ):
        self.ant_population = ant_population
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho

        # Initialize the environment of the ant colony
        self.environment = Environment(self.rho, ant_population)

        # Initialize the list of ants of the ant colony
        self.ants = []

        # Initialize the ants of the ant colony
        for i in range(ant_population):

            # Initialize an ant on a random initial location
            random_location = random.choice(self.environment.get_possible_locations())
            ant = Ant(self.alpha, self.beta, random_location)

            # Position the ant in the environment of the ant colony so that it can move around
            ant.join(self.environment)

            # Add the ant to the ant colony
            self.ants.append(ant)

    # Solve the ant colony optimization problem
    def solve(self):
        for _ in range(self.iterations):
            tours = []
            for ant in self.ants:
                ant.run()
                tours.append(ant.visited_cities)
            self.environment.update_pheromone_map(tours)

        self.ants[0].run()
        tour = self.ants[0].visited_cities

        graph = self.environment.topology.get_graph()
        nodes = self.environment.topology.get_nodes()
        pos = {}
        for node in nodes:
            coords = self.environment.topology.node_coords[node]
            pos[node] = tuple(coords)

        # The solution will be a list of the visited cities
        solution = tour

        tour = tour + [tour[0]]  # Make full round
        edgelist = []
        for i in range(len(tour) - 1):
            edgelist.append((tour[i], tour[i + 1]))
        options = {
            "node_size": 70,
        }
        nx.draw_networkx_nodes(graph, pos=pos, **options)
        nx.draw_networkx_edges(
            graph, pos=pos, alpha=0.01
        )  # draw all edges with transparency
        nx.draw_networkx_edges(
            graph, pos=pos, edgelist=edgelist, edge_color="red"
        )  # highlight the edges in the path

        plt.savefig("graph.png")

        # Initially, the shortest distance is set to infinite
        shortest_distance = self.ants[0].travelled_distance

        return solution, shortest_distance


def main():
    # Intialize the ant colony
    ant_colony = AntColony(48, 1000, 1, 5, 0.5)

    # Solve the ant colony optimization problem
    solution, distance = ant_colony.solve()
    print("Solution: ", solution)
    print("Distance: ", distance)


if __name__ == "__main__":
    main()
