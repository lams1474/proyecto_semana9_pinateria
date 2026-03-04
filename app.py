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

    # Acceso directo al diccionario (más eficiente)
    producto = inventario.productos.get(id)

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
# EXPORTACIONES
# =========================

@app.route("/exportar_txt")
def exportar_txt():
    inventario = Inventario()
    inventario.exportar_txt()
    return redirect(url_for("ver_txt"))


@app.route("/ver_txt")
def ver_txt():
    try:
        with open("data/datos.txt", "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
    except FileNotFoundError:
        contenido = "No hay datos exportados."

    return render_template("datos.html", contenido=contenido)


@app.route("/exportar_json")
def exportar_json():
    inventario = Inventario()
    inventario.exportar_json()
    return redirect(url_for("ver_json"))


@app.route("/ver_json")
def ver_json():
    try:
        with open("data/datos.json", "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
    except FileNotFoundError:
        contenido = "No hay datos exportados."

    return render_template("datos.html", contenido=contenido)


@app.route("/exportar_csv")
def exportar_csv():
    inventario = Inventario()
    inventario.exportar_csv()
    return redirect(url_for("ver_csv"))


@app.route("/ver_csv")
def ver_csv():
    try:
        with open("data/datos.csv", "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
    except FileNotFoundError:
        contenido = "No hay datos exportados."

    return render_template("datos.html", contenido=contenido)


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