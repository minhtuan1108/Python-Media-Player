from PyQt5.QtWidgets import QFrame, QGraphicsDropShadowEffect

from ui.components.VideoContent import VideoContent


# This frame is use for containing content of screen, stay under of top menu bar
class MainFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
                background-color: #FFFFFF;
                border-radius: 10px;
        """)
        self.setLayout(VideoContent(self).layout())
