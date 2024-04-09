import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QWidget

from ui.components.MainFrame import MainFrame


# Main container for all screen
class MediaPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Python Media Player')
        self.setWindowIcon(QIcon('/themes/logo.png'))

        # Tạo widget để chứa các thành phần bên trong
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet("""
            background-color: rgba(22, 20, 22, 0.76);
        """)

        # Tạo một layout để chứa các thành phần bên trong
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.setContentsMargins(10, 0, 10, 0)

        # Thêm component cần test vào đây
        self.hBoxLayout.addWidget(MainFrame())

        self.setLayout(self.hBoxLayout)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MediaPlayer()
    window.setGeometry(300, 300, 600, 400)
    window.show()
    sys.exit(app.exec_())
