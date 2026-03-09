from ast import Import

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import json
import csv

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

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Producto {self.nombre}>"

# Crear tabla si no existe
with app.app_context():
    db.create_all()

# =========================
# FUNCIONES DE PERSISTENCIA
# =========================

def guardar_en_txt(producto):

    with open("productos.txt", "a", encoding="utf-8") as f:
        f.write(f"{producto.id},{producto.nombre},{producto.cantidad},{producto.precio}\n")


def guardar_en_json(producto):

    datos = []

    if os.path.exists("productos.json"):

        with open("productos.json", "r", encoding="utf-8") as f:
            try:
                datos = json.load(f)
            except json.JSONDecodeError:
                datos = []

    datos.append({
        "id": producto.id,
        "nombre": producto.nombre,
        "cantidad": producto.cantidad,
        "precio": producto.precio
    })

    with open("productos.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)


def guardar_en_csv(producto):

    archivo_existe = os.path.exists("productos.csv")

    with open("productos.csv", "a", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        if not archivo_existe:
            writer.writerow(["id", "nombre", "cantidad", "precio"])

        writer.writerow([
            producto.id,
            producto.nombre,
            producto.cantidad,
            producto.precio
        ])

# =========================
# RUTAS PRINCIPALES
# =========================

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/productos")
def productos():

    lista_productos = Producto.query.all()

    return render_template(
        "productos.html",
        productos=lista_productos
    )

# =========================
# AGREGAR PRODUCTO
# =========================

@app.route("/agregar", methods=["GET", "POST"])
def agregar_producto():

    if request.method == "POST":

        try:
            id_producto = int(request.form["id"])
            nombre = request.form["nombre"].strip()
            cantidad = int(request.form["cantidad"])
            precio = float(request.form["precio"])
        except ValueError:
            return "Error: datos inválidos"

        if nombre == "" or cantidad < 0 or precio < 0:
            return "Error: valores incorrectos"

        nuevo_producto = Producto(
            id=id_producto,
            nombre=nombre,
            cantidad=cantidad,
            precio=precio
        )

        db.session.add(nuevo_producto)
        db.session.commit()

        # Guardar también en archivos
        guardar_en_txt(nuevo_producto)
        guardar_en_json(nuevo_producto)
        guardar_en_csv(nuevo_producto)

        return redirect(url_for("productos"))

    return render_template("agregar.html")

# =========================
# ELIMINAR PRODUCTO
# =========================

@app.route("/eliminar/<int:id>")
def eliminar_producto(id):

    producto = Producto.query.get_or_404(id)

    db.session.delete(producto)
    db.session.commit()

    return redirect(url_for("productos"))

# =========================
# EDITAR PRODUCTO
# =========================

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):

    producto = Producto.query.get_or_404(id)

    if request.method == "POST":

        try:
            cantidad = int(request.form["cantidad"])
            precio = float(request.form["precio"])
        except ValueError:
            return "Error: datos inválidos"

        if cantidad < 0 or precio < 0:
            return "Error: valores negativos"

        producto.cantidad = cantidad
        producto.precio = precio

        db.session.commit()

        return redirect(url_for("productos"))

    return render_template("editar.html", producto=producto)

# =========================
# BUSCAR PRODUCTO
# =========================

@app.route("/buscar", methods=["GET", "POST"])
def buscar_producto():

    resultados = []

    if request.method == "POST":

        nombre = request.form["nombre"]

        resultados = Producto.query.filter(
            Producto.nombre.ilike(f"%{nombre}%")
        ).all()

    return render_template(
        "buscar.html",
        productos=resultados
    )

# =========================
# VISUALIZAR PERSISTENCIA
# =========================

@app.route("/datos")
def ver_datos():

    datos_txt = []
    datos_json = []
    datos_csv = []

    # TXT
    if os.path.exists("productos.txt"):
        with open("productos.txt", "r", encoding="utf-8") as f:
            datos_txt = f.readlines()

    # JSON
    if os.path.exists("productos.json"):
        with open("productos.json", "r", encoding="utf-8") as f:
            try:
                datos_json = json.load(f)
            except json.JSONDecodeError:
                datos_json = []

    # CSV
    if os.path.exists("productos.csv"):
        with open("productos.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            datos_csv = list(reader)

    return render_template(
        "datos.html",
        txt=datos_txt,
        json_datos=datos_json,
        csv_datos=datos_csv
    )

# =========================
# EJECUCIÓN
# =========================

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)