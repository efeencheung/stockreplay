from PySide2.QtCore import QRectF
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QGraphicsItem


class PriceLine(QGraphicsItem):
    def __init__(self, size, pen):
        QGraphicsItem.__init__(self)
        self.size = size
        self.pen = pen

    def boundingRect(self):
        return QRectF(0, 0, self.size.width(), self.size.height())
    

    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.setRenderHint(QPainter.Antialiasing)
