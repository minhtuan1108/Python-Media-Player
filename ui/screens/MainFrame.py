from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui.components.VideoContent import VideoContent
from ui.components.VideoHaveSeen import VideoHaveSeen


# This frame is use for containing content of screen, stay under of top menu bar
class MainFrame(QFrame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        # self.parent.navBar.on_button_clicked(self)
        self.setStyleSheet("background-color: #FFFFFF; border-radius: 10px;")

        # Khởi tạo các thành phần của MainFrame
        self.videoContent = VideoContent(self)
        self.videoHaveSeen = VideoHaveSeen(self)

        # Thêm VideoHaveSeen vào layout của MainFrame và ẩn nó ban đầu
        self.layout = QGridLayout()
        self.layout.addWidget(self.videoContent, 0, 0)
        self.layout.addWidget(self.videoHaveSeen, 0, 0)
        # self.videoHaveSeen.setVisible(False)
        self.setLayout(self.layout)
        self.videoContent.inputDialog.move(self.frameGeometry().center())
        self.menu = QMenu()
        self.menu.setStyleSheet(self.styleSheet())
        self.myinfo = "©2016\nAxel Schneider\n\nMouse Wheel = Zoom\nUP = Volume Up\nDOWN = Volume Down\n" + \
                      "LEFT = < 1 Minute\nRIGHT = > 1 Minute\n" + \
                      "SHIFT+LEFT = < 10 Minutes\nSHIFT+RIGHT = > 10 Minutes"
        self.create_shortcut()

    def create_shortcut(self):
        self.shortcutOpenLocal = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_O), self)
        self.shortcutOpenLocal.activated.connect(self.open_file)
        self.shortcutPlayUrl = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_W), self)
        self.shortcutPlayUrl.activated.connect(lambda: self.videoContent.media_player.get_url_from_clip("http"))
        self.shortcutPlayYT = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Y), self)
        self.shortcutPlayYT.activated.connect(lambda: self.videoContent.media_player.get_url_from_clip("youtube"))
        self.openInputDialog = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_N), self)
        self.openInputDialog.activated.connect(self.videoContent.open_input_dialog)
        self.shortcutFullscreen = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_F), self)
        self.shortcutFullscreen.activated.connect(self.fullscreen)
        self.shortcutHistory = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_F), self)
        self.shortcutHistory.activated.connect(self.view_history)
        # self.shortcutInfo = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_I), self)
        # self.shortcutInfo.activated.connect(self.fullscreen)
        self.shortcutQuit = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q), self)
        self.shortcutQuit.activated.connect(self.quit)
        self.increaseVolumn = QShortcut(QKeySequence(Qt.Key_Up), self.videoContent)
        self.increaseVolumn.activated.connect(lambda: self.videoContent.media_player.setVolume(self.videoContent.media_player.volume() + 1))
        self.descreaseVolumn = QShortcut(QKeySequence(Qt.Key_Down), self.videoContent)
        self.descreaseVolumn.activated.connect(lambda: self.videoContent.media_player.setVolume(self.videoContent.media_player.volume() - 1))
        self.forward10s = QShortcut(QKeySequence(Qt.Key_Right), self.videoContent)
        self.forward10s.activated.connect(self.videoContent.play_forward_10)
        self.playback10s = QShortcut(QKeySequence(Qt.Key_Left), self.videoContent)
        self.playback10s.activated.connect(self.videoContent.play_back_10)
        self.playPauseVideo = QShortcut(QKeySequence(Qt.Key_Space), self.videoContent)
        self.playPauseVideo.activated.connect(self.videoContent.play_pause_video)

    def context_menu_requested(self, point):
        self.menu.clear()
        # goi ham de add cac chuc nang cua xem video vao menu context
        self.videoContent.add_item_context_menu()
        actionHistory = self.menu.addAction("History (Ctrl + H)")
        actionclipboard = self.menu.addSeparator()
        self.actionFull = self.menu.addAction(QIcon.fromTheme("view-fullscreen"), "Normal screen (Ctrl + F)" if self.parent.windowState() & Qt.WindowFullScreen else "Fullscreen (Ctrl + F)")
        actionSep = self.menu.addSeparator()
        actionInfo = self.menu.addAction(QIcon.fromTheme("help-about"), "Info (Ctrl + I)")
        action5 = self.menu.addSeparator()
        actionQuit = self.menu.addAction(QIcon.fromTheme("application-exit"), "Exit (Ctrl +  Q)")

        actionHistory.triggered.connect(self.view_history)
        actionQuit.triggered.connect(self.quit)
        self.actionFull.triggered.connect(self.fullscreen)
        # actionInfo.triggered.connect(self.handle_info)
        self.menu.exec_(self.mapToGlobal(QPoint(point.x(), point.y() - 100)))

    def open_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                                                  QDir.homePath() + "/Videos",
                                                  "Media (*.webm *.mp4 *.ts *.avi *.mpeg *.mpg *.mkv *.VOB *.m4v *.3gp *.mp3 *.m4a *.wav *.ogg *.flac *.m3u *.m3u8)")

        if fileName != '':
            self.videoContent.load_film(fileName)
            print("File loaded")

    def fullscreen(self, event = None):
        if self.parent.windowState() & Qt.WindowFullScreen:
            # QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.parent.showNormal()
            self.videoContent.fullscreenButton.setIcon(QIcon("assets/expand.png"))
            self.actionFull.setText("Fullscreen (Ctrl + F)")
            print("no Fullscreen")
        else:
            self.parent.showFullScreen()
            # QApplication.setOverrideCursor(Qt.BlankCursor)
            self.videoContent.fullscreenButton.setIcon(QIcon("assets/exit_fullscreen.png"))
            self.actionFull.setText("Normal Screen (Ctrl + F)")
            print("Fullscreen entered")

    def view_history(self):
        if not self.videoContent.isHidden():
            self.videoContent.hide()
            self.videoHaveSeen.show()

    def show_fullscreen(self, event):
        self.parent.showFullScreen()

    def close_fullscreen(self, event):
        self.parent.showNormal()

    def quit(self):
        self.videoContent.stop_media_player()
        # self.resume_screensaver()
        print("Goodbye ...")
        QApplication.quit()

    def close_window_event(self, event):
        print("Close window")
        self.videoContent.currentPosition = self.videoContent.media_player.position()
        self.videoContent.currentDuration = self.videoContent.media_player.duration()
        self.videoContent.media_player.stop()
        event.accept()

    def on_click_btn(self, text):
        print(text)
        if text == "Library":
            self.videoContent.hide()
            self.videoHaveSeen.show()
        elif text == "Now Playing":
            self.videoHaveSeen.hide()
            self.videoContent.show()

    def styleSheet(self):
        return """
            QMenu {
                background: rgba(98, 98, 98, 90);
                color: white;
                border: 1px solid #ccc; /* Đường viền */
                padding: 4px;
            }
            QMenu::item {
                padding: 4px 20px;
            }
            QMenu::item:selected {
                background: rgba(98, 98, 98, 255);
            }
        """
