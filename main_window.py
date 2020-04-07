from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QMainWindow, QAction


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("掌趣科技")
        self.setCentralWidget(widget)

        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("文件")
        exit_action = QAction("退出", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

        self.setMinimumSize(600, 400)
