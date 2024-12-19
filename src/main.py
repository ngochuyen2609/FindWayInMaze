from PyQt5 import QtWidgets, uic
import sys
from MazeWidget import MazeWidget
from MazeLogic import MazeLogic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("src/ui/application.ui", self)  # Load the .ui file
        self.verticalLayoutAstar = self.findChild(QtWidgets.QVBoxLayout, "verticalLayoutAstar")
        geometry = self.verticalLayoutAstar.geometry()
        self.astar_widget = MazeWidget(width=geometry.width(), height=geometry.height(), cell_size=20)
        self.verticalLayoutAstar.addWidget(self.astar_widget)
        
        self.verticalLayoutGreedyBFS = self.findChild(QtWidgets.QVBoxLayout, "verticalLayoutGreedyBFS")
        geometry = self.verticalLayoutGreedyBFS.geometry()
        self.greedy_widget = MazeWidget(width=geometry.width(), height=geometry.height(), cell_size=20)
        self.verticalLayoutGreedyBFS.addWidget(self.greedy_widget)
        
        self.createMaze = self.findChild(QtWidgets.QPushButton, "createMaze")
        self.createMaze.clicked.connect(self.generate_maze)
        self.displayCells = self.findChild(QtWidgets.QPushButton, "displayCells")
        self.displayCells.clicked.connect(self.display)
        self.clearPaths = self.findChild(QtWidgets.QPushButton, "clearPath")
        self.clearPaths.clicked.connect(self.clearOldPath)
        
        self.heuristicEuclid = self.findChild(QtWidgets.QPushButton, "heuristicEuclid")
        self.heuristicEuclid.clicked.connect(lambda: self.solve(2))
        self.heuristicManhattan = self.findChild(QtWidgets.QPushButton, "heuristicManhattan")
        self.heuristicManhattan.clicked.connect(lambda: self.solve(1))

        # Find label and entry widgets for width and height
        self.widthLabel = self.findChild(QtWidgets.QLabel, "labelEndX")
        self.heightLabel = self.findChild(QtWidgets.QLabel, "labelEndY")
        self.widthEntry = self.findChild(QtWidgets.QLineEdit, "widthEntry")
        self.heightEntry = self.findChild(QtWidgets.QLineEdit, "heightEntry")
        self.startX = self.findChild(QtWidgets.QLineEdit, "startX")
        self.startY = self.findChild(QtWidgets.QLineEdit, "startY")
        self.endX = self.findChild(QtWidgets.QLineEdit, "endX")
        self.endY = self.findChild(QtWidgets.QLineEdit, "endY")

    def generate_maze(self):
        try:
            # Lấy giá trị width, height từ input
            global width 
            width = int(self.widthEntry.text())
            global height
            height = int(self.heightEntry.text())

            if 0 < width <= 50 and 0 < height <= 50:
                # Update label information
                self.widthLabel.setText(f"X (default X = {(width-1)}):")
                self.heightLabel.setText(f"Y (default Y = {(height-1)}):")

                # Tạo logic chung cho mê cung
                global maze_logic
                maze_logic = MazeLogic(width, height)
                maze_logic.create_maze(width, height)

                # Lấy maze_map chung
                maze_map = maze_logic.maze_map

                # Cập nhật mê cung vào cả hai widgets
                self.astar_widget.maze_logic.maze_map = maze_map
                self.astar_widget.create_maze(width, height)

                self.greedy_widget.maze_logic.maze_map = maze_map
                self.greedy_widget.create_maze(width, height)

                self.astar_widget.update()
                self.greedy_widget.update()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Please enter valid values within the specified limits.")

        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Invalid input: {e}")
            
    def display(self):
        try:
            startX = int(self.startX.text())
            startY = int(self.startY.text())
            endX = int(self.endX.text())
            endY = int(self.endY.text())

            if width != 0 and height != 0:
                # Xác minh tọa độ
                if maze_logic.validate_coordinates(startX, startY, 0) and maze_logic.validate_coordinates(endX, endY, 1):
                    maze_logic.source = (startX, startY)
                    maze_logic.destination = (endX, endY)
                    
                    self.astar_widget.display(maze_logic.source, maze_logic.destination)
                    self.greedy_widget.display(maze_logic.source, maze_logic.destination)
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "Invalid coordinates.")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Please create the maze first.")
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Invalid input: {e}")

    def solve(self, typ):
        # Kiểm tra nếu maze_logic chưa được khởi tạo
        if width == 0 and height == 0:
            QtWidgets.QMessageBox.warning(self, "Error", "Please create the maze first.")
            return

        self.astar_widget.solve(maze_logic.source, maze_logic.destination,typ=1,typH = typ)
        self.greedy_widget.solve(maze_logic.source, maze_logic.destination,typ=2,typH = typ)
        
    def clearOldPath(self):
        if width == 0 and height == 0:
            QtWidgets.QMessageBox.warning(self, "Error", "Please create the maze first.")
            return

        self.astar_widget.clearPath()
        self.greedy_widget.clearPath()

        
            
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())