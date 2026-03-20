from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import json
import csv
# Importación desde tu carpeta 'conexion' (Semana 13)
from conexion.conexion import obtener_conexion

app = Flask(__name__)

# ==========================================
# SEMANA 12: CONFIGURACIÓN SQLITE (SQLAlchemy)
# ==========================================
# Crea el archivo inventario.db que se ve en tu imagen
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ProductoORM(db.Model):
    __tablename__ = "productos_sqlite"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

# ==========================================
# SEMANA 12: PERSISTENCIA EN ARCHIVOS (Carpeta data/)
# ==========================================
def guardar_en_archivos(p):
    # Ruta según tu explorador de archivos en la imagen
    ruta_base = "data/"
    if not os.path.exists(ruta_base): os.makedirs(ruta_base)

    # 1. TXT
    with open(os.path.join(ruta_base, "productos.txt"), "a", encoding="utf-8") as f:
        f.write(f"{p['id']},{p['nombre']},{p['stock']},{p['precio']}\n")

    # 2. JSON
    ruta_json = os.path.join(ruta_base, "productos.json")
    datos_json = []
    if os.path.exists(ruta_json):
        with open(ruta_json, "r", encoding="utf-8") as f:
            try: datos_json = json.load(f)
            except: datos_json = []
    datos_json.append(p)
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(datos_json, f, indent=4)

    # 3. CSV
    ruta_csv = os.path.join(ruta_base, "productos.csv")
    existe = os.path.exists(ruta_csv)
    with open(ruta_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not existe: writer.writerow(["id", "nombre", "stock", "precio"])
        writer.writerow([p["id"], p["nombre"], p["stock"], p["precio"]])

# ==========================================
# RUTAS DEL SISTEMA
# ==========================================

@app.route("/")
def inicio():
    # Semana 09: Mensaje de bienvenida del negocio
    return render_template("index.html")

@app.route("/productos")
def listar_productos():
    # Semana 13: Consulta a MySQL (Aiven)
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        lista = cursor.fetchall()
        conexion.close()
        return render_template("productos.html", productos=lista)
    return "Error de conexión con MySQL Aiven"

@app.route("/agregar", methods=["GET", "POST"])
def agregar_producto():
    if request.method == "POST":
        p_dict = {
            "id": int(request.form["id"]),
            "nombre": request.form["nombre"],
            "stock": int(request.form["stock"]),
            "precio": float(request.form["precio"])
        }

        # PERSISTENCIA 1: MySQL (Semana 13)
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO productos (id, nombre, stock, precio) VALUES (%s, %s, %s, %s)",
                (p_dict["id"], p_dict["nombre"], p_dict["stock"], p_dict["precio"])
            )
            conexion.commit()
            conexion.close()

        # PERSISTENCIA 2: SQLite (Semana 12)
        nuevo_p = ProductoORM(id=p_dict["id"], nombre=p_dict["nombre"], 
                              stock=p_dict["stock"], precio=p_dict["precio"])
        db.session.add(nuevo_p)
        db.session.commit()

        # PERSISTENCIA 3: Archivos (Semana 12)
        guardar_en_archivos(p_dict)

        return redirect(url_for("listar_productos"))
    return render_template("producto_form.html")

@app.route("/datos")
def ver_datos():
    # Semana 12: Ruta para visualizar persistencia local
    return render_template("datos.html")

if __name__ == "__main__":
    app.run(debug=True)
