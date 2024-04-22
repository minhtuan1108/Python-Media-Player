from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton


class TitleBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(240, 240, 240))  # Màu nền của title bar
        self.setPalette(palette)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Title label
        self.title_label = QLabel("My Video Player")
        self.title_label.setStyleSheet("font-weight: bold;font-family: Arial; font-size: 12pt; color: #333333")
        layout.addSpacing(10)
        layout.addWidget(self.title_label, Qt.AlignLeft)

        # Minimize button
        self.minimize_button = QPushButton("─")
        self.minimize_button.clicked.connect(self.window().showMinimized)
        layout.addWidget(self.minimize_button)
        self.minimize_button.setStyleSheet(styleButton(self))
        self.minimize_button.setFixedSize(45,30)

        # Maximize button
        self.maximize_button = QPushButton("□")
        self.maximize_button.clicked.connect(self.toggle_maximize)
        layout.addWidget(self.maximize_button)
        self.maximize_button.setStyleSheet(styleButton(self))
        self.maximize_button.setFixedSize(45,30)

        # Close button
        self.close_button = QPushButton("X")
        self.close_button.clicked.connect(self.window().close)
        layout.addWidget(self.close_button)
        self.close_button.setStyleSheet(styleButton(self))
        self.close_button.setFixedSize(45,30)

        # Title bar height
        self.setFixedHeight(30)
        
        # Window dragging
        self.draggable = True
        

    def toggle_maximize(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def mousePressEvent(self, event):
        
        if event.button() == Qt.LeftButton and self.draggable:
            print(1)
            self.drag_position = event.globalPos() - self.parent().frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.draggable:
            print(2)
            self.window().move(event.globalPos() - self.drag_position)
            event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(240, 240, 240))
        painter.drawRect(self.rect())

def styleButton(self):
    return """
    QPushButton{
        background-color: rgba(240, 240, 240, 0);
        pandding: 10px;
        border: none; 
    }
    QPushButton:hover {
        background-color: #C0C0C0;
    }
"""