from PySide2.QtCore import QRectF, Qt
from PySide2.QtGui import QColor, QPainter, QPen
from PySide2.QtWidgets import QGraphicsItem
from price_model import PriceModel


class SecondYaxis(QGraphicsItem):
    def __init__(self, size, max, min):
        QGraphicsItem.__init__(self)
        self.size = size
        self.max = max
        self.min = min

    def boundingRect(self):
        return QRectF(0, 0, self.size.width(), self.size.height())

    def paint(self, painter, option, widget):
        pen = QPen(QColor(117, 117, 117))
        painter.setPen(pen)

        y1 = self.max
        y2 = int((self.max - self.min) / 2)
        y3 = self.min

        ly1_rect = QRectF(0, 0, 56, 15)
        ly2_rect = QRectF(0, self.size.height() / 2 - 7.5, 56, 15)
        ly3_rect = QRectF(0, self.size.height() - 15, 56, 15)

        painter.drawText(ly1_rect, Qt.AlignRight, str(y1))
        painter.drawText(ly2_rect, Qt.AlignRight, str(y2))
        painter.drawText(ly3_rect, Qt.AlignRight, str(y3))

        ry1_rect = QRectF(self.size.width() - 56, 0, 56, 15)
        ry2_rect = QRectF(self.size.width() - 56, self.size.height() /
                          2 - 7.5, 56, 15)
        ry3_rect = QRectF(self.size.width() - 56, self.size.height() - 15,
                          56, 15)

        painter.drawText(ry1_rect, Qt.AlignLeft, str(y1))
        painter.drawText(ry2_rect, Qt.AlignLeft, str(y2))
        painter.drawText(ry3_rect, Qt.AlignLeft, str(y3))
