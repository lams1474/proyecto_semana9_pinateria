from flask import Flask, render_template
import os

app = Flask(__name__)

# Ruta principal
@app.route("/")
def inicio():
    return render_template("index.html")

# Ruta Acerca de
@app.route("/about")
def about():
    return render_template("about.html")

# Ruta Productos
@app.route("/productos")
def productos():
    lista_productos = ["Globos", "Piñatas", "Velas", "Peluches"]
    return render_template("productos.html", productos=lista_productos)

# Configuración para Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
