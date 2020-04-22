import pandas as pd
import sqlite3

from datetime import datetime
from PySide2.QtCore import Qt, QSizeF
from PySide2.QtGui import QBrush, QColor, QPalette, QPainter, QPainterPath, QPixmap, QPen, QTransform
from PySide2.QtWidgets import QFrame, QGraphicsLineItem, QGraphicsRectItem, QGraphicsScene, QGraphicsView, QHBoxLayout, \
    QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from cross_line_background import CrossLineBackground
from price_line import PriceLine


class MainWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(18, 18, 18))
        palette.setColor(QPalette.Foreground, QColor(226, 226, 226))

        self.gray_pen = QPen(QColor(255, 255, 255, 17.75), 1)

        self.title = QLabel("掌趣科技")
        self.time_btn = QPushButton("分时", self)
        self.time_btn.setFixedSize(32, 17)
        self.time_btn.setCheckable(True)
        self.time_btn.setChecked(True)
        self.time_btn.clicked.connect(self.time_line)
        self.tick_btn = QPushButton("逐笔", self)
        self.tick_btn.setFixedSize(32, 17)
        self.tick_btn.setCheckable(True)
        self.tick_btn.clicked.connect(self.tick_line)
        self.k_btn = QPushButton("K线", self)
        self.k_btn.setFixedSize(32, 17)
        self.k_btn.setCheckable(True)
        self.k_btn.clicked.connect(self.k_line)
        self.top = QWidget(self)
        self.top.setObjectName("top")
        self.top_layout = QHBoxLayout()
        self.top_layout.setSpacing(8)
        self.top_layout.setMargin(0)
        self.top_layout.setAlignment(Qt.AlignLeft)
        self.top.setLayout(self.top_layout)
        self.top.setStyleSheet("\
            QWidget#top{background:rgba(255,255,255,0.05)}\
            QPushButton{border:0}\
            QPushButton:checked{background:rgba(255,255,255,0.16);border:0}\
            QPushButton:hover{background:rgba(255,255,255,0.16);border:0}\
            QPushButton:pressed{background:rgba(255,255,255,0.16)}")
        self.top_layout.addWidget(self.title)
        self.top_layout.addWidget(self.time_btn)
        self.top_layout.addWidget(self.tick_btn)
        self.top_layout.addWidget(self.k_btn)

        top_size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.top.setSizePolicy(top_size)
        self.top.setContentsMargins(8, 4, 8, 4)
        self.top.setFixedHeight(25)

        self.market_scene = QGraphicsScene()
        self.market = QGraphicsView(self.market_scene)
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
        self.setLayout(self.main_layout)
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setSizePolicy(size)

    def showEvent(self, event):
        #self.market_scene.setSceneRect(0, 0, self.market.width(), self.market.height())
        #self.height = self.market_scene.height()
        #self.width = self.market_scene.width()
        self.height = self.market.height()
        self.width = self.market.width()
        self.draw()

    def resizeEvent(self, event):
        self.market_scene.setSceneRect(0, 0, self.market.width(), self.market.height())
        transform = QTransform((event.size().width()-120)/680, 0, 0, event.size().height()/575, 0, 0)
        if hasattr(self, 'time_price_line'):
            self.time_price_line.setTransform(transform)
        if hasattr(self, 'tick_price_line'):
            self.tick_price_line.setTransform(transform)
        if hasattr(self, 'cross_line_background'):
            self.cross_line_background.setTransform(transform)

    def draw(self):
        self.market_scene.clear()
        self.market_scene.addLine(0, 0, self.market.width()-1, 0, self.gray_pen)

        self.cross_line_background = CrossLineBackground(QSizeF(self.width - 120, \
                self.height - 320), self.gray_pen)
        self.cross_line_background.setPos(60, 0)

        pen = QPen(QColor(187, 134, 252))
        self.time_price_line = PriceLine(QSizeF(self.width-120, self.height-320), pen, 'time')
        self.time_price_line.setPos(60, 0)

        self.market_scene.addItem(self.cross_line_background)
        self.market_scene.addItem(self.time_price_line)

    def time_line(self):
        self.time_btn.setChecked(True)
        self.tick_btn.setChecked(False)
        self.k_btn.setChecked(False)
        self.time_price_line.setVisible(True)
        self.tick_price_line.setVisible(False)
        
    def tick_line(self):
        self.time_btn.setChecked(False)
        self.tick_btn.setChecked(True)
        self.k_btn.setChecked(False)

        self.time_price_line.setVisible(False)
        if hasattr(self, 'tick_price_line'):
            self.tick_price_line.setVisible(True)
        else:
            pen = QPen(QColor(187, 134, 252))
            self.tick_price_line = PriceLine(QSizeF(self.width-120, self.height-320), pen, 'tick')
            self.tick_price_line.setPos(60, 0)
            self.market_scene.addItem(self.tick_price_line)

    def k_line(self):
        self.time_btn.setChecked(False)
        self.tick_btn.setChecked(False)
        self.k_btn.setChecked(True)
