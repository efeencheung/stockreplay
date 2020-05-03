import math

from PySide2.QtCore import QRectF
from PySide2.QtGui import QBrush, QColor, QPen
from PySide2.QtWidgets import QGraphicsItem


class VolumeBar(QGraphicsItem):
    def __init__(self, size, price_model):
        QGraphicsItem.__init__(self)
        self.size = size
        self.price_model = price_model
        self.data = self.price_model.vol_data

    def boundingRect(self):
        return QRectF(0, 0, self.size.width(), self.size.height())

    def paint(self, painter, option, widget):
        red_pen = QPen(QColor(255, 23, 24))
        red_brush = QBrush(QColor(255, 23, 24))
        gray_pen = QPen(QColor(117, 117, 117))
        gray_brush = QBrush(QColor(117, 117, 117))
        green_pen = QPen(QColor(25, 183, 83))
        green_brush = QBrush(QColor(25, 183, 83))

        width = (self.size.width() - 241) / 242
        print(width)
        for i in range(len(self.data)):
            if self.data[i][2] == "long":
                painter.setPen(red_pen)
                brush = red_brush
            elif self.data[i][2] == "short":
                painter.setPen(green_pen)
                brush = green_brush
            else:
                painter.setPen(gray_pen)
                brush = gray_brush

            height = int(self.data[i][1] / self.price_model.max_vol *
                         self.size.height())
            start_y = int(self.size.height() - height)
            if start_y + height > self.size.height():
                height = height - 1
            if self.data[i][1] > 0:
                painter.drawRect(i * width + i, start_y,
                                 width - 1, height - 1)
            if self.data[i][2] == "short":
                painter.fillRect(i * width + i, start_y,
                                 width-1, height-1, brush)
