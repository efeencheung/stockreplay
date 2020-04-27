from PySide2.QtCore import Qt, QRectF
from PySide2.QtGui import QPainter, QPen
from PySide2.QtWidgets import QGraphicsItem


class PosText(QGraphicsItem):
    def __init__(self, size):
        QGraphicsItem.__init__(self)
        self.size = size
        self.pen = QPen(Qt.white, 1, Qt.DashDotLine)

    def boundingRect(self):
        return QRectF(0, 0, self.size.width(), self.size.height())
    

    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        self.h_line = painter.drawLine(0, 0, self.size.width(), 0)
        self.v_line = painter.drawLine(0, 0, 0, self.size.height())
