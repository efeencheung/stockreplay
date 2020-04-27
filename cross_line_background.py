from PySide2.QtCore import QRectF
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QGraphicsItem

class CrossLineBackground(QGraphicsItem):
    def __init__(self, size, pen):
        QGraphicsItem.__init__(self)
        self.size = size
        self.pen = pen
        self.pen.setCosmetic(True)

    def boundingRect(self):
        return QRectF(0, 0, self.size.width(), self.size.height())
    
    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.drawRect(0, 0, self.size.width(), self.size.height())
        painter.drawLine(0, self.size.height() / 4, self.size.width(), \
            self.size.height() / 4)
        painter.drawLine(0, self.size.height() / 2, self.size.width(), \
            self.size.height() / 2)
        painter.drawLine(0, self.size.height() * 3 / 4, self.size.width(), \
            self.size.height() * 3 / 4)
        painter.drawLine((self.size.width()) / 4, 0, self.size.width() / 4, \
            self.size.height())
        painter.drawLine((self.size.width()) / 2, 0, self.size.width() / 2, \
            self.size.height())
        painter.drawLine((self.size.width()) * 3 / 4, 0, self.size.width() * 3 / 4, \
            self.size.height())
