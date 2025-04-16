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

    start = (1, 1)
    goal = (len(maze)-2, len(maze[0])-2) #el laberinto tiene bordes, asi que hubo que hacer un ajuste.

    if algo.lower() == "bfs":
        print("\nResolviendo laberinto con BFS...")
        path = bfs(maze, start, goal)
        if path:
            print("Camino encontrado:")
            print(path)
        else:
            print("No se encontró camino desde {} hasta {}.".format(start, goal))
    else:
        print("Algoritmo '{}' no implementado. Usando BFS por defecto.".format(algo))
        path = bfs(maze, start, goal)
        if path:
            print("Camino encontrado:")
            print(path)
        else:
            print("No se encontró camino desde {} hasta {}.".format(start, goal))
