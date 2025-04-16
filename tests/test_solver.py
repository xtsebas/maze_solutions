# test_solver.py

# Agregamos la ruta base para que Python pueda encontrar el módulo 'maze'
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from maze.solver import bfs

def test_bfs():
    # Definición de un laberinto simple (0: camino, 1: muro)
    maze_simple = [
        [0, 0, 1, 1],
        [1, 0, 1, 1],
        [1, 0, 0, 0],
        [1, 1, 1, 0]
    ]
    start = (0, 0)
    goal = (3, 3)
    
    path = bfs(maze_simple, start, goal)
    if path:
        print("Camino encontrado en laberinto simple:")
        print(path)
    else:
        print("No se encontró camino en el laberinto simple.")

if __name__ == "__main__":
    test_bfs()
