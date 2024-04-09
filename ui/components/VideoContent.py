from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel, QSlider, QToolButton, QComboBox, \
    QFrame


class VideoContent(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(10, 5, 10, 5)

        # Tạo khung chứa video
        self.videoWidget = QVideoWidget()
        self.videoWidget.setStyleSheet("""
                background-color: black
        """)

        # Tạo frame để điều chỉnh layout
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.StyledPanel)

        self.frame.setStyleSheet("""
                QFrame{
                    border-radius: 5px;
                    box-shadow: inset 20px 20px 40px rgba(0, 0, 0, 1); /* Shadow effect */
                }
                QToolButton { 
                    background-color: transparent; border: none; 
                }
        """)

        # Tạo khung chứa các chức năng của video
        self.containButtonsBox = QHBoxLayout()
        self.frame.setLayout(self.containButtonsBox)

        # Tạo button play
        self.playButton = QToolButton()
        self.playButton.setIcon(QIcon("assets/play.png"))

        # Tạo button tua tới 10s
        self.forward10Button = QToolButton()
        self.forward10Button.setIcon(QIcon("assets/forward10.png"))

        # Tạo button tua ngược 10s
        self.replay10Button = QToolButton()
        self.replay10Button.setIcon(QIcon("assets/replay10.png"))

        # Tạo Label loa
        self.speakerButton = QToolButton()
        self.speakerButton.setIcon(QIcon("assets/speaker.png"))

        # Tạo thanh âm lượng
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setValue(50)  # Default volume
        self.volumeSlider.setTickPosition(QSlider.TicksBelow)
        self.volumeSlider.setTickInterval(10)
        self.volumeSlider.valueChanged.connect(self.changeVolume)
        self.volumeSlider.setStyleSheet("""
                    QSlider{
                        background-color: none
                    }
                   QSlider::groove:horizontal {
                       border: none;
                       height: 5px; /* Chiều cao của thanh slider */
                       background: none; /* Màu nền của thanh slider */
                       margin: 2px 0;
                       border-radius: 2px; /* Bo tròn các góc */
                   }
                   QSlider::handle:horizontal {
                       background: #FFFFFF; /* Màu của handle */
                       border: 1px solid #5c5c5c;
                       width: 12px; /* Chiều rộng của handle */
                       height: 12px; /* Chiều cao của handle */
                       margin: -4px 0; /* Điều chỉnh vị trí handle */
                       border-radius: 6px; /* Bo tròn các góc */
                   }
               """)

        # Tạo nút chỉnh tốc độ video
        self.speedComboBox = QComboBox()
        self.speedComboBox.addItems(['0.5x', '0.75x', '1.0x', '1.25x', '1.5x', '1.75x', '2.0x'])  # Tốc độ video có thể chọn

        # Thêm các button vào layout
        self.containButtonsBox.addWidget(self.replay10Button)
        self.containButtonsBox.addWidget(self.playButton)
        self.containButtonsBox.addWidget(self.forward10Button)
        self.containButtonsBox.addWidget(self.speakerButton)
        self.containButtonsBox.addWidget(self.volumeSlider)

        self.addWidget(self.videoWidget)
        self.addWidget(self.frame)

    def changeVolume(self, volume):
        self.volumeSlider.setValue(volume)
