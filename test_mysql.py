# test_mysql.py
from conexion.conexion import obtener_conexion

try:
    conn = obtener_conexion()
    if conn.is_connected():
        print("✅ ¡Conexión exitosa a Aiven MySQL!")
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        print(f"Conectado a la base: {db_name}")
        conn.close()
except Exception as e:
    print(f"❌ Error de conexión: {e}")
