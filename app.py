
from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

import sqlite3
import models

app = Flask(__name__) #Crear una instancia de la aplicación Flask

app.secret_key = 'clave_secreta_super_segura'  # Clave para firmar las cookies de sesión

@app.route('/')
def index():
    return render_template('index.html') #Renderizar la plantilla index.html

# Definir una ruta para la página de inicio, que renderiza la plantilla index.html
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Verificar credenciales usando models
        if models.verificar_contraseña(username, password):
            user_id = models.get_usuario_id(username)
            session["user_id"] = user_id
            return redirect("/")
        else:
            return "Credenciales incorrectas"
        
    return render_template("login.html")


@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    if "user_id" not in session:
        return redirect("/login")
    
    if request.method == "POST":
        nombre = request.form.get("nombre")
        telefono = request.form.get("telefono")
        direccion = request.form.get("direccion")
        email = request.form.get("email")
        models.crear_cliente(nombre, telefono, direccion, email)
        return redirect("/clientes")
    
    clientes = models.get_clientes()
    return render_template("clientes.html", clientes=clientes)

@app.route("/servicios", methods=["GET", "POST"])
def servicios():
    if "user_id" not in session:
        return redirect("/login")
    if request.method == "POST":
        cliente_id = request.form.get("cliente_id")
        tipo_servicio = request.form.get("tipo_servicio")
        fecha = request.form.get("fecha")
        descripcion = request.form.get("descripcion")
        models.crear_servicio(cliente_id, tipo_servicio, fecha, descripcion)
        return redirect("/servicios")
    clientes = models.get_clientes_lista()
    servicios = models.get_servicios()
    return render_template("servicios.html", clientes=clientes, servicios=servicios)


@app.route("/productos", methods=["GET", "POST"])
def productos():
    if "user_id" not in session:
        return redirect("/login")
    
    if request.method == "POST":
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")
        stock = request.form.get("stock")
        models.crear_producto(nombre, precio, stock)
        return redirect("/productos")
    
    productos = models.get_productos()
    return render_template("productos.html", productos=productos)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/eliminar_cliente/<int:id>")
def eliminar_cliente(id):
    if "user_id" not in session:
        return redirect("/login")
    models.eliminar_cliente(id)
    flash("Cliente eliminado correctamente", "success")
    return redirect("/clientes")

@app.route("/editar_cliente/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    if "user_id" not in session:
        return redirect("/login")
    if request.method == "POST":
        nombre = request.form.get("nombre")
        telefono = request.form.get("telefono")
        direccion = request.form.get("direccion")
        email = request.form.get("email")
        models.actualizar_cliente(id, nombre, telefono, direccion, email)
        return redirect("/clientes")
    cliente = models.get_cliente(id)
    return render_template("editar_cliente.html", cliente=cliente)

@app.route("/cliente/<int:id>")
def ver_cliente(id):
    if "user_id" not in session:
        return redirect("/login")
    cliente = models.get_cliente(id)
    servicios = models.get_servicios_cliente(id)
    return render_template("cliente_detalle.html", cliente=cliente, servicios=servicios)

@app.route("/eliminar_servicio/<int:id>")
def eliminar_servicio(id):
    if "user_id" not in session:
        return redirect("/login")
    models.eliminar_servicio(id)
    return redirect("/servicios")

if __name__ == '__main__': #Verificar si el script se está ejecutando directamente
    app.run(debug=True)