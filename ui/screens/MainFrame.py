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

    def context_menu_requested(self, point):
        self.menu.clear()
        # goi ham de add cac chuc nang cua xem video vao menu context
        self.videoContent.add_item_context_menu()
        actionclipboard = self.menu.addSeparator()

        self.actionFull = self.menu.addAction(QIcon.fromTheme("view-fullscreen"), "Normal screen (f)" if self.parent.windowState() & Qt.WindowFullScreen else "Fullscreen (f)")
        actionSep = self.menu.addSeparator()
        actionInfo = self.menu.addAction(QIcon.fromTheme("help-about"), "Info (i)")
        action5 = self.menu.addSeparator()
        actionQuit = self.menu.addAction(QIcon.fromTheme("application-exit"), "Exit (q)")

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

    def fullscreen(self, event):
        if self.parent.windowState() & Qt.WindowFullScreen:
            # QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.parent.showNormal()
            print("no Fullscreen")
        else:
            self.parent.showFullScreen()
            # QApplication.setOverrideCursor(Qt.BlankCursor)
            self.actionFull.setText("Normal Screen")
            print("Fullscreen entered")

    def show_fullscreen(self):
        self.parent.showFullScreen()

    def close_fullscreen(self):
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
