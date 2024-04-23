import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from ui.screens.MainWindow import MediaPlayer





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MediaPlayer()
    window.setWindowTitle('Python Media Player')
    window.setWindowIcon(QIcon('assets/logo.png'))
    window.setGeometry(300, 300, 600, 400)
    window.show()
    sys.exit(app.exec_())
