from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel, QSlider, QToolButton, QComboBox, \
    QFrame, QGraphicsEffect, QGraphicsOpacityEffect, QGraphicsDropShadowEffect, QGridLayout

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
        self.media_player = MyMediaPlayer(self)

        self.media_player.setVideoOutput(self.videoWidget)
        self.media_player.play_from_url("https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8")
        # Tạo frame để điều chỉnh layout
        self.frame = QFrame()
        self.frame.hide()
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFixedHeight(80)
        self.frame.setStyleSheet("""
                        QFrame{
                            background-color: rgba(0, 0, 0, 0.15);
                        }

                        QToolButton{
                            background-color: none;
                        }
                """)

        # Tạo effect object
        # self.effect = QGraphicsDropShadowEffect()
        # self.effect.setBlurRadius(15)
        # self.effect.setOffset(0, -10)
        # self.frame.setGraphicsEffect(self.effect)

        # Tạo khung chứa thanh thời gian của video và các nút chức năng
        self.containerBox = QVBoxLayout()
        self.frame.setLayout(self.containerBox)

        # Tạo khung chứa các chức năng của video
        self.containButtonsBox = QHBoxLayout()
        self.containerBox.addLayout(self.containButtonsBox)

        # Tạo button play
        self.playButton = QToolButton()
        self.playButton.setIcon(QIcon("assets/play.png"))
        self.playButton.setIconSize(QSize(32, 32))

        # Tạo button tua tới 10s
        self.forward10Button = QToolButton()
        self.forward10Button.setIcon(QIcon("assets/forward10.png"))

        # Tạo button tua ngược 10s
        self.replay10Button = QToolButton()
        self.replay10Button.setIcon(QIcon("assets/replay10.png"))

        # Tạo Label loa
        self.speakerButton = QToolButton()
        self.speakerButton.setIcon(QIcon("assets/speaker.png"))
        self.speakerButton.setIconSize(QSize(32, 32))

        # Tạo thanh âm lượng
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setFixedWidth(100)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setValue(50)  # Default volume
        self.volumeSlider.valueChanged.connect(self.changeVolume)
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
        self.speedComboBox.addItems(['0.5x', '0.75x', '1.0x', '1.25x', '1.5x', '1.75x', '2.0x'])  # Tốc độ video có thể chọn

        # Thêm các button vào layout
        self.containButtonsBox.addWidget(self.replay10Button)
        self.containButtonsBox.addWidget(self.playButton)
        self.containButtonsBox.addWidget(self.forward10Button)
        self.containButtonsBox.addWidget(self.speakerButton)
        self.containButtonsBox.addWidget(self.volumeSlider)

        self.addWidget(self.videoWidget, 0, 0)
        self.addWidget(self.frame, 0, 0, Qt.AlignBottom)

    def changeVolume(self, volume):
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