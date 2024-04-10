import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QSlider, QFrame
from PyQt5.QtCore import Qt

class CustomSlider(QSlider):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
            QSlider::groove:horizontal {
                border: none;
                height: 6px;
                background-color: #ddd;
                margin: 0px;
            }

            QSlider::handle:horizontal {
                background-color: #2196F3;
                border: 2px solid #fff;
                width: 12px;
                margin: -3px 0;
                border-radius: 6px;
            }
        """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom Slider Example")
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        # Tạo slider và frame
        self.slider = CustomSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        layout.addWidget(self.slider)

        self.frame = QFrame(self.slider)
        self.frame.setStyleSheet("background-color: #2196F3;")
        self.frame.setFixedWidth(50)
        layout.addWidget(self.frame)

        self.slider.sliderMoved.connect(self.move_frame)
        self.slider.valueChanged.connect(self.move_frame)

    def move_frame(self, value):
        groove_rect = self.slider.style().subControlRect(QSlider.Slider, self.slider, QSlider.Groove)
        groove_pos = self.slider.mapToGlobal(groove_rect.topLeft())
        frame_pos = self.mapFromGlobal(groove_pos)
        self.frame.move(frame_pos)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
