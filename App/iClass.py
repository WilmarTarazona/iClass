import time

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utils.Camara import Camara
from Models.Alumno import alumno
from Utils.Constantes_iClass import *
from Utils.Solicitudes import solicitud

class iClass(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(TEXTO_TITULO_VENTANA)
        self.resize(ANCHO_VENTANA, ALTO_VENTANA)
        self.componentes_visuales()
        self.componentes_funcionales()
    
    def componentes_visuales(self) -> None:
        widget = QWidget(self)
        self.layout_gui = QGridLayout()

        # Camara -> Label
        self.video_label = QLabel()
        self.video_label.setStyleSheet("border : solid black;" "border-width : 20px 1px 20px 1px;")
        self.layout_gui.addWidget(self.video_label, 0, 0, 8, 1)

        # Fecha y hora -> Label
        self.fecha_hora_label = QLabel()
        self.fecha_hora_label.setFont(QFont('Arial', 50, QFont.Bold))
        self.layout_gui.addWidget(self.fecha_hora_label, 0, 1)

        # Controlar examen -> Botón
        self.examen_boton = QPushButton(TEXTO_INICIAR_EXAMEN_BOTON)
        self.examen_boton.clicked.connect(self.iniciar_examen)
        self.examen_boton.setFixedWidth(250)
        self.layout_gui.addWidget(self.examen_boton, 1, 1)

        self.setMenuWidget(widget)
        widget.setLayout(self.layout_gui)
    
    def componentes_funcionales(self) -> None:
        # Camara -> Image
        self.camara = Camara()
        self.camara.start()
        self.camara.ImageUpdate.connect(self.ImageUpdateSlot)

        # Timer 1 segundo
        timer_1s = QTimer(self)
        timer_1s.timeout.connect(self.timer_1s)
        timer_1s.start(1000)

    def ImageUpdateSlot(self, Image) -> None:
        self.video_label.setPixmap(QPixmap.fromImage(Image))

    def timer_1s(self) -> None:
        self.mostrar_fecha_hora()
    
    def mostrar_fecha_hora(self) -> None:
        self.fecha_hora_label.setText(QDateTime.currentDateTime().toString('dd/MM/yyyy \n hh:mm:ss'))
    
    def grabar_evento(self, descripcion_evento: str, tiempo: float, prueba: str, aviso: str) -> bool:
        json = {"ID_PROGRAMA": alumno.data.ID_PROGRAMA,
                "NOMBRE_ESTUDIANTE": alumno.data.NOMBRE_ESTUDIANTE,
                "APELLIDO_ESTUDIANTE": alumno.data.APELLIDO_ESTUDIANTE,
                "DESCRIPCION_EVENTO": descripcion_evento,
                "HORA_EVENTO": time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(tiempo)),
                "CAPTURA_PRUEBA": prueba,
                "ID_EVENTO": None,
                "AVISO_USUARIO": aviso,
                "ID_INSTITUCION": alumno.programa.data.ID_INSTITUCION,
                "ID_ALUMNO": alumno.data.ID_ALUMNO}
        estado, _ = solicitud("POST", URL + '/evento', json)
        if estado:
            return True
        else:
            return False

    def iniciar_examen(self) -> None:
        if time.strftime("%a, %d %b %Y %I:%M:%S %p %Z\n") > alumno.programa.data.FECHA_INICIO or time.strftime("%a, %d %b %Y %I:%M:%S %p %Z\n") < alumno.programa.data.FECHA_FIN:
            QMessageBox.warning(self, 'Error', 'No está dentro de la hora programada del examen')
        else:
            instrucciones = QMessageBox(self)
            instrucciones.setText(TEXTO_INICIO_EXAMEN)
            instrucciones.setInformativeText(TEXTO_INSTRUCCIONES_INICIO_EXAMEN)
            instrucciones.setStandardButtons(QMessageBox.Ok)
            instrucciones.setBaseSize(400, 150)
            instrucciones_valor = instrucciones.exec()
            if instrucciones_valor == QMessageBox.Ok:
                estado_validacion = self.camara.compare_faces(alumno.data.FOTO_ALUMNO)
                if estado_validacion == 0:
                    QMessageBox.warning(self, 'Error', 'No se ha detectado personas en cámara')
                elif estado_validacion == 1:
                    QMessageBox.warning(self, 'Error', 'Usuario no reconocido, la incidencia se mandará al supervisor')
                    self.grabar_evento("Usuario no reconocido en validación", time.time(), self.camara.get_frame(), "Usuario no reconocido, la incidencia se mandará al supervisor")
                elif estado_validacion == 2:
                    QMessageBox.warning(self, 'Error', 'Más de una persona en cámara, la incidencia se mandará al supervisor')
                    self.grabar_evento("Varios usuarios en validación", time.time(), self.camara.get_frame(), "Usuario no reconocido, la incidencia se mandará al supervisor")
                else:
                    self.examen_boton.setText(TEXTO_FINALIZAR_EXAMEN_BOTON)
                    self.examen_boton.clicked.disconnect()
                    self.examen_boton.clicked.connect(self.finalizar_examen)
    
    def finalizar_examen(self) -> None:
        self.close()