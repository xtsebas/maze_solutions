import random
import pandas as pd
import os
import sys
import tkinter as tk
import threading
import time
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
    algorithms = ['bfs', 'dfs', 'ucs', 'a_star']

    maze_key, maze = list(mazes.items())[0]
    start, goal = generate_start_goal(maze)

    root = tk.Tk()
    root.title(f"Visualización Comparativa - {maze_key}")
    canvas_size = 300
    scale = canvas_size // len(maze)
    canvases = {}

    # Crear layout 2x2 con etiquetas arriba
    for idx, algo in enumerate(algorithms):
        row, col = divmod(idx, 2)

        # Etiqueta con el nombre del algoritmo
        label = tk.Label(root, text=algo.upper(), font=('Arial', 12, 'bold'))
        label.grid(row=row*2, column=col, pady=(10, 0))

        # Canvas debajo de la etiqueta
        canvas = tk.Canvas(root, width=canvas_size, height=canvas_size + 40, bg='white')
        canvas.grid(row=row*2 + 1, column=col, padx=10, pady=5)
        canvases[algo] = canvas

    def draw_maze(canvas, maze):
        for i, row in enumerate(maze):
            for j, cell in enumerate(row):
                color = 'black' if cell == 1 else 'white'
                canvas.create_rectangle(j*scale, i*scale, (j+1)*scale, (i+1)*scale, fill=color, outline='')

    def draw_point(canvas, pos, color):
        i, j = pos
        canvas.create_rectangle(j*scale, i*scale, (j+1)*scale, (i+1)*scale, fill=color, outline='')

    def run_solver(algorithm):
        canvas = canvases[algorithm]
        draw_maze(canvas, maze)
        draw_point(canvas, start, 'green')
        draw_point(canvas, goal, 'red')

        def step_callback(pos):
            draw_point(canvas, pos, 'blue')
            canvas.update()
            time.sleep(0.002)

        result = solve_simulation(maze, algorithm, start, goal, step_callback=step_callback)

        for pos in result['path']:
            draw_point(canvas, pos, 'orange')
            canvas.update()
            time.sleep(0.002)

        canvas.create_text(5, canvas_size + 5, anchor='nw',
                           text=f"Tiempo: {result['time_taken']:.3f}s", fill='black', font=('Arial', 9))
        canvas.create_text(5, canvas_size + 20, anchor='nw',
                           text=f"Ruta: {result['path_length']} pasos", fill='black', font=('Arial', 9))

    for algo in algorithms:
        threading.Thread(target=run_solver, args=(algo,)).start()

    root.mainloop()
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
    
