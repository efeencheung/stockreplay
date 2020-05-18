from PySide2.QtCore import QRectF


class PlotArea:
    def __init__(self, size):
        self.size = size
        self.serieses = []
        self.max_y = 0
        self.min_y = 0
        self.bg_type = 1

    def add_series(self, series):
        self.serieses.append(series)

    def set_max_y(self, max_y):
        self.max_y = max_y

    def set_min_y(self, min_y):
        self.min_y = min_y

    def set_bg_type(self, bg_type):
        self.bg_type = bg_type

    def boundingRect(self):
        return QRectF(0, 0, self.w(), self.h())

    def w(self):
        return self.w()

    def h(self):
        return self.h()

    def paint(self, painter, option, widget):
        # 画背景
        painter.setPen(self.grey_pen)
        painter.drawRect(0, 0, self.w(), self.h())
        painter.drawLine(0, self.h() / 2, self.w(), self.h() / 2)
        painter.drawLine((self.w()) / 2, 0, self.w() / 2, self.h())
        painter.drawLine((self.w()) / 4, 0, self.w() / 4, self.h())
        painter.drawLine((self.w()) * 3 / 4, 0, self.w() * 3 / 4, self.h())
        if self.type == 1:
            painter.drawLine(0, self.h() / 4, self.w(), self.h() / 4)
            painter.drawLine(0, self.h() * 3 / 4, self.w(), self.h() * 3 / 4)
