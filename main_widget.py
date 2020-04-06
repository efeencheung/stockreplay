from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QPalette
from PySide2.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, \
    QVBoxLayout, QWidget


class MainWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(18, 18, 18))
        palette.setColor(QPalette.Foreground, QColor(226, 226, 226))

        self.title = QLabel("掌趣科技")
        self.tick_btn = QPushButton("逐笔", self)
        self.tick_btn.setFixedSize(32, 16)
        self.second_btn = QPushButton("分时", self)
        self.second_btn.setFixedSize(32, 16)
        self.k_btn = QPushButton("K线", self)
        self.k_btn.setFixedSize(32, 16)
        self.top = QWidget(self)
        self.top.setObjectName("top")
        self.top_layout = QHBoxLayout()
        self.top_layout.setSpacing(8)
        self.top_layout.setMargin(0)
        self.top_layout.setAlignment(Qt.AlignLeft)
        self.top.setLayout(self.top_layout)
        self.top.setStyleSheet("\
            QWidget#top{background:rgba(255,255,255,0.05)}\
            QPushButton{background:rgba(255,255,255,0.16);border:0}\
            QPushButton:pressed{background:rgba(255,255,255,0.16)}")
        self.top_layout.addWidget(self.title)
        self.top_layout.addWidget(self.second_btn)
        self.top_layout.addWidget(self.tick_btn)
        self.top_layout.addWidget(self.k_btn)
        print(self.top.objectName())

        top_size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.top.setSizePolicy(top_size)
        self.top.setContentsMargins(8, 0, 8, 0)
        self.top.setFixedHeight(24)

        self.content = QWidget()

        self.main_layout = QVBoxLayout()
        self.main_layout.setMargin(0)
        self.main_layout.addWidget(self.top)
        self.main_layout.addWidget(self.content)
        self.setLayout(self.main_layout)
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setSizePolicy(size)
