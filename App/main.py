import sys

from Login import Login
from iClass import iClass
from PyQt5.QtWidgets import *

if __name__ == '__main__':
    App = QApplication(sys.argv)
    login = Login()
    if login.exec() == 1:
        main = iClass()
        main.show()
        sys.exit(App.exec())