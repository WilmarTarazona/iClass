import requests
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