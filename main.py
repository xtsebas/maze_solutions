import tkinter as tk
import threading
import random
import time

from maze.generator_maze import MazeGenerator
from experiments.comparation import generate_k_mazes, compare_search_algorithms
from experiments.analysis import generate_analytics_from_csv

from maze.visualizer import (
    draw_wall,
    draw_matrix,
    draw_path,
    CELL_SIZE
)
from maze.solver import solve_simulation

# Variables globales para almacenar las matrices generadas
matrix_kruskal = None
matrix_prim = None

def start_generation(canvas, method):
    global matrix_kruskal, matrix_prim

    rng = random.Random(42)
    maze = MazeGenerator(60, 80, rng)

    def step(i1, j1, i2, j2):
        draw_wall(canvas, i1, j1, i2, j2, delay=1)

    if method == 'kruskal':
        maze.generate_kruskal(step)
        matrix_kruskal = maze.to_matrix()
    else:
        maze.generate_prim(step)
        matrix_prim = maze.to_matrix()

    # Dibujar entrada y salida
    x0, y0 = 0 * CELL_SIZE + CELL_SIZE//2, 0 * CELL_SIZE + CELL_SIZE//2
    xe, ye = (maze.rows - 1) * CELL_SIZE + CELL_SIZE//2, (maze.cols - 1) * CELL_SIZE + CELL_SIZE//2
    canvas.create_oval(x0 - 4, y0 - 4, x0 + 4, y0 + 4, fill='green', outline='green')
    canvas.create_oval(xe - 4, ye - 4, xe + 4, ye + 4, fill='red', outline='red')
    canvas.update()

def GenerateMaze():
    root = tk.Tk()
    root.title("Laberintos - Kruskal y Prim")

    canvas1 = tk.Canvas(root, width=800, height=600, bg='black')
    canvas1.grid(row=1, column=0)
    canvas2 = tk.Canvas(root, width=800, height=600, bg='black')
    canvas2.grid(row=1, column=1)

    tk.Label(root, text="Kruskal", bg='black', fg='white').grid(row=0, column=0)
    tk.Label(root, text="Prim",    bg='black', fg='white').grid(row=0, column=1)

    t1 = threading.Thread(target=start_generation, args=(canvas1, 'kruskal'))
    t2 = threading.Thread(target=start_generation, args=(canvas2, 'prim'))
    t1.start()
    t2.start()

    root.mainloop()

def start_resolution(canvas, maze_matrix, algo):
    rows = len(maze_matrix)
    cols = len(maze_matrix[0])
    cell_size = CELL_SIZE // 2
    start = (1, 1)
    goal  = (rows - 2, cols - 2)

    #dibujar el laberinto
    draw_matrix(canvas, maze_matrix, cell_size=cell_size)

    # busqueda colearando las celdas
    def step(cell):
        i, j = cell
        x, y = j * cell_size, i * cell_size
        canvas.create_rectangle(
            x + 1, y + 1,
            x + cell_size - 1, y + cell_size - 1,
            fill='cyan', outline='cyan'
        )
        canvas.update()
        time.sleep(0.001)

    result = solve_simulation(maze_matrix, algo, start, goal, step_callback=step)

    # solucion
    if result.get("path"):
        draw_path(canvas, result["path"], delay=10, cell_size=cell_size)

def main():
    global matrix_kruskal, matrix_prim

    while True:
        print("\nSeleccione paso a ejecutar:")
        print("1. Laberinto - Generación (Kruskal y Prim)")
        print("2. Solución de Laberinto")
        print("3. Tabla de soluciones")
        print("0. Salir")

        choice = input("\nIngrese una opción (0-3): ").strip()

        if choice == "1":
            GenerateMaze()
            print("\nPrimeras 10 filas de matrix_kruskal:")
            for row in matrix_kruskal[:10]:
                print(''.join(str(cell) for cell in row))

        elif choice == "2":
            if matrix_kruskal is None and matrix_prim is None:
                print("Aún no se ha generado ningún laberinto. Ejecute la opción 1 primero.")
                continue

            print("\nSeleccione el laberinto a resolver:")
            print("1. Laberinto generado con Kruskal")
            print("2. Laberinto generado con Prim")
            lab_choice = input("Ingrese 1 o 2: ").strip()
            if lab_choice == "1":
                maze_matrix = matrix_kruskal
            elif lab_choice == "2":
                maze_matrix = matrix_prim
            else:
                print("Opción no válida. Volviendo al menú principal.")
                continue

            print("\nSeleccione el algoritmo de resolución:")
            print("1. BFS")
            print("2. DFS")
            print("3. Cost Uniform Search")
            print("4. A*")
            algo_map = {"1":"bfs", "2":"dfs", "3":"ucs", "4":"a_star"}
            algo = algo_map.get(input("Ingrese número de algoritmo: ").strip(), "bfs")

            # Definimos filas y columnas antes de usar cols/rows
            rows = len(maze_matrix)
            cols = len(maze_matrix[0])

            # Ventana de resolución más pequeña
            root_sol = tk.Tk()
            root_sol.title(f"Laberinto Solución - {algo.upper()}")
            canvas = tk.Canvas(
                root_sol,
                width=cols * (CELL_SIZE//2),
                height=rows * (CELL_SIZE//2),
                bg='black'
            )
            canvas.pack()

            t = threading.Thread(
                target=start_resolution,
                args=(canvas, maze_matrix, algo)
            )
            t.start()
            root_sol.mainloop()

        elif choice == "3":
            print("Tabla de soluciones:")
            mazes = generate_k_mazes(k=25, size=(45,55), method='kruskal')
            compare_search_algorithms(mazes=mazes, visualize=True)
            generate_analytics_from_csv()

        elif choice == "0":
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
