import sys
from MainWindow import MainWindow
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)
main_window = MainWindow()
app.exec()

