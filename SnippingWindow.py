import time
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow
from ScreenshotWindow import ScreenshotWindow


class SnippingWindow(QMainWindow):
    def __init__(self, screen, parent=None):
        super(SnippingWindow, self).__init__(parent)
        self.screen = screen
        self.screenshot_window = None
        self.parent = parent
        self.setWindowOpacity(0.3)
        self.begin = self.end = None
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(self.screen.geometry())

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw the red outline around the entire window
        pen = QPen(QColor(255, 0, 0), 3)  # Red color with 3px width
        painter.setPen(pen)
        painter.drawRect(self.rect().adjusted(1, 1, -1, -1))

        # If a region is being selected, draw the selection rectangle
        if self.begin and self.end:
            rect = QRect(self.begin, self.end)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 0, 0, 100))
            painter.drawRect(self.rect())
            painter.setBrush(QColor(255, 0, 0, 100))
            painter.drawRect(rect)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
            if self.parent:
                self.parent.show()

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = None
        self.update()

    def mouseMoveEvent(self, event):
        # Constrain the cursor position within the screen's geometry
        x = max(self.screen.geometry().left(), min(event.globalX(), self.screen.geometry().right() - 1))
        y = max(self.screen.geometry().top(), min(event.globalY(), self.screen.geometry().bottom() - 1))
        QCursor.setPos(x, y)
        self.end = self.mapFromGlobal(QPoint(x, y))
        self.update()

    def mouseReleaseEvent(self, event):
        # Constrain the final position
        x = max(self.screen.geometry().left(), min(event.globalX(), self.screen.geometry().right() - 1))
        y = max(self.screen.geometry().top(), min(event.globalY(), self.screen.geometry().bottom() - 1))
        self.end = self.mapFromGlobal(QPoint(x, y))
        self.update()  # Trigger a final paint event
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        self.capture_screen(x1, y1, x2, y2)
        self.close()
        if self.parent:
            self.parent.show()

    def capture_screen(self, x1, y1, x2, y2):
        self.hide()
        QApplication.processEvents()
        time.sleep(0.1)
        # Use the coordinates directly without additional offset adjustments
        global_x1 = x1
        global_y1 = y1
        global_x2 = x2
        global_y2 = y2
        # Ensure capturing is within the screen bounds
        capture_width = max(0, global_x2 - global_x1)
        capture_height = max(0, global_y2 - global_y1)
        if capture_width > 0 and capture_height > 0:
            screenshot = self.screen.grabWindow(0, global_x1, global_y1, capture_width, capture_height)
            self.display_screenshot_window(screenshot)
        else:
            print("Invalid capture area, skipping screenshot.")

    def display_screenshot_window(self, screenshot):
        self.screenshot_window = ScreenshotWindow(screenshot)
        self.screenshot_window.move(self.screen.geometry().topLeft() + QPoint(100, 100))
        self.screenshot_window.show()
