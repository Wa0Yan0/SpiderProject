from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication


class MainUi:
    def __init__(self):
        qFile = QFile("ui/spider.ui")
        qFile.open(QFile.ReadOnly)
        qFile.close()
        self.ui = QUiLoader().load(qFile)
        self.ui.rentButton.clicked.connect(self.spider_rent)

    def spider_rent(self):
        print('111111111')

def main():
    app = QApplication([])
    gui = MainUi()
    gui.ui.show()
    app.exec_()


if __name__ == '__main__':
    main()
