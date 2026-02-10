from flask import Flask

# Crear la aplicación Flask
app = Flask(__name__)

# Ruta principal
@app.route('/')
def inicio():
    return 'Bienvenido a la Tienda Online – Piñatería Bryan & Kevin'

# Ruta dinámica basada en el negocio
@app.route('/producto/<nombre>')
def producto(nombre):
    return f'Producto: {nombre} – disponible en la tienda.'

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
