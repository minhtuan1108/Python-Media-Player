import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class InputUrlDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Input Dialog")
        # self.setGeometry()

        # Tao layout
        layout = QGridLayout()

        contentLayout = QVBoxLayout()
        contentLayout.setAlignment(Qt.AlignHCenter)
        bottomLayout = QHBoxLayout()
        bottomLayout.setAlignment(Qt.AlignRight)
        layout.addLayout(contentLayout, 0, 0)
        layout.addLayout(bottomLayout, 1, 0)

        # Tao o nhap lieu
        self.label = QLabel('Enter url')
        self.textField = QLineEdit()
        self.textField.setPlaceholderText("https://...")
        # self.exampleLabel = QLabel('Template:')

        contentLayout.addWidget(self.label)
        contentLayout.addWidget(self.textField)

        # Tao button
        self.playButton = QPushButton("Play")
        self.playButton.clicked.connect(self.handle_play)
        self.cancel = QPushButton("Cancel")
        self.cancel.clicked.connect(self.handle_close)

        bottomLayout.addWidget(self.playButton)
        bottomLayout.addWidget(self.cancel)

        self.setLayout(layout)

    def handle_play(self):
        url = self.textField.text().rstrip()
        print("Input url: " + url)
        if url != None:
            if "youtube.com" in url:
                self.handle_close()
                self.parent.media_player.get_url_from_clip('youtube')
            elif "http" in url:
                self.handle_close()
                self.parent.media_player.get_url_from_clip('http')
            else:
                # Thông báo lỗi
                QMessageBox.critical(self, "Error", "Your url invalid format")

        
    def handle_close(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InputUrlDialog()
    window.show()
    sys.exit(app.exec_())
        


