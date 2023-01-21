from PySide6.QtWidgets import QMainWindow, QMenu, QToolBar, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QKeySequence
from DrawingWidget import DrawingWidget
from DataHandler import DataHandler


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.drawing = DrawingWidget()
        self.data_handler = DataHandler("data.csv")

        # Menubar
        self.setWindowTitle("DigitRecognition")
        self.menu_bar = self.menuBar()
        self.toolbar_menu = QMenu("Toolbar")
        self.menu_bar.addMenu(self.toolbar_menu)

        # Actions
        self.clear_drawing_action = QAction("Clear drawing")
        self.clear_drawing_action.setToolTip("Shortcut: C")
        self.clear_drawing_action.setShortcut(QKeySequence("C"))
        self.clear_drawing_action.triggered.connect(self.clear_drawing_action_triggered)
        self.menu_bar.addAction(self.clear_drawing_action)

        self.generate_data_action = QAction("Generate data")
        self.generate_data_action.triggered.connect(self.generate_data_action_triggered)
        self.test_data_action = QAction("Test data")
        self.test_data_action.triggered.connect(self.test_data_action_triggered)
        self.toolbar_menu.addActions([self.generate_data_action, self.test_data_action])

        # Toolbars
        self.generate_data_toolbar = QToolBar("Generate data")
        self.generate_data_toolbar.setIconSize(QSize(15, 15))

        self.generate_data_toolbar.addWidget(QLabel("Classification: "))
        self.classification_lineedit = QLineEdit()
        self.generate_data_toolbar.addWidget(self.classification_lineedit)
        self.add_to_datafile_btn = QPushButton("Add to datafile")
        self.add_to_datafile_btn.pressed.connect(self.add_to_datafile_btn_pressed)
        self.generate_data_toolbar.addWidget(self.add_to_datafile_btn)

        self.test_data_toolbar = QToolBar("Test data")
        self.generate_data_action.trigger()

        self.setCentralWidget(self.drawing)
        self.show()

    def generate_data_action_triggered(self):
        self.removeToolBar(self.test_data_toolbar)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.generate_data_toolbar)
        self.generate_data_toolbar.show()

    def test_data_action_triggered(self):
        self.removeToolBar(self.generate_data_toolbar)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.test_data_toolbar)
        self.test_data_toolbar.show()

    def clear_drawing_action_triggered(self):
        self.drawing.clear_image()

    def add_to_datafile_btn_pressed(self):
        self.data_handler.add_data_to_file(self.drawing.image, self.classification_lineedit.text())
        self.drawing.clear_image()
