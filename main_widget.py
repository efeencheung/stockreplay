import pandas as pd
import sqlite3

from datetime import datetime
from PySide2.QtCore import Qt, QSizeF
from PySide2.QtGui import QBrush, QColor, QPalette, QPainter, QPainterPath, QPixmap, QPen
from PySide2.QtWidgets import QFrame, QGraphicsLineItem, QGraphicsRectItem, QGraphicsScene, QGraphicsView, QHBoxLayout, \
    QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from cross_line_background import CrossLineBackground


class MainWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(18, 18, 18))
        palette.setColor(QPalette.Foreground, QColor(226, 226, 226))

        self.gray_pen = QPen(QColor(255, 255, 255, 17.75), 1)

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
        self.market = QGraphicsView(self.market_scene)
        self.market.setObjectName("market")
        self.market.setFrameShape(QFrame.NoFrame)
        self.market.setStyleSheet("\
            QWidget#market{background:rgba(255,255,255,0.05)}")

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
        self.market_scene.setSceneRect(0, 0, self.market.width(), self.market.height())
        self.market_scene.clear()
        self.market_scene.addLine(0, 0, self.market.width(), 0, self.gray_pen)
        self.height = self.market_scene.height()
        self.width = self.market_scene.width()

        self.deal_data()

        self.draw_bg()
        self.draw_price()

    def draw_bg(self):
        cross_line_bg = CrossLineBackground(QSizeF(self.width - 80, \
                self.height - 20), self.gray_pen)
        cross_line_bg.setPos(40, 0)

    def draw_price(self):
        pen = QPen(QColor(187, 134, 252))
        path = QPainterPath()
        for index, row in self.df.iterrows():
            if index < datetime(2020, 3, 25, 9, 30, 0) or \
                    index > datetime(2020, 3, 25, 15, 0, 0) or \
                    (index > datetime(2020, 3, 25, 11, 30, 0) and \
                    index < datetime(2020, 3, 25, 13, 0, 0)):
                continue

            timestamp = index.timestamp() - 28800
            if index >= datetime(2020, 3, 25, 13, 0, 0):
                timestamp = index.timestamp() - 5400 - 28800

            (x, y) = self.to_point(timestamp, row["price"])
            if index == datetime(2020, 3, 25, 9, 30, 0):
                path.moveTo(40, y)
                continue

            path.lineTo(x, y)
        self.market_scene.addPath(path, pen)

    def deal_data(self):
        conn = sqlite3.connect('stock.db')        
        self.origin_df = pd.read_sql_query("\
            SELECT datetime(time, 'unixepoch', 'localtime') time_index,\
            price, volume FROM sz_300315", conn, index_col='time_index')
        self.origin_df.index = pd.to_datetime(self.origin_df.index)

        price = self.origin_df["price"].resample('60S', label='right', closed='right').last()
        volume = self.origin_df["volume"].resample('60S', label='right', closed='right').sum()
        self.df = pd.concat([price, volume], axis=1)
        max_price = self.df["price"].max()
        min_price = self.df["price"].min()
        prev_price = 5.39
        if abs(max_price - prev_price) > abs(min_price - prev_price):
            self.max_y = prev_price + abs(max_price - prev_price)
            self.min_y = prev_price - abs(max_price - prev_price)
        else:
            self.max_y = prev_price + abs(min_price - prev_price)
            self.min_y = prev_price - abs(min_price - prev_price)
        self.diff_x = 14400
        self.diff_y = self.max_y - self.min_y
        self.min_x = datetime(2020, 3, 25, 9, 30, 00).timestamp()

    def to_point(self, ox, oy):
        y = (self.max_y - oy) * (self.height - 20) / self.diff_y
        x = (ox - self.min_x) * (self.width - 80) / self.diff_x + 40

        return (x, y)

