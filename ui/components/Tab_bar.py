from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
class Tab_Bar(QHBoxLayout):
    def __init__(self):
        super().__init__()
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
        
        self.addWidget(self.frame) # add frame vào layout
        
        self.frame.setStyleSheet("""
                                    background-color: transparent;
                                    text-align: center;
                                    font-size: 16px;
                                    font-weight: bold;
                                """)
            
        # Create and style buttons
        self.button1 = QPushButton("Now playing")
        self.button1.clicked.connect(self.on_click_btn1)
        self.button1.setFixedSize(145, 40)

        self.button2 = QPushButton("Library")
        self.button2.clicked.connect(self.on_click_btn2)
        self.button2.setFixedSize(145, 40)

        self.button3 = QPushButton("Playlist")
        self.button3.clicked.connect(self.on_click_btn3)
        self.button3.setFixedSize(145, 40)
        
        # set style for button
        self.default_style = "background-color: #969696; color: black; border-radius: 20px; font-size: 16px;"
        self.button1.setStyleSheet(self.default_style)
        self.button2.setStyleSheet(self.default_style)
        self.button3.setStyleSheet(self.default_style)
       
        # Create state machine
        self.state_machine = QStateMachine()
        
        # STATE_NAMES =   [
        #                 'now_playing',
        #                 'library',
        #                 'playlist'
        #                 ]
            
        # Define states for each button
        
        self.my_string1 = "Now playing"
        self.my_string2 = "Library"
        self.my_string3 = "Playlist"
        
        # tạo 3 biến state 
        self.now_playing_state = QState()
        self.library_state = QState()
        self.playlist_state = QState()
        
        # Gán giá trị cho các biến bằng phương thức assignProperty()
        self.now_playing_state.assignProperty(self, "my_string1", self.button1.text())
        self.library_state.assignProperty(self, "my_string2", self.button2.text())
        self.playlist_state.assignProperty(self, "my_string3", self.button3.text())
        
        # Connect button clicks to transitions
        self.button1.clicked.connect(self.on_button_clicked)
        self.button2.clicked.connect(self.on_button_clicked)
        self.button3.clicked.connect(self.on_button_clicked)
        
        # Set initial state (can be any button)
        self.state_machine.setInitialState(self.now_playing_state)
        
        # Add buttons to the horizontal layout
        self.hbox_layouts.addWidget(self.button1)
        self.hbox_layouts.addWidget(self.button2)
        self.hbox_layouts.addWidget(self.button3)

        # Define transitions and button style changes
        self.now_playing_state.addTransition(self.button1.clicked, self.now_playing_state)  # No change for same button
        self.now_playing_state.addTransition(self.button2.clicked, self.library_state)
        self.now_playing_state.addTransition(self.button3.clicked, self.playlist_state)

        self.library_state.addTransition(self.button1.clicked, self.now_playing_state)
        self.library_state.addTransition(self.button2.clicked, self.library_state)  # No change for same button
        self.library_state.addTransition(self.button3.clicked, self.playlist_state)

        self.playlist_state.addTransition(self.button1.clicked, self.now_playing_state)
        self.playlist_state.addTransition(self.button2.clicked, self.library_state)
        self.playlist_state.addTransition(self.button3.clicked, self.playlist_state)  # No change for same button

        # Update button style on entering a state (optional)
        self.state_machine.entered.connect(self.update_button_style)
    
        
    def on_button_clicked(self):
        print(0)
    # Get the button that emitted the signal (sender())
        clicked_button = self.sender()
        button_name = clicked_button.objectName()  # Get button object name

    # Trigger transition based on button name
        self.state_machine.setObjectName(button_name)
    
    def update_button_style(self, state):
        print(1)
        # Set styles based on the current state
        active_button_style = "background-color: white; color: black; border-radius: 20px; font-size: 16px;"  # Define your active button style
        default_style = self.default_style

        if state == self.now_playing_state:
            self.button1.setStyleSheet(active_button_style)
            self.button2.setStyleSheet(default_style)
            self.button3.setStyleSheet(default_style)
        elif state == self.library_state:
            self.button1.setStyleSheet(default_style)
            self.button2.setStyleSheet(active_button_style)
            self.button3.setStyleSheet(default_style)
        elif state == self.playlist_state:
            self.button1.setStyleSheet(default_style)
            self.button2.setStyleSheet(default_style)
            self.button3.setStyleSheet(active_button_style)
        
    def on_click_btn1(self):
    # Hiển thị giao diện 1
        print("Giao diện 1 được chọn")

    def on_click_btn2(self):
        # Hiển thị giao diện 2
        print("Giao diện 2 được chọn")

    def on_click_btn3(self):
        # Hiển thị giao diện 3
        print("Giao diện 3 được chọn")