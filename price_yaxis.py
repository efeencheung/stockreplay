from PySide2.QtCore import QRect, QRectF, Qt
from PySide2.QtGui import QColor, QPainter, QPainterPath, QPen
from PySide2.QtWidgets import QGraphicsItem
from price_model import PriceModel


class PriceYaxis(QGraphicsItem):
    def __init__(self, size, price_model):
        QGraphicsItem.__init__(self)
        self.size = size
        self.price_model = PriceModel()
        self.data = self.price_model.data

    def boundingRect(self):
        return QRectF(0, 0, self.size.width(), self.size.height())
    

    def paint(self, painter, option, widget):
        red_pen = QPen(QColor(255, 23, 24))
        gray_pen = QPen(QColor(189, 189, 189))
        green_pen = QPen(QColor(25, 183, 83))

        ly1 = self.price_model.max_y
        ly2 = (self.price_model.max_y + self.price_model.yestoday_close) / 2
        ly2 = "{:.2f}".format(ly2)
        ly3 = self.price_model.yestoday_close
        ly4 = (self.price_model.yestoday_close + self.price_model.min_y) / 2
        ly4 = "{:.2f}".format(ly4)
        ly5 = self.price_model.min_y

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(red_pen)
        ly1_rect = QRect(0, 0, 60, 16)
        painter.drawText(ly1_rect, Qt.AlignRight, str(ly1))
        ly2_rect = QRect(0, self.size.height()/4-8, 60, 16)
        painter.drawText(ly2_rect, Qt.AlignRight, str(ly2))
        painter.setPen(gray_pen)
        ly3_rect = QRect(0, self.size.height()/2-8, 60, 16)
        painter.drawText(ly3_rect, Qt.AlignRight, str(ly3))
        painter.setPen(green_pen)
        ly4_rect = QRect(0, self.size.height()*3/4-8, 60, 16)
        painter.drawText(ly4_rect, Qt.AlignRight, str(ly4))
        ly5_rect = QRect(0, self.size.height()-16, 60, 16)
        painter.drawText(ly5_rect, Qt.AlignRight, str(ly5))

