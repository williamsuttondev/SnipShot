from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QDialog, QMenu, QAction

class ScreenshotWindow(QDialog):
    def __init__(self, screenshot, parent=None):
        super(ScreenshotWindow, self).__init__(parent)
        self.screenshot = screenshot

        self.setWindowTitle("Screenshot Preview")
        self.setGeometry(100, 100, 800, 600)  # Set initial size to 800x600
        self.setMinimumSize(400, 300)  # Optional: Set a minimum size

        layout = QVBoxLayout()

        # Display the screenshot
        self.screenshot_label = QLabel(self)
        self.screenshot_label.setAlignment(Qt.AlignCenter)
        self.screenshot_label.setPixmap(
            self.screenshot.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(self.screenshot_label)

        # Copy to Clipboard button
        self.copy_button = QPushButton("Copy to Clipboard", self)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.copy_button)

        self.setLayout(layout)

    def resizeEvent(self, event):
        # Scale the screenshot to fit the new window size
        self.screenshot_label.setPixmap(
            self.screenshot.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        super(ScreenshotWindow, self).resizeEvent(event)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(self.screenshot)

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(self.copy_to_clipboard)
        context_menu.addAction(copy_action)
        context_menu.exec_(event.globalPos())