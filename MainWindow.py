from PySide6.QtWidgets import QMainWindow
from DrawingWidget import DrawingWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DigitRecognition")
        self.setCentralWidget(DrawingWidget())

        self.show()
