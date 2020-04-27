from PySide2.QtWidgets import QGraphicsView


class MainView(QGraphicsView):
    def __init__(self, scene):
        QGraphicsView.__init__(self, scene)

    def mouseMoveEvent(self, event):
        print(event.pos())
