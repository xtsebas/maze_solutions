import time

# tamaño por defecto de celda (para generación completa)
CELL_SIZE = 10

# velocidad de animación por defecto (en ms)
DEFAULT_STEP_DELAY = 1  # para draw_wall
default_path_delay = 10   # para draw_path

def draw_wall(canvas, i1, j1, i2, j2, delay=DEFAULT_STEP_DELAY):
    x1, y1 = j1 * CELL_SIZE, i1 * CELL_SIZE
    x2, y2 = j2 * CELL_SIZE, i2 * CELL_SIZE
    canvas.create_line(
        x1 + CELL_SIZE // 2, y1 + CELL_SIZE // 2,
        x2 + CELL_SIZE // 2, y2 + CELL_SIZE // 2,
        fill='white'
    )
    canvas.update()
    time.sleep(delay / 1000.0)


def draw_matrix(canvas, matrix, cell_size=CELL_SIZE):
    canvas.delete("all")
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0

    for i in range(rows):
        for j in range(cols):
            x, y = j * cell_size, i * cell_size
            color = 'white' if matrix[i][j] == 0 else 'black'
            canvas.create_rectangle(
                x, y,
                x + cell_size, y + cell_size,
                fill=color,
                outline=color
            )
    canvas.update()


def draw_path(canvas, path, delay=default_path_delay, cell_size=CELL_SIZE):
    for (i, j) in path:
        x, y = j * cell_size, i * cell_size
        canvas.create_rectangle(
            x + 2, y + 2,
            x + cell_size - 2, y + cell_size - 2,
            fill='blue', outline='blue'
        )
        canvas.update()
        time.sleep(delay / 1000.0)
