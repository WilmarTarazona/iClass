import sys
import time

from Login import Login
from iClass import iClass
from PyQt5.QtWidgets import *
from Utils.Constantes_Eventos import *
from Utils.Funciones import grabar_evento

def quit_signal():
    grabar_evento(DESCRIPCION_EVENTO_6, time.time(), None, ID_EVENTO_6, DESCRIPCION_EVENTO_6)

if __name__ == '__main__':
    App = QApplication(sys.argv)
    App.aboutToQuit.connect(quit_signal)
    login = Login()
    if login.exec() == 1:
        main = iClass()
        main.show()
        sys.exit(App.exec())