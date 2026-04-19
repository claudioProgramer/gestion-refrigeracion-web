import sqlite3
from werkzeug.security import generate_password_hash

password_hash = generate_password_hash("1234") # Generar un hash de la contraseña "1234" para mayor seguridad

conn = sqlite3.connect("database.db") # Conexión a la base de datos (se creará si no existe)
cursor = conn.cursor() # Crear un cursor para ejecutar comandos SQL

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    direccion TEXT,
    email TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

# Crear la tabla de servicios, con una clave foránea que referencia a la tabla de clientes
cursor.execute("""
CREATE TABLE IF NOT EXISTS servicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    tipo_servicio TEXT,
    fecha TEXT,
    descripcion TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
)
""")

# Crear la tabla de productos, con campos para el nombre, precio y stock
cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL,
    stock INTEGER
)
""")

# Insertar un usuario por defecto (admin) con la contraseña "1234" (hashada para mayor seguridad)
cursor.execute("""
INSERT OR IGNORE INTO usuarios (username, password)
VALUES (?, ?)
""", ("admin", password_hash))

conn.commit() # Guardar los cambios en la base de datos
conn.close() # Cerrar la conexión a la base de datos

print("Base de datos creada correctamente.")