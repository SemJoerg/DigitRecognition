from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QImage, QPixmap, QResizeEvent, QPainter, QPen, QMouseEvent
from PySide6.QtCore import Qt


class DrawingWidget(QLabel):

    def __init__(self):
        super().__init__()
        self.setMinimumSize(128, 128)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.__image_size = 24
        self.brush_size = 2

        # Creates White/Black image |   1 = White    0 = Black
        self.image = QImage(self.__image_size, self.__image_size, QImage.Format.Format_Mono)
        self.image.fill(1)
        self.update_image()

    def update_image(self) -> None:
        self.setPixmap(QPixmap(self.image).scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def clear_image(self) -> None:
        self.image.fill(1)
        self.update_image()

    def draw_point_on_image(self, x: int, y: int) -> None:
        painter = QPainter(self.image)
        painter.setPen(QPen(Qt.GlobalColor.black, self.brush_size, Qt.PenStyle.SolidLine))
        painter.drawPoint(x, y)
        painter.end()
        self.update_image()

    def try_drawing_labelpoint(self, label_x: int, label_y: int) -> None:
        pixmap_width = self.pixmap().size().width()
        pixmap_height = self.pixmap().size().height()
        delta_x = int((self.size().width() - pixmap_width) / 2)
        delta_y = int((self.size().height() - pixmap_height) / 2)
        pixmap_x = label_x - delta_x
        pixmap_y = label_y - delta_y

        if pixmap_x < 0 or pixmap_y < 0 or pixmap_x > pixmap_width or pixmap_y > pixmap_height:
            return

        image_x = int(pixmap_x * self.__image_size / pixmap_width)
        image_y = int(pixmap_y * self.__image_size / pixmap_height)

        self.draw_point_on_image(image_x, image_y)

    # Events
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.update_image()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.try_drawing_labelpoint(event.x(), event.y())

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.try_drawing_labelpoint(event.x(), event.y())

