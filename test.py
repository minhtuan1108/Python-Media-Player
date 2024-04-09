import sys

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QApplication, QFrame, QVBoxLayout


class StyledLayoutWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Set background color and corner radius for the widget
        self.setStyleSheet('background-color: black; border-radius: 10px; padding: 10px;')

        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet('background-color: white; border-radius: 40px;')

        vbox = QVBoxLayout()
        vbox.addWidget(frame)

        hbox = QHBoxLayout()
        btn1 = QPushButton('Button 1')
        btn1.setStyleSheet('background-color: yellow; border-radius: 10px;')
        btn2 = QPushButton('Button 2')
        btn2.setStyleSheet('background-color: green; border-radius: 10px')
        hbox.addWidget(btn1)
        hbox.addWidget(btn2)
        frame.setLayout(hbox)
        self.setLayout(vbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StyledLayoutWidget()
    window.setWindowTitle('Styled Layout Example')
    window.setGeometry(100, 100, 400, 200)
    window.show()
    sys.exit(app.exec_())
