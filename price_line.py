from PySide2.QtCore import QRectF
from PySide2.QtGui import QPainter, QPainterPath
from PySide2.QtWidgets import QGraphicsItem


class PriceLine(QGraphicsItem):
    def __init__(self, size, pen, price_model):
        QGraphicsItem.__init__(self)
        self.size = size
        self.pen = pen
        self.price_model = price_model
        self.data = self.price_model.data

    def boundingRect(self):
        return QRectF(0, 0, self.size.width(), self.size.height())

    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        for i in range(len(self.data)):
            (x, y) = self.to_point(self.data[i][0], self.data[i][1])
            if i == 0:
                path.moveTo(0, y)
                continue
            path.lineTo(x, y)

        painter.drawPath(path)

    def to_point(self, ox, oy):
        y = (self.price_model.max_y - oy) * self.size.height() /\
            self.price_model.diff_y
        x = (ox - self.price_model.min_x) * self.size.width() /\
            self.price_model.diff_x

        return (x, y)
