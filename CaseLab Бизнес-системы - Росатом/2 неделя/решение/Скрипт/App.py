import sys
from pathlib import Path

from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget
from Tabs import *


class App(QMainWindow):
    """ Приложение """

    def __init__(self):
        super(App, self).__init__()

        # region Window Params

        self.setWindowTitle("Title")
        self.setGeometry(300, 100, 800, 600)

        # endregion

        # region Tab View

        self.tab_view = TabView(self)
        self.setCentralWidget(self.tab_view)

        # endregion

        self.setStyleSheet(Path('Styles/stylesheet.qss').read_text())

        self.show()


class TabView(QWidget):
    """
    Окно вкладок

    :param self.tab1 Вкладка «Срочный займ»\n
    :param self.tab2 Вкладка «Займ с изменением процентной ставки»\n
    :param self.tab3 Вкладка «Займ с досрочным гашением»
    """

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        # region Tabs

        self.tab_view = QTabWidget()
        self.tab1 = Tab1(self)
        self.tab2 = Tab2(self)
        self.tab3 = Tab3(self)

        # endregion

        # region Adding Tabs

        self.tab_view.addTab(self.tab1, "Займ 1")
        self.tab_view.addTab(self.tab2, "Займ 2")
        self.tab_view.addTab(self.tab3, "Займ 3")

        # endregion

        # region Grid Layout

        self.grid = QGridLayout()
        self.grid.addWidget(self.tab_view)
        self.setLayout(self.grid)

        # endregion


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
