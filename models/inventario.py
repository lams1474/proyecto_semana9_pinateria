from models.producto import Producto
from database.db import conectar

class Inventario:
    def __init__(self):
        self.productos = {}
        self.cargar_desde_bd()

    # Cargar productos al iniciar
    def cargar_desde_bd(self):
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        filas = cursor.fetchall()
        conexion.close()

        for fila in filas:
            producto = Producto(fila[0], fila[1], fila[2], fila[3])
            self.productos[producto.get_id()] = producto

    # CREATE
    def agregar_producto(self, producto):
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO productos (id, nombre, cantidad, precio) VALUES (?, ?, ?, ?)",
            (producto.get_id(), producto.get_nombre(), producto.get_cantidad(), producto.get_precio())
        )

        conexion.commit()
        conexion.close()

        self.productos[producto.get_id()] = producto

    # DELETE
    def eliminar_producto(self, id):
        if id in self.productos:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
            conexion.commit()
            conexion.close()

            del self.productos[id]

    # UPDATE
    def actualizar_producto(self, id, cantidad=None, precio=None):
        if id in self.productos:
            conexion = conectar()
            cursor = conexion.cursor()

            if cantidad is not None:
                cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (cantidad, id))
                self.productos[id].set_cantidad(cantidad)

            if precio is not None:
                cursor.execute("UPDATE productos SET precio = ? WHERE id = ?", (precio, id))
                self.productos[id].set_precio(precio)

            conexion.commit()
            conexion.close()

    # READ
    def buscar_por_nombre(self, nombre):
        resultados = []
        for producto in self.productos.values():
            if nombre.lower() in producto.get_nombre().lower():
                resultados.append(producto)
        return resultados

    def mostrar_todos(self):
        return list(self.productos.values())