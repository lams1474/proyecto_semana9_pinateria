from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# =========================
# CONFIGURACIÓN SQLITE + SQLALCHEMY
# =========================

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# MODELO DE DATOS (ORM)
# =========================

class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Producto {self.nombre}>"

# Crear tabla si no existe
with app.app_context():
    db.create_all()

# =========================
# RUTAS
# =========================

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/productos")
def productos():
    productos = Producto.query.all()
    return render_template("productos.html", productos=productos)


@app.route("/agregar", methods=["GET", "POST"])
def agregar_producto():
    if request.method == "POST":
        nuevo_producto = Producto(
            id=int(request.form["id"]),
            nombre=request.form["nombre"],
            cantidad=int(request.form["cantidad"]),
            precio=float(request.form["precio"])
        )

        db.session.add(nuevo_producto)
        db.session.commit()

        return redirect(url_for("productos"))

    return render_template("agregar.html")


@app.route("/eliminar/<int:id>")
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for("productos"))


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)

    if request.method == "POST":
        producto.cantidad = int(request.form["cantidad"])
        producto.precio = float(request.form["precio"])
        db.session.commit()
        return redirect(url_for("productos"))

    return render_template("editar.html", producto=producto)


@app.route("/buscar", methods=["GET", "POST"])
def buscar_producto():
    resultados = []

    if request.method == "POST":
        nombre = request.form["nombre"]
        resultados = Producto.query.filter(
            Producto.nombre.ilike(f"%{nombre}%")
        ).all()

    return render_template("buscar.html", productos=resultados)


# =========================
# EJECUCIÓN
# =========================

if __name__ == "__main__":
    app.run(debug=True)