# forms/producto_form.py

class ProductoForm:
    def __init__(self, request_form):
        """
        Esta clase procesa y limpia los datos que vienen del 
        formulario HTML antes de enviarlos al servicio.
        """
        self.id = request_form.get('id')
        self.nombre = request_form.get('nombre')
        self.cantidad = request_form.get('cantidad')
        self.precio = request_form.get('precio')

    def es_valido(self):
        """
        Validación básica para asegurar que no haya campos vacíos
        y que los números sean correctos.
        """
        try:
            if not self.nombre or len(self.nombre) < 2:
                return False
            if int(self.cantidad) < 0:
                return False
            if float(self.precio) <= 0:
                return False
            return True
        except (ValueError, TypeError):
            return False

    def obtener_datos(self):
        """Retorna los datos listos para ser usados por el modelo"""
        return {
            "id": int(self.id) if self.id else None,
            "nombre": self.nombre,
            "cantidad": int(self.cantidad),
            "precio": float(self.precio)
        }