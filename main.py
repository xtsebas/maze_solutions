import tkinter as tk
import threading
import random
from maze.generator_maze import MazeGenerator
from maze.visualizer import draw_wall

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
    while True:
        print("\n Seleccione paso a ejecutar:")
        print("1. Laberiton - Kruskal y Prim")
        print("2️. Solucion de Laberinto")
        print("3️. Tabla de soluciones")
        print("0️. Salir")

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
            pass
        elif choice == "3":
            pass
        elif choice == "0":
            print("\nSaliendo del programa. ¡Hasta luego!")
            break
        else:
            print("\n Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()