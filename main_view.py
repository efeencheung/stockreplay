from PySide2.QtCore import Qt, QSizeF
from PySide2.QtGui import QColor, QPen
from PySide2.QtWidgets import QGraphicsLineItem, QGraphicsTextItem, QGraphicsView

from cross_line_background import CrossLineBackground
from pos_text import PosText
from price_line import PriceLine
from price_model import PriceModel
from price_yaxis import PriceYaxis


class MainView(QGraphicsView):
    def __init__(self, scene):
        QGraphicsView.__init__(self, scene)
        self.padding_h = 60
        self.scene = scene
        self.gray_pen = QPen(QColor(255, 255, 255, 17.75), 1)
        self.timer_id = 0

    def mouseMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if x < self.width() - self.padding_h and x > self.padding_h and y < self.height()*3/5:
            self.pos_h_line.setVisible(True)
            self.pos_v_line.setVisible(True)
            self.pos_h_line.setY(y)
            self.pos_v_line.setX(x)
            self.price.setVisible(True)
            self.price.setY(y-7)
        else: 
            self.pos_h_line.setVisible(False)
            self.pos_v_line.setVisible(False)
            self.price.setVisible(False)

    def resizeEvent(self, event):
        self.scene.setSceneRect(0, 0, self.width(), self.height())
        self.draw()
        if self.timer_id:
            self.killTimer(self.timer_id)
            self.timer_id = 0
        self.timer_id = self.startTimer(100)

    #def timerEvent(self, event):
        #self.draw()

    def draw(self):
        self.price_model = PriceModel()
        self.scene.clear()
        self.scene.addLine(0, 0, self.padding_h, 0, self.gray_pen)
        self.scene.addLine(self.width()-self.padding_h, \
            0, self.width(), 0, self.gray_pen)
        self.scene.addLine(0, self.height()*3/5, self.padding_h,\
            self.height()*3/5, self.gray_pen)
        self.scene.addLine(self.width()-self.padding_h, \
            self.height()*3/5, self.width(), self.height()*3/5, self.gray_pen)

        self.cross_line_background = CrossLineBackground(\
            QSizeF(self.width()-self.padding_h*2, \
            self.height()*3/5), self.gray_pen)
        self.cross_line_background.setPos(60, 0)

        pen = QPen(QColor(33, 150, 243))
        self.price_line = PriceLine(\
            QSizeF(self.width()-self.padding_h*2, \
            self.height()*3/5), pen, price_model)
        self.price_line.setPos(self.padding_h, 0)

        self.left_yaxis = PriceYaxis(QSizeF(self.width(), \
            self.height()*3/5), price_model)

        pos_pen = QPen(Qt.white, 1, Qt.DashDotLine)
        self.pos_h_line = QGraphicsLineItem(0, 0, self.width()-self.padding_h*2, 0)
        self.pos_h_line.setPen(pos_pen)
        self.pos_h_line.setPos(self.padding_h, 0)
        self.pos_v_line = QGraphicsLineItem(0, 0, 0, self.height()*3/5)
        self.pos_v_line.setPen(pos_pen)
        self.pos_v_line.setPos(self.padding_h, 0)
        self.pos_h_line.setVisible(False)
        self.pos_v_line.setVisible(False)

        self.price = PosText(QSizeF(self.padding_h-2, 14), \
            str(price_model.yestoday_close), Qt.AlignRight)
        self.price.setPos(1, self.height()*3/10-7.5)
        self.price.setVisible(False)

        self.scene.addItem(self.cross_line_background)
        self.scene.addItem(self.pos_h_line)
        self.scene.addItem(self.pos_v_line)
        self.scene.addItem(self.price_line)
        self.scene.addItem(self.left_yaxis)
        self.scene.addItem(self.price)
