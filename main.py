import numpy as np
import matplotlib.pyplot as plt

class AntColonyOptimization:
    def __init__(self, num_ants, num_iterations, pheromone_factor, evaporation_rate):
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.pheromone_factor = pheromone_factor
        self.evaporation_rate = evaporation_rate

    def optimize_path(self, distances, start_point, end_point, obstacles):
        num_cities = len(distances)
        pheromones = np.ones((num_cities, num_cities))
        best_path = None
        best_distance = float('inf')

        for iteration in range(self.num_iterations):
            ant_paths = []
            ant_distances = []

            for ant in range(self.num_ants):
                path = [start_point]
                current_point = start_point
                visited = set([start_point])

                while current_point != end_point:
                    next_point = self.select_next_point(current_point, visited, pheromones, distances)
                    path.append(next_point)
                    visited.add(next_point)
                    current_point = next_point

                path_distance = self.calculate_path_distance(path, distances)
                ant_paths.append(path)
                ant_distances.append(path_distance)

                if path_distance < best_distance:
                    best_path = path
                    best_distance = path_distance

            self.update_pheromones(pheromones, ant_paths, ant_distances)

        return best_path, best_distance

    def select_next_point(self, current_point, visited, pheromones, distances):
        remaining_points = list(set(range(len(distances))) - visited)
        probabilities = [((pheromones[current_point][i] ** self.pheromone_factor) * (1 / distances[current_point][i])) for i in remaining_points]
        probabilities /= np.sum(probabilities)
        next_point = np.random.choice(remaining_points, p=probabilities)
        return next_point

    def calculate_path_distance(self, path, distances):
        distance = 0
        for i in range(len(path) - 1):
            distance += distances[path[i]][path[i+1]]
        return distance

    def update_pheromones(self, pheromones, ant_paths, ant_distances):
        for i in range(len(pheromones)):
            for j in range(len(pheromones[0])):
                pheromones[i][j] *= (1 - self.evaporation_rate)

        for i, path in enumerate(ant_paths):
            for j in range(len(path) - 1):
                pheromones[path[j]][path[j+1]] += (1 / ant_distances[i])

def plot_cities(cities):
    for city in cities:
        plt.scatter(city[0], city[1], color='blue')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.title('Cities')
    plt.grid(True)
    plt.show()

def plot_path(cities, path, obstacles):
    for city in cities:
        plt.scatter(city[0], city[1], color='blue')
    for obstacle in obstacles:
        plt.scatter(obstacle[0], obstacle[1], color='black', marker='s')
    for i in range(len(path) - 1):
        x = [cities[path[i]][0], cities[path[i+1]][0]]
        y = [cities[path[i]][1], cities[path[i+1]][1]]
        plt.plot(x, y, color='red')
    plt.scatter(cities[path[0]][0], cities[path[0]][1], color='green', label='Start')
    plt.scatter(cities[path[-1]][0], cities[path[-1]][1], color='yellow', label='End')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.title('Optimal Path with Obstacles')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage:
if __name__ == "__main__":
    np.random.seed(0)
    num_cities = 20
    cities = np.random.randint(0, 100, size=(num_cities, 2))
    distances = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(num_cities):
            distances[i][j] = np.linalg.norm(cities[i] - cities[j])

    num_ants = 20
    num_iterations = 100
    pheromone_factor = 1
    evaporation_rate = 0.1

    obstacles = np.random.randint(0, 100, size=(10, 2))  # Generating 10 random obstacles

    aco = AntColonyOptimization(num_ants, num_iterations, pheromone_factor, evaporation_rate)
    start_point = 0
    end_point = 1
    best_path, best_distance = aco.optimize_path(distances, start_point, end_point, obstacles)

    plot_cities(cities)
    plot_path(cities, best_path, obstacles)

# import numpy as np
# import matplotlib.pyplot as plt

# class AntColonyOptimization:
#     def __init__(self, num_ants, num_iterations, pheromone_factor, evaporation_rate):
#         self.num_ants = num_ants
#         self.num_iterations = num_iterations
#         self.pheromone_factor = pheromone_factor
#         self.evaporation_rate = evaporation_rate

#     def optimize_path(self, distances, start_point, end_point):
#         num_cities = len(distances)
#         pheromones = np.ones((num_cities, num_cities))
#         best_path = None
#         best_distance = float('inf')

#         for iteration in range(self.num_iterations):
#             ant_paths = []
#             ant_distances = []

#             for ant in range(self.num_ants):
#                 path = [start_point]
#                 current_point = start_point
#                 visited = set([start_point])

#                 while current_point != end_point:
#                     next_point = self.select_next_point(current_point, visited, pheromones, distances)
#                     path.append(next_point)
#                     visited.add(next_point)
#                     current_point = next_point

#                 path_distance = self.calculate_path_distance(path, distances)
#                 ant_paths.append(path)
#                 ant_distances.append(path_distance)

#                 if path_distance < best_distance:
#                     best_path = path
#                     best_distance = path_distance

#             self.update_pheromones(pheromones, ant_paths, ant_distances)

#         return best_path, best_distance

#     def select_next_point(self, current_point, visited, pheromones, distances):
#         remaining_points = list(set(range(len(distances))) - visited)
#         probabilities = [((pheromones[current_point][i] ** self.pheromone_factor) * (1 / distances[current_point][i])) for i in remaining_points]
#         probabilities /= np.sum(probabilities)
#         next_point = np.random.choice(remaining_points, p=probabilities)
#         return next_point

#     def calculate_path_distance(self, path, distances):
#         distance = 0
#         for i in range(len(path) - 1):
#             distance += distances[path[i]][path[i+1]]
#         return distance

#     def update_pheromones(self, pheromones, ant_paths, ant_distances):
#         for i in range(len(pheromones)):
#             for j in range(len(pheromones[0])):
#                 pheromones[i][j] *= (1 - self.evaporation_rate)

#         for i, path in enumerate(ant_paths):
#             for j in range(len(path) - 1):
#                 pheromones[path[j]][path[j+1]] += (1 / ant_distances[i])


# def plot_path(distances, path):
#     x = np.arange(len(distances))
#     y = np.arange(len(distances))
#     xx, yy = np.meshgrid(x, y)
#     plt.figure(figsize=(8, 6))
#     plt.pcolormesh(xx, yy, distances, cmap='viridis')
#     plt.colorbar(label='Distance')
#     plt.plot(xx, yy, 'ko', ms=8)
#     for i in range(len(path) - 1):
#         plt.plot([path[i], path[i + 1]], [path[i], path[i + 1]], 'r-', lw=2)
#     plt.xlim(0, len(distances) - 1)
#     plt.ylim(0, len(distances) - 1)
#     plt.title('Optimal Path')
#     plt.xlabel('Cities')
#     plt.ylabel('Cities')
#     plt.grid(True)
#     plt.show()


# # Example usage:
# if __name__ == "__main__":
#     # Example distances between cities (replace with your actual data)
#     distances = np.array([[0, 10, 20, 30],
#                           [10, 0, 25, 35],
#                           [20, 25, 0, 15],
#                           [30, 35, 15, 0]])

#     num_ants = 10
#     num_iterations = 100
#     pheromone_factor = 1
#     evaporation_rate = 0.1

#     aco = AntColonyOptimization(num_ants, num_iterations, pheromone_factor, evaporation_rate)
#     start_point = 0
#     end_point = 3
#     best_path, best_distance = aco.optimize_path(distances, start_point, end_point)
#     print("Best Path:", best_path)
#     print("Best Distance:", best_distance)

#     plot_path(distances, best_path)
