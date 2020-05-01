from PySide2.QtCore import Qt, QSizeF
from PySide2.QtGui import QColor, QPen
from PySide2.QtWidgets import QFrame, QGraphicsLineItem, \
    QGraphicsTextItem, QGraphicsView

from cross_line_background import CrossLineBackground
from pos_text import PosText
from price_line import PriceLine
from price_model import PriceModel
from price_yaxis import PriceYaxis


class MainView(QGraphicsView):
    def __init__(self, scene):
        QGraphicsView.__init__(self, scene)
        self.setMouseTracking(True)
        self.setFrameShape(QFrame.NoFrame)
        self.padding_h = 60
        self.main_y = 25
        self.scene = scene
        self.gray_pen = QPen(QColor(224, 224, 224), 1)
        self.timer_id = 0
        self.price_model = PriceModel()

    def mouseMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if x < self.width() - self.padding_h and x > self.padding_h \
            and y < self.price_area_height+self.main_y \
            and y > self.main_y:
            self.pos_h_line.setVisible(True)
            self.pos_v_line.setVisible(True)
            self.pos_h_line.setY(y)
            self.pos_v_line.setX(x)
            self.price.setVisible(True)
            self.rov.setVisible(True)
            self.price.setY(y-7)
            self.rov.setY(y-7)

            price = round((self.price_model.max_y - (y-self.main_y)/\
                self.price_area_height*self.price_model.diff_y), 2)
            rov = round((price-self.price_model.yestoday_close)/self.price_model.yestoday_close*100, 2)
            price = "{:.2f}".format(price)
            rov = "{:.2f}%".format(rov)
            self.price.set_text(price)
            self.rov.set_text(rov)
        else: 
            self.pos_h_line.setVisible(False)
            self.pos_v_line.setVisible(False)
            self.price.setVisible(False)
            self.rov.setVisible(False)

    def resizeEvent(self, event):
        self.scene.setSceneRect(0, 0, self.width(), self.height())
        self.price_area_height = (self.height() - self.main_y) * 3 / 5
        self.draw()
        if self.timer_id:
            self.killTimer(self.timer_id)
            self.timer_id = 0
        self.timer_id = self.startTimer(100)

    #def timerEvent(self, event):
        #self.draw()

    def draw(self):
        self.scene.clear()
        self.scene.addLine(0, self.main_y, self.padding_h, \
            self.main_y, self.gray_pen)
        self.scene.addLine(self.width()-self.padding_h, \
            self.main_y, self.width(), self.main_y, self.gray_pen)
        self.scene.addLine(0, self.price_area_height+self.main_y, \
            self.padding_h, self.price_area_height+self.main_y, \
            self.gray_pen)
        self.scene.addLine(self.width()-self.padding_h, \
            self.price_area_height+self.main_y, self.width(), \
            self.price_area_height+self.main_y, self.gray_pen)

        self.cross_line_background = CrossLineBackground(\
            QSizeF(self.width()-self.padding_h*2, \
            self.price_area_height), self.gray_pen)
        self.cross_line_background.setPos(60, self.main_y)

        pen = QPen(QColor(33, 150, 243))
        self.price_line = PriceLine(\
            QSizeF(self.width()-self.padding_h*2, \
            self.price_area_height), pen, self.price_model)
        self.price_line.setPos(self.padding_h, self.main_y)

        self.yaxis = PriceYaxis(QSizeF(self.width(), \
            self.price_area_height), self.price_model)
        self.yaxis.setPos(0, self.main_y)

        pos_pen = QPen(QColor(117, 117, 117), 1, Qt.DashDotLine)
        self.pos_h_line = QGraphicsLineItem(0, 0, self.width()-self.padding_h*2, 0)
        self.pos_h_line.setPen(pos_pen)
        self.pos_h_line.setPos(self.padding_h, self.main_y)
        self.pos_v_line = QGraphicsLineItem(0, 0, 0, self.price_area_height)
        self.pos_v_line.setPen(pos_pen)
        self.pos_v_line.setPos(self.padding_h, self.main_y)
        self.pos_h_line.setVisible(False)
        self.pos_v_line.setVisible(False)

        self.price = PosText(QSizeF(self.padding_h-2, 15), \
            str(self.price_model.yestoday_close), Qt.AlignRight)
        self.price.setPos(1, (self.height()-self.main_y)*3/10-7.5)
        self.price.setVisible(False)
        self.rov = PosText(QSizeF(self.padding_h-2, 15), \
            '0.00%', Qt.AlignLeft)
        self.rov.setPos(self.width()-self.padding_h+1, (self.height()-self.main_y)*3/10-7.5)
        self.rov.setVisible(False)

        self.title = self.scene.addText('掌趣科技')
        self.title.setPos(4, 0)

        self.scene.addItem(self.cross_line_background)
        self.scene.addItem(self.pos_h_line)
        self.scene.addItem(self.pos_v_line)
        self.scene.addItem(self.price_line)
        self.scene.addItem(self.yaxis)
        self.scene.addItem(self.price)
        self.scene.addItem(self.rov)
