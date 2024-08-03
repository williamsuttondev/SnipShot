import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from SnippingWindow import SnippingWindow

# Constants for window geometry
WINDOW_X = 100
WINDOW_Y = 100
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 100
BUTTON_X = 50
BUTTON_Y = 20
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60


def screen_at(point):
    """Returns the screen at the given point.
    Args:
        point (QPoint): The point to check which screen it belongs to.
    Returns:
        QScreen: The screen that contains the given point, or the primary screen if none found.
    """
    for screen in QApplication.screens():
        if screen.geometry().contains(point):
            return screen
    return QApplication.primaryScreen()


class SnippingTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self._snipping_window = None  # Private member to hold the snipping window instance
        self.setWindowTitle('Snipping Tool')
        self.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)  # Set fixed size to make it non-resizable

        # Create and configure the start button
        self.start_button = QPushButton('Capture Screenshot', self)
        self.start_button.setGeometry(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.start_button.clicked.connect(self.start_snipping)
        self.show()

    def start_snipping(self):
        """Starts the snipping process by hiding the main window and showing the snipping window."""
        self.hide()
        screen = screen_at(self.geometry().center())
        self._snipping_window = SnippingWindow(screen, self)
        self._snipping_window.showFullScreen()


def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    snipping_tool = SnippingTool()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
