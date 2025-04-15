import random
from .utils import DisjointSet
from PIL import Image, ImageDraw
import os
import re

CELL_SIZE = 10

class MazeGenerator:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[{'N': True, 'S': True, 'E': True, 'W': True} for _ in range(cols)] for _ in range(rows)]
        self.visited = [[False]*cols for _ in range(rows)]

    def remove_wall(self, i1, j1, i2, j2, direction):
        if direction == 'N':
            self.grid[i1][j1]['N'] = False
            self.grid[i2][j2]['S'] = False
        elif direction == 'W':
            self.grid[i1][j1]['W'] = False
            self.grid[i2][j2]['E'] = False

    def generate_kruskal(self, callback=lambda *args: None):
        walls = []
        for i in range(self.rows):
            for j in range(self.cols):
                if i > 0: walls.append(((i, j), (i - 1, j), 'N'))
                if j > 0: walls.append(((i, j), (i, j - 1), 'W'))
        random.shuffle(walls)

        ds = DisjointSet(self.rows * self.cols)
        for (i1, j1), (i2, j2), direction in walls:
            idx1 = i1 * self.cols + j1
            idx2 = i2 * self.cols + j2
            if ds.union(idx1, idx2):
                self.remove_wall(i1, j1, i2, j2, direction)
                callback(i1, j1, i2, j2)

        self.grid[0][0]['W'] = False
        self.grid[self.rows - 1][self.cols - 1]['E'] = False

    def generate_prim(self, callback=lambda *args: None):
        start = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
        frontier = []
        self.visited[start[0]][start[1]] = True
        self._add_frontier(*start, frontier)

        while frontier:
            i, j, ni, nj, direction, opposite = frontier.pop(random.randint(0, len(frontier)-1))
            if not self.visited[ni][nj]:
                self.grid[i][j][direction] = False
                self.grid[ni][nj][opposite] = False
                self.visited[ni][nj] = True
                callback(i, j, ni, nj)
                self._add_frontier(ni, nj, frontier)
        
        self.grid[0][0]['W'] = False
        self.grid[self.rows - 1][self.cols - 1]['E'] = False

    def _add_frontier(self, i, j, frontier):
        for (di, dj, direction, opposite) in [(-1,0,'N','S'),(1,0,'S','N'),(0,-1,'W','E'),(0,1,'E','W')]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.rows and 0 <= nj < self.cols and not self.visited[ni][nj]:
                frontier.append((i, j, ni, nj, direction, opposite))
    
    def save_as_image(self):
        os.makedirs("results", exist_ok=True)

        # Buscar los archivos existentes tipo maze_###.png
        existing = os.listdir("results")
        nums = []
        for name in existing:
            match = re.match(r"maze_(\\d+)\\.png", name)
            if match:
                nums.append(int(match.group(1)))
        next_num = max(nums, default=0) + 1
        filename = f"maze_{next_num:03d}.png"
        full_path = os.path.join("results", filename)

        # Crear imagen
        img = Image.new("RGB", (self.cols * CELL_SIZE, self.rows * CELL_SIZE), "black")
        draw = ImageDraw.Draw(img)

        for i in range(self.rows):
            for j in range(self.cols):
                x, y = j * CELL_SIZE, i * CELL_SIZE
                cell = self.grid[i][j]
                if cell['N']:
                    draw.line([(x, y), (x + CELL_SIZE, y)], fill="white")
                if cell['W']:
                    draw.line([(x, y), (x, y + CELL_SIZE)], fill="white")
                if cell['S']:
                    draw.line([(x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE)], fill="white")
                if cell['E']:
                    draw.line([(x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE)], fill="white")

        # Entrada (verde) y salida (rojo)
        draw.ellipse([(5 - 4, 5 - 4), (5 + 4, 5 + 4)], fill="green")
        ex = (self.cols - 1) * CELL_SIZE + 5
        ey = (self.rows - 1) * CELL_SIZE + 5
        draw.ellipse([(ex - 4, ey - 4), (ex + 4, ey + 4)], fill="red")

        img.save(full_path)

    def to_matrix(self):
        matrix = [[1 for _ in range(self.cols * 2 + 1)] for _ in range(self.rows * 2 + 1)]
        for i in range(self.rows):
            for j in range(self.cols):
                r, c = i * 2 + 1, j * 2 + 1
                matrix[r][c] = 0
                if not self.grid[i][j]['N']:
                    matrix[r - 1][c] = 0
                if not self.grid[i][j]['S']:
                    matrix[r + 1][c] = 0
                if not self.grid[i][j]['W']:
                    matrix[r][c - 1] = 0
                if not self.grid[i][j]['E']:
                    matrix[r][c + 1] = 0
        return matrix