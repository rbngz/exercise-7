import tsplib95

# Class representing the environment of the ant colony
"""
    rho: pheromone evaporation rate
"""


class Environment:
    def __init__(self, rho, ant_count):

        self.rho = rho
        self.ant_count = ant_count

        # Initialize the environment topology
        print("Initializing environment topology...")
        self.topology = tsplib95.load("att48-specs/att48.tsp")

        # Intialize the pheromone map in the environment
        self.initialize_pheromone_map()

    # Intialize the pheromone trails in the environment
    def initialize_pheromone_map(self):
        dimension = self.topology.dimension
        print(f"Initializing pheromone map with dimensions: {dimension}x{dimension}")

        init_value = self._get_initial_pheromone_value()
        self.pheromone_map = [[init_value] * dimension for _ in range(dimension)]

    # Update the pheromone trails in the environment
    def update_pheromone_map(self, tours):
        print("Updating pheromone map...")
        print(f"Applying evaporation rate of {self.rho}")

        # Evaporation of pheromone
        updated_map = []
        for row in self.pheromone_map:
            updated_row = []
            for value in row:
                updated_value = value * (1 - self.rho)
                updated_row.append(updated_value)
            updated_map.append(updated_row)

        print("Adding pheromone to trails")

        # print(f"Total num of tours {len(tours)}")
        # Adding of pheromones
        for tour in tours:
            # print(tour)
            # Compute total cost of tour
            cost = 0
            for i in range(len(tour) - 1):
                weight = self.get_distance(tour[i], tour[i + 1])
                cost += weight

            pheromone_amount = 1 / cost
            # print(f"Cost of tour {cost}, pheromone amount: {pheromone_amount}")

            # Add pheromone to map
            for i in range(len(tour) - 1):
                # Adjusted for map indexing at zero
                map_coords = tour[i] - 1, tour[i + 1] - 1
                updated_map[map_coords[0]][map_coords[1]] = (
                    updated_map[map_coords[0]][map_coords[1]] + pheromone_amount
                )
                # Update both directions
                updated_map[map_coords[1]][map_coords[0]] = (
                    updated_map[map_coords[1]][map_coords[0]] + pheromone_amount
                )

        self.pheromone_map = updated_map
        # print(self.pheromone_map)

    # Get pheromone value of trail in the environment
    def get_pheromone_value(self, current_node, next_node):
        return self.pheromone_map[current_node - 1][next_node - 1]

    def get_distance(self, current_node, next_node):
        edge = current_node, next_node
        return self.topology.get_weight(*edge)  # pseudo euclidian distance

    # Get the environment topology
    def get_possible_locations(self):
        return list(self.topology.get_nodes())

    # Get the initial pheromone default value
    def _get_initial_pheromone_value(self):
        nodes = list(self.topology.get_nodes())
        cnn_sum = 0
        for i in range(len(nodes)):
            nodes_copy = nodes.copy()
            first = nodes_copy.pop(i)
            cnn = self._recursive_nn(first, nodes_copy, 0)
            cnn_sum += cnn
        avg_cnn = int(cnn_sum / len(nodes))

        init_value = self.ant_count / avg_cnn
        print(
            f"Computed initial pheromone value: {init_value:.8f} "
            f"from number of ants: {self.ant_count} / average C^nn: {avg_cnn}"
        )
        return init_value

    # Recursive method for computing the total cost of the nearest neighbor algorithm
    def _recursive_nn(self, current_node, remaining_nodes, cost):
        if len(remaining_nodes) == 1:
            distance = self.get_distance(current_node, remaining_nodes[0])
            return cost + distance
        else:
            min_distance = None
            for node in remaining_nodes:
                distance = self.get_distance(current_node, node)
                if min_distance == None:
                    min_distance = (node, distance)
                else:
                    if distance < min_distance[1]:
                        min_distance = (node, distance)

            current_node = min_distance[0]
            remaining_nodes.remove(current_node)
            cost += min_distance[1]
            return self._recursive_nn(current_node, remaining_nodes, cost)
