import pandas as pd
import sqlite3

from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QPalette, QPainter, QPen
from PySide2.QtWidgets import QGraphicsLineItem, QGraphicsScene, QGraphicsView, QHBoxLayout, \
    QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget


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

        top_size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.top.setSizePolicy(top_size)
        self.top.setContentsMargins(8, 0, 8, 0)
        self.top.setFixedHeight(24)

        self.market_scene = QGraphicsScene()
        conn = sqlite3.connect('stock.db')        
        origin_df = pd.read_sql_query("SELECT datetime(time, 'unixepoch', 'localtime') time,\
            price, volume, type FROM sz_300315", conn, index_col='time')
        origin_df.index = pd.to_datetime(origin_df.index)
        price = origin_df["price"].resample('60S', label='right').last()
        volume = origin_df["volume"].resample('60S', label='right').sum()
        print(pd.concat([price, volume], axis=1))
        pen = QPen(QColor(187, 134, 252))
        self.market_scene.addLine(0, 188, 20, 168, pen)
        self.market_scene.addLine(21, 168, 40, 198, pen)
        self.market_scene.addLine(41, 198, 60, 158, pen)
        self.market_scene.addLine(61, 158, 80, 188, pen)
        self.market_scene.addLine(81, 188, 100, 198, pen)
        #self.line.mapToScene(0, 0, 100, 100)
        self.market = QGraphicsView(self.market_scene)
        self.market.setObjectName("market")
        self.market.setRenderHint(QPainter.Antialiasing)
        self.market.setStyleSheet("\
            QWidget#market{background:rgba(255,255,255,0.05)}")
        #aa = self.market(self.market.viewport().geometry()).boundingRect()

        self.main_layout = QVBoxLayout()
        self.main_layout.setMargin(0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.top)
        self.main_layout.addWidget(self.market)
        self.setLayout(self.main_layout)
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setSizePolicy(size)

    def resizeEvent(self, event):
        self.market_scene.setSceneRect(0, 0, self.market.width()-2, self.market.height()-2)
        print(self.market.size())
