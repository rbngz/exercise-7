import numpy as np

from environment import Environment
from ant import Ant
import random
import matplotlib.pyplot as plt
import networkx as nx

random.seed(42)

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

        locations = self.environment.get_possible_locations()
        random.shuffle(locations)

        # Initialize the ants of the ant colony
        for i in range(ant_population):

            # Initialize an ant on a random initial location
            # random_location = random.choice(self.environment.get_possible_locations())
            ant = Ant(self.alpha, self.beta, locations[i])

            # Position the ant in the environment of the ant colony so that it can move around
            ant.join(self.environment)

            # Add the ant to the ant colony
            self.ants.append(ant)

    # Solve the ant colony optimization problem
    def solve(self):
        # Draw Graph
        graph = self.environment.topology.get_graph()
        nodes = self.environment.topology.get_nodes()
        pos = {}
        for node in nodes:
            coords = self.environment.topology.node_coords[node]
            pos[node] = tuple(coords)
        options = {
            "node_size": 70,
        }

        # Run simulation
        for i in range(self.iterations):
            print(f"Running iteration {i}...")
            nx.draw_networkx_nodes(graph, pos=pos, **options)
            locations = self.environment.get_possible_locations()
            random.shuffle(locations)
            tours = []
            for j, ant in enumerate(self.ants):
                ant.run()
                tours.append(ant.visited_cities)
                # Reset ant
                ant.reset(locations[j])
            self.environment.update_pheromone_map(tours)
            for tour in tours:
                edgelist = []
                for j in range(len(tour) - 1):
                    edgelist.append((tour[j], tour[j + 1]))
                nx.draw_networkx_edges(
                    graph, pos=pos, edgelist=edgelist, edge_color="red", alpha=0.02
                )  # highlight the edges in the path
            if i % 100 == 0:
                plt.savefig(f"graphs/graph{i}.png")
            plt.clf()

        self.ants[0].run()
        tour = self.ants[0].visited_cities

        # The solution will be a list of the visited cities
        solution = tour

        tour = tour + [tour[0]]  # Make full round

        # Initially, the shortest distance is set to infinite
        shortest_distance = self.ants[0].travelled_distance

        return solution, shortest_distance


def main():
    # Intialize the ant colony
    ant_colony = AntColony(ant_population=48, iterations=101, alpha=1, beta=5, rho=0.5)

    # Solve the ant colony optimization problem
    solution, distance = ant_colony.solve()
    print("Solution: ", solution)
    print("Distance: ", distance)


if __name__ == "__main__":
    main()
