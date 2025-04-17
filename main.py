import tkinter as tk
import threading
import random
from maze.generator_maze import MazeGenerator
from maze.visualizer import draw_wall
from experiments.comparation import generate_k_mazes
# Se importa la función solve_maze desde solver.py (donde implementaste BFS, etc.)
from maze.solver import solve_maze
from experiments.analysis import generate_analytics_from_csv
from experiments.comparation import compare_search_algorithms
from experiments.analysis import generate_analytics_from_csv
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
        maze.save_as_image(method_name='kruskal')
    else:
        maze.generate_prim(step)
        matrix_prim = maze.to_matrix()
        maze.save_as_image(method_name='prim')

    # Dibujar entrada (verde) y salida (rojo)
    # En este ejemplo, la entrada es la celda (0,0) y la salida la celda inferior derecha.
    x0, y0 = 0 * 10 + 5, 0 * 10 + 5
    xe, ye = (maze.cols - 1) * 10 + 5, (maze.rows - 1) * 10 + 5
    canvas.create_oval(x0 - 4, y0 - 4, x0 + 4, y0 + 4, fill='green', outline='green')
    canvas.create_oval(xe - 4, ye - 4, xe + 4, ye + 4, fill='red', outline='red')
    canvas.update()

    return matrix_kruskal, matrix_prim

def GenerateMaze():
    root = tk.Tk()
    root.title("Laberintos - Kruskal y Prim")

    canvas1 = tk.Canvas(root, width=800, height=600, bg='black')
    canvas1.grid(row=1, column=0)
    canvas2 = tk.Canvas(root, width=800, height=600, bg='black')
    canvas2.grid(row=1, column=1)

    tk.Label(root, text="Kruskal", bg='black', fg='white').grid(row=0, column=0)
    tk.Label(root, text="Prim", bg='black', fg='white').grid(row=0, column=1)

    t1 = threading.Thread(target=start_generation, args=(canvas1, 'kruskal'))
    t2 = threading.Thread(target=start_generation, args=(canvas2, 'prim'))
    t1.start()
    t2.start()

    root.mainloop()

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

            print("\nPrimeras 10 filas de matrix_prim:")
            for row in matrix_prim[:10]:
                print(''.join(str(cell) for cell in row))

        elif choice == "2":
            # Selección del laberinto a resolver
            if matrix_kruskal is None and matrix_prim is None:
                print("Aún no se ha generado ningún laberinto. Por favor, ejecute la opción 1 primero.")
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

            # Selección del algoritmo a usar par3
            # a la resolución
            print("\nSeleccione el algoritmo de resolución:")
            print("1. BFS")
            print("2. DFS")
            print("3. Cost Uniform Search")
            print("4. A*")
            algo_choice = input("Ingrese el número del algoritmo a usar: ").strip()

            if algo_choice == "1":
                algo = "bfs"
            elif algo_choice in ["2", "3", "4"]:
                print("El algoritmo seleccionado aún no se ha implementado. Se usará BFS por defecto.")
                algo = "bfs"
            else:
                print("Opción de algoritmo no válida. Se usará BFS por defecto.")
                algo = "bfs"
            
            print("\nResolviendo laberinto con el algoritmo {}...".format(algo))
            # La función solve_maze se encargará de aplicar el algoritmo seleccionado y mostrar el resultado.
            solve_maze(maze_matrix, algo)
            
        elif choice == "3":
            print("Tabla de soluciones: (Funcionalidad pendiente)")
            mazes = generate_k_mazes(
                k = 2,
                size = (45,55),
                method='kruskal'
                )
            compare_search_algorithms(mazes=mazes, visualize=True)
            generate_analytics_from_csv()
        elif choice == "0":
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
