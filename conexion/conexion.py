import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="1234",  
            database="pinateria_bryan_kevin",
            auth_plugin="mysql_native_password"
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None