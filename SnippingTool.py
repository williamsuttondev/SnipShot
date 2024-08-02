import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter, QColor, QClipboard
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QDialog, QPushButton, QVBoxLayout


class SnippingTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Snipping Tool')
        self.setGeometry(100, 100, 300, 100)
        self.start_button = QPushButton('Capture Screenshot', self)
        self.start_button.setGeometry(50, 20, 200, 60)
        self.start_button.clicked.connect(self.start_snipping)
        self.show()

    def start_snipping(self):
        self.hide()
        #self.snipping_window = SnippingWindow(self)
        #self.snipping_window.showFullScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    snipping_tool = SnippingTool()
    sys.exit(app.exec_())
