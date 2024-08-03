import time
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow
from ScreenshotWindow import ScreenshotWindow

# Constants for window properties
WINDOW_OPACITY = 0.3
PEN_COLOR = QColor(255, 0, 0)  # Red color
PEN_WIDTH = 3
SELECTION_COLOR = QColor(0, 0, 0, 100)  # Semi-transparent black
HIGHLIGHT_COLOR = QColor(255, 0, 0, 100)  # Semi-transparent red
SLEEP_DURATION = 0.1
SCREENSHOT_OFFSET_X = 100
SCREENSHOT_OFFSET_Y = 100


class SnippingWindow(QMainWindow):
    def __init__(self, screen, parent=None):
        """Initialize the SnippingWindow.

        Args:
            screen (QScreen): The screen where the snipping window will be displayed.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super(SnippingWindow, self).__init__(parent)
        self._screen = screen
        self._screenshot_window = None
        self._parent = parent
        self.setWindowOpacity(WINDOW_OPACITY)
        self._begin = self._end = None
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(self._screen.geometry())

    def paintEvent(self, event):
        """Handle the paint event to draw the selection rectangle.

        Args:
            event (QPaintEvent): The paint event.
        """
        painter = QPainter(self)

        # Draw the red outline around the entire window
        pen = QPen(PEN_COLOR, PEN_WIDTH)
        painter.setPen(pen)
        painter.drawRect(self.rect().adjusted(1, 1, -1, -1))

        # If a region is being selected, draw the selection rectangle
        if self._begin and self._end:
            rect = QRect(self._begin, self._end)
            painter.setPen(Qt.NoPen)
            painter.setBrush(SELECTION_COLOR)
            painter.drawRect(self.rect())
            painter.setBrush(HIGHLIGHT_COLOR)
            painter.drawRect(rect)

    def keyPressEvent(self, event):
        """Handle the key press event to close the window on Escape key.

        Args:
            event (QKeyEvent): The key press event.
        """
        if event.key() == Qt.Key_Escape:
            self.close()
            if self._parent:
                self._parent.show()

    def mousePressEvent(self, event):
        """Handle the mouse press event to start the selection.

        Args:
            event (QMouseEvent): The mouse press event.
        """
        self._begin = event.pos()
        self._end = None
        self.update()

    def mouseMoveEvent(self, event):
        """Handle the mouse move event to update the selection rectangle.

        Args:
            event (QMouseEvent): The mouse move event.
        """
        # Constrain the cursor position within the screen's geometry
        x = max(self._screen.geometry().left(), min(event.globalX(), self._screen.geometry().right() - 1))
        y = max(self._screen.geometry().top(), min(event.globalY(), self._screen.geometry().bottom() - 1))
        QCursor.setPos(x, y)
        self._end = self.mapFromGlobal(QPoint(x, y))
        self.update()

    def mouseReleaseEvent(self, event):
        """Handle the mouse release event to finalize the selection.

        Args:
            event (QMouseEvent): The mouse release event.
        """
        # Constrain the final position
        x = max(self._screen.geometry().left(), min(event.globalX(), self._screen.geometry().right() - 1))
        y = max(self._screen.geometry().top(), min(event.globalY(), self._screen.geometry().bottom() - 1))
        self._end = self.mapFromGlobal(QPoint(x, y))
        self.update()  # Trigger a final paint event
        x1 = min(self._begin.x(), self._end.x())
        y1 = min(self._begin.y(), self._end.y())
        x2 = max(self._begin.x(), self._end.x())
        y2 = max(self._begin.y(), self._end.y())
        self.capture_screen(x1, y1, x2, y2)
        self.close()
        if self._parent:
            self._parent.show()

    def capture_screen(self, x1, y1, x2, y2):
        """Capture the selected screen area.

        Args:
            x1 (int): The x-coordinate of the top-left corner.
            y1 (int): The y-coordinate of the top-left corner.
            x2 (int): The x-coordinate of the bottom-right corner.
            y2 (int): The y-coordinate of the bottom-right corner.
        """
        self.hide()
        QApplication.processEvents()
        time.sleep(SLEEP_DURATION)
        # Use the coordinates directly without additional offset adjustments
        global_x1 = x1
        global_y1 = y1
        global_x2 = x2
        global_y2 = y2
        # Ensure capturing is within the screen bounds
        capture_width = max(0, global_x2 - global_x1)
        capture_height = max(0, global_y2 - global_y1)
        if capture_width > 0 and capture_height > 0:
            screenshot = self._screen.grabWindow(0, global_x1, global_y1, capture_width, capture_height)
            self.display_screenshot_window(screenshot)
        else:
            print("Invalid capture area, skipping screenshot.")

    def display_screenshot_window(self, screenshot):
        """Display the captured screenshot in a new window.

        Args:
            screenshot (QPixmap): The captured screenshot.
        """
        self._screenshot_window = ScreenshotWindow(screenshot)
        self._screenshot_window.move(
            self._screen.geometry().topLeft() + QPoint(SCREENSHOT_OFFSET_X, SCREENSHOT_OFFSET_Y))
        self._screenshot_window.show()
