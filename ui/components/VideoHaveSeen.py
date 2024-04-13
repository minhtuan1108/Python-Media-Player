import sys
import json
from PyQt5.QtGui import QIcon,QCursor
from PyQt5.QtCore import Qt,QSize,QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabBar,QMessageBox ,QDialog,QVBoxLayout, QLabel,QWidget, QHBoxLayout, QFrame, QPushButton,QScrollArea,QMenu
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
        self.frame_tab = QFrame()
        self.hbox_layout_tab = QHBoxLayout()
        self.frame_tab.setLayout(self.hbox_layout_tab)
        self.hbox_layout_tab.addWidget(self.tab_bar)
        
        #CSS Frame Tab
        self.frame_tab.setFixedWidth(300)
        
        # Khung chua danh sach Qhbox layout
        self.frame = QFrame()
        self.frame.setFixedSize(800,650)
        self.frame.setStyleSheet("""
                                 border-radius: 20%;
                                 background-color: white;
                                 """)
        self.frame_layout = QFrame()
        self.vbox_layout = QVBoxLayout()
        
        # khung chua Button
        self.vbox_layout_list = QVBoxLayout()
        self.frame.setLayout(self.vbox_layout)
        
        # Tạo một QScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        # self.frame.setLayout(self.scroll_area)
        self.vbox_layout.addWidget(self.scroll_area)
        self.scroll_area.setWidget(self.frame_layout)
        self.frame_layout.setLayout(self.vbox_layout_list)
        
        self.vbox_layout_list.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.frame_tab)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.frame)
        self.central_widget.setLayout(self.layout)
        #  tao label
        self.label = QLabel("Bạn có chắc chắn muốn xóa không?")
        
        # Lưu trữ trạng thái của các tab
        self.tab_states = [False, False, False]
        
        self.buttons = {}  # Dictionary để lưu trữ các nút theo tab index
        
        self.tab_changed(0) # Goi chay cung UI khi render UI
    # Xử lý sự kiện khi tab được chọn
    def tab_changed(self, index):
        
        # Loại bỏ layout của các tab khác
        for i, state in enumerate(self.tab_states):
            if i != index and state == True:
                self.remove_layout()
        
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
        self.remove_layout()  # Loại bỏ layout cũ (nếu có)
        
        with open("videolocal.json","r") as f:
            data = json.load(f)
        
        for video in data["videos"]:
            url = video['url']
            duration = video['duration']
            saved_at = video['saved_at']
            btn_local = QPushButton(f"{url}\n{duration}, {saved_at}")
            btn_local.setIcon(QIcon('./assets/local.png'))
            btn_local.setIconSize(QSize(50, 50))  # Đặt kích thước của biểu tượng
            btn_local.setStyleSheet('''
                                QPushButton {
                                    background-color: #f0f0f0; /* Màu nền */
                                    padding: 10px; /* Khoảng cách nội dung và viền */
                                    font-size: 16px; /* Kích thước font chữ */
                                    font-family: "Times New Roman";
                                    padding-right: 10px;
                                }   
                                QPushButton::hover {
                                    background-color: #e0e0e0; /* Màu nền khi di chuột qua */
                                }
                                QPushButton::pressed {
                                    background-color: #d0d0d0; /* Màu nền khi nhấn */
                                }
                            ''')         
            self.vbox_layout_list.addWidget(btn_local)
            btn_local.clicked.connect(self.showPopupMenu)   
            
        self.buttons[index] = btn_local
        print("Local layout rendered")

    def render_network(self):
        index = 1
        self.remove_layout()  # Loại bỏ layout cũ (nếu có)
        
        with open("videonetwork.json","r") as f:
            data = json.load(f)
        
        for video in data['videos']:
            url = video['url']
            duration = video['duration']
            saved_at = video['saved_at']
            btn_network = QPushButton(f"{url}\n{duration}, {saved_at}")
            btn_network.setIcon(QIcon('./assets/netword.png'))
            btn_network.setIconSize(QSize(50, 50))  
            self.vbox_layout_list.addWidget(btn_network)
            btn_network.setStyleSheet("""
                                QPushButton {
                                    background-color: #f0f0f0; /* Màu nền */
                                    padding: 10px; /* Khoảng cách nội dung và viền */
                                    font-size: 16px; /* Kích thước font chữ */
                                    font-family: "Times New Roman";
                                }
                                QPushButton:hover {
                                    background-color: #e0e0e0; /* Màu nền khi di chuột qua */
                                }
                                QPushButton:pressed {
                                    background-color: #d0d0d0; /* Màu nền khi nhấn */
                                }
                            """)
            btn_network.clicked.connect(self.showPopupMenu)   
        self.buttons[index] = btn_network

    def render_youtube(self):
        index = 2
        self.remove_layout()  # Loại bỏ layout cũ (nếu có)
        
        with open("videoyoutube.json","r") as f:
            data = json.load(f)
        for video in data['videos']:
            url = video['url']
            duration = video['duration']
            saved_at = video['saved_at']    
            btn_youtube = QPushButton(f"{url}\n{duration}, {saved_at}")
            btn_youtube.setIcon(QIcon('./assets/youtube.png'))
            btn_youtube.setIconSize(QSize(50, 50))
            self.vbox_layout_list.addWidget(btn_youtube)
            btn_youtube.setStyleSheet("""
                                QPushButton {
                                    background-color: #f0f0f0; /* Màu nền */
                                    padding: 10px; /* Khoảng cách nội dung và viền */
                                    font-size: 16px; /* Kích thước font chữ */
                                    font-family: "Times New Roman";
                                }
                                QPushButton:hover {
                                    background-color: #e0e0e0; /* Màu nền khi di chuột qua */
                                }
                                QPushButton:pressed {
                                    background-color: #d0d0d0; /* Màu nền khi nhấn */
                                }
                            """)
            btn_youtube.clicked.connect(self.showPopupMenu)   
        self.buttons[index] = btn_youtube
        

    
    # Loại bỏ layout của tab khi không được chọn
    def remove_layout(self):
        # Xóa tất cả các widget con của vbox_layout_list
        while self.vbox_layout_list.count() > 0:
            widget = self.vbox_layout_list.takeAt(0).widget()
            if widget is not None:
                widget.deleteLater()

        # Xóa các nút từ self.buttons
        self.buttons.clear()


    def showPopupMenu(self):
        # Tạo một menu popup
        self.popup_menu = QMenu(self)
        # Thêm các mục vào menu popup
        self.action1 = self.popup_menu.addAction("Phát")
        self.action2 = self.popup_menu.addAction("Xóa")
        self.action2.triggered.connect(self.actionDelete)
        # Lấy tọa độ của sự kiện chuột và hiển thị menu popup tại vị trí đó
        cursor_pos = QCursor.pos()
        self.popup_menu.exec_(cursor_pos)
        print("menu")
        
    def actionDelete(self):
        reply = QMessageBox.question(self, 'Xác nhận xóa', 'Bạn có chắc muốn xóa?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print('Đã xóa!')
            # Thực hiện hành động xóa ở đây
        else:
            print('Hủy bỏ xóa')        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())