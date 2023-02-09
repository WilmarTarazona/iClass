import cv2
import base64
import numpy as np
import face_recognition
import time

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Utils.Funciones import grabar_evento
from Utils.Constantes_Eventos import *

class Camara(QThread):
    ImageUpdate = pyqtSignal(QImage)
    
    def __init__(self) -> None:
        super().__init__()
        self.active_thread = False
        self.validation = False

    def run(self):
        self.active_thread = True
        Capture = cv2.VideoCapture(0)
        faces_validation = 0
        position_eyes = [0, 0, 0, 0] # L, T, R, B
        while self.active_thread:
            ret, self.frame = Capture.read()
            if ret:
                # Send image to GUI
                Image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(1015, 1015, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)

                # Validations during exam
                if self.validation:
                    # Detects number of faces
                    if self.detect_faces() == 1:
                        faces_validation += 1
                        if faces_validation > 5:
                            grabar_evento(DESCRIPCION_EVENTO_1, time.time(), self.get_frame(), ID_EVENTO_1, DESCRIPCION_EVENTO_1)
                            faces_validation = 0
                    else:
                        faces_validation = 0
                        # Detects eyes' position
                        cx, _ = self.find_ratios(self.left_eye_roi, [self.left_l, self.left_t, self.left_r, self.left_b], self.mid)
                        _, cy = self.find_ratios(self.right_eye_roi, [self.right_l, self.right_t, self.right_r, self.right_b])
                        if cx != 0 and cy != 0:
                            if cx > -200:
                                position_eyes[0] += 1
                            elif cx < -315:
                                position_eyes[2] += 1
                            if cy < -105:
                                position_eyes[1] += 1
                            elif cy > -102:
                                position_eyes[3] += 1
                            else:
                                position_eyes = [0, 0, 0, 0] # L, T, R, B
                            if position_eyes[0] > 5:
                                grabar_evento(DESCRIPCION_EVENTO_2 + "Izquierda", time.time(), self.get_frame(), ID_EVENTO_2, DESCRIPCION_EVENTO_2 + "Izquierda")
                                position_eyes[0] = 0
                            elif position_eyes[1] > 5:
                                grabar_evento(DESCRIPCION_EVENTO_2 + "Arriba", time.time(), self.get_frame(), ID_EVENTO_2, DESCRIPCION_EVENTO_2 + "Arriba")
                                position_eyes[1] = 0
                            elif position_eyes[2] > 5:
                                grabar_evento(DESCRIPCION_EVENTO_2 + "Derecha", time.time(), self.get_frame(), ID_EVENTO_2, DESCRIPCION_EVENTO_2 + "Derecha")
                                position_eyes[2] = 0
                            elif position_eyes[3] > 5:
                                grabar_evento(DESCRIPCION_EVENTO_2 + "Abajo", time.time(), self.get_frame(), ID_EVENTO_2, DESCRIPCION_EVENTO_2 + "Abajo")
                                position_eyes[3] = 0


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

    def detect_faces(self):
        small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_landmarks_list = face_recognition.face_landmarks(rgb_small_frame)
        if len(face_landmarks_list) == 0 or len(face_landmarks_list) > 1:
            return 1
        else:
            left_eye = face_landmarks_list[0]["left_eye"]
            right_eye = face_landmarks_list[0]["right_eye"]
            self.mid = int((left_eye[1][0] + left_eye[4][0]) // 2)
            
            self.left_l, self.left_t, self.left_r, self.left_b = left_eye[0][0], left_eye[-1][1], left_eye[3][0], left_eye[2][1]
            self.left_eye_roi = small_frame[int(self.left_b * 0.95): int(self.left_t * 1.05), int(self.left_l * 0.95): int(self.left_r * 1.05)]

            self.right_l, self.right_t, self.right_r, self.right_b = right_eye[0][0], right_eye[-1][1], right_eye[3][0], right_eye[1][1]
            self.right_eye_roi = small_frame[int(self.right_b * 0.95): int(self.right_t * 1.05), int(self.right_l * 0.95): int(self.right_r * 1.05)]
            return 0
        
    def find_ratios(self, roi, eye_positions, mid=0):
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)
        _, threshold = cv2.threshold(gray_roi, 50, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)
            try:
                M = cv2.moments(contour)
                cx = int(M['m10'] / M['m00']) + mid
                cy = int(M['m01'] / M['m00'])
                x_ratio = (eye_positions[0] - cx)/(cx - eye_positions[2]) * 100
                y_ratio = (cy - eye_positions[1])/(eye_positions[3] - cy) * 100
                return x_ratio, y_ratio
            except:
                pass
        return 0, 0

    def stop(self):
        self.active_thread = False
        self.quit()