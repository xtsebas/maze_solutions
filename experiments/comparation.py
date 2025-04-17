import random
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from maze.generator_maze import MazeGenerator

def generate_k_mazes(k: int, size: tuple, method: str = 'kruskal'):
    mazes = {}
    rows, cols = size

    for i in range(k):
        rng = random.Random(i + 42)  # Semilla distinta por cada i
        maze = MazeGenerator(rows, cols, rng)

        if method == 'kruskal':
            maze.generate_kruskal(lambda *_: None)  # No dibuja nada
            key = f'kruskal_{i}'
        else:
            maze.generate_prim(lambda *_: None)
            key = f'prim_{i}'

        mazes[key] = maze.to_matrix()
        maze.save_as_image(method_name=key)

    return mazes

def compare_search_algorithms(mazes : dict, visualize = True):
    if visualize:
        visualize_simulation(mazes) # show Tk with process
    else:
        simulate(mazes) # just get stats on logs
        
"""
simulation core for search algorithms
"""
def visualize_simulation(mazes: dict):
    for maze in mazes:
        pass

def simulate(mazes : dict):
    for maze in mazes:
        pass
    
