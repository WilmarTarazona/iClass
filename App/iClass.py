import time

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utils.Camara import Camara
from Models.Alumno import alumno
from Utils.Tracker import Tracker
from Models.Programa import programa
from Utils.Constantes_iClass import *
from Utils.Funciones import grabar_evento

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

        # Tracker -> Softwares
        self.tracker = Tracker()

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

    def iniciar_examen(self) -> None:
        if time.strftime("%a, %d %b %Y %I:%M:%S %p %Z\n") > programa.data.FECHA_INICIO or time.strftime("%a, %d %b %Y %I:%M:%S %p %Z\n") < programa.data.FECHA_FIN:
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
                if estado_validacion == 0: # No detecta cara
                    QMessageBox.warning(self, 'Error', ESTADO_VALIDACION_0)
                elif estado_validacion == 1: # Cara desconocida
                    QMessageBox.warning(self, 'Error', ESTADO_VALIDACION_1)
                    grabar_evento("Validación fallida", time.time(), self.camara.get_frame(), ESTADO_VALIDACION_1)
                elif estado_validacion == 2: # Varias caras
                    QMessageBox.warning(self, 'Error', ESTADO_VALIDACION_2)
                    grabar_evento("Varios usuarios en validación", time.time(), self.camara.get_frame(), ESTADO_VALIDACION_2)
                else: # Validación correcta
                    self.examen_boton.setText(TEXTO_FINALIZAR_EXAMEN_BOTON)
                    self.examen_boton.clicked.disconnect()
                    self.examen_boton.clicked.connect(self.finalizar_examen)
                    self.camara.start_validation()
                    self.tracker.start()
    
    def finalizar_examen(self) -> None:
        self.camara.stop()
        self.tracker.stop()
        self.close()