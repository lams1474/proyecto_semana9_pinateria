# services/producto_service.py
from conexion.conexion import obtener_conexion
from models.producto import Producto

class ProductoService:
    @staticmethod
    def obtener_todos():
        lista = []
        con = obtener_conexion()
        if con:
            cur = con.cursor(dictionary=True)
            cur.execute("SELECT * FROM productos")
            for row in cur.fetchall():
                # Usamos .get() para evitar el KeyError si el nombre varía
                id_p = row.get('id') or row.get('id_producto')
                nombre = row.get('nombre')
                # Aquí estaba el error: intentamos 'cantidad' o 'stock'
                cantidad = row.get('cantidad') if row.get('cantidad') is not None else row.get('stock')
                precio = row.get('precio')
                
                p = Producto(id_p, nombre, cantidad, precio)
                lista.append(p)
            con.close()
        return lista