from collections import deque

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
    Resuelve el laberinto usando el algoritmo seleccionado.

    Parámetros:
      maze: matriz del laberinto (lista de listas) con 0 (camino) y 1 (muro).
      algo: string que indica el algoritmo a usar ("bfs" o "dfs").
    """
    # Ajusta la entrada y salida según el borde de muros
    start = (1, 1)
    goal  = (len(maze) - 2, len(maze[0]) - 2)

    algo = algo.lower()
    if algo == "bfs":
        print("\nResolviendo laberinto con BFS...")
        path = bfs(maze, start, goal)
    elif algo == "dfs":
        print("\nResolviendo laberinto con DFS...")
        path = dfs(maze, start, goal)
    else:
        print(f"\nAlgoritmo '{algo}' no implementado. Usando BFS por defecto.")
        path = bfs(maze, start, goal)

    # Mostrar resultado
    if path:
        print("Camino encontrado:")
        print(path)
    else:
        print(f"No se encontró camino desde {start} hasta {goal}.")

