from collections import deque
import heapq
def bfs(maze, start, goal, return_visited=False):
    queue = deque([start])
    visited = set([start])
    parent = {}

    while queue:
        current = queue.popleft()
        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            return (path, visited) if return_visited else path

        x, y = current
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (x + dx, y + dy)
            if is_valid(maze, neighbor) and neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return (None, visited) if return_visited else None

def dfs(maze, start, goal, return_visited=False):
    visited = set()
    parent = {}

    def _dfs(current):
        if current == goal:
            return True

        x, y = current
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (x + dx, y + dy)
            if is_valid(maze, neighbor) and neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                if _dfs(neighbor):
                    return True
        return False

    visited.add(start)
    if not _dfs(start):
        return (None, visited) if return_visited else None

    path = []
    cur = goal 
    while cur != start:
        path.append(cur)
        cur = parent[cur]
    path.append(start)
    path.reverse()
    return (path, visited) if return_visited else path

def ucs(maze, start, goal, return_visited=False):
    costs = {start: 0}
    parent = {}
    frontier = []
    heapq.heappush(frontier, (0, start[0] + start[1], start))
    visited = set()

    while frontier:
        current_cost, _, current = heapq.heappop(frontier)

        if current == goal:
            path = []
            node = goal
            while node != start:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()
            return (path, visited) if return_visited else path

        if current in visited:
            continue
        visited.add(current)

        x, y = current
        for dx, dy in [(-1,0),(1,0), (0,-1),(0,1)]:
            neighbor = (x + dx, y + dy)
            if not is_valid(maze, neighbor):
                continue
            new_cost = current_cost + 1

            if neighbor not in costs or new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                parent[neighbor] = current
                tie = neighbor[0] + neighbor[1]
                heapq.heappush(frontier, (new_cost, tie, neighbor))

    return (None, visited) if return_visited else None

def a_star(maze, start, goal, return_visited=False):
    open_set = []
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    parent = {}
    closed = set()

    heapq.heappush(open_set, (f_score[start], start[0]*start[1], start))

    while open_set:
        current_f, _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            node = goal
            while node != start:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()
            return (path, closed) if return_visited else path

        if current in closed:
            continue
        closed.add(current)

        x, y = current
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            neigh = (x+dx, y+dy)
            if not is_valid(maze, neigh):
                continue

            tentative_g = g_score[current] + 1
            if neigh not in g_score or tentative_g < g_score[neigh]:
                parent[neigh] = current
                g_score[neigh] = tentative_g
                f = tentative_g + heuristic(neigh, goal)
                f_score[neigh] = f
                tie = neigh[0] * neigh[1]
                if neigh not in closed:
                    heapq.heappush(open_set, (f, tie, neigh))

    return (None, closed) if return_visited else None



def heuristic(a, b):
    #usamos la distancia Manhattan 
    # Distancia = |fila_a - fila_b| + |columna_a - columna_b|
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def is_valid(maze, position):
    rows = len(maze)
    if rows == 0:
        return False
    cols = len(maze[0])

    x,y = position

    if x < 0 or x >= rows or y < 0 or y >= cols:
        return False
    
    if maze[x][y] != 0:
        return False
    
    return True

def solve_maze(maze, algo):
    """
    Resuelve el laberinto usando el algoritmo seleccionado: bfs, dfs o ucs.
    """
    start = (1, 1)
    goal = (len(maze)-2, len(maze[0])-2)
    algo = algo.lower()

    if algo == 'bfs':
        print("\nEjecutando BFS...")
        path = bfs(maze, start, goal)
    elif algo == 'dfs':
        print("\nEjecutando DFS...")
        path = dfs(maze, start, goal)
    elif algo in ('ucs', 'cost', 'dijkstra'):
        print("\nEjecutando Uniform Cost Search (Dijkstra)...")
        path = ucs(maze, start, goal)
    elif algo in ('a_star', 'a*'):
        print("\nEjecutando A*...")
        path = a_star(maze, start, goal)
    else:
        print(f"\nAlgoritmo '{algo}' no implementado. Usando BFS por defecto.")
        path = bfs(maze, start, goal)

    if path:
        print("Camino encontrado:")
        print(path)
    else:
        print(f"No se encontró camino desde {start} hasta {goal}.")

import time
from collections import defaultdict

def solve_simulation(maze: list, algorithm: str, start: tuple, goal: tuple):
    result = {
        "algorithm": algorithm,
        "nodes_explored": 0,
        "path_length": 0,
        "time_taken": 0,
        "found_path": False
    }

    start_time = time.time()
    
    if algorithm == 'bfs':
        path, visited = bfs(maze, start, goal, return_visited=True)
    elif algorithm == 'dfs':
        path, visited = dfs(maze, start, goal, return_visited=True)
    elif algorithm in ('ucs', 'cost', 'dijkstra'):
        path, visited = ucs(maze, start, goal, return_visited=True)
    elif algorithm in ('a_star', 'a*'):
        path, visited = a_star(maze, start, goal, return_visited=True)
    else:
        raise ValueError(f"Algoritmo '{algorithm}' no implementado.")
    
    end_time = time.time()

    result["time_taken"] = end_time - start_time
    result["nodes_explored"] = len(visited)
    result["found_path"] = path is not None
    result["path_length"] = len(path) if path else 0

    return result
