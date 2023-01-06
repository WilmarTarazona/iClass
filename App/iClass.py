import time

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utils.Camara import Camara
from Models.Alumno import alumno
from Utils.Constantes_iClass import *

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

    def iniciar_examen(self) -> None:
        print(time.strftime("%a, %d %b %Y %I:%M:%S %p %Z\n"))
        # AÑADIR VALIDACIÓN DE TIEMPOS

        instrucciones = QMessageBox(self)
        instrucciones.setText(TEXTO_INICIO_EXAMEN)
        instrucciones.setInformativeText(TEXTO_INSTRUCCIONES_INICIO_EXAMEN)
        instrucciones.setStandardButtons(QMessageBox.Ok)
        instrucciones.setBaseSize(400, 150)
        instrucciones_valor = instrucciones.exec()
        if instrucciones_valor == QMessageBox.Ok:
            if not self.validar_usuario():
                # SE HA DETECTADO USUARIO NO RECONOCIDO LA INCIDENCIA SE MANDARÁ AL SUPERVISOR
                # SE HA DETECTADO MÁS DE UNA PERSONA EN LA VISIÓN DE LA CÁMARA LA INCIDENCIA SE MANDARÁ AL SUPERVISOR
                pass
            self.examen_boton.setText(TEXTO_FINALIZAR_EXAMEN_BOTON)
    
    def validar_usuario(self) -> bool:
        """
        IMPLEMENTAR COMPARACIÓN ENTRE FOTO DE BD Y CAMARA
        """
        return True