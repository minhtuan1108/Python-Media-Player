import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QWidget, QVBoxLayout

from ui.components.MainFrame import MainFrame
from ui.components.Tab_bar import Tab_Bar


# Main container for all screen
class MediaPlayer(QMainWindow):
    def __init__(self):
        super().__init__()


        # Tạo widget để chứa các thành phần bên trong
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setWindowIcon(QIcon('assets/logo.png'))
        
        self.central_widget.setStyleSheet("""
                background: black;
        """)

        # Tạo một layout để chứa các thành phần bên trong
        self.hBoxLayout = QVBoxLayout()
        self.hBoxLayout.setContentsMargins(10, 0, 10, 0)

        # Thêm component cần test vào đây
        self.hBoxLayout.addLayout(Tab_Bar())
        self.hBoxLayout.addWidget(MainFrame())

        self.central_widget.setLayout(self.hBoxLayout)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MediaPlayer()
    window.setWindowTitle('Python Media Player')
    window.setWindowIcon(QIcon('assets/logo.png'))
    window.setGeometry(300, 300, 600, 400)
    window.show()
    sys.exit(app.exec_())
