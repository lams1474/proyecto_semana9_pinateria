import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',       # Usuario por defecto de XAMPP
            password='1234',       # XAMPP por defecto no tiene contraseña
            database='pinateria' # ¡ASEGÚRATE QUE TU BASE SE LLAME ASÍ!
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None  # Si hay error, devuelve None (esto causaba tu falla)