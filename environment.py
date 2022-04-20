import tsplib95

# Class representing the environment of the ant colony
"""
    rho: pheromone evaporation rate
"""


class Environment:
    def __init__(self, rho, ant_count):

        self.rho = rho

        # Initialize the environment topology
        print("Initializing environment topology...")
        self.topology = tsplib95.load("att48-specs/att48.tsp")

        # Intialize the pheromone map in the environment
        self.initialize_pheromone_map(ant_count)

    # Intialize the pheromone trails in the environment
    def initialize_pheromone_map(self, ant_count):
        dimension = self.topology.dimension
        print(f"Initializing pheromone map with dimensions: {dimension}x{dimension}")

        init_value = self._get_initial_pheromone_value(ant_count)
        self.pheromone_map = [[init_value] * dimension for _ in range(dimension)]

    # Update the pheromone trails in the environment
    def update_pheromone_map(self):
        pass

    # Get the pheromone trails in the environment
    def get_pheromone_map(self):
        pass

    # Get the environment topology
    def get_possible_locations(self):
        pass

    # Get the initial pheromone default value
    def _get_initial_pheromone_value(self, ant_count):
        nodes = list(self.topology.get_nodes())
        first = nodes.pop(0)
        cnn = self._recursive_nn(first, nodes, 0)
        init_value = ant_count / cnn
        print(f"Computed initial pheromone value: {init_value:.8f}")
        return init_value

    # Recursive method for computing the total cost of the nearest neighbor algorithm
    def _recursive_nn(self, current_node, remaining_nodes, cost):
        coords_current = self.topology.node_coords[current_node]
        if len(remaining_nodes) == 1:
            coords_other = self.topology.node_coords[remaining_nodes[0]]
            distance = tsplib95.distances.euclidean(coords_current, coords_other)
            return cost + distance
        else:
            min_distance = None
            for node in remaining_nodes:
                coords_other = self.topology.node_coords[node]
                distance = tsplib95.distances.euclidean(coords_current, coords_other)
                if min_distance == None:
                    min_distance = (node, distance)
                else:
                    if distance < min_distance[1]:
                        min_distance = (node, distance)

            current_node = min_distance[0]
            remaining_nodes.remove(current_node)
            cost += min_distance[1]
            return self._recursive_nn(current_node, remaining_nodes, cost)
