from PySide2.QtCore import QRectF, Qt
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
        gray_pen = QPen(QColor(117, 117, 117))
        green_pen = QPen(QColor(25, 183, 83))

        ly1 = self.price_model.max_y
        ly2 = (self.price_model.max_y + self.price_model.yestoday_close) / 2
        ly2 = "{:.2f}".format(ly2)
        ly3 = self.price_model.yestoday_close
        ly4 = (self.price_model.yestoday_close + self.price_model.min_y) / 2
        ly4 = "{:.2f}".format(ly4)
        ly5 = self.price_model.min_y

        ly1_rect = QRectF(0, 0, 56, 15)
        ly2_rect = QRectF(0, self.size.height()/4-7.5, 56, 15)
        ly3_rect = QRectF(0, self.size.height()/2-7.5, 56, 15)
        ly4_rect = QRectF(0, self.size.height()*3/4-7.5, 56, 15)
        ly5_rect = QRectF(0, self.size.height()-15, 56, 15)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(red_pen)
        painter.drawText(ly1_rect, Qt.AlignRight, str(ly1))
        painter.drawText(ly2_rect, Qt.AlignRight, str(ly2))
        painter.setPen(gray_pen)
        painter.drawText(ly3_rect, Qt.AlignRight, str(ly3))
        painter.setPen(green_pen)
        painter.drawText(ly4_rect, Qt.AlignRight, str(ly4))
        painter.drawText(ly5_rect, Qt.AlignRight, str(ly5))

        max_percent = round((self.price_model.max_y-self.price_model.yestoday_close)/self.price_model.yestoday_close*100, 2)
        ry1 = str(max_percent) + '%'
        ry2 = str(round(max_percent/2, 2)) + '%'
        ry3 = '0.00%'
        ry4 = '-' + ry2
        ry5 = '-' + ry1

        ry1_rect = QRectF(self.size.width()-56, 0, 56, 15)
        ry2_rect = QRectF(self.size.width()-56, self.size.height()/4-7.5, 56, 15)
        ry3_rect = QRectF(self.size.width()-56, self.size.height()/2-7.5, 56, 15)
        ry4_rect = QRectF(self.size.width()-56, self.size.height()*3/4-7.5, 56, 15)
        ry5_rect = QRectF(self.size.width()-56, self.size.height()-15, 56, 15)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(red_pen)
        painter.drawText(ry1_rect, Qt.AlignLeft, str(ry1))
        painter.drawText(ry2_rect, Qt.AlignLeft, str(ry2))
        painter.setPen(gray_pen)
        painter.drawText(ry3_rect, Qt.AlignLeft, str(ry3))
        painter.setPen(green_pen)
        painter.drawText(ry4_rect, Qt.AlignLeft, str(ry4))
        painter.drawText(ry5_rect, Qt.AlignLeft, str(ry5))
