from PyQt5.QtWidgets import QFrame

from ui.components.VideoContent import VideoContent


# This frame is use for containing content of screen, stay under of top menu bar
class MainFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
                background-color: #FFFFFF;
                border-radius: 40px 40px 0px 0px;
                box-shadow: 12px 12px 8px purple;
        """)
        self.setLayout(VideoContent())
