from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import json
import csv
from conexion.conexion import obtener_conexion

app = Flask(__name__)

# =========================
# CONFIGURACIÓN SQLITE (Solo práctica Semanas previas)
# =========================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ProductoORM(db.Model):
    __tablename__ = "productos_sqlite"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False) # Cambiado a stock
    precio = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

# =========================
# PERSISTENCIA EN ARCHIVOS
# =========================
def guardar_en_txt(p):
    # Asegura que la carpeta data exista
    if not os.path.exists("data"): os.makedirs("data")
    ruta = os.path.join("data", "productos.txt")
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(f"{p['id']},{p['nombre']},{p['stock']},{p['precio']}\n")

def guardar_en_json(p):
    if not os.path.exists("data"): os.makedirs("data")
    ruta = os.path.join("data", "productos.json")
    datos = []
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            try: datos = json.load(f)
            except: datos = []
    datos.append(p)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)

def guardar_en_csv(p):
    if not os.path.exists("data"): os.makedirs("data")
    ruta = os.path.join("data", "productos.csv")
    archivo_existe = os.path.exists(ruta)
    with open(ruta, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not archivo_existe:
            writer.writerow(["id", "nombre", "stock", "precio"])
        writer.writerow([p["id"], p["nombre"], p["stock"], p["precio"]])

# =========================
# FUNCIÓN DE SINCRONIZACIÓN (MYSQL -> ARCHIVOS)
# =========================
def sincronizar_mysql_a_archivos():
    # 1. Obtener todos los productos de MySQL
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM producto")
    todos_los_productos = cursor.fetchall()
    conexion.close()

    # 2. Asegurar carpeta data
    if not os.path.exists("data"):
        os.makedirs("data")

    # 3. Limpiar/Resetear los archivos actuales
    rutas = {
        "txt": os.path.join("data", "productos.txt"),
        "json": os.path.join("data", "productos.json"),
        "csv": os.path.join("data", "productos.csv")
    }
    
    # Abrir archivos en modo 'w' para borrar contenido previo
    open(rutas["txt"], "w", encoding="utf-8").close()
    open(rutas["json"], "w", encoding="utf-8").close()
    # Para el CSV escribimos el encabezado primero
    with open(rutas["csv"], "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "nombre", "stock", "precio"])

    # 4. Volver a llenar los archivos con los datos actuales de MySQL
    for p in todos_los_productos:
        p_dict = {
            "id": p['id_producto'], 
            "nombre": p['nombre'], 
            "stock": p['stock'], 
            "precio": float(p['precio'])
        }
        guardar_en_txt(p_dict)
        guardar_en_json(p_dict)
        guardar_en_csv(p_dict)

# =========================
# RUTAS PRINCIPALES
# =========================
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

# =========================
# CRUD PRODUCTO (MYSQL)
# =========================
@app.route("/productos")
def productos():
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM producto")
        lista_productos = cursor.fetchall()
        conexion.close()
        return render_template("productos.html", productos=lista_productos)
    return "Error en la conexión a la base de datos."

@app.route("/agregar", methods=["GET", "POST"])
def agregar_producto():
    if request.method == "POST":
        id_p = int(request.form["id"])
        nom = request.form["nombre"].strip()
        stk = int(request.form["stock"])
        pre = float(request.form["precio"])

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO producto (id_producto, nombre, stock, precio) VALUES (%s, %s, %s, %s)",
            (id_p, nom, stk, pre)
        )
        conexion.commit()
        conexion.close()

        # Persistencia en archivos
        p_dict = {"id": id_p, "nombre": nom, "stock": stk, "precio": pre}
        guardar_en_txt(p_dict)
        guardar_en_json(p_dict)
        guardar_en_csv(p_dict)

        return redirect(url_for("productos"))
    return render_template("agregar.html")

@app.route("/eliminar/<int:id>")
def eliminar_producto(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM producto WHERE id_producto=%s", (id,))
    conexion.commit()
    conexion.close()
    return redirect(url_for("productos"))

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    if request.method == "POST":
        stk = int(request.form["stock"])
        pre = float(request.form["precio"])
        cursor.execute("UPDATE producto SET stock=%s, precio=%s WHERE id_producto=%s", (stk, pre, id))
        conexion.commit()
        conexion.close()
        return redirect(url_for("productos"))
    
    cursor.execute("SELECT * FROM producto WHERE id_producto=%s", (id,))
    producto = cursor.fetchone()
    conexion.close()
    return render_template("editar.html", producto=producto)

# =========================
# CRUD USUARIOS
# =========================
@app.route("/usuarios")
def lista_usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conexion.close()
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/agregar_usuario", methods=["GET", "POST"])
def agregar_usuario():
    if request.method == "POST":
        nom = request.form["nombre"]
        eml = request.form["mail"]
        pwd = request.form["password"]

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)",
            (nom, eml, pwd)
        )
        conexion.commit()
        conexion.close()
        return redirect(url_for("lista_usuarios"))
    return render_template("registro_usuario.html")

# =========================
# OTROS
# =========================
@app.route("/buscar", methods=["GET", "POST"])
def buscar_producto():
    resultados = []
    if request.method == "POST":
        nom = request.form["nombre"]
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM producto WHERE nombre LIKE %s", ("%" + nom + "%",))
        resultados = cursor.fetchall()
        conexion.close()
    return render_template("buscar.html", productos=resultados)

@app.route("/datos")
def ver_datos():
    # 1. Leer TXT
    txt_datos = []
    ruta_txt = os.path.join("data", "productos.txt")
    if os.path.exists(ruta_txt):
        with open(ruta_txt, "r", encoding="utf-8") as f:
            txt_datos = f.readlines()
            
    # 2. Leer JSON
    json_datos = []
    ruta_json = os.path.join("data", "productos.json")
    if os.path.exists(ruta_json):
        with open(ruta_json, "r", encoding="utf-8") as f:
            try: json_datos = json.load(f)
            except: json_datos = []
            
    # 3. Leer CSV
    csv_datos = []
    ruta_csv = os.path.join("data", "productos.csv")
    if os.path.exists(ruta_csv):
        with open(ruta_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            csv_datos = list(reader)

    # Enviamos las 3 variables que el HTML espera
    return render_template("datos.html", txt_datos=txt_datos, json_datos=json_datos, csv_datos=csv_datos)

# =========================
# UTILIDADES (PEGA ESTO AQUÍ)
# =========================
@app.route("/sincronizar_ahora")
def ejecutar_sincronizacion():
    sincronizar_mysql_a_archivos()
    return "¡Sincronización completada! Los archivos ahora coinciden con la base de datos."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)