from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter, QColor, QClipboard
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QDialog


class ScreenshotWindow(QDialog):
    def __init__(self, screenshot, parent=None):
        super(ScreenshotWindow, self).__init__(parent)
        self.screenshot = screenshot

        self.setWindowTitle("Screenshot Preview")
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()

        # Display the screenshot
        self.screenshot_label = QLabel(self)
        self.screenshot_label.setPixmap(self.screenshot)
        layout.addWidget(self.screenshot_label)

        # Copy to Clipboard button
        self.copy_button = QPushButton("Copy to Clipboard", self)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.copy_button)

        self.setLayout(layout)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(self.screenshot)