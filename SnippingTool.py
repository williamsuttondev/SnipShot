import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from SnippingWindow import SnippingWindow


def screen_at(point):
    """Returns the screen at the given point"""
    for screen in QApplication.screens():
        if screen.geometry().contains(point):
            return screen
    return QApplication.primaryScreen()


class SnippingTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Snipping Tool')
        self.setGeometry(100, 100, 300, 100)
        self.setFixedSize(300, 100)  # Set fixed size to make it non-resizable
        self.start_button = QPushButton('Capture Screenshot', self)
        self.start_button.setGeometry(50, 20, 200, 60)
        self.start_button.clicked.connect(self.start_snipping)
        self.show()

    def start_snipping(self):
        self.hide()
        screen = screen_at(self.geometry().center())
        self.snipping_window = SnippingWindow(screen, self)
        self.snipping_window.showFullScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    snipping_tool = SnippingTool()
    sys.exit(app.exec_())