from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer
import tkinter.messagebox as messagebox
from PyQt5.QtCore import Qt
import random
import sys


class MazeLogic:
    def __init__(self, width, height):
        self.scene = QtWidgets.QGraphicsScene()
        self.width = width
        self.height = height
        self.grid = []
        self.maze_map = {}
        self._stack = []
        self._closed = []
        self.source =(0,0)
        self.destination = (width - 1, height - 1)
        self.cell_size = 20
            
    #Phá tường giữa hai ô liền kề trong mê cung.
    def break_wall(self, x1, y1, x2, y2):
        # Break the wall between two cells
        #T - top edge of the cell
        #R - right edge of the cell
        #B - bottom edge of the cell
        #L - left edge of the cell
        if x1 == x2:
            if y1 + 1 == y2:
                self.maze_map[(x1, y1)]['B'] = 1
                self.maze_map[(x2, y2)]['T'] = 1
            else:
                self.maze_map[(x1, y1)]['T'] = 1
                self.maze_map[(x2, y2)]['B'] = 1
        else:
            if x1 + 1 == x2:
                self.maze_map[(x1, y1)]['R'] = 1
                self.maze_map[(x2, y2)]['L'] = 1
            else:
                self.maze_map[(x1, y1)]['L'] = 1
                self.maze_map[(x2, y2)]['R'] = 1

    def add_random_loops(self, percentage_loop):
        total_cells = self.width * self.height
        loops_to_create = int(total_cells * percentage_loop / 100)
        directions = {'T': (0, -1), 'B': (0, 1), 'L': (-1, 0), 'R': (1, 0)}

        def is_valid_removal(x1, y1, direction):
            dx, dy = directions[direction]
            x2, y2 = x1 + dx, y1 + dy
            if (x2, y2) not in self.maze_map:
                return False
            if self.maze_map[(x1, y1)][direction] == 1:
                return False
            return True

        while loops_to_create > 0:
            x1, y1 = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            possible_directions = list(directions.keys())
            random.shuffle(possible_directions)

            for direction in possible_directions:
                if is_valid_removal(x1, y1, direction):
                    dx, dy = directions[direction]
                    x2, y2 = x1 + dx, y1 + dy
                    self.break_wall(x1, y1, x2, y2)
                    loops_to_create -= 1
                    break

    #Tạo một mê cung ngẫu nhiên sử dụng thuật toán DFS (Depth First Search).
    def create_maze(self, width_entry, height_entry):
        self.width = width_entry
        self.height = height_entry
        # Initialize grid and maze map
        self.grid = [(x, y) for x in range(self.width) for y in range(self.height)]
        self.maze_map = {(x, y): {'T': 0, 'B': 0, 'L': 0, 'R': 0} for x, y in self.grid}

        # Start maze generation
        x, y = 0, 0
        self._stack = [(x, y)]
        self._closed = [(x, y)]
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while self._stack:
            cell = []
            for dx, dy in directions:
                u, v = x + dx, y + dy
                if (u, v) not in self._closed and (u, v) in self.grid:
                    cell.append((u, v))

            if cell:
                u, v = random.choice(cell)
                self.break_wall(x, y, u, v)
                self._closed.append((u, v))
                self._stack.append((u, v))
                x, y = u, v
            else:
                x, y = self._stack.pop()
                
        # Thêm các vòng lặp ngẫu nhiên với tỷ lệ 20%
        self.add_random_loops(percentage_loop=20)
        # print("Maze created:", self.maze_map)
        
    
    
    #Mục đích: Kiểm tra và khởi tạo kích thước mê cung dựa trên đầu vào
    def check_size_of_maze(self, width_entry, height_entry, widget_width, widget_height):
        try:
            self.width = width_entry
            self.height = height_entry

            if not (0 < self.width <= 50 and 0 < self.height <= 50):
                QtWidgets.QMessageBox.warning(None, "Error", "Maze dimensions are out of bounds! Width must be between 1-50, height must be between 1-50.")
                return

            padding = 0  # Chừa khoảng trống
            # size of a square of maze
            self.cell_size = min(
                (widget_width - padding) // self.width,
                (widget_height - padding) // self.height
            )
            if self.cell_size <= 0:
                QtWidgets.QMessageBox.warning(None, "Error", "Widget size is too small for this maze!")
                return

            # Cập nhật đích đến và tạo mê cung
            #
            self.destination = (self.width - 1, self.height - 1)

            print(f"Maze created with dimensions: {self.width}x{self.height}, Cell size: {self.cell_size}")

        except ValueError as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Invalid input: {e}")


    #Kiểm tra tính hợp lệ của tọa độ đầu vào (ô bắt đầu hoặc ô kết thúc).
    def validate_coordinates(self, x_entry, y_entry, typ):
        try:
            x_value = x_entry
            y_value = y_entry
            if x_value and y_value:
                x = int(x_value)
                y = int(y_value)
                if 0 <= x < self.width and 0 <= y < self.height:
                    if typ == 0:
                        self.source = (x, y)
                    else:
                        self.destination = (x, y)
                    return True
                else:
                    messagebox.showerror(
                        "Invalid Coordinate",
                        f"Error: Coordinate ({x}, {y}) is out of bounds. It must be within (0, 0) to ({self.width-1}, {self.height-1})."
                    )
                    return False
            else:
                return True
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Error: Coordinate values must be integers."
            )
            return False