import cv2
import base64
import numpy as np
import face_recognition

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

    def compare_faces(self, photo):
        rgb_frame = self.frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        if len(face_locations) == 0:
            return 0
        elif len(face_locations) > 1:
            return 2
        face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)

        decoded = base64.b64decode(photo)
        np_data = np.frombuffer(decoded, np.uint8)
        img = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
        bd_encoding = face_recognition.face_encodings(img)[0]

        matches = face_recognition.compare_faces(bd_encoding, face_encoding)
        if matches:
            return 3
        else:
            return 1

    def stop(self):
        self.hilo_activo = False
        self.quit()