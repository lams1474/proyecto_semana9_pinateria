from flask import Flask
import os

app = Flask(__name__)

# Ruta principal
@app.route("/")
def inicio():
    return """
    <h1>Bienvenido a Tienda Online – Piñatería Bryan & Kevin</h1>
    <p>Catálogo de productos y detalles para toda ocasión.</p>

    <h3>Productos destacados:</h3>
    <ul>
        <li><a href="/producto/globos">Ver producto: Globos</a></li>
        <li><a href="/producto/peluches">Ver producto: Peluches</a></li>
        <li><a href="/producto/velas">Ver producto: Velas</a></li>
    </ul>
    """

# Ruta dinámica adaptada al negocio
@app.route("/producto/<nombre>")
def producto(nombre):
    return f"""
    <h2>Producto: {nombre.capitalize()}</h2>
    <p>Disponible en Piñatería Bryan & Kevin.</p>
    <a href="/">Volver al inicio</a>
    """

# Punto de entrada para Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
