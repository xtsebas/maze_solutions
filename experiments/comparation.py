import random
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from maze.generator_maze import MazeGenerator
from maze.solver import solve_simulation

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

import random
import pandas as pd

import pandas as pd

def simulate(mazes: dict):
    results = []
    algorithms = ['bfs', 'dfs', 'ucs', 'a_star']

    for key, maze in mazes.items():
        start, goal = generate_start_goal(maze)
        print(f"\nSimulando en {key}: start={start}, goal={goal}")

        for algo in algorithms:
            res = solve_simulation(maze, algo, start, goal)
            res['maze'] = key
            results.append(res)

    # Crear DataFrame
    df = pd.DataFrame(results)

    df['rank'] = df.groupby('maze')['time_taken'].rank(method='min')

    rank1_counts = df[df['rank'] == 1]['algorithm'].value_counts().reset_index()
    rank1_counts.columns = ['algorithm', 'times_rank1']

    print("\nConteo de primeros lugares por algoritmo:")
    print(rank1_counts)


    return df, rank1_counts


def generate_start_goal(maze, min_manhattan=10):
    rows, cols = len(maze), len(maze[0])

    while True:
        start = (random.randint(1, rows - 2), random.randint(1, cols - 2))
        goal = (random.randint(1, rows - 2), random.randint(1, cols - 2))

        if maze[start[0]][start[1]] == 0 and maze[goal[0]][goal[1]] == 0:
            dx = abs(start[0] - goal[0])
            dy = abs(start[1] - goal[1])
            if dx + dy >= min_manhattan:
                return start, goal
    
