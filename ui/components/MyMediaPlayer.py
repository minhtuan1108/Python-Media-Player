from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QMessageBox
from pytube import YouTube

from datetime import datetime


class MyMediaPlayer(QMediaPlayer):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.clip = QApplication.clipboard()
        # self.process = QProcess(self)
        # self.process.readyRead.connect(self.data_ready)
        # self.process.finished.connect(self.play_from_url)
        self.isError = False
        self.fileDataName = ""
        self.localFile = ""
        self.youtubeUrl = ""
        self.myurl = ""
        self.title = ""

    def get_url_from_clip(self, fromSource):
        self.parent.currentPosition = self.position()
        self.parent.currentDuration = self.duration()
        self.stop()
        self.myurl = self.clip.text()
        print(self.myurl)
        if self.clip.mimeData().hasText() and "youtube.com" in self.myurl or "http" in self.myurl:
            if fromSource == 'youtube':
                print("Play from youtube")
                self.get_youtube_url()
            elif fromSource == 'http':
                print("Play from url")
                self.play_from_url()
        else:
            # Hien Dialog cho nguoi dung nhap url
            print("Hello world")
            self.parent.inputDialog.show()

    def play_from_url(self, isYTUrl = False):
        # self.pause()
        
        print("File data name: ", self.fileDataName)
        try:
            self.setMedia(QMediaContent(QUrl(self.myurl)))
            self.play()
            print(self.state() != QMediaPlayer.StoppedState)
            if self.state() != QMediaPlayer.StoppedState:
                print("# Nếu có thể phát thì set lại play button")
                self.parent.playButton.setEnabled(True)
                self.parent.downloadButton.setEnabled(True)
                data = {
                    "id": None,
                    "url": self.youtubeUrl if isYTUrl else self.myurl,
                    "title": self.title,
                    "duration": self.duration(),
                    "position": 0,
                    "saved_at": self.get_current_time_string(),
                    "last_saw": self.get_current_time_string(),
                }

                # reset title attribute
                self.title = ""
            
                if isYTUrl:
                    self.parent.store_url(data, "youtube")
                    print("File data name: youtube")
                    self.fileDataName = "youtube"
                else:
                    self.parent.store_url(data, "http")
                    self.fileDataName = "http"
                    print("File data name: http")
        except Exception as e:
            QMessageBox.critical(self.parent.parent, 'Error', "Can't load file ! Try again!")
            print(e)
        print(self.myurl)

    def get_youtube_url(self):
        try:
            self.youtubeUrl = self.myurl
            yt = YouTube(self.myurl)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            self.title = yt.title
            self.myurl = stream.url
            self.play_from_url(True)
        except:
            QMessageBox.critical(self.parent.parent, 'Error', "Can't load youtube file ! Try again!")
            

    def load_film(self, file):
        self.parent.currentPosition = self.position()
        self.parent.currentDuration = self.duration()
        self.stop()
        self.setMedia(QMediaContent(QUrl.fromLocalFile(file)))
        self.parent.playButton.setEnabled(True)
        self.play()
        if self.state() != QMediaPlayer.StoppedState:
            self.parent.playButton.setEnabled(True)
            self.parent.downloadButton.setEnable(True)
            self.myurl = file
            data = {
                    "id": None,
                    "url": file,
                    "title": self.title,
                    "duration": self.duration(),
                    "position": 0,
                    "saved_at": self.get_current_time_string(),
                    "last_saw": self.get_current_time_string(),
                }
            self.parent.store_url(data, "local_file")
            self.fileDataName = "local_file"
        # self.reset_variable()

    def reset_variable(self):
        self.isError = False
        self.fileDataName = ""
        self.localFile = ""
        self.youtubeUrl = ""
        self.myurl = ""
        self.title = ""

    def get_current_time_string(self):
        current_time = datetime.now()

        # Chuyển đổi thành chuỗi theo định dạng "dd/mm/yyyy HH:mm"
        formatted_time = current_time.strftime("%d/%m/%Y %H:%M")
        return formatted_time