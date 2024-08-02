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
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowState(Qt.WindowFullScreen)

    def paintEvent(self, event):
        if self.begin and self.end:
            rect = QRect(self.begin, self.end)
            painter = QPainter(self)
            painter.setPen(Qt.NoPen)
            painter.setBrush((0, 0, 0, 100))
            painter.drawRect(self.rect())
            painter.setBrush(QColor(128, 128, 255, 128))
            painter.drawRect(rect)
