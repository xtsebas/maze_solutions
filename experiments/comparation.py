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
import tkinter as tk
import threading
import time

def visualize_simulation(mazes: dict):
    algorithms = ['bfs', 'dfs', 'ucs', 'a_star']
    maze_keys = list(mazes.keys())
    current_maze_index = [0]
    canvas_size = 300
    canvases = {}
    scale = None
    running_threads = {}
    results = {}

    root = tk.Tk()
    title_var = tk.StringVar()
    title_var.set("Visualización Comparativa")
    tk.Label(root, textvariable=title_var, font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=(10, 10))

    for idx, algo in enumerate(algorithms):
        row, col = divmod(idx, 2)
        tk.Label(root, text=algo.upper(), font=('Arial', 12, 'bold')).grid(row=row*2+1, column=col)
        canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg='white')
        canvas.grid(row=row*2+2, column=col, padx=10, pady=5)
        canvases[algo] = canvas

    # Canvas para la tabla
    table_canvas = tk.Canvas(root, width=canvas_size * 2, height=120, bg='lightgray')
    table_canvas.grid(row=6, column=0, columnspan=2, pady=10)

    def draw_maze(canvas, maze, scale):
        for i, row in enumerate(maze):
            for j, cell in enumerate(row):
                color = 'black' if cell == 1 else 'white'
                canvas.create_rectangle(j*scale, i*scale, (j+1)*scale, (i+1)*scale, fill=color, outline='')

    def draw_point_safe(canvas, pos, color, scale):
        i, j = pos
        def callback():
            canvas.create_rectangle(j*scale, i*scale, (j+1)*scale, (i+1)*scale, fill=color, outline='')
        root.after(0, callback)

    def draw_table():
        table_canvas.delete("all")
        sorted_algos = sorted(results.items(), key=lambda x: x[1]['time_taken'])
        for rank, (algo, res) in enumerate(sorted_algos, start=1):
            res['rank'] = rank

        headers = ['Algoritmo', 'Tiempo (s)', 'Distancia', 'Nodos', 'Ranking']
        col_widths = [150, 120, 100, 100, 100]
        y = 10

        # Encabezado
        x = 10
        for i, h in enumerate(headers):
            table_canvas.create_text(x, y, anchor='nw', text=h, font=('Courier', 10, 'bold'))
            x += col_widths[i]
        y += 25

        # Filas ordenadas por ranking
        sorted_by_rank = sorted(results.items(), key=lambda x: x[1]['rank'])
        for algo, res in sorted_by_rank:
            values = [
                algo.upper(),
                f"{res['time_taken']:.3f}",
                f"{res['path_length']}",
                f"{res['nodes_explored']}",
                f"#{res['rank']}"
            ]
            x = 10
            for i, val in enumerate(values):
                table_canvas.create_text(x, y, anchor='nw', text=val, font=('Courier', 10))
                x += col_widths[i]
            y += 20


    def run_solver(algo, maze, start, goal):
        canvas = canvases[algo]
        draw_maze(canvas, maze, scale)
        draw_point_safe(canvas, start, 'green', scale)
        draw_point_safe(canvas, goal, 'red', scale)

        def step_callback(pos):
            draw_point_safe(canvas, pos, 'blue', scale)
            time.sleep(0.002)

        res = solve_simulation(maze, algo, start, goal, step_callback=step_callback)
        results[algo] = res

        for pos in res['path']:
            draw_point_safe(canvas, pos, 'orange', scale)
            time.sleep(0.002)

        running_threads[algo] = True
        if len(running_threads) == 4:
            draw_table()
            root.after(2000, next_maze)

    def start_algorithms(maze_key, maze, start, goal):
        running_threads.clear()
        results.clear()
        for canvas in canvases.values():
            canvas.delete("all")
        table_canvas.delete("all")

        for algo in algorithms:
            t = threading.Thread(target=run_solver, args=(algo, maze, start, goal))
            t.start()

    def next_maze():
        if current_maze_index[0] >= len(maze_keys):
            title_var.set("Simulación completa 🚀")
            return

        maze_key = maze_keys[current_maze_index[0]]
        maze = mazes[maze_key]
        current_maze_index[0] += 1
        nonlocal scale
        scale = canvas_size // len(maze)
        start, goal = generate_start_goal(maze)
        title_var.set(f"{maze_key} | Start: {start} | Goal: {goal}")
        start_algorithms(maze_key, maze, start, goal)

    next_maze()
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
    
