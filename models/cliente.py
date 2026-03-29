# models/cliente.py

class Cliente:
    def __init__(self, id_cliente, nombre, cedula, telefono):
        self._id_cliente = id_cliente
        self._nombre = nombre
        self._cedula = cedula
        self._telefono = telefono

    # Getters
    def get_id(self): return self._id_cliente
    def get_nombre(self): return self._nombre
    def get_cedula(self): return self._cedula
    def get_telefono(self): return self._telefono

    # Setters
    def set_nombre(self, nombre): self._nombre = nombre
    def set_cedula(self, cedula): self._cedula = cedula
    def set_telefono(self, telefono): self._telefono = telefono

    def __str__(self):
        return f"Cliente: {self._nombre} | CI: {self._cedula}"