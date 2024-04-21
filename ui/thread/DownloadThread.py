
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from pytube import YouTube
import m3u8_To_MP4
class DownloadThread(QThread):
    finished = pyqtSignal()

    def __init__(self, url, dir, filename, type, parent=None):
        super().__init__(parent)
        self.url = url
        self.dir = dir
        self.filename = filename
        self.type = type

    def run(self):
        try:
            if self.type == "youtube":
                yt = YouTube(self.url)
                stream = yt.streams.get_highest_resolution()
                stream.download(self.dir, self.filename)
            else:
                m3u8_To_MP4.multithread_download(self.url, mp4_file_dir=self.dir, mp4_file_name=self.filename)
            QMessageBox.information(None, "Download Completed", "Video has been downloaded successfully!")
        except Exception as e:
            QMessageBox.warning(None, "Error", f"An error occurred: {e}")
        finally:
            self.finished.emit()