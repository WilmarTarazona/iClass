import sys
import cv2
import time
import base64
import keyboard
import pyautogui
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utils.Constantes_Eventos import *
from Utils.Funciones import grabar_evento

if sys.platform in ['Windows', 'win32', 'cygwin']:
    import win32gui
    import uiautomation as auto
elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
    from AppKit import NSWorkspace
    from Foundation import *

class Tracker(QThread):
    def __init__(self) -> None:
        super().__init__()
        self.active_thread = None
    
    def run(self) -> None:
        self.active_thread = True
        active_window_name = ""

        while self.active_thread:
            new_window_name = self.get_active_window()
            if active_window_name != new_window_name:
                if active_window_name != '':
                    if new_window_name != "Python":
                        grabar_evento(DESCRIPCION_EVENTO_3, time.time(), self.capture_window(), ID_EVENTO_3, DESCRIPCION_EVENTO_3)
                    if active_window_name == "Microsoft Word" or active_window_name == "Microsoft Excel" or active_window_name == "Microsoft PowerPoint":
                        grabar_evento(DESCRIPCION_EVENTO_4, time.time(), self.capture_window(), ID_EVENTO_4, DESCRIPCION_EVENTO_4)
                active_window_name = new_window_name
            if sys.platform in ['Windows', 'win32', 'cygwin']:
                if keyboard.is_pressed('ctrl+c') or keyboard.is_pressed('ctrl+v'):
                    grabar_evento(DESCRIPCION_EVENTO_5, time.time(), self.capture_window(), ID_EVENTO_5, DESCRIPCION_EVENTO_5)
            elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
                if keyboard.is_pressed('cmd+c') or keyboard.is_pressed('cmd+v'):
                    grabar_evento(DESCRIPCION_EVENTO_5, time.time(), self.capture_window(), ID_EVENTO_5, DESCRIPCION_EVENTO_5)

    def capture_window(self):
        window = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(window), cv2.COLOR_RGB2BGR)
        buffer = cv2.imencode('.png', image)[1]
        encoded = base64.b64encode(buffer)
        decoded = encoded.decode('utf-8')
        return decoded

    def get_active_window(self):
        if sys.platform in ['Windows', 'win32', 'cygwin']:
            window = win32gui.GetForegroundWindow()
            _active_window_name = win32gui.GetWindowText(window)
        elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
            _active_window_name = (NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName'])
        return _active_window_name
    
    def stop(self):
        self.active_thread = False
        self.quit()