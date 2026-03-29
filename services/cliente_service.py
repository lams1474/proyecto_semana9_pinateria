# services/cliente_service.py
from conexion.conexion import obtener_conexion
from models.cliente import Cliente

class ClienteService:
    @staticmethod
    def listar_clientes():
        clientes = []
        con = obtener_conexion()
        if con:
            cur = con.cursor(dictionary=True)
            cur.execute("SELECT * FROM clientes")
            for row in cur.fetchall():
                c = Cliente(row['id_cliente'], row['nombre'], row['cedula'], row['telefono'])
                clientes.append(c)
            con.close()
        return clientes

    @staticmethod
    def registrar_cliente(cliente):
        con = obtener_conexion()
        if con:
            cur = con.cursor()
            cur.execute("INSERT INTO clientes (nombre, cedula, telefono) VALUES (%s, %s, %s)", 
                        (cliente.get_nombre(), cliente.get_cedula(), cliente.get_telefono()))
            con.commit()
            con.close()