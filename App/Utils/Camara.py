import cv2
import base64

from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Camara(QThread):
    ImageUpdate = pyqtSignal(QImage)
    
    def __init__(self) -> None:
        super().__init__()
        self.hilo_activo = None
    
    def run(self):
        self.hilo_activo = True
        Capture = cv2.VideoCapture(0)
        while self.hilo_activo:
            ret, self.frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)

                Pic = ConvertToQtFormat.scaled(1015, 1015, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)

    def get_frame(self):
        buffer = cv2.imencode('.png', self.frame)[1]
        encoded = base64.b64encode(buffer)
        decoded = encoded.decode('utf-8')
        return decoded
    
    def stop(self):
        self.hilo_activo = False
        self.quit()