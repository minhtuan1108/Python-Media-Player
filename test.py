import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")
        self.media_player = QMediaPlayer(self)
        self.video_widget = QVideoWidget()
        self.pip_video_widget = QVideoWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        self.setLayout(layout)

        # Load video
        video_url = "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8"  # Example YouTube video
        media_content = QMediaContent(QUrl(video_url))
        self.media_player.setMedia(media_content)
        self.media_player.setVideoOutput(self.video_widget)

        # Play button
        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play)
        layout.addWidget(self.play_button)

        # Picture-in-picture button
        self.pip_button = QPushButton("Picture-in-Picture", self)
        self.pip_button.clicked.connect(self.show_pip)
        layout.addWidget(self.pip_button)

    def play(self):
        self.media_player.play()

    def show_pip(self):
        if not self.pip_video_widget.parent():
            self.create_pip_widget()
        elif self.pip_video_widget.parentWidget().isVisible():
            self.pip_video_widget.parentWidget().hide()
        else:
            self.pip_video_widget.parentWidget().show()

    def create_pip_widget(self):
        self.pip_video_widget.setParent(self)
        self.pip_video_widget.setGeometry(10, 10, 320, 240)

        self.media_player.setVideoOutput(self.pip_video_widget)
        self.media_player.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
