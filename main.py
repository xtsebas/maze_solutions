import tkinter as tk
import threading
from maze.generator_maze import MazeGenerator
from maze.visualizer import draw_wall, draw_grid

def start_generation(canvas, method):
    maze = MazeGenerator(60, 80)

    def step(i1, j1, i2, j2):
        draw_wall(canvas, i1, j1, i2, j2, delay=1)

    if method == 'kruskal':
        maze.generate_kruskal(step)
    else:
        maze.generate_prim(step)

    # Dibujar entrada (verde) y salida (rojo)
    x0, y0 = 0 * 10 + 5, 0 * 10 + 5
    xe, ye = (maze.cols - 1) * 10 + 5, (maze.rows - 1) * 10 + 5
    canvas.create_oval(x0 - 4, y0 - 4, x0 + 4, y0 + 4, fill='green', outline='green')
    canvas.create_oval(xe - 4, ye - 4, xe + 4, ye + 4, fill='red', outline='red')
    canvas.update()


def main():
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

if __name__ == "__main__":
    main()