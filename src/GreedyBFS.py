from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QGraphicsView, QGraphicsScene
from MazeLogic import MazeLogic  # Assuming you have MazeLogic class
import MazeSolvingAlgorithm as MSA

class GreedyBFSWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, width=10, height=10, cell_size=20):
        super().__init__(parent)
        self.maze_logic = MazeLogic(width, height)  # Khởi tạo MazeLogic
        self.cell_size = cell_size
        self.width = width
        self.height = height
        self.maze_map = {}  

        # Tạo nhãn hiển thị thông tin
        self.path_len_label = QLabel("Greedy BFS Path Length: 0", self)
        self.search_len_label = QLabel("Greedy BFS Search Length: 0", self)

        # Tạo Scene và View để hiển thị mê cung
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        
        # Tạo layout và thêm các thành phần
        layout = QVBoxLayout(self)
        layout.addWidget(self.path_len_label)
        layout.addWidget(self.search_len_label)
        layout.addWidget(self.view)
        self.setLayout(layout)
        
        self.source =(0,0)
        self.destination = (width - 1, height - 1)

    def create_maze(self, width, height):
        # Lấy kích thước của view
        view_width = self.view.viewport().width()
        view_height = self.view.viewport().height()

        # Tính toán kích thước ô (cell_size) dựa trên kích thước view và số ô
        self.cell_size = min(view_width // width, view_height // height)

        # Cập nhật lại kích thước scene để vừa với view
        scene_width = self.cell_size * width
        scene_height = self.cell_size * height
        self.scene.setSceneRect(0, 0, scene_width, scene_height)

        # Cập nhật maze_logic
        self.width = width
        self.height = height
        self.maze_logic.check_size_of_maze(width, height, scene_width, scene_height)
        self.maze_map = self.maze_logic.maze_map  # Lấy dữ liệu mê cung
        # Vẽ mê cung lên scene
        self.draw_maze_on_scene()


    def draw_maze_on_scene(self):
        """Vẽ mê cung từ maze_map lên QGraphicsScene."""
        self.scene.clear()  # Xóa nội dung cũ
        self.cell_size = self.maze_logic.cell_size  # Lấy cell_size từ MazeLogic

        for (x, y), edges in self.maze_map.items():
            x1 = x * self.cell_size
            y1 = y * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size

            # Vẽ các cạnh của ô dựa trên thông tin trong maze_map
            if edges['T'] == 0:  # Cạnh trên
                self.scene.addLine(x1, y1, x2, y1, QPen(Qt.black, 2))
            if edges['R'] == 0:  # Cạnh phải
                self.scene.addLine(x2, y1, x2, y2, QPen(Qt.black, 2))
            if edges['B'] == 0:  # Cạnh dưới
                self.scene.addLine(x2, y2, x1, y2, QPen(Qt.black, 2))
            if edges['L'] == 0:  # Cạnh trái
                self.scene.addLine(x1, y2, x1, y1, QPen(Qt.black, 2))

    
    def display(self, source, destination):
        self.source =source
        self.destination = destination

        # In các ô bắt đầu và kết thúc
        self.print_cell(source[0], source[1], "tomato")
        self.print_cell(destination[0], destination[1], "tomato")
        self.scene.update()
        
    # Tô màu một ô trong mê cung.
    def print_cell(self, x, y, color):
        if (x, y) == self.source or (x, y) == self.destination:
            color = "red"  # Highlight source and destination
            
        x1 = x * self.cell_size
        y1 = y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        print(f"x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}")

        # Draw cell
        rect = self.scene.addRect(x1, y1, x2 - x1, y2 - y1, QPen(Qt.NoPen), QColor(color))
        self.scene.update() 
        
        # Draw maze edges
        edges = self.maze_map.get((x, y), {})
        if edges.get('T') == 0:
            self.scene.addLine(x1, y1, x2, y1, Qt.black)  # Top
        if edges.get('R') == 0:
            self.scene.addLine(x2, y1, x2, y2, Qt.black)  # Right
        if edges.get('B') == 0:
            self.scene.addLine(x2, y2, x1, y2, Qt.black)  # Bottom
        if edges.get('L') == 0:
            self.scene.addLine(x1, y2, x1, y1, Qt.black)  # Left

    #Hiển thị đường đi tìm kiếm hoặc đường đi kết quả trên giao diện.   
    def tracePath(self, Path, color, onComplete=None):
        if len(Path) == 0:
            if onComplete:
                onComplete()
            return

        x, y = Path.pop(0)  # pop first element
        self.print_cell(x, y, color)
        
        if len(Path) > 0:
            QTimer.singleShot(200, lambda: self.tracePath(Path, color, onComplete))  # Delay the next step
        else:
            if onComplete:
                QTimer.singleShot(200, onComplete)  # Call onComplete when finished
    
    def solve(self, source, destination, typ):
        
        # Thực hiện tìm đường (logic A* cần được cài đặt trong MazeLogic)
        search_path, forward_path = MSA.greedyBFS(self.maze_map, self.width, self.height, source, destination,typ)

        # Hiển thị đường đi
        self.tracePath(search_path, "#00BFFF", lambda: self.tracePath(forward_path, "#FFFF00"))

        # Cập nhật thông tin
        self.path_len_label.setText(f"Greedy BFS Path Length: {len(forward_path) + 1}")
        self.search_len_label.setText(f"Greedy BFS Search Length: {len(search_path)}")
        self.scene.update() 