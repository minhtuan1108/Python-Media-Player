import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabBar, QVBoxLayout, QWidget, QHBoxLayout, QFrame

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Tạo một Tab Bar
        self.tab_bar = QTabBar()

        # Thêm các tab vào Tab Bar
        self.tab_bar.addTab("Local")
        self.tab_bar.addTab("Netword")
        self.tab_bar.addTab("Youtube")

        # Khi một tab được chọn, gọi hàm tab_changed
        self.tab_bar.currentChanged.connect(self.tab_changed)

        # Thêm Tab Bar vào layout chính
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Khung chua tab bar
        self.hbox_layout_tab = QHBoxLayout()
        self.hbox_layout_tab.addWidget(self.tab_bar)
        
        # Khung chua danh sach Qhbox layout
        self.frame = QFrame()
        self.frame.setFixedSize(500,500)
        
        # khung chua Qpanel
        self.hbox_layout_list = QHBoxLayout()
        self.frame.setLayout(self.hbox_layout_list)
        
        
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.hbox_layout_tab)
        self.layout.addWidget(self.frame)
        self.central_widget.setLayout(self.layout)

    # Xử lý sự kiện khi tab được chọn
    def tab_changed(self, index):
        text = self.tab_bar.tabText(index)
        print(text)
        if text == "Local":
          self.tab_bar.currentChanged.connect(self.render_local)
        elif text == "Netword":
            self.tab_bar.currentChanged.connect(self.render_netword)
        elif text == "Youtube":
            self.tab_bar.currentChanged.connect(self.render_youtube)
        # print(f"Tab {index+1} selected")
    
    def render_local(self):
        print("local")
    
    def render_netword(self):
        print("netword")
    
    def render_youtube(self):
        print("youtube")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())