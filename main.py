import sys

from main_window import MainWindow
from main_widget import MainWidget
from PySide2.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet("QWidget{font-size: 12px; color: rgb(226, 226, 226)}")
    #app.setStyleSheet("QPushButton{background-color: rgb(29, 29, 29)}")

    widget = MainWidget()
    window = MainWindow(widget)
    window.show()

    sys.exit(app.exec_())
