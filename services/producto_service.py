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
                # Manejo de nombres de columnas flexibles
                id_p = row.get('id') or row.get('id_producto')
                nombre = row.get('nombre')
                cantidad = row.get('cantidad') if row.get('cantidad') is not None else row.get('stock')
                precio = row.get('precio')
                
                p = Producto(id_p, nombre, cantidad, precio)
                lista.append(p)
            con.close()
        return lista

    @staticmethod
    def insertar(producto):
        """
        Inserta un objeto Producto en la base de datos MySQL.
        Soluciona el AttributeError en app.py
        """
        con = obtener_conexion()
        if con:
            try:
                cur = con.cursor()
                # Ajustamos la consulta SQL a las columnas de tu tabla
                sql = "INSERT INTO productos (id, nombre, cantidad, precio) VALUES (%s, %s, %s, %s)"
                
                # Usamos los métodos del objeto Producto que definiste en models/producto.py
                # Si en tu modelo los métodos se llaman distinto (ej. get_id), cámbialos aquí:
                valores = (
                    producto.get_id(), 
                    producto.get_nombre(), 
                    producto.get_cantidad(), 
                    producto.get_precio()
                )
                
                cur.execute(sql, valores)
                con.commit()
                con.close()
                return True
            except Exception as e:
                print(f"Error al insertar en MySQL: {e}")
                if con: con.close()
                return False
        return False