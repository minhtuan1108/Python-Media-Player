import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QFrame
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MediaPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Player")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.central_widget.setStyleSheet("""
                                          background-color: gray; 
                                          """)

        # main box layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        # khoảng cách giữa 2 layout
        self.layout.setSpacing(0)
        
        self.hbox_layout = QHBoxLayout() # hbox lớn được bọc bởi frame
        self.hbox_layouts = QHBoxLayout()   # hbox nhỏ được bọc bởi frame_layout
        
        self.hbox_layout.setAlignment(Qt.AlignCenter)
    
        self.frame = QFrame() # frame lớn bọc hbox_layout
        self.frame_layout = QFrame() # frame_layout nhỏ bọc hbox_layouts

        self.frame_layout.setStyleSheet("""
                                    background-color: #969696;
                                    text-align: center;
                                    font-size: 16px;
                                    font-weight: bold;
                                    border-radius: 40px;
                                    
                                        """)
        self.frame_layout.setFixedSize(500,80)
        
        self.frame_layout.setLayout(self.hbox_layouts) # set hbox_layouts vào frame_layout
        
        self.hbox_layout.addWidget(self.frame_layout) # set frame_layout vào hbox_layout
        
        self.frame.setLayout(self.hbox_layout) # set frame_layout vào frame
        
        self.frame.setFixedHeight(100)
        
        self.layout.addWidget(self.frame) # add frame vào layout
        
        self.frame.setStyleSheet("""
                                    background-color: gray;
                                    text-align: center;
                                    font-size: 16px;
                                    font-weight: bold;
                                """)
            
        # Create and style buttons
        self.button1 = QPushButton("Now playing")
        self.button1.clicked.connect(self.on_click_btn1)
        self.button1.setStyleSheet("background-color: white; color: black; border-radius: 20px ;font-size: 16px;")
        self.button1.setFixedSize(145, 40)

        self.button2 = QPushButton("Library")
        self.button2.clicked.connect(self.on_click_btn2)
        self.button2.setStyleSheet("""background-color: white; color: black; border-radius: 20px ;font-size: 16px;""")
        self.button2.setFixedSize(145, 40)

        self.button3 = QPushButton("Playlist")
        self.button3.clicked.connect(self.on_click_btn3)
        self.button3.setStyleSheet("background-color: white; color: black; border-radius: 20px ;font-size: 16px;")
        self.button3.setFixedSize(145, 40)
       

       
        
        # Add buttons to the horizontal layout
        self.hbox_layouts.addWidget(self.button1)
        self.hbox_layouts.addWidget(self.button2)
        self.hbox_layouts.addWidget(self.button3)
        

        self.webview = QWebEngineView()
        self.layout.addWidget(self.webview)
        

    def on_click_btn1(self):
        # Hiển thị giao diện 1
        print("Giao diện 1 được chọn")

    def on_click_btn2(self):
        # Hiển thị giao diện 2
        print("Giao diện 2 được chọn")

    def on_click_btn3(self):
        # Hiển thị giao diện 3
        print("Giao diện 3 được chọn")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MediaPlayer()
    ex.show()
    sys.exit(app.exec_())