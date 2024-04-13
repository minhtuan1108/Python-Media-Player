from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui.components.VideoContent import VideoContent


# This frame is use for containing content of screen, stay under of top menu bar
class MainFrame(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setStyleSheet("background-color: #FFFFFF; border-radius: 10px;")
        self.videoContent = VideoContent(self)
        self.setLayout(self.videoContent.layout())
        self.myinfo = "©2016\nAxel Schneider\n\nMouse Wheel = Zoom\nUP = Volume Up\nDOWN = Volume Down\n" + \
                      "LEFT = < 1 Minute\nRIGHT = > 1 Minute\n" + \
                      "SHIFT+LEFT = < 10 Minutes\nSHIFT+RIGHT = > 10 Minutes"


    def context_menu_requested(self, point):
        self.menu = QMenu()
        actionFile = self.menu.addAction(QIcon.fromTheme("video-x-generic"), "open File (o)")
        actionclipboard = self.menu.addSeparator()
        actionURL = self.menu.addAction(QIcon.fromTheme("browser"), "URL from Internet (u)")
        actionclipboard = self.menu.addSeparator()
        actionYTurl = self.menu.addAction(QIcon.fromTheme("youtube"), "URL from YouTube (y)")
        actionclipboard = self.menu.addSeparator()
        actionToggle = self.menu.addAction(QIcon.fromTheme("next"), "show / hide Slider (s)")
        actionFull = self.menu.addAction(QIcon.fromTheme("view-fullscreen"), "Fullscreen (f)")
        action169 = self.menu.addAction(QIcon.fromTheme("tv-symbolic"), "16 : 9")
        action43 = self.menu.addAction(QIcon.fromTheme("tv-symbolic"), "4 : 3")
        actionSep = self.menu.addSeparator()
        actionInfo = self.menu.addAction(QIcon.fromTheme("help-about"), "Info (i)")
        action5 = self.menu.addSeparator()
        actionQuit = self.menu.addAction(QIcon.fromTheme("application-exit"), "Exit (q)")

        actionFile.triggered.connect(self.open_file)
        actionQuit.triggered.connect(self.quit)
        actionFull.triggered.connect(self.fullscreen)
        # actionInfo.triggered.connect(self.handleInfo)
        # actionToggle.triggered.connect(self.toggleSlider)
        # actionURL.triggered.connect(self.playFromURL)
        # actionYTurl.triggered.connect(self.getYTUrl)
        # action169.triggered.connect(self.screen169)
        # action43.triggered.connect(self.screen43)
        self.menu.exec_(self.mapToGlobal(point))


    def open_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                                                  QDir.homePath() + "/Videos",
                                                  "Media (*.webm *.mp4 *.ts *.avi *.mpeg *.mpg *.mkv *.VOB *.m4v *.3gp *.mp3 *.m4a *.wav *.ogg *.flac *.m3u *.m3u8)")

        if fileName != '':
            self.loadFilm(fileName)
            print("File loaded")

    def fullscreen(self, event):
        if self.parent.windowState() & Qt.WindowFullScreen:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.parent.showNormal()
            print("no Fullscreen")
        else:
            self.parent.showFullScreen()
            QApplication.setOverrideCursor(Qt.BlankCursor)
            print("Fullscreen entered")

    def quit(self):
        self.videoContent.stop_media_player()
        self.resume_screensaver()
        print("Goodbye ...")
        QApplication.quit()