import mysql.connector
import os

def obtener_conexion():
    try:
        # Esto lee lo que configuraste en Render
        return mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            port=int(os.environ.get("DB_PORT", 3306)),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS"),
            database=os.environ.get("DB_NAME")
        )
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None