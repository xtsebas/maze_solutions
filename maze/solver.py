from collections import deque
import heapq
def bfs (maze, start, goal):
    
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
            return path
        
        x, y = current
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (x + dx, y + dy)

            if is_valid(maze, neighbor) and neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return None

def dfs (maze, start, goal):
    visited = set()
    parent = {}

    #recursividad, usamos la celda actual.
    def _dfs(current):
        #caso base
        if current == goal:
            return True
    
        x, y = current

        #aca recorremos los vecinos
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (x + dx, y + dy)
            if is_valid(maze, neighbor) and neighbor not in visited:
                visited.add(neighbor)
                #registramos de donde venimos
                parent[neighbor] = current
                #aplicamos recursividad
                if _dfs(neighbor):
                    return True
        #si ningun vecino encontro la salida volvemos a la posicion anterior e iniciamos de nuevo
        return False
    
    visited.add(start)
    #llamamos a la recursion
    if not _dfs(start):
        return None
    
    path = []
    cur = goal 
    while cur != start:
        path.append(cur)
        cur = parent[cur]
    path.append(start)
    path.reverse()
    return path

def ucs (maze, start, goal):
    costs = {start:0} #para cada celda guardamos el menor coste con el que llegamos hasta a ella
    parent = {}

    frontier = [] #cola de prioridad
    heapq.heappush(frontier, (0, start[0] + start[1], start)) #metemos una tupla a la heap

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
            return path
        
        if current in visited:
            continue
        visited.add(current)

        x, y = current

        for dx, dy in [(-1,0),(1,0), (0,-1),(0,1)]:
            neighbor = (x + dx, y + dy) #calcilar vecinos
            if not is_valid(maze, neighbor):
                continue
            new_cost = current_cost + 1 #calcular el nuevo coste hasta el vecino. Cada paso vale 1

            if neighbor not in costs or new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                parent[neighbor] = current
                tie = neighbor[0] + neighbor[1] #si dos nodos tienen el mismo costo priorizamos el que está más arriba a la izquierda
                heapq.heappush(frontier, (new_cost, tie, neighbor))
    
    return None


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
    # Ajustamos puntos de entrada y salida (bordes exteriores son muros)
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
    else:
        print(f"\nAlgoritmo '{algo}' no implementado. Usando BFS por defecto.")
        path = bfs(maze, start, goal)

    if path:
        print("Camino encontrado:")
        print(path)
    else:
        print(f"No se encontró camino desde {start} hasta {goal}.")