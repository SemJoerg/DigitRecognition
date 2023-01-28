from PySide6.QtWidgets import QMainWindow, QMenu, QToolBar, QLabel, QComboBox, QPushButton, QMessageBox
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QKeySequence, QFont
from DrawingWidget import DrawingWidget
from data_handler import DataHandler
import tensorflow as tf
import numpy as np
from tensorflow import keras


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.drawing = DrawingWidget()
        self.data_handler = DataHandler("data.npz")
        self.model: keras.models.Model = keras.models.load_model("./models/main_model")
        font = QFont()
        font.setPointSize(13)

        # Menubar
        self.setWindowTitle("DigitRecognition")
        self.menu_bar = self.menuBar()
        self.toolbar_menu = QMenu("Toolbar")
        self.menu_bar.addMenu(self.toolbar_menu)

        # Actions
        self.clear_drawing_action = QAction("Clear drawing")
        self.clear_drawing_action.setToolTip("Shortcut: C")
        self.clear_drawing_action.setShortcut(QKeySequence("Backspace"))
        self.clear_drawing_action.triggered.connect(self.clear_drawing_action_triggered)
        self.menu_bar.addAction(self.clear_drawing_action)

        self.generate_data_action = QAction("Generate data")
        self.generate_data_action.triggered.connect(self.generate_data_action_triggered)
        self.test_data_action = QAction("Test data")
        self.test_data_action.triggered.connect(self.test_data_action_triggered)
        self.toolbar_menu.addActions([self.generate_data_action, self.test_data_action])

        # Toolbars
        self.generate_data_toolbar = QToolBar("Generate data")
        self.classificationn_label = QLabel("Classification: ")
        self.generate_data_toolbar.addWidget(self.classificationn_label)
        self.classification_combobox = QComboBox()
        self.classification_combobox.addItems(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.generate_data_toolbar.addWidget(self.classification_combobox)
        self.add_to_datafile_btn = QPushButton("Add to datafile")
        self.add_to_datafile_btn.pressed.connect(self.add_to_datafile_btn_pressed)
        self.add_to_datafile_btn.setShortcut(QKeySequence("Enter"))
        self.generate_data_toolbar.addWidget(self.add_to_datafile_btn)

        self.plot_data_btn = QPushButton("Plot first 100 entries")
        self.plot_data_btn.pressed.connect(self.plot_data_btn_pressed)
        self.generate_data_toolbar.addWidget(self.plot_data_btn)

        self.classificationn_label.setFont(font)
        self.classification_combobox.setFont(font)
        self.add_to_datafile_btn.setFont(font)

        self.test_data_toolbar = QToolBar("Test data")
        self.detect_digit_btn = QPushButton("Detect Digit")
        self.detect_digit_btn.pressed.connect(self.detect_digit_btn_pressed)
        self.detect_digit_btn.setFont(font)
        self.detect_digit_btn.setShortcut("Space")
        self.test_data_toolbar.addWidget(self.detect_digit_btn)


        self.test_data_action.trigger()
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
        self.data_handler.add_data_to_file(self.drawing.image, int(self.classification_combobox.currentText()))
        self.drawing.clear_image()

    def plot_data_btn_pressed(self):
        self.data_handler.plot_data()

    def detect_digit_btn_pressed(self):
        prediction_data: np.ndarray = self.model.predict(np.array([DataHandler.image_to_nparray(self.drawing.image)], dtype=np.int8))
        prediction = np.argmax(prediction_data)
        QMessageBox.information(self, "Prediction", f"You draw a {prediction}")
        self.drawing.clear_image()