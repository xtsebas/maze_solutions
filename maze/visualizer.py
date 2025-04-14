import time

CELL_SIZE = 10

def draw_wall(canvas, i1, j1, i2, j2, delay=1):
    x1, y1 = j1 * CELL_SIZE, i1 * CELL_SIZE
    x2, y2 = j2 * CELL_SIZE, i2 * CELL_SIZE
    canvas.create_line(x1 + CELL_SIZE // 2, y1 + CELL_SIZE // 2,
                       x2 + CELL_SIZE // 2, y2 + CELL_SIZE // 2,
                       fill='white')
    canvas.update()
    time.sleep(delay / 1000.0)

def draw_grid(canvas, grid):
    canvas.delete("all")
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            x, y = j * CELL_SIZE, i * CELL_SIZE
            cell = grid[i][j]
            if cell['N']: canvas.create_line(x, y, x + CELL_SIZE, y, fill='white')
            if cell['W']: canvas.create_line(x, y, x, y + CELL_SIZE, fill='white')
            if cell['S']: canvas.create_line(x, y + CELL_SIZE, x + CELL_SIZE, y + CELL_SIZE, fill='white')
            if cell['E']: canvas.create_line(x + CELL_SIZE, y, x + CELL_SIZE, y + CELL_SIZE, fill='white')
