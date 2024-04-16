from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
# from ui.components.VideoContent import VideoContent
# from ui.components.VideoHaveSeen import VideoHaveSeen
from ui.screens.MainFrame import MainFrame


class Nav_Bar(QHBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.hbox_layout = QHBoxLayout()  # hbox lớn được bọc bởi frame
        self.hbox_layouts = QHBoxLayout()  # hbox nhỏ được bọc bởi frame_layout
        self.hbox_layout.setAlignment(Qt.AlignCenter)
        self.frame = QFrame()  # frame lớn bọc hbox_layout
        self.frame_layout = QFrame()  # frame_layout nhỏ bọc hbox_layouts

        self.frame_layout.setStyleSheet("""
                                    background-color: #969696;
                                    text-align: center;
                                    font-size: 16px;
                                    font-weight: bold;
                                    border-radius: 30px;
                                    
                                        """)
        self.frame_layout.setFixedSize(500, 60)

        self.frame_layout.setLayout(self.hbox_layouts)  # set hbox_layouts vào frame_layout

        self.hbox_layout.addWidget(self.frame_layout)  # set frame_layout vào hbox_layout

        self.frame.setLayout(self.hbox_layout)  # set frame_layout vào frame

        self.frame.setFixedHeight(100)

        self.addWidget(self.frame)  # add frame vào layout

        self.frame.setStyleSheet("""
                                    background-color: transparent;
                                    text-align: center;
                                    font-size: 16px;
                                    font-weight: bold;
                                """)

        # Create and style buttons
        self.button1 = QPushButton("Library")
        self.button1.setIcon(QIcon('./assets/library.png'))
        self.button1.setFixedSize(145, 40)
        self.button1.clicked.connect(lambda: parent.mainFrame.on_click_btn("Library"))

        self.button2 = QPushButton("Now Playing")
        self.button2.setIcon(QIcon('./assets/nowplaying.png'))
        self.button2.clicked.connect(lambda: parent.mainFrame.on_click_btn("Now Playing"))
        self.button2.setFixedSize(145, 40)

        self.button3 = QPushButton("Playlist")
        self.button3.setIcon(QIcon('./assets/playlist.png'))
        # self.button3.clicked.connect(self.on_click_btn)
        self.button3.setFixedSize(145, 40)

        # set style for button
        self.active_button_style = "background-color: white; color: black; border-radius: 20px; font-size: 16px;"
        self.default_style = "background-color: #969696; color: black; border-radius: 20px; font-size: 16px;"
        self.button1.setStyleSheet(self.default_style)
        self.button2.setStyleSheet(self.active_button_style)
        self.button3.setStyleSheet(self.default_style)

        # Connect button clicks to transitions
        self.button1.clicked.connect(self.on_button_clicked)
        self.button2.clicked.connect(self.on_button_clicked)
        self.button3.clicked.connect(self.on_button_clicked)
        
        
        # Add buttons to the horizontal layout
        self.hbox_layouts.addWidget(self.button1)
        self.hbox_layouts.addWidget(self.button2)
        self.hbox_layouts.addWidget(self.button3)

    def on_button_clicked(self):
        sender = self.sender()
        text = sender.text()
        if text == "Library":
            self.button1.setStyleSheet(self.active_button_style)
            self.button2.setStyleSheet(self.default_style)
            self.button3.setStyleSheet(self.default_style)
        elif text == "Now Playing":
            self.button1.setStyleSheet(self.default_style)
            self.button2.setStyleSheet(self.active_button_style)
            self.button3.setStyleSheet(self.default_style)
        elif text == "Playlist":
            self.button1.setStyleSheet(self.default_style)
            self.button2.setStyleSheet(self.default_style)
            self.button3.setStyleSheet(self.active_button_style)
