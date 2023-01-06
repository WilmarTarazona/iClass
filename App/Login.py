from PyQt5.QtWidgets import *
from Models.Alumno import alumno
from Utils.Constantes import URL
from collections import namedtuple
from Utils.Constantes_Login import *
from Utils.Solicitudes import solicitud

class Login(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(TEXTO_TITULO_VENTANA)
        self.resize(ANCHO_VENTANA, ALTO_VENTANA)
        self.componentes_visuales()
    
    def componentes_visuales(self) -> None:
        layout = QGridLayout()

        # Usuario -> Label & Input
        usuario_label = QLabel('Usuario')
        layout.addWidget(usuario_label, 0, 0)
        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText('Ingresar usuario')
        layout.addWidget(self.usuario_input, 0, 1)

        # Contraseña -> Label & Input
        contra_label = QLabel('Contraseña')
        layout.addWidget(contra_label, 1, 0)
        self.contra_input = QLineEdit()
        self.contra_input.setPlaceholderText('Ingresar contraseña')
        layout.addWidget(self.contra_input, 1, 1)

        # Iniciar Sesión -> Botón
        iniciarSesion_boton = QPushButton('Iniciar Sesión')
        iniciarSesion_boton.clicked.connect(self.validar_usuario)
        layout.addWidget(iniciarSesion_boton, 3, 0, 1, 2)

        self.setLayout(layout)

    def validar_usuario(self):
        json = {'USUARIO': self.usuario_input.text(),
                'PASSWORD_ALUMNO': self.contra_input.text()}
        url = URL + '/alumno'
        estado, respuesta = solicitud("POST", url, json, 10)
        if estado:
            diccionario = respuesta['datos']
            alumno.data = namedtuple("Alumno", diccionario.keys())(*diccionario.values())
            QMessageBox.information(self, 'Exito', "Bienvenido '{0}'".format(alumno.data.NOMBRE_ALUMNO))
            alumno.programa.obtener_data(alumno.data.ID_PROGRAMA)
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', respuesta['mensaje'])

# asdsadas
# dasdsa