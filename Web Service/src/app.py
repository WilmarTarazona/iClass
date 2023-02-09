import oracledb
from flask import Flask, jsonify, request

oracledb.defaults.fetch_lobs = False

app = Flask(__name__)

def establecer_conexion():
    """
    Establece conexión con base de datos
    """
    # IMPORTANTE: Es recomendable que los siguientes valores se establezcan como variables de ambiente, y se recuperen de esa manera
    conexion = oracledb.connect(user="GINNET01", password="Ginnet2022.1", dsn="bdgn.ddns.net:1521/bdginnet", encoding="UTF-8")
    return conexion

@app.route('/')
def indice():
    """
    Muestra mensaje de bienvenida en página principal
    """
    return("iClassAPI")

@app.route('/alumno', methods=["POST"])
def validar_credenciales() -> jsonify:
    """
    Validar datos(usuario y contraseña) para inicio de sesión
    """
    try:
        conexion = establecer_conexion()
    except:
        return jsonify({'error': conexion, 'mensaje': "Error conectando a la base de datos", 'exito': False})
    
    try:
        data = request.get_json()
        if data.get("USUARIO") == '' or data.get("PASSWORD_ALUMNO") == '':
            return jsonify({'mensaje': "Datos incompletos", 'exito': False})
        with conexion.cursor() as cursor:
            estudiante = None
            cursor.callproc('DOC_SDEL.ALUMNO_MOSTRAR', [data.get("USUARIO"), data.get("PASSWORD_ALUMNO")])
            for results in cursor.getimplicitresults():
                for row in results:
                    estudiante = {'ID_ALUMNO': row[0],
                                  'ID_PROGRAMA': row[1],
                                  'NOMBRE_ALUMNO': row[2],
                                  'APELLIDO_PATERNO_ALUMNO': row[3],
                                  'APELLIDO_MATERNO_ALUMNO': row[4],
                                  'DNI_ALUMNO': row[5],
                                  'URL_FOTO_ALUMNO': row[6],
                                  'CORREO_ALUMNO': row[7],
                                  'FOTO_ALUMNO': row[8].decode('utf-8'),
                                  'USUARIO': row[9],
                                  'PASSWORD_ALUMNO': row[10],
                                  'ASISTENCIA': row[11]}
            if estudiante:
                return jsonify({'datos': estudiante, 'mensaje': "Ok", 'exito': True})
            else:
                return jsonify({'mensaje': "Datos incorrectos", 'exito': False})
    except Exception as e:
        print(e)
        return jsonify({'mensaje': "Error en el procedimiento", 'exito': False})

@app.route('/alumno/imagen', methods=['PUT'])
def actualizar_alumno_imagen() -> jsonify:
    """
    Actualizar imagen y estado de asistencia de alumno
    """
    try:
        conexion = establecer_conexion()
    except:
        return jsonify({'error': conexion, 'mensaje': "Error conectando a la base de datos", 'exito': False})

    try:
        with conexion.cursor() as cursor:
            cursor.callproc('DOC_SDEL.ALUMNO_FOTO_ACTUALIZAR', list(request.json.values()))
            conexion.commit()
            return jsonify({'mensaje': "Ok", 'exito': True})
    except Exception as e:
        print(e)
        return jsonify({'mensaje': "Error al actualizar imagen", 'exito': False})

@app.route('/evento', methods=['POST'])
def grabar_evento() -> jsonify:
    """
    Crea evento
    """
    try:
        conexion = establecer_conexion()
    except Exception as e:
        return jsonify({'error': e, 'mensaje': "Error conectando a la base de datos", 'exito': False})

    try:
        with conexion.cursor() as cursor:
            cursor.callproc('DOC_SDEL.BITACORA_EVENTOS_GRABAR', list(request.json.values()))
            conexion.commit()
            return jsonify({'mensaje': "Ok", 'exito': True})
    except Exception as e:
        print(e)
        return jsonify({'mensaje': "Error al grabar evento", 'exito': False})

@app.route('/programa/<ID_PROGRAMA>', methods=['GET'])
def listar_programa(ID_PROGRAMA: str) -> jsonify:
    """
    Lista datos de la tabla programa
    """
    try:
        conexion = establecer_conexion()
    except Exception:
        return jsonify({'error': conexion, 'mensaje': "Error conectando a la base de datos", 'exito': False})

    try:
        with conexion.cursor() as cursor:
            programa = None
            cursor.callproc('DOC_SDEL.PROGRAMA_MOSTRAR', [ID_PROGRAMA])
            for results in cursor.getimplicitresults():
                for row in results:
                    programa = {'ID_PROGRAMA': row[0],
                                'NOMBRE_PROGRAMA': row[1],
                                'DESCRIPCION_PROGRAMA': row[2],
                                'TIPO_AUTENTIFICACION': row[3],
                                'FECHA_INICIO': row[4],
                                'FECHA_FIN': row[5],
                                'ID_INSTITUCION': row[6]}
            if programa:
                return jsonify({'datos': programa, 'mensaje': "Ok", 'exito': True})
            else:
                return jsonify({'mensaje': "Datos incorrectos", 'exito': False})
    except Exception as e:
        print(e)
        return jsonify({'mensaje': "Error en el procedimiento", 'exito': False})
    
if __name__ == '__main__':
    app.run(debug=True) # Habilita modo de depuración para que actualiza cambios en vivo