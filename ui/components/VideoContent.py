from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *

from ui.components.MediaPlayer import MyMediaPlayer


class VideoContent(QGridLayout):
    def __init__(self, parent: QFrame):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        # Thiết lập sự kiện chuột
        parent.enterEvent = self.frame_enter_event
        parent.leaveEvent = self.frame_leave_event

        # Tạo khung chứa video
        self.videoWidget = QVideoWidget()
        self.videoWidget.setStyleSheet("border-radius: 20px")
        self.videoWidget.mousePressEvent = self.play_pause_video
        self.media_player = MyMediaPlayer(self)
        self.media_player.setVideoOutput(self.videoWidget)
        self.media_player.play_from_url("https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8")

        # Tạo frame để điều chỉnh layout
        self.frame = QFrame()
        self.frame.hide()
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFixedHeight(80)
        self.frame.setStyleSheet("""
                            QFrame {
                                 background-color: rgba(0, 0, 0, 0.15);
                                 border-radius: 10px;
                            }

                            QPushButton{
                                background-color: none;
                            }
            """)

        # Tạo khung chứa thanh thời gian của video và các nút chức năng
        self.containerBox = QVBoxLayout()
        self.frame.setLayout(self.containerBox)

        # Tạo khung chứa các chức năng của video
        self.containButtonsBox = QHBoxLayout()

        # Tạo button play
        self.playButton = QPushButton()
        self.playButton.setIcon(QIcon("assets/pause.png"))
        self.playButton.setIconSize(QSize(32, 32))
        self.playButton.clicked.connect(self.play_pause_video)

        # Tạo button tua tới 10s
        self.forward10Button = QPushButton()
        self.forward10Button.setIcon(QIcon("assets/forward10.png"))

        # Tạo button tua ngược 10s
        self.replay10Button = QPushButton()
        self.replay10Button.setIcon(QIcon("assets/replay10.png"))

        # Tạo layout chưa 3 nút bên trên
        self.playVideoBox = QHBoxLayout()
        self.playVideoBox.setAlignment(Qt.AlignLeft)
        self.playVideoBox.addWidget(self.replay10Button)
        self.playVideoBox.addWidget(self.playButton)
        self.playVideoBox.addWidget(self.forward10Button)
        self.containButtonsBox.addLayout(self.playVideoBox)

        # Tạo Label loa
        self.speakerButton = QPushButton()
        self.speakerButton.setIcon(QIcon("assets/speaker.png"))
        self.speakerButton.setFixedWidth(32)
        self.speakerButton.setIconSize(QSize(32, 32))

        # Tạo thanh âm lượng
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setFixedWidth(100)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setValue(100)  # Default volume
        self.volumeSlider.sliderMoved.connect(self.changeVolume)
        # self.volumeSlider.sliderReleased.connect(self.slider_released)
        # Khi thanh trượt được nhấn, xử lý sự kiện
        # self.volumeSlider.sliderPressed.connect(self.slider_pressed)
        self.slider_style = """
                    QSlider{
                        background-color: none
                    }
                   QSlider::groove:horizontal {
                       border: none;
                       height: 6px; /* Chiều cao của thanh slider */
                       margin: 0px;
                       border-radius: 3px; /* Bo tròn các góc */
                       background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:%s #0B23FF, stop:%s #999999);
                   }
                   QSlider::handle:horizontal {
                       background: #FFFFFF; /* Màu của handle */
                       border: none;
                       width: 16px; /* Chiều rộng của handle */
                       height: 16px; /* Chiều cao của handle */
                       margin: -5px 0; /* Điều chỉnh vị trí handle */
                       border-radius: 8px; /* Bo tròn các góc */
                   }
               """
        self.setStyleSheetSlider()

        # Tạo nút chỉnh tốc độ video
        self.speedComboBox = QComboBox()
        self.speedComboBox.addItems(
            ['0.5x', '0.75x', '1.0x', '1.25x', '1.5x', '1.75x', '2.0x'])  # Tốc độ video có thể chọn

        # Tạo box chứa phần điều chỉnh âm lượng và tốc độ phát
        self.soundBox = QHBoxLayout()
        self.soundBox.setAlignment(Qt.AlignRight)
        # self.soundBox.addWidget(self.speedComboBox)
        self.soundBox.addWidget(self.speakerButton)
        self.soundBox.addWidget(self.volumeSlider)
        self.containButtonsBox.addLayout(self.soundBox)

        # Tạo thanh thời gian
        self.timeSlider = QSlider(Qt.Horizontal)
        self.timeSlider.setStyleSheet(stylesheet(self))
        self.timeSlider.setRange(0, 100)
        self.timeSlider.setValue(50)
        # self.positionSlider.sliderMoved.connect(self.setPosition)
        self.timeSlider.setSingleStep(2)
        self.timeSlider.setPageStep(20)
        self.timeSlider.setAttribute(Qt.WA_TranslucentBackground, True)

        self.containerBox.addWidget(self.timeSlider)
        self.containerBox.addLayout(self.containButtonsBox)

        self.addWidget(self.videoWidget, 0, 0)
        self.addWidget(self.frame, 0, 0, Qt.AlignBottom)

    def changeVolume(self, volume):
        print(volume)
        filepath = 'assets/mute.png'
        if volume > 60:
            filepath = "assets/speaker.png"
        elif volume > 0:
            filepath = "assets/low-speaker.png"
        self.speakerButton.setIcon(QIcon(filepath))
        self.volumeSlider.setValue(volume)
        self.setStyleSheetSlider()

    def setStyleSheetSlider(self):
        slider_value = self.volumeSlider.value() / 100
        self.volumeSlider.setStyleSheet(self.slider_style % (str(0), str(slider_value)))

    def frame_enter_event(self, event):
        # Hiển thị nút khi di chuyển chuột vào frame
        self.frame.show()

    def frame_leave_event(self, event):
        # Ẩn frame khi di chuyển chuột ra khỏi frame
        self.frame.hide()

    def play_pause_video(self, event = None):
        # Phát hoặc tạm dừng video
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.playButton.setIcon(QIcon("assets/play.png"))
        else:
            self.media_player.play()
            self.playButton.setIcon(QIcon("assets/pause.png"))

def stylesheet(self):
    return """
QSlider{
background-color: none;
}

QSlider::handle:horizontal {
background: transparent;
width: 16px;
height: 16px;
margin: -5px 0;
border-radius: 8px;
}

QSlider::groove:horizontal {
border: none;
height: 6px;
margin: 0px;
border-radius: 3px;
background: #9a9a9a
}

QSlider::sub-page:horizontal {
height: 6px;
border-radius: 3px;
margin: 0px 0;
background: #0007ff;
}

QSlider::handle:hover{
background: white;
width: 16px;
height: 16px;
margin: -5px 0;
border-radius: 8px;
}
    """
