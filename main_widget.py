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


    def resizeEvent(self, event):
        self.market_scene.setSceneRect(0, 0, self.market.width(), self.market.height())
        self.height = self.market.height()
        self.width = self.market.width()
        self.draw()

    def draw(self):
        self.market_scene.clear()
        self.market_scene.addLine(0, 0, self.market.width()-1, 0, self.gray_pen)

        self.cross_line_background = CrossLineBackground(QSizeF(self.width - 120, \
                self.height - 320), self.gray_pen)
        self.cross_line_background.setPos(60, 0)

        pen = QPen(QColor(187, 134, 252))
        self.price_line = PriceLine(QSizeF(self.width-120, self.height-320), pen)
        self.price_line.setPos(60, 0)

        self.market_scene.addItem(self.cross_line_background)
        self.market_scene.addItem(self.price_line)
