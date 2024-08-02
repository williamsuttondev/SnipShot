import sys
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from ScreenshotWindow import ScreenshotWindow

class SnippingWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SnippingWindow, self).__init__()
        self.screenshot_window = None
        self.parent = parent
        self.setWindowOpacity(0.3)
        self.begin = self.end = None
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowState(Qt.WindowFullScreen)

        # Get the screen where the application window is displayed
        self.screen_geometry = self.screen().geometry()

    def paintEvent(self, event):
        if self.begin and self.end:
            rect = QRect(self.begin, self.end)
            painter = QPainter(self)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 0, 0, 100))
            painter.drawRect(self.rect())
            painter.setBrush(QColor(255, 0, 0, 255))
            painter.drawRect(rect)

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = None
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        self.capture_screen(x1, y1, x2, y2)
        self.close()
        self.parent.show()

    def capture_screen(self, x1, y1, x2, y2):
        screen = QApplication.primaryScreen()
        # Correcting the capture area based on the screen where the application is running
        offset = self.screen_geometry.topLeft()
        x1 += offset.x()
        y1 += offset.y()
        screenshot = screen.grabWindow(0, x1, y1, x2 - x1, y2 - y1)
        self.display_screenshot_window(screenshot)

    def display_screenshot_window(self, screenshot):
        self.screenshot_window = ScreenshotWindow(screenshot)
        # Position the window on the same screen as the application
        self.screenshot_window.move(self.screen_geometry.topLeft() + QPoint(100, 100))  # Adjust offset as needed
        self.screenshot_window.show()