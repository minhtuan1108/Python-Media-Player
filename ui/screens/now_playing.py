import sys

from PyQt5.QtCore import QRect
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QApplication


class NowPlayingScreen(QWidget):
    def __init__(self):
        super().__init__()

        # create containers
        self.mainContainer = QHBoxLayout(self)
        self.mainContainer.setObjectName("maincontainer")
        self.mainContainer.setGeometry(QRect(50, 50, 300, 200))
        self.setLayout(self.mainContainer)

        self.setWindowTitle('Test CSS')
        self.setStyleSheet("""
            QHBoxLayout#maincontainer {
                background-color: black;
            }
        """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NowPlayingScreen()
    window.setGeometry(200, 200, 600, 400)
    window.show()
    sys.exit(app.exec_())
