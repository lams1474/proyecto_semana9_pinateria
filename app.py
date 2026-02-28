from flask import Flask, render_template, request, redirect, url_for
import os

from database.db import crear_tabla
from models.inventario import Inventario
from models.producto import Producto

# Crear tabla si no existe
crear_tabla()

app = Flask(__name__)

# =========================
# RUTAS FLASK
# =========================

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/productos")
def productos():
    inventario = Inventario()
    productos = inventario.mostrar_todos()
    return render_template("productos.html", productos=productos)

@app.route("/agregar", methods=["GET", "POST"])
def agregar_producto():
    if request.method == "POST":
        id = int(request.form["id"])
        nombre = request.form["nombre"]
        cantidad = int(request.form["cantidad"])
        precio = float(request.form["precio"])

        inventario = Inventario()
        producto = Producto(id, nombre, cantidad, precio)
        inventario.agregar_producto(producto)

        return redirect(url_for("productos"))

    return render_template("agregar.html")

@app.route("/eliminar/<int:id>")
def eliminar_producto_web(id):
    inventario = Inventario()
    inventario.eliminar_producto(id)
    return redirect(url_for("productos"))

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    inventario = Inventario()
    productos = inventario.mostrar_todos()

    producto = None
    for p in productos:
        if p.get_id() == id:
            producto = p
            break

    if request.method == "POST":
        cantidad = int(request.form["cantidad"])
        precio = float(request.form["precio"])
        inventario.actualizar_producto(id, cantidad, precio)
        return redirect(url_for("productos"))

    return render_template("editar.html", producto=producto)

@app.route("/buscar", methods=["GET", "POST"])
def buscar_producto():
    resultados = []
    if request.method == "POST":
        nombre = request.form["nombre"]
        inventario = Inventario()
        resultados = inventario.buscar_por_nombre(nombre)

    return render_template("buscar.html", productos=resultados)

# =========================
# MENÚ CONSOLA
# =========================

def menu():
    inventario = Inventario()

    while True:
        print("\n=== Sistema de Inventario - Piñatería Bryan & Kevin ===")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto")
        print("5. Mostrar todos")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            id = int(input("ID: "))
            nombre = input("Nombre: ")
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: "))

            producto = Producto(id, nombre, cantidad, precio)
            inventario.agregar_producto(producto)
            print("Producto agregado correctamente.")

        elif opcion == "2":
            id = int(input("ID del producto a eliminar: "))
            inventario.eliminar_producto(id)
            print("Producto eliminado.")

        elif opcion == "3":
            id = int(input("ID del producto a actualizar: "))
            cantidad = int(input("Nueva cantidad: "))
            precio = float(input("Nuevo precio: "))
            inventario.actualizar_producto(id, cantidad, precio)
            print("Producto actualizado.")

        elif opcion == "4":
            nombre = input("Nombre a buscar: ")
            resultados = inventario.buscar_por_nombre(nombre)
            for p in resultados:
                print(p)

        elif opcion == "5":
            productos = inventario.mostrar_todos()
            for p in productos:
                print(p)

        elif opcion == "6":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida.")

# =========================
# BLOQUE PRINCIPAL
# =========================

if __name__ == "__main__":

    if os.environ.get("RENDER"):
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)

    else:
        modo = input("¿Desea ejecutar el sistema en modo consola? (s/n): ")

        if modo.lower() == "s":
            menu()
        else:
            port = int(os.environ.get("PORT", 5000))
            app.run(host="0.0.0.0", port=port)