# Python Video Player App
This Python application is a simple video player that allows you to play videos from various sources including local files, m3u8 files from the internet, and YouTube links. It provides basic functionalities such as play/pause, seek forward and backward by 10 seconds, and download video files,...

## Features
* Play Videos: Play videos from local files, m3u8 files, and YouTube links.
* Seek Functionality: Seek forward and backward by 10 seconds.
* Download Videos: Download video files to your local machine.
* History: Let user know what they saw.
* Simple Interface: User-friendly interface for easy navigation and control.

## Requirements
* Python 3.x
* Gstreamer
* PyQt5
* PyQtWebEngine
* pytube
* ffmpeg
* m3u8-To-MP4

## Installation
1. Clone this repository:

```bash
git clone https://github.com/minhtuan1108/PythonMediaPlayer.git
cd PythonMediaPlayer
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```

or install one by one dependency:

* PyQt5 install:

```bash
pip install PyQt5
```

* PyQtWebEngine install:
```bash
pip install PyQtWebEngine
```

* pytube install:
```bash
pip install pytube
```

* ffmpeg install (for Linux):
```bash
# On Ubuntu / Debian:
sudo apt-get update
sudo apt-get install ffmpeg
# On CentOS / Fedora:
sudo yum install epel-release
sudo yum install ffmpeg
```

* m3u8-To-MP4 install:
```bash
python -m pip install m3u8_To_MP4
```
View more on <a href="https://github.com/h2soong/m3u8_To_MP4">m3u8-To-MP4</a> github.

3. Install Gstreamer:
* On Ubuntu / Debian:
```bash
apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```
* On Fedora:
```bash
dnf install gstreamer1-devel gstreamer1-plugins-base-tools gstreamer1-doc gstreamer1-plugins-base-devel gstreamer1-plugins-good gstreamer1-plugins-good-extras gstreamer1-plugins-ugly gstreamer1-plugins-bad-free gstreamer1-plugins-bad-free-devel gstreamer1-plugins-bad-free-extras
```
For more option to download, go to <a href="https://gstreamer.freedesktop.org/documentation/installing/index.html">installing gstreamer</a>

## Usage

Run the application using Python3:
```bash
python3 /path/to/your/app/PythonMediaPlayer/main.py
```

## Basic guide to use
<b>1. Play video:</b>
   First right click to show menu context
   
   * Choose play from url to play file m3u8 from the internet
    ![image](https://github.com/minhtuan1108/minhtuan1108.github.io/blob/main/repositories_data/python_media_player/typeUrl.png)
   
   * Or choose play from youtube to play video from youtube link
    ![image](https://github.com/minhtuan1108/minhtuan1108.github.io/blob/main/repositories_data/python_media_player/typeYT.png)
   
   * Or choose open local to play audio file from local
    ![image](https://github.com/minhtuan1108/minhtuan1108.github.io/blob/main/repositories_data/python_media_player/typeLocal.png)
   
   * After choose type to play, app will get your url from clipboard or will show input url for play from url/youtube link.
      ![image](https://github.com/minhtuan1108/minhtuan1108.github.io/blob/main/repositories_data/python_media_player/nhapurl.png)
   
   * For local file, app will open folder manager and you can choose your file to play
<b>2. View history:</b>
   There is three tag in history(library) folder:

   * Local history (place to store your video you seen from local file:
     ![image](https://github.com/minhtuan1108/minhtuan1108.github.io/blob/main/repositories_data/python_media_player/tablocal.png)
     
   * Youtube history (store your history played file in youtube links):
     ![image](https://github.com/minhtuan1108/minhtuan1108.github.io/blob/main/repositories_data/python_media_player/tabytb.png)
     
   * Network history (place to store file you played from url):
     ![image](https://github.com/minhtuan1108/minhtuan1108.github.io/blob/main/repositories_data/python_media_player/tabnetwork.png)
