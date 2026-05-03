from collections import deque

class OnlineSearchAgent:

    def __init__(self, grid_size, start, goal):
        self.grid_size = grid_size
        self.start = start
        self.goal = goal
        self.position = start
        # Mapa conocido: -1 desconocido, 0 libre, 1 obstáculo
        self.known_map = [[-1 for _ in range(grid_size)] for _ in range(grid_size)]
        self.known_map[start[0]][start[1]] = 0  # Posición inicial conocida
        self.path = [start]
        self.visited = set([start])

    def get_neighbors(self, pos):
        #Obtener vecinos válidos en la rejilla.
        x, y = pos
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                neighbors.append((nx, ny))
        return neighbors

    def sense_environment(self, pos):
        #Simular sensado del entorno (en un entorno real, esto sería percepción).
        # Para este ejemplo, asumimos un mapa fijo con obstáculos
        obstacles = [(1, 1), (2, 2)]  # Obstáculos fijos
        if pos in obstacles:
            return 1  # Obstáculo
        return 0  # Libre

    def online_dfs(self):
        #Búsqueda online usando DFS para explorar.
        stack = [self.position]
        came_from = {self.position: None}

        while stack:
            current = stack[-1]

            if current == self.goal:
                # Reconstruir camino
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            # Explorar vecinos
            explored_new = False
            for neighbor in self.get_neighbors(current):
                if neighbor not in self.visited:
                    # Sensar el vecino
                    self.known_map[neighbor[0]][neighbor[1]] = self.sense_environment(neighbor)
                    if self.known_map[neighbor[0]][neighbor[1]] == 0:  # Libre
                        self.visited.add(neighbor)
                        stack.append(neighbor)
                        came_from[neighbor] = current
                        explored_new = True
                        break  # En DFS online, explorar uno a la vez

            if not explored_new:
                stack.pop()  # Backtrack

        return None  # No encontrado

# Ejemplo de uso
agent = OnlineSearchAgent(grid_size=4, start=(0, 0), goal=(3, 3))
path = agent.online_dfs()
if path:
    print(f"Camino encontrado: {path}")
else:
    print("No se encontró camino.")