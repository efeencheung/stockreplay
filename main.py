import sys

from main_window import MainWindow
from main_view import MainView
from PySide2.QtWidgets import QApplication, QGraphicsScene

if __name__ == "__main__":
    app = QApplication([])
    #app.setStyleSheet("QWidget{font-size: 12px; color: rgb(226, 226, 226)}")

    scene = QGraphicsScene()
    view = MainView(scene)
    window = MainWindow(view)
    window.show()

    sys.exit(app.exec_())
