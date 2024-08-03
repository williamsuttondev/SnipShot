from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QDialog, QMenu, QAction

# Constants for window properties
WINDOW_TITLE = "Screenshot Preview"
WINDOW_X = 100
WINDOW_Y = 100
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MIN_WINDOW_WIDTH = 400
MIN_WINDOW_HEIGHT = 300
BUTTON_TEXT = "Copy to Clipboard"
CONTEXT_MENU_COPY_TEXT = "Copy"


class ScreenshotWindow(QDialog):
    def __init__(self, screenshot, parent=None):
        """Initialize the ScreenshotWindow.

        Args:
            screenshot (QPixmap): The screenshot to display.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super(ScreenshotWindow, self).__init__(parent)
        self._screenshot = screenshot

        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

        layout = QVBoxLayout()

        # Display the screenshot
        self._screenshot_label = QLabel(self)
        self._screenshot_label.setAlignment(Qt.AlignCenter)
        self._screenshot_label.setPixmap(
            self._screenshot.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(self._screenshot_label)

        # Copy to Clipboard button
        self._copy_button = QPushButton(BUTTON_TEXT, self)
        self._copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self._copy_button)

        self.setLayout(layout)

    def resizeEvent(self, event):
        """Handle the resize event to scale the screenshot.

        Args:
            event (QResizeEvent): The resize event.
        """
        self._screenshot_label.setPixmap(
            self._screenshot.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        super(ScreenshotWindow, self).resizeEvent(event)

    def copy_to_clipboard(self):
        """Copy the screenshot to the clipboard."""
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(self._screenshot)

    def contextMenuEvent(self, event):
        """Handle the context menu event to provide a copy option.

        Args:
            event (QContextMenuEvent): The context menu event.
        """
        context_menu = QMenu(self)
        copy_action = QAction(CONTEXT_MENU_COPY_TEXT, self)
        copy_action.triggered.connect(self.copy_to_clipboard)
        context_menu.addAction(copy_action)
        context_menu.exec_(event.globalPos())
