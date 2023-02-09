import requests
import time

from Utils.Constantes import *
from Models.Alumno import alumno
from requests.exceptions import Timeout

def solicitud(method: str, url: str, json: dict = None, timeout: int = None) -> tuple:
    if method == "GET":
        try:
            r = requests.get(url, timeout=timeout).json()
            if r['exito']:
                return True, r
            else:
                return False, r
        except Timeout:
            return False, {'mensaje': "Error con el servicio web"}
    if method == "POST":
        try:
            r = requests.post(url, json=json, timeout=timeout).json()
            if r['exito']:
                return True, r
            else:
                return False, r
        except Timeout:
            return False, {'mensaje': "Error con el servicio web"}
    if method == "PUT":
        try:
            r = requests.put(url, timeout=timeout).json()
            if r['exito']:
                return True, r
            else:
                return False, r
        except Timeout:
            return False, {'mensaje': "Error con el servicio web"}

def grabar_evento(descripcion_evento: str, tiempo: float, prueba: str, id_evento: str, aviso: str) -> bool:
    json = {"ID_PROGRAMA": alumno.data.ID_PROGRAMA,
            "NOMBRE_ESTUDIANTE": alumno.data.NOMBRE_ALUMNO,
            "APELLIDO_ESTUDIANTE": alumno.data.APELLIDO_PATERNO_ALUMNO,
            "DESCRIPCION_EVENTO": descripcion_evento,
            "HORA_EVENTO": time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(tiempo)),
            "CAPTURA_PRUEBA": prueba,
            "ID_EVENTO": id_evento,
            "AVISO_USUARIO": aviso,
            "ID_INSTITUCION": alumno.programa.data.ID_INSTITUCION,
            "ID_ALUMNO": alumno.data.ID_ALUMNO}
    estado, _ = solicitud("POST", URL + '/evento', json)
    if estado:
        return True
    else:
        return False