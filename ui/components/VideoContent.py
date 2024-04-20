from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider, QComboBox, QGridLayout, \
    QMessageBox, QWidget

from ui.components.MyMediaPlayer import MyMediaPlayer
from ui.components.InputUrlDialog import InputUrlDialog

import json


class VideoContent(QFrame):
    def __init__(self, parent = None):
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
        self.videoWidget.mouseDoubleClickEvent = self.parent.show_fullscreen

        self.media_player = MyMediaPlayer(self)
        self.media_player.stateChanged.connect(self.state_change)
        self.media_player.positionChanged.connect(self.position_change)
        self.media_player.durationChanged.connect(self.duration_change)
        self.media_player.error.connect(self.handleError)
        self.media_player.setVideoOutput(self.videoWidget)
        self.currentPosition = 0
        self.currentDuration = 0

        # Tạo frame chứa layout bao gồm các nút play và tua video
        self.centerFrame = QFrame()
        self.centerFrame.setStyleSheet("background-color: rgba(0, 0, 0, 0.05);")

        # Tạo layout để chứa các widget play và tua video
        self.centerHbox = QHBoxLayout()
        self.centerHbox.setAlignment(Qt.AlignCenter)
        self.centerFrame.setLayout(self.centerHbox)

        # Tạo button play cho center frame
        self.playButtonCenter = QPushButton()
        self.playButtonCenter.setIcon(QIcon("assets/play.png"))
        self.playButtonCenter.setIconSize(QSize(40, 40))
        self.playButtonCenter.setStyleSheet("background: none;")
        self.playButtonCenter.clicked.connect(self.play_pause_video)

        # Tạo button tua tới 10s cho center frame
        self.forward10Button = QPushButton()
        self.forward10Button.setIcon(QIcon("assets/forward10.png"))
        self.forward10Button.setIconSize(QSize(32, 32))
        self.forward10Button.setStyleSheet("background: none;")
        self.forward10Button.clicked.connect(self.play_forward_10)

        # Tạo button tua ngược 10s cho center fame
        self.replay10Button = QPushButton()
        self.replay10Button.setIcon(QIcon("assets/replay10.png"))
        self.replay10Button.setIconSize(QSize(32, 32))
        self.replay10Button.setStyleSheet("background: none;")
        self.replay10Button.clicked.connect(self.play_back_10)

        # Tao layout chua 3 nut treen
        self.centerButtonBox = QHBoxLayout()
        self.centerButtonBox.setAlignment(Qt.AlignCenter)
        self.centerButtonBox.addWidget(self.replay10Button)
        self.centerButtonBox.addWidget(self.playButtonCenter)
        self.centerButtonBox.addWidget(self.forward10Button)
        self.centerHbox.addLayout(self.centerButtonBox)

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
        self.playButton.setIcon(QIcon("assets/play.png"))
        self.playButton.setIconSize(QSize(32, 32))
        self.playButton.clicked.connect(self.play_pause_video)

        # Tao label dem thoi gian
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setStyleSheet("background-color: none;color: white;")

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

        # Tao frame fix voi noi dung de xu ly su kien
        self.soundFixedFrame = QFrame()
        self.soundFixedFrame.setMinimumWidth(36)
        self.soundFixedFrame.setMaximumWidth(150)
        self.soundFixedFrame.enterEvent = self.speaker_enter_event
        self.soundFixedFrame.leaveEvent = self.speaker_leave_event
        self.soundFixedFrame.setStyleSheet("background-color: none;")

        # Tao layout fix de chua
        self.soundFixedBox = QHBoxLayout()
        self.soundFixedBox.setAlignment(Qt.AlignLeft)
        self.soundFixedBox.addWidget(self.speakerButton)
        self.soundFixedBox.addWidget(self.volumeSlider)
        self.soundFixedFrame.setLayout(self.soundFixedBox)

        # Tạo layout chưa cac nút bên trên
        self.playVideoBox = QHBoxLayout()
        self.playVideoBox.setAlignment(Qt.AlignLeft)
        self.playVideoBox.addWidget(self.replay10Button, 0, Qt.AlignLeft)
        self.playVideoBox.addWidget(self.playButton, 0, Qt.AlignLeft)
        self.playVideoBox.addWidget(self.forward10Button, 0, Qt.AlignLeft)
        self.playVideoBox.addWidget(self.soundFixedFrame, 0, Qt.AlignLeft)
        self.playVideoBox.addWidget(self.time_label, 0, Qt.AlignLeft)
        self.containButtonsBox.addLayout(self.playVideoBox)

        # Tạo box chứa phần điều chỉnh ben phai
        self.rightBox = QHBoxLayout()
        self.rightBox.setAlignment(Qt.AlignRight)

        self.miniVideoButton = QPushButton()
        self.miniVideoButton.setIcon(QIcon("assets/minivideo.png"))
        self.miniVideoButton.setIconSize(QSize(28,28))
        # self.miniVideoButton.clicked.connect(self.minisizing_video)

        self.fullscreenButton = QPushButton()
        self.fullscreenButton.setIcon(QIcon("assets/expand.png"))
        self.fullscreenButton.setIconSize(QSize(28,28))
        self.fullscreenButton.clicked.connect(self.parent.fullscreen)

        self.rightBox.addWidget(self.miniVideoButton, 0, Qt.AlignRight)
        self.rightBox.addSpacing(15)
        self.rightBox.addWidget(self.fullscreenButton, 0, Qt.AlignRight)
        self.rightBox.addSpacing(40)

        self.containButtonsBox.addLayout(self.rightBox)

        # tạo widget video cho mini video
        self.miniVideoWidget = QVideoWidget()
        self.miniVideoWidget.setStyleSheet("border-radius: 20px;")
        # self.miniVideoWidget.mousePressEvent = self.play_pause_video
        # self.miniVideoWidget.mouseDoubleClickEvent = self.parent.showFullScreen
        
        self.miniVideoLayout = QHBoxLayout()
        self.miniVideoLayout.addWidget(self.miniVideoWidget)

        self.miniVideoFrame = QFrame()
        self.miniVideoFrame.setLayout(self.miniVideoLayout)


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

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.videoWidget, 0, 0)
        # self.grid_layout.addWidget(self.centerFrame, 0, 0, Qt.AlignCenter)
        self.grid_layout.addWidget(self.frame, 0, 0, Qt.AlignBottom)

        self.setLayout(self.grid_layout)

    def add_item_context_menu(self):
        actionFile = self.parent.menu.addAction(QIcon("assets/folder.png"), "open File (Ctrl + O)")
        actionclipboard = self.parent.menu.addSeparator()
        actionURL = self.parent.menu.addAction(QIcon.fromTheme("browser"), "URL from Internet (Ctrl + W)")
        actionclipboard = self.parent.menu.addSeparator()
        actionYTurl = self.parent.menu.addAction(QIcon("assets/youtube.png"), "URL from YouTube (Ctrl + Y)")
        actionOpenInputDialog = self.parent.menu.addAction("Open input dialog (Ctrl + N)")

        actionFile.triggered.connect(self.parent.open_file)
        actionURL.triggered.connect(lambda: self.media_player.get_url_from_clip('http'))
        actionYTurl.triggered.connect(lambda: self.media_player.get_url_from_clip('youtube'))
        actionOpenInputDialog.triggered.connect(self.open_input_dialog)

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
        print("In enter event")
        self.frame.show()
        # self.centerFrame.show()

    def frame_leave_event(self, event):
        # Ẩn frame khi di chuyển chuột ra khỏi frame
        self.frame.hide()
        # self.centerFrame.hide()

    def handle_mouse_in_frame(self, event):
        pass

    def load_film(self, file):
        self.media_player.load_film(file)

    def speaker_enter_event(self, event):
        self.volumeSlider.show()

    def speaker_leave_event(self, event):
        # print(event)
        self.volumeSlider.hide()

    def speaker_onclick(self):
        # Tắt hoặc bật âm thanh video
        # print(self.volumeSlider.value())
        if self.volumeSlider.value() > 0:
            self.speakerButton.setIcon(QIcon("assets/mute.png"))
            self.volumeSlider.setValue(0)
            self.media_player.setVolume(0)
        else:
            if self.currentVolume > 60:
                self.speakerButton.setIcon(QIcon("assets/speaker.png"))
            else:
                self.speakerButton.setIcon(QIcon("assets/low-speaker.png"))
            self.volumeSlider.setValue(self.currentVolume)
            self.media_player.setVolume(self.currentVolume)

    def stop_media_player(self):
        self.media_player.stop()

    def state_change(self, event):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(QIcon("assets/pause.png"))
        elif self.media_player.state() == QMediaPlayer.PausedState:
            self.playButton.setIcon(QIcon("assets/play.png"))
        elif self.media_player.state() == QMediaPlayer.StoppedState:
            # print("Video da bi huy: ", self.media_player.media().canonicalUrl().url())
            # print("Huy o giay thu: ", self.currentPosition)
            # print("Duration hien tai: ", self.currentDuration)
            # Store last position video
            url = self.media_player.youtubeUrl if self.media_player.fileDataName == "youtube" else self.media_player.myurl
            # print("Url: ", url)
            self.update_url(self.media_player.fileDataName, url, self.currentPosition, self.currentDuration)
            self.playButton.setIcon(QIcon("assets/replay.png"))

    def play_pause_video(self, event):
        print("# Phát hoặc tạm dừng video")
        if self.media_player.state() == QMediaPlayer.PlayingState:
            print("Pause video")
            self.media_player.pause()
            # self.pip_media_player.pause()
        else:
            if self.media_player.state() == QMediaPlayer.StoppedState: 
                self.set_position(0)
            print("Play video")
            self.media_player.play()
            # self.pip_media_player.play()

        
    def play_forward_10(self):
        # duration = self.media_player.duration()
        # print("Duration in forward: ", duration)
        self.set_position(self.media_player.position() + 10000)

    def play_back_10(self):
        self.media_player.setPosition(self.media_player.position() - 10000)
        if self.media_player.state() == QMediaPlayer.StoppedState:
            self.media_player.play()

    def set_position(self, time):
        duration = self.media_player.duration()
        # print("Time:", time)
        # print("Duration", duration)
        if time >= duration and duration > 0:
            self.media_player.stop()
            self.media_player.setPosition(duration)
            self.currentPosition = self.media_player.position()
        else:
            self.media_player.setPosition(time)
        self.update_time_label()

    def position_change(self, position):
        # print("In position change")
        # if position == self.media_player.duration():
        #     self.media_player.pause()
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

    def open_input_dialog(self):
        self.inputDialog.show()

    def update_time_label(self):
        # Cập nhật label với thời gian hiện tại và thời lượng toàn bộ của video
        current_time = int(self.media_player.position() / 1000) # Đổi từ milliseconds thành giây
        total_time = int(self.media_player.duration() / 1000) # Đổi từ milliseconds thành giây        
        # print(current_time)
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

    # def minisizing_video(self):
    #     w = 200
    #     h = 80
    #     parentPos = self.parent.pos()
    #     parentSize = self.parent.size()
    #     posX = parentPos.x() + (parentSize.width() - w)/2
    #     posY = parentPos.y() + (parentSize.height() - h)/2
    #     print("Vi tri X cua mini video", posX)
    #     print("Vi tri Y cua mini video", posY)
    #     self.miniVideoFrame.setGeometry(posX, posY, w, h)
    #     self.pip_media_player.setMedia(self.media_player.media())
    #     self.media_player.setVideoOutput(None)
    #     self.pip_media_player.play()
    #     self.miniVideoFrame.show()
    #     # self.miniVideoFrame.update()


    def store_url(self, dictData, filename):
        print("store url function")
        listData = []
        conflict = False
        lastId = 0

        try:
            with open("data/" + filename + "_data.json", "r") as file:
                try:
                    listData = json.load(file)
                    # print(listData)
                    for data in listData:
                        # print(data["id"])
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
        print("Update url")
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