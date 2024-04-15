from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *

from ui.components.MediaPlayer import MyMediaPlayer
from ui.components.InputUrlDialog import InputUrlDialog

import json


class VideoContent(QGridLayout):
    def __init__(self, parent: QFrame):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.parent = parent
        self.inputDialog = InputUrlDialog(self)
        # Thiết lập sự kiện chuột
        parent.setMouseTracking(True)
        parent.enterEvent = self.frame_enter_event
        parent.leaveEvent = self.frame_leave_event
        parent.mouseReleaseEvent = self.handle_mouse_in_frame

        # Tạo khung chứa video
        self.videoWidget = QVideoWidget()
        self.videoWidget.setStyleSheet("border-radius: 20px;")
        self.videoWidget.mousePressEvent = self.play_pause_video
        self.videoWidget.mouseDoubleClickEvent = self.parent.showFullScreen
        self.media_player = MyMediaPlayer(self)
        self.media_player.setVideoOutput(self.videoWidget)
        self.media_player.stateChanged.connect(self.state_change)
        self.media_player.positionChanged.connect(self.position_change)
        self.media_player.durationChanged.connect(self.duration_change)
        self.media_player.error.connect(self.handleError)
        self.currentPosition = 0
        self.currentDuration = 0

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
        self.forward10Button.clicked.connect(self.play_forward_10)

        # Tạo button tua ngược 10s
        self.replay10Button = QPushButton()
        self.replay10Button.setIcon(QIcon("assets/replay10.png"))
        self.replay10Button.clicked.connect(self.play_back_10)

        # Tao label dem thoi gian
        self.time_label = QLabel()
        self.time_label.setStyleSheet("background-color: none;")

        # Tạo layout chưa cac nút bên trên
        self.playVideoBox = QHBoxLayout()
        self.playVideoBox.setAlignment(Qt.AlignLeft)
        self.playVideoBox.addWidget(self.replay10Button)
        self.playVideoBox.addWidget(self.playButton)
        self.playVideoBox.addWidget(self.forward10Button)
        self.playVideoBox.addWidget(self.time_label)
        self.containButtonsBox.addLayout(self.playVideoBox)

        # Tạo Label loa
        self.speakerButton = QPushButton()
        self.speakerButton.setIcon(QIcon("assets/speaker.png"))
        self.speakerButton.setFixedWidth(32)
        self.speakerButton.setIconSize(QSize(32, 32))
        self.speakerButton.clicked.connect(self.speaker_onclick)

        # Tạo thanh âm lượng
        self.currentVolume = 100
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.hide()
        self.volumeSlider.setFixedWidth(100)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setValue(self.currentVolume)  # Default volume
        self.volumeSlider.sliderMoved.connect(self.changeVolume)  
        self.volumeSlider.setStyleSheet(stylesheet(self))

        # Tạo nút chỉnh tốc độ video
        self.speedComboBox = QComboBox()
        self.speedComboBox.addItems(
            ['0.5x', '0.75x', '1.0x', '1.25x', '1.5x', '1.75x', '2.0x'])  # Tốc độ video có thể chọn

        # Tạo box chứa phần điều chỉnh âm lượng và tốc độ phát
        self.soundBox = QHBoxLayout()
        self.soundBox.setAlignment(Qt.AlignRight)

        # Tao frame fix voi noi dung de xu ly su kien
        self.soundFixedFrame = QFrame()
        self.soundFixedFrame.setMinimumWidth(36)
        self.soundFixedFrame.setMaximumWidth(150)
        self.soundFixedFrame.enterEvent = self.speaker_enter_event
        self.soundFixedFrame.leaveEvent = self.speaker_leave_event
        self.soundFixedFrame.setStyleSheet("background-color: none;")

        # Tao layout fix de chua
        self.soundFixedBox = QHBoxLayout()
        self.soundFixedBox.setAlignment(Qt.AlignRight)
        self.soundFixedBox.addWidget(self.speakerButton)
        self.soundFixedBox.addWidget(self.volumeSlider)
        self.soundFixedFrame.setLayout(self.soundFixedBox)
        self.soundBox.addWidget(self.soundFixedFrame)
        self.containButtonsBox.addLayout(self.soundBox)

        # Tạo thanh thời gian
        self.timeSlider = QSlider(Qt.Horizontal)
        self.timeSlider.setStyleSheet(stylesheet(self))
        self.timeSlider.setRange(0, 100)
        self.timeSlider.setValue(100)
        self.timeSlider.sliderMoved.connect(self.set_position)
        self.timeSlider.setSingleStep(2)
        self.timeSlider.setPageStep(20)
        self.timeSlider.setAttribute(Qt.WA_TranslucentBackground, True)

        self.containerBox.addWidget(self.timeSlider)
        self.containerBox.addLayout(self.containButtonsBox)

        self.addWidget(self.videoWidget, 0, 0)
        self.addWidget(self.frame, 0, 0, Qt.AlignBottom)

    def add_item_context_menu(self):
        actionFile = self.parent.menu.addAction(QIcon.fromTheme("video-x-generic"), "open File (o)")
        actionclipboard = self.parent.menu.addSeparator()
        actionURL = self.parent.menu.addAction(QIcon.fromTheme("browser"), "URL from Internet (u)")
        actionclipboard = self.parent.menu.addSeparator()
        actionYTurl = self.parent.menu.addAction(QIcon.fromTheme("youtube"), "URL from YouTube (y)")

        actionFile.triggered.connect(self.parent.open_file)
        actionURL.triggered.connect(lambda: self.media_player.get_url_from_clip('http'))
        actionYTurl.triggered.connect(lambda: self.media_player.get_url_from_clip('youtube'))

    def changeVolume(self, volume):
        print(volume)
        filepath = 'assets/mute.png'
        if volume > 60:
            filepath = "assets/speaker.png"
        elif volume > 0:
            filepath = "assets/low-speaker.png"
        self.speakerButton.setIcon(QIcon(filepath))
        self.volumeSlider.setValue(volume)
        self.media_player.setVolume(volume)
        self.currentVolume = volume

    def frame_enter_event(self, event):
        # Hiển thị nút khi di chuyển chuột vào frame
        self.frame.show()

    def frame_leave_event(self, event):
        # Ẩn frame khi di chuyển chuột ra khỏi frame
        self.frame.hide()

    def handle_mouse_in_frame(self, event):
        pass

    def load_film(self, file):
        self.media_player.load_film(file)

    def stop_media_player(self):
        self.media_player.stop()

    def state_change(self, event):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(QIcon("assets/pause.png"))
        elif self.media_player.state() == QMediaPlayer.PausedState:
            self.playButton.setIcon(QIcon("assets/play.png"))
        elif self.media_player.state() == QMediaPlayer.StoppedState:
            # print("Video da bi huy: ", self.media_player.myurl)
            print("Huy o giay thu: ", self.currentPosition)
            print("Duration hien tai: ", self.currentDuration)
            # Store last position video
            url = self.media_player.youtubeUrl if self.media_player.fileDataName == "youtube" else self.media_player.myurl
            self.update_url(self.media_player.fileDataName, url, self.currentPosition, self.currentDuration)
            self.playButton.setIcon(QIcon("assets/replay.png"))

    def play_pause_video(self, event):
        # Phát hoặc tạm dừng video
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def speaker_enter_event(self, event):
        self.volumeSlider.show()

    def speaker_leave_event(self, event):
        # print(event)
        self.volumeSlider.hide()

    def speaker_onclick(self):
        # Tắt hoặc bật âm thanh video
        if self.volumeSlider.value() > 0:
            self.speakerButton.setIcon(QIcon("assets/mute.png"))
            self.volumeSlider.setValue(0)
            self.media_player.setVolume(0)
        else:
            if self.currentVolume > 60:
                self.speakerButton.setIcon(QIcon("assets/mute.png"))
            else:
                self.speakerButton.setIcon(QIcon("assets/low-speaker.png"))
            self.volumeSlider.setValue(self.currentVolume)
            self.media_player.setVolume(self.currentVolume)
        
    def play_forward_10(self):
        duration = self.media_player.duration()
        if self.media_player.position() + 10000 > duration:
            self.media_player.setPosition(duration - 1)
        else:
            self.media_player.setPosition(self.media_player.position() + 10000)

    def play_back_10(self):
        self.media_player.setPosition(self.media_player.position() - 10000)

    def set_position(self, time):
        self.media_player.setPosition(time)
        self.update_time_label()

    def position_change(self, position):
        # print("In position change")
        self.timeSlider.setValue(position)
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(self.media_player.position())
        self.update_time_label()
    
    def duration_change(self, duration):
        # print("In duration change")
        self.timeSlider.setRange(0, duration)
        self.currentDuration = duration
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(self.media_player.duration())
        self.update_time_label()

    def handleError(self):
        # self.playButton.setEnabled(False)
        errorString = self.media_player.errorString()
        if "Cannot play stream of type:" in errorString:
            QMessageBox.critical(self.parent.parent, 'Error', errorString)
            self.media_player.setMedia(QMediaContent())
        print("Error: ", errorString)

    def update_time_label(self):
        # Cập nhật label với thời gian hiện tại và thời lượng toàn bộ của video
        current_time = int(self.media_player.position() / 1000) # Đổi từ milliseconds thành giây
        total_time = int(self.media_player.duration() / 1000) # Đổi từ milliseconds thành giây        
        print(current_time)
        current_qtime = QTime(0, 0).addSecs(current_time)
        total_qtime = QTime(0, 0).addSecs(total_time)
        if current_time >= 60*60:
            current_time_string = current_qtime.toString("hh:mm:ss")
        else:
            current_time_string = current_qtime.toString("mm:ss")
        if total_time >= 60*60:
            total_time_string = total_qtime.toString("hh:mm:ss")
        else:
            total_time_string = total_qtime.toString("mm:ss")
        self.time_label.setText(f"{current_time_string} / {total_time_string}")        

    def store_url(self, dictData, filename):
        print("store url function")
        listData = []
        conflict = False
        lastId = 0

        try:
            with open("data/" + filename + "_data.json", "r") as file:
                try:
                    listData = json.load(file)
                    print(listData)
                    for data in listData:
                        print(data["id"])
                        if(data["url"] == dictData["url"]):
                            data["last_saw"] = self.media_player.get_current_time_string()
                            conflict = True
                            break
                        lastId = data["id"]

                    if not conflict:
                        dictData["id"] = lastId + 1
                        listData.append(dictData)
                except json.decoder.JSONDecodeError as e:
                    dictData["id"] = lastId + 1
                    listData.append(dictData)
                    print("Json decode error: ", e)
        except FileNotFoundError:
            dictData["id"] = lastId + 1
            listData.append(dictData)
            print("Find not found")
    
        try:
            with open("data/" + filename + "_data.json", "w") as file:
                json.dump(listData, file)
        except:
            QMessageBox.warning(self.parent, "Warning", "Can't store your url to data")

    def update_url(self, filename, url, position, duration):
        listData = []
        try:
            with open("data/" + filename + "_data.json", "r") as file:
                listData = json.load(file)
                for data in listData:
                    if data["url"] == url:
                        print("Hello")
                        data["position"] = position
                        data["duration"] = duration
                        break
        except Exception as e:
            print("Store last video position error: ", e)

        try:
            with open("data/" + filename + "_data.json", "w") as file:
                json.dump(listData, file)
        except:
            print("Can't update position time")





def stylesheet(self):
    return """
QSlider{
background-color: none;
padding: 0px;
}

QSlider::handle:horizontal {
background: none;
width: 6px;
height: 6px;
margin: 0px 0;
padding: 0px;
border-radius: 3px;
}

QSlider::groove:horizontal {
border: none;
height: 6px;
margin: 0px;
padding: 0px;
border-radius: 3px;
background: #9a9a9a
}

QSlider::sub-page:horizontal {
height: 6px;
border-radius: 3px;
margin: 0px 0;
padding: 0px;
background: #0007ff;
}

QSlider::handle:hover{
background: white;
width: 16px;
height: 16px;
margin: -5px 0px;
padding: 0px;
border-radius: 8px;
}

QLabel
{
background: black;
color: #585858;
border: 0px solid #076100;
font-size: 8pt;
font-weight: bold;
}
    """