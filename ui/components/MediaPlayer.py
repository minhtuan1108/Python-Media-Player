from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class MyMediaPlayer(QMediaPlayer):
    def __init__(self, parent=None):
        super().__init__()

    def play_pause_video(self, parent):
        # Phát hoặc tạm dừng video
        if self.state() == QMediaPlayer.PlayingState:
            self.pause()
        else:
            self.play()

    def play_from_url(self, url):
        if url:
            self.setMedia(QMediaContent(QUrl.fromUserInput(url)))
            self.play()
