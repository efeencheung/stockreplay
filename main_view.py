from PySide2.QtCore import Qt, QSizeF
from PySide2.QtGui import QColor, QPen
from PySide2.QtWidgets import QFrame, QGraphicsLineItem, QGraphicsView

from cross_line_background import CrossLineBackground
from pos_text import PosText
from price_line import PriceLine
from price_model import PriceModel
from price_yaxis import PriceYaxis
from second_yaxis import SecondYaxis
from volume_bar import VolumeBar


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
        if (x < self.width() - self.padding_h and x > self.padding_h) \
                and ((y < self.price_area_height + self.main_y
                     and y > self.main_y)
                     or (y < (self.height() - self.main_y) and
                     y > self.price_area_height + self.main_y * 2)):
            self.pos_h_line.setVisible(True)
            self.pos_v_line.setVisible(True)
            self.pos_h_line.setY(y)
            self.pos_v_line.setX(x)

            if y > self.main_y and y < self.price_area_height + self.main_y:
                self.price.setVisible(True)
                self.rov.setVisible(True)
                self.price.setY(y-7)
                self.rov.setY(y-7)

                price = round((self.price_model.max_y - (y - self.main_y) /
                               self.price_area_height *
                               self.price_model.diff_y), 2)
                rov = round((price - self.price_model.yestoday_close
                             ) / self.price_model.yestoday_close * 100, 2)
                price = "{:.2f}".format(price)
                rov = "{:.2f}%".format(rov)
                self.price.set_text(price)
                self.rov.set_text(rov)
            if y > self.price_area_height + self.main_y * 2 \
               and y < self.height() - self.main_y:
                self.vol_l.setVisible(True)
                self.vol_r.setVisible(True)
                self.vol_l.setY(y-7)
                self.vol_r.setY(y-7)
        else:
            self.pos_h_line.setVisible(False)
            self.pos_v_line.setVisible(False)
            self.price.setVisible(False)
            self.rov.setVisible(False)
            self.vol_l.setVisible(False)
            self.vol_r.setVisible(False)

    def resizeEvent(self, event):
        self.scene.setSceneRect(0, 0, self.width(), self.height())
        self.price_area_height = (self.height() - self.main_y) * 3 / 5
        self.draw()
        if self.timer_id:
            self.killTimer(self.timer_id)
            self.timer_id = 0
        self.timer_id = self.startTimer(100)

    # def timerEvent(self, event):
        # self.draw()

    def draw(self):
        self.scene.clear()

        # 画标题
        self.title = self.scene.addText('掌趣科技')
        self.title.setPos(4, 0)

        # 画补横线
        self.scene.addLine(0, self.main_y, self.padding_h,
                           self.main_y, self.gray_pen)
        self.scene.addLine(self.width()-self.padding_h,
                           self.main_y, self.width(),
                           self.main_y, self.gray_pen)
        self.scene.addLine(0, self.price_area_height + self.main_y,
                           self.padding_h, self.price_area_height +
                           self.main_y, self.gray_pen)
        self.scene.addLine(self.width() - self.padding_h,
                           self.price_area_height + self.main_y, self.width(),
                           self.price_area_height + self.main_y, self.gray_pen)

        # 画背景价格区域背景
        self.price_area_background = \
            CrossLineBackground(QSizeF(self.width() - self.padding_h * 2,
                                       self.price_area_height), self.gray_pen)
        self.price_area_background.setPos(self.padding_h, self.main_y)

        # 画价格曲线
        pen = QPen(QColor(33, 150, 243))
        self.price_line = PriceLine(QSizeF(self.width() - self.padding_h*2 - 2,
                                    self.price_area_height), pen,
                                    self.price_model)
        self.price_line.setPos(self.padding_h + 1, self.main_y)

        # 画价格区域左右Y轴
        self.price_yaxis = PriceYaxis(QSizeF(self.width(),
                                      self.price_area_height),
                                      self.price_model)
        self.price_yaxis.setPos(0, self.main_y)

        # 画游标十字线，以及左右Y轴X轴显示
        pos_pen = QPen(QColor(117, 117, 117), 1, Qt.DashDotLine)
        self.pos_h_line = QGraphicsLineItem(0, 0, self.width() -
                                            self.padding_h*2, 0)
        self.pos_h_line.setPen(pos_pen)
        self.pos_h_line.setPos(self.padding_h, self.main_y)
        self.pos_v_line = QGraphicsLineItem(0, 0, 0, self.height() -
                                            self.main_y * 2)
        self.pos_v_line.setPen(pos_pen)
        self.pos_v_line.setPos(self.padding_h, self.main_y)
        self.pos_h_line.setVisible(False)
        self.pos_v_line.setVisible(False)
        self.price = PosText(QSizeF(self.padding_h - 2, 15), str(
                             self.price_model.yestoday_close), Qt.AlignRight)
        self.price.setPos(1, (self.height()-self.main_y)*3/10-7.5)
        self.price.setVisible(False)
        self.rov = PosText(QSizeF(self.padding_h-2, 15), '0.00%', Qt.AlignLeft)
        self.rov.setPos(self.width() - self.padding_h + 1, (self.height() -
                        self.main_y)*3/10-7.5)
        self.rov.setVisible(False)
        self.vol_l = PosText(QSizeF(self.padding_h-2, 15), '0', Qt.AlignRight)
        self.vol_l.setPos(1, (self.height()-self.main_y)*3/10-7.5)
        self.vol_l.setVisible(False)
        self.vol_r = PosText(QSizeF(self.padding_h-2, 15), '0', Qt.AlignLeft)
        self.vol_r.setPos(self.width() - self.padding_h + 1, (self.height() -
                          self.main_y)*3/10-7.5)
        self.vol_r.setVisible(False)

        # 画副图区域背景
        self.second_area_background = \
            CrossLineBackground(QSizeF(self.width() - self.padding_h * 2,
                                       self.height() - self.price_area_height
                                       - self.main_y * 3), self.gray_pen, 2)
        self.second_area_background.setPos(self.padding_h, self.main_y * 2 +
                                           self.price_area_height)

        # 画副标题一
        self.title1 = self.scene.addText('成交量')
        self.title1.setPos(4, self.main_y + self.price_area_height)

        # 画副图分割线
        self.scene.addLine(0, self.main_y * 2 + self.price_area_height,
                           self.width(), self.main_y * 2 +
                           self.price_area_height, self.gray_pen)
        self.scene.addLine(0, self.height() - self.main_y,
                           self.width(), self.height() - self.main_y,
                           self.gray_pen)

        # 画副图一
        self.vol = VolumeBar(QSizeF(self.width() - self.padding_h * 2 - 2,
                             self.height() - self.price_area_height -
                             self.main_y * 3), self.price_model)
        self.vol.setPos(self.padding_h + 1, self.main_y * 2 +
                        self.price_area_height)

        # 画副图区域左右Y轴
        self.second_yaxis = SecondYaxis(QSizeF(self.width(),
                                        self.height() - self.main_y * 3 -
                                        self.price_area_height),
                                        self.price_model.max_vol, 0)
        self.second_yaxis.setPos(0, self.main_y * 2 + self.price_area_height)

        self.scene.addItem(self.price_area_background)
        self.scene.addItem(self.price_line)
        self.scene.addItem(self.price_yaxis)
        self.scene.addItem(self.second_area_background)
        self.scene.addItem(self.vol)
        self.scene.addItem(self.second_yaxis)
        self.scene.addItem(self.pos_h_line)
        self.scene.addItem(self.pos_v_line)
        self.scene.addItem(self.price)
        self.scene.addItem(self.rov)
        self.scene.addItem(self.vol_l)
        self.scene.addItem(self.vol_r)
