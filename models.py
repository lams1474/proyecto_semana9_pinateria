from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email):
        self.id = str(id_usuario) 
        self.nombre = nombre
        self.email = email

    def get_id(self):
        return str(self.id)