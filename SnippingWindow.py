import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter, QColor, QClipboard
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QDialog


class SnippingWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SnippingWindow, self).__init__()
        self.parent = parent
        self.setWindowOpacity(0.3)
        self.begin = self.end = None
        self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowState(Qt.WindowFullScreen)

    def paintEvent(self, event):
        if self.begin and self.end:
            rect = QRect(self.begin, self.end)
            painter = QPainter(self)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 0, 0, 100))
            painter.drawRect(self.rect())
            painter.setBrush(QColor(255, 0, 0, 255))
            painter.drawRect(rect)

    def mousePressEvent(self, a0):
        self.begin = a0.pos()
        self.end = None
        self.update()

    def mouseMoveEvent(self, a0):
        self.end = a0.pos()
        self.update()

    # def mouseReleaseEvent(self, a0):
    #     x1 = min(self.begin.x(), self.end.x())
    #     y1 = min(self.begin.y(), self.end.y())
    #     x2 = max(self.begin.x(), self.end.x())
    #     y2 = max(self.begin.y(), self.end.y())
    #     self.capture_screen(x1, y2, x2, y2)
    #     self.close()
    #     self.parent.show()
