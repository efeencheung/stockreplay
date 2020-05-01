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
        painter.fillRect(QRectF(1, 1, self.size.width()-1, self.size.height()-1), QBrush(Qt.white))
        painter.drawText(3, 0, self.size.width()-6, \
            self.size.height(), self.align, self.text)

    def set_text(self, text):
        self.text = text
