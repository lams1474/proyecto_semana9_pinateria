import mysql.connector
import os

def obtener_conexion():
    try:
        # Configuración para que funcione con Aiven (SSL Requerido)
        return mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            port=int(os.environ.get("DB_PORT", 20271)), # Puerto de Aiven
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS"),
            database=os.environ.get("DB_NAME"),
            # IMPORTANTE PARA AIVEN:
            ssl_disabled=False,
            ssl_verify_cert=False # Para evitar el error de certificado que vimos antes
        )
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None
