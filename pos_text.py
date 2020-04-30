from PySide2.QtCore import Qt, QRectF
from PySide2.QtGui import QBrush, QColor, QPainter, QPen
from PySide2.QtWidgets import QGraphicsItem


class PosText(QGraphicsItem):
    def __init__(self, size, text, align):
        QGraphicsItem.__init__(self)
        self.size = size
        self.text = text
        self.align = align

    def boundingRect(self):
        return QRectF(0, 0, self.size.width(), self.size.height())

    def paint(self, painter, option, widget):
        pen = QPen(QColor(33, 150, 243))
        painter.setPen(pen)
        painter.drawRect(self.boundingRect())
        painter.fillRect(QRectF(1, 1, self.size.width()-2, self.size.height()-2), QBrush(QColor(29, 29, 29)))
        painter.drawText(0, 0, self.size.width()-4, \
            self.size.height(), self.align, self.text)

    def set_text(text):
        self.text = text
