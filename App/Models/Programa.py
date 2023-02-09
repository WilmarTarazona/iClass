from Utils.Funciones import solicitud
from collections import namedtuple
from Utils.Constantes import URL

class Programa():
    def __init__(self) -> None:
        self.data = None
    
    def obtener_data(self, id_programa) -> None:
        estado, respuesta = solicitud("GET", URL + '/programa/{0}'.format(id_programa))
        if estado:
            diccionario = respuesta['datos']
            self.data = namedtuple("Programa", diccionario.keys())(*diccionario.values())

programa = Programa()