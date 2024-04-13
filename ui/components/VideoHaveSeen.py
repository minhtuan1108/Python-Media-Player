import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabBar, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QPushButton
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Tạo một Tab Bar
        self.tab_bar = QTabBar()

        # Thêm các tab vào Tab Bar
        self.tab_bar.addTab("Local")
        self.tab_bar.addTab("Network")
        self.tab_bar.addTab("Youtube")

        # Khi một tab được chọn, gọi hàm tab_changed
        self.tab_bar.tabBarClicked.connect(self.tab_changed)

        # Thêm Tab Bar vào layout chính
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Khung chua tab bar
        self.hbox_layout_tab = QHBoxLayout()
        self.hbox_layout_tab.addWidget(self.tab_bar)
        
        # Khung chua danh sach Qhbox layout
        self.frame = QFrame()
        self.frame.setFixedSize(800,800)
        self.frame.setStyleSheet("""
                                 background-color: black;
                                 """)
        
        # khung chua Button
        self.vbox_layout_list = QVBoxLayout()
        self.frame.setLayout(self.vbox_layout_list)
        
        
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.hbox_layout_tab)
        self.layout.addWidget(self.frame)
        self.central_widget.setLayout(self.layout)
        
        # Lưu trữ trạng thái của các tab
        self.tab_states = [False, False, False]
        
        self.buttons = {}  # Dictionary để lưu trữ các nút theo tab index
        
        self.tab_changed(0) # Goi chay cung UI khi render UI
        
    # Xử lý sự kiện khi tab được chọn
    def tab_changed(self, index):
        print(f"Tab {index} selected")
        
        # Loại bỏ layout của các tab khác
        for i, state in enumerate(self.tab_states):
            if i != index and state == True:
                self.remove_layout(i)
        
        # Cập nhật trạng thái của tab được chọn
        self.tab_states[index] = True
        
        text = self.tab_bar.tabText(index)
        if text == "Local":
            self.render_local()   
        elif text == "Network":  
            self.render_network()
        elif text == "Youtube":
            self.render_youtube()

    def render_local(self):
        index = 0
        self.remove_layout(index)  # Loại bỏ layout cũ (nếu có)
        btn_local = QPushButton()
        btn_local.setIcon(QIcon('./assets/local.png'))
        self.vbox_layout_list.addWidget(btn_local)
        self.buttons[index] = btn_local
        print("Local layout rendered")

    def render_network(self):
        index = 1
        self.remove_layout(index)  # Loại bỏ layout cũ (nếu có)
        btn_network = QPushButton()
        btn_network.setIcon(QIcon('./assets/netword.png'))  # Sửa lại đường dẫn hình ảnh
        self.vbox_layout_list.addWidget(btn_network)
        self.buttons[index] = btn_network
        print("Network layout rendered")

    def render_youtube(self):
        index = 2
        self.remove_layout(index)  # Loại bỏ layout cũ (nếu có)
        btn_youtube = QPushButton()
        btn_youtube.setIcon(QIcon('./assets/youtube.png'))
        self.vbox_layout_list.addWidget(btn_youtube)
        self.buttons[index] = btn_youtube
        print("Youtube layout rendered")

    
    # Loại bỏ layout của tab khi không được chọn
    def remove_layout(self, index):
        if index in self.buttons:  # Kiểm tra xem có nút được tạo cho tab này không
            button = self.buttons[index]  # Lấy nút từ dictionary
            self.vbox_layout_list.removeWidget(button)  # Loại bỏ nút khỏi layout
            button.deleteLater()  # Loại bỏ button khỏi bộ nhớ
            print(f"Button of Tab {index} removed")

            # Xóa nút khỏi dictionary
            del self.buttons[index]

                    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())