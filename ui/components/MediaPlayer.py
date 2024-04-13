from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication


class MyMediaPlayer(QMediaPlayer):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.clip = QApplication.clipboard()
        self.process = QProcess(self)
        self.process.readyRead.connect(self.data_ready)
        self.process.finished.connect(self.play_from_url)

        self.myurl = ""

    def get_url_from_clip(self, fromSource):
        self.myurl = self.clip.text()
        if self.myurl != '':
            if fromSource == 'http':
                self.play_from_url()
            elif fromSource == 'youtube':
                self.get_youtube_url()
        else:
            # Hien Dialog cho nguoi dung nhap url
            pass


    def data_ready(self):
        self.myurl = str(self.process.readAll(), encoding='utf8').rstrip()  ###
        self.myurl = self.myurl.partition("\n")[0]
        print(self.myurl)
        self.clip.setText(self.myurl)
        self.play_from_url(self.myurl)

    def play_from_url(self):
        self.pause()
        self.setMedia(QMediaContent(QUrl(self.myurl)))
        self.parent.playButton.setEnabled(True)
        self.play()
        print(self.myurl)

    def get_youtube_url(self, url):
        cmd = "youtube-dl -g -f best " + self.myurl
        print("grabbing YouTube URL")
        self.process.start(cmd)

    
