from PySide2.QtGui import QColor, QPalette
from PySide2.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,QVBoxLayout, QWidget)


class MainWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(18, 18, 18))
        palette.setColor(QPalette.Foreground, QColor(226, 226, 226))

        self.title = QLabel("掌趣科技")
        self.second_btn = QPushButton("分时", self)
        self.second_btn.setAutoFillBackground(True)
        self.tick_btn = QPushButton("逐笔", self)
        self.k_btn = QPushButton("K线", self)
        self.k5m_btn = QPushButton("5分钟", self)
        self.top = QWidget(self)
        self.top_layout = QHBoxLayout()
        self.top_layout.setMargin(8)
        self.top.setLayout(self.top_layout)
        self.top.setStyleSheet("QPushButton{background:rgb(29, 29, 29)}")
        self.top_layout.addWidget(self.title)
        self.top_layout.addWidget(self.second_btn)
        self.top_layout.addWidget(self.tick_btn)
        self.top_layout.addWidget(self.k_btn)
        self.top_layout.addWidget(self.k5m_btn)

        top_size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.top.setSizePolicy(top_size)
        self.top.setFixedHeight(40)

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
