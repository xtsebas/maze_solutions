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

    def _add_frontier(self, i, j, frontier):
        for (di, dj, direction, opposite) in [(-1,0,'N','S'),(1,0,'S','N'),(0,-1,'W','E'),(0,1,'E','W')]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.rows and 0 <= nj < self.cols and not self.visited[ni][nj]:
                frontier.append((i, j, ni, nj, direction, opposite))