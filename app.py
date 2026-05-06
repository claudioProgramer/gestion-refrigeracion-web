# Assisted by ChatGPT for conceptual guidance on:
# - Flask routing and request handling
# - SQLite database interactions
# - User authentication and session management

from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

import sqlite3

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

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Buscar el usuario en la base de datos
        cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        # Verificar la contraseña usando check_password_hash
        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            return redirect("/")
        else:
            return "Credenciales incorrectas"
        
    return render_template("login.html")


@app.route("/clientes", methods=["GET", "POST"]) #Definir una ruta para la página de clientes, que acepta tanto solicitudes GET como POST
def clientes():
    if "user_id" not in session:
        return redirect("/login")
    
    if request.method == "POST":
        # Obtener los datos del formulario
        nombre = request.form.get("nombre")
        telefono = request.form.get("telefono")
        direccion = request.form.get("direccion")
        email = request.form.get("email")

        # Conectar a la base de datos y guardar los datos del cliente
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO clientes (nombre, telefono, direccion, email)
            VALUES (?, ?, ?, ?)
        """, (nombre, telefono, direccion, email))

        conn.commit() #Guardar los cambios en la base de datos
        conn.close() # Cerrar la conexión a la base de datos

        return redirect("/clientes")
    
    # si es una solicitud GET, mostrar la lista de clientes
    conn = sqlite3.connect("database.db") 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes") #Ejecutar una consulta para obtener todos los clientes
    clientes = cursor.fetchall() #Obtener los resultados de la consulta en una lista de tuplas
    conn.close() #Cerrar la conexión a la base de datos

    return render_template("clientes.html", clientes=clientes) #Renderizar la plantilla clientes.html y pasar la lista de clientes como contexto

@app.route("/servicios" , methods=["GET", "POST"])
def servicios():
    if "user_id" not in session:
        return redirect("/login")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    if request.method == "POST":
        cliente_id = request.form.get("cliente_id")
        tipo_servicio = request.form.get("tipo_servicio")
        fecha = request.form.get("fecha")
        descripcion = request.form.get("descripcion")
        cursor.execute("""
            INSERT INTO servicios (cliente_id, tipo_servicio, fecha, descripcion)
            VALUES (?, ?, ?, ?)
        """, (cliente_id, tipo_servicio, fecha, descripcion))
        conn.commit()
        conn.close()
        return redirect("/servicios")
    # 🔥 GET: traer clientes para el select
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall() #Obtener todos los clientes para mostrar en el formulario de servicios (para seleccionar a qué cliente se le asigna el servicio)
    # 🔥 #Ejecutar una consulta SQL para obtener los servicios junto con el nombre del cliente asociado, utilizando una JOIN entre las tablas servicios y clientes
    cursor.execute("""SELECT servicios.id, clientes.nombre, servicios.tipo_servicio, servicios.fecha, servicios.descripcion
        FROM servicios JOIN clientes ON servicios.cliente_id = clientes.id ORDER BY servicios.fecha DESC""")
    servicios = cursor.fetchall()
    conn.close()
    return render_template("servicios.html", clientes=clientes, servicios=servicios)


@app.route("/productos", methods=["GET", "POST"])
def productos():
    if "user_id" not in session:
        return redirect("/login")
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")
        stock = request.form.get("stock")

        cursor.execute("""
            INSERT INTO productos (nombre, precio, stock)
            VALUES (?, ?, ?)
        """, (nombre, precio, stock))

        conn.commit()
        conn.close()

        return redirect("/productos")
    
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    
    return render_template("productos.html", productos=productos)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/eliminar_cliente/<int:id>") #Definir una ruta para eliminar un cliente, con un parámetro de ID que se espera sea un entero
def eliminar_cliente(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    # 🔥 Primero eliminar servicios relacionados
    cursor.execute("DELETE FROM servicios WHERE cliente_id = ?", (id,))
    # 🔥 Luego eliminar el cliente
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Cliente eliminado correctamente", "success")
    return redirect("/clientes")

@app.route("/editar_cliente/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    if request.method == "POST":
        nombre = request.form.get("nombre")
        telefono = request.form.get("telefono")
        direccion = request.form.get("direccion")
        email = request.form.get("email")
        cursor.execute("""
            UPDATE clientes
            SET nombre = ?, telefono = ?, direccion = ?, email = ?
            WHERE id = ?
        """, (nombre, telefono, direccion, email, id))
        conn.commit()
        conn.close()
        return redirect("/clientes")
    # GET → traer datos actuales
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (id,))
    cliente = cursor.fetchone()
    conn.close()
    return render_template("editar_cliente.html", cliente=cliente)

@app.route("/cliente/<int:id>")
def ver_cliente(id):
    if "user_id" not in session:
        return redirect("/login")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    # Obtener datos del cliente
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (id,))
    cliente = cursor.fetchone()
    # Obtener servicios de ese cliente ordenados por fecha descendente
    cursor.execute("""
        SELECT tipo_servicio, fecha, descripcion
        FROM servicios
        WHERE cliente_id = ?
        ORDER BY fecha DESC
    """, (id,))
    servicios = cursor.fetchall()
    conn.close()
    return render_template("cliente_detalle.html", cliente=cliente, servicios=servicios)

@app.route("/eliminar_servicio/<int:id>")
def eliminar_servicio(id):
    if "user_id" not in session:
        return redirect("/login")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM servicios WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/servicios")

if __name__ == '__main__': #Verificar si el script se está ejecutando directamente
    app.run(debug=True)