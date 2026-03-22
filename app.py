from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os, json, csv

# Importamos la conexión
try:
    from conexion.conexion import obtener_conexion
except:
    def obtener_conexion(): return None

from models import Usuario

app = Flask(__name__)
app.secret_key = 'pinateria_2026_secreta'

# --- 1. CONFIGURACIÓN LOGIN (SEMANA 14) ---
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    # Soporte para admin estático
    if user_id == "1": return Usuario(1, "Luis Admin", "admin@gmail.com")
    
    # Cargar usuario desde MySQL (Requisito 2.1)
    con = obtener_conexion()
    if con:
        try:
            cur = con.cursor(dictionary=True)
            cur.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
            u = cur.fetchone()
            con.close()
            if u: return Usuario(u['id_usuario'], u['nombre'], u['email'])
        except: pass
    return None

# --- 2. CONFIGURACIÓN SQLITE (ORM) ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ProductoORM(db.Model):
    __tablename__ = "productos_sqlite"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Float)

with app.app_context():
    db.create_all()

# --- 3. PERSISTENCIA Y SINCRONIZACIÓN ---
def guardar_en_archivos(p):
    carpeta = "data"
    if not os.path.exists(carpeta): os.makedirs(carpeta)
    ruta_json = os.path.join(carpeta, "productos.json")
    datos_j = []
    if os.path.exists(ruta_json):
        with open(ruta_json, "r") as f:
            try: datos_j = json.load(f)
            except: datos_j = []
    datos_j.append(p)
    with open(ruta_json, "w") as f: json.dump(datos_j, f, indent=4)

    # TXT
    with open(os.path.join(carpeta, "productos.txt"), "a") as f:
        f.write(f"{p['id']},{p['nombre']},{p['cantidad']},{p['precio']}\n")

    # CSV
    ruta_csv = os.path.join(carpeta, "productos.csv")
    ex = os.path.exists(ruta_csv)
    with open(ruta_csv, "a", newline="") as f:
        esc = csv.writer(f)
        if not ex: esc.writerow(["id", "nombre", "cantidad", "precio"])
        esc.writerow([p["id"], p["nombre"], p["cantidad"], p["precio"]])

def sincronizar_archivos(productos_db):
    carpeta = "data"
    if not os.path.exists(carpeta): os.makedirs(carpeta)
    with open(os.path.join(carpeta, "productos.json"), "w") as f: json.dump(productos_db, f, indent=4)
    with open(os.path.join(carpeta, "productos.txt"), "w") as f:
        for p in productos_db: f.write(f"{p['id']},{p['nombre']},{p['cantidad']},{p['precio']}\n")
    with open(os.path.join(carpeta, "productos.csv"), "w", newline="") as f:
        esc = csv.writer(f); esc.writerow(["id", "nombre", "cantidad", "precio"])
        for p in productos_db: esc.writerow([p["id"], p["nombre"], p["cantidad"], p["precio"]])

# --- 4. RUTAS DE AUTENTICACIÓN (SEMANA 14) ---

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nom = request.form.get('nombre')
        em = request.form.get('email')
        pw = request.form.get('password')
        
        con = obtener_conexion()
        if con:
            try:
                cur = con.cursor()
                cur.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", (nom, em, pw))
                con.commit()
                con.close()
                flash("Usuario registrado exitosamente. Ahora puedes iniciar sesión.")
                return redirect(url_for('login'))
            except Exception as e:
                flash(f"Error al registrar: {e}")
    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        em, pw = request.form.get('email'), request.form.get('password')
        # Admin estático
        if em == "admin@gmail.com" and pw == "1234":
            login_user(Usuario(1, "Luis Admin", "admin@gmail.com"))
            return redirect(url_for('inicio'))
        
        # Validación en MySQL (Requisito 2.2)
        con = obtener_conexion()
        if con:
            cur = con.cursor(dictionary=True)
            cur.execute("SELECT * FROM usuarios WHERE email=%s AND password=%s", (em, pw))
            u = cur.fetchone()
            con.close()
            if u:
                login_user(Usuario(u['id_usuario'], u['nombre'], u['email']))
                return redirect(url_for('inicio'))
        flash("Credenciales incorrectas")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- 5. RUTAS DEL SISTEMA (PROTEGIDAS) ---

@app.route("/")
def inicio(): return render_template("index.html")

@app.route("/about")
def about(): return render_template("about.html")

@app.route("/productos")
@login_required # Protección de ruta (Requisito 2.2)
def productos():
    lista = []
    try:
        con = obtener_conexion()
        if con:
            cur = con.cursor(dictionary=True)
            cur.execute("SELECT * FROM productos")
            datos = cur.fetchall()
            con.close()
            for p in datos:
                lista.append({
                    "id": p.get('id') or p.get('id_producto'),
                    "nombre": p.get('nombre'),
                    "cantidad": p.get('cantidad') or p.get('stock') or 0,
                    "precio": p.get('precio')
                })
            if lista: sincronizar_archivos(lista)
    except: pass
    if not lista and os.path.exists("data/productos.json"):
        with open("data/productos.json", "r") as f:
            try: lista = json.load(f)
            except: lista = []
    return render_template("productos.html", productos=lista)

@app.route("/agregar", methods=["GET", "POST"])
@login_required
def agregar_producto():
    if request.method == "POST":
        p = {"id": int(request.form["id"]), "nombre": request.form["nombre"],
             "cantidad": int(request.form["cantidad"]), "precio": float(request.form["precio"])}
        con = obtener_conexion()
        if con:
            try:
                cur = con.cursor()
                cur.execute("INSERT INTO productos VALUES (%s,%s,%s,%s)", (p['id'], p['nombre'], p['cantidad'], p['precio']))
                con.commit(); con.close()
            except: pass
        guardar_en_archivos(p)
        nuevo_orm = ProductoORM(id=p['id'], nombre=p['nombre'], cantidad=p['cantidad'], precio=p['precio'])
        db.session.add(nuevo_orm); db.session.commit()
        return redirect(url_for("productos"))
    return render_template("agregar.html")

@app.route("/datos")
@login_required
def ver_datos():
    t, j, c = [], [], []
    if os.path.exists("data/productos.txt"):
        with open("data/productos.txt", "r") as f: t = f.readlines()
    if os.path.exists("data/productos.json"):
        with open("data/productos.json", "r") as f:
            try: j = json.load(f)
            except: j = []
    if os.path.exists("data/productos.csv"):
        with open("data/productos.csv", "r") as f: c = list(csv.reader(f))
    return render_template("datos.html", txt=t, json_datos=j, csv_datos=c)

@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):
    con = obtener_conexion(); cur = con.cursor(dictionary=True)
    if request.method == "POST":
        cur.execute("UPDATE productos SET cantidad=%s, precio=%s WHERE id=%s", (request.form["cantidad"], request.form["precio"], id))
        con.commit(); con.close(); return redirect(url_for("productos"))
    cur.execute("SELECT * FROM productos WHERE id=%s", (id,))
    p = cur.fetchone(); con.close(); return render_template("editar.html", producto=p)

@app.route("/eliminar/<int:id>")
@login_required
def eliminar_producto(id):
    con = obtener_conexion()
    if con:
        cur = con.cursor(); cur.execute("DELETE FROM productos WHERE id=%s", (id,))
        con.commit(); con.close()
    return redirect(url_for("productos"))

if __name__ == "__main__":
    app.run(debug=True)