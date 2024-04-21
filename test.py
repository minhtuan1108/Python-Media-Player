import ffmpeg
from PyQt5.QtWidgets import QApplication
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import sys
import m3u8_To_MP4
import threading

import m3u8_To_MP4.v2_multithreads_processor

m3u8_url = "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8"
def multithread_download(m3u8_uri, customized_http_header=None,
                         max_retry_times=3, max_num_workers=100,
                         mp4_file_dir='./', mp4_file_name='m3u8_To_MP4',
                         tmpdir=None):
    with m3u8_To_MP4.v2_multithreads_processor.MultiThreadsUriCrawler(m3u8_uri,
                                                                      customized_http_header,
                                                                      max_retry_times,
                                                                      max_num_workers,
                                                                      mp4_file_dir,
                                                                      mp4_file_name,
                                                                      tmpdir) as crawler:
        crawler.fetch_mp4_by_m3u8_uri(True)
        print("Download completed! Hehe")

multithread_download(m3u8_url)
