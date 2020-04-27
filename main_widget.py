import pandas as pd
import sqlite3

from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QPalette, QPen
from PySide2.QtWidgets import QFrame, QGraphicsScene, QHBoxLayout, \
    QLabel, QSizePolicy, QVBoxLayout, QWidget

from main_view import MainView


class MainWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(18, 18, 18))
        palette.setColor(QPalette.Foreground, QColor(226, 226, 226))

        self.title = QLabel("掌趣科技")
        self.top = QWidget(self)
        self.top.setObjectName("top")
        self.top_layout = QHBoxLayout()
        self.top_layout.setSpacing(8)
        self.top_layout.setMargin(0)
        self.top_layout.setAlignment(Qt.AlignLeft)
        self.top.setLayout(self.top_layout)
        self.top.setStyleSheet("QWidget#top{background:rgba(255,255,255,0.05)}")
        self.top_layout.addWidget(self.title)

        top_size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.top.setSizePolicy(top_size)
        self.top.setContentsMargins(8, 2, 8, 2)
        self.top.setFixedHeight(21)

        scene = QGraphicsScene()
        self.market = MainView(scene)
        self.market.setAlignment(Qt.AlignTop)
        self.market.setObjectName("market")
        self.market.setFrameShape(QFrame.NoFrame)
        self.market.setStyleSheet("\
            QWidget#market{background:rgba(255,255,255,0.05)}")

        self.main_layout = QVBoxLayout()
        self.main_layout.setMargin(0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.top)
        self.main_layout.addWidget(self.market)
        self.market.setMouseTracking(True)
        self.setLayout(self.main_layout)
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setSizePolicy(size)
