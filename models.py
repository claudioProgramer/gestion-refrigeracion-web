"""
Funciones de acceso a base de datos.
Aquí centralizamos todas las operaciones SQL para no repetir código.
"""

import sqlite3
from werkzeug.security import check_password_hash

DB_PATH = "database.db"

# ============ USUARIOS ============

def get_usuario_por_username(username):
    """Busca un usuario por nombre de usuario. Retorna una tupla (id, username, password_hash) o None."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def verificar_contraseña(username, password):
    """Retorna True si las credenciales son válidas, False en caso contrario."""
    usuario = get_usuario_por_username(username)
    if usuario and check_password_hash(usuario[2], password):
        return True
    return False

def get_usuario_id(username):
    """Retorna el ID del usuario si existe, None si no."""
    usuario = get_usuario_por_username(username)
    return usuario[0] if usuario else None


# ============ CLIENTES ============

def get_clientes():
    """Retorna lista de todos los clientes."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def get_cliente(cliente_id):
    """Retorna datos de un cliente específico, o None si no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    conn.close()
    return cliente

def crear_cliente(nombre, telefono, direccion, email):
    """Crea un nuevo cliente. Retorna True si éxito, False si error."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO clientes (nombre, telefono, direccion, email)
            VALUES (?, ?, ?, ?)
        """, (nombre, telefono, direccion, email))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al crear cliente: {e}")
        return False

def actualizar_cliente(cliente_id, nombre, telefono, direccion, email):
    """Actualiza datos de un cliente. Retorna True si éxito, False si error."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE clientes
            SET nombre = ?, telefono = ?, direccion = ?, email = ?
            WHERE id = ?
        """, (nombre, telefono, direccion, email, cliente_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al actualizar cliente: {e}")
        return False

def eliminar_cliente(cliente_id):
    """Elimina un cliente y sus servicios asociados. Retorna True si éxito, False si error."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Primero eliminar servicios asociados
        cursor.execute("DELETE FROM servicios WHERE cliente_id = ?", (cliente_id,))
        # Luego eliminar el cliente
        cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al eliminar cliente: {e}")
        return False


# ============ SERVICIOS ============

def get_servicios():
    """Retorna lista de todos los servicios con nombre del cliente."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT servicios.id, clientes.nombre, servicios.tipo_servicio, 
               servicios.fecha, servicios.descripcion
        FROM servicios 
        JOIN clientes ON servicios.cliente_id = clientes.id 
        ORDER BY servicios.fecha DESC
    """)
    servicios = cursor.fetchall()
    conn.close()
    return servicios

def get_clientes_lista():
    """Retorna lista de clientes para usar en select (sin servicios extra)."""
    return get_clientes()

def crear_servicio(cliente_id, tipo_servicio, fecha, descripcion):
    """Crea un nuevo servicio. Retorna True si éxito, False si error."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO servicios (cliente_id, tipo_servicio, fecha, descripcion)
            VALUES (?, ?, ?, ?)
        """, (cliente_id, tipo_servicio, fecha, descripcion))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al crear servicio: {e}")
        return False

def get_servicios_cliente(cliente_id):
    """Retorna lista de servicios de un cliente específico."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tipo_servicio, fecha, descripcion
        FROM servicios
        WHERE cliente_id = ?
        ORDER BY fecha DESC
    """, (cliente_id,))
    servicios = cursor.fetchall()
    conn.close()
    return servicios

def eliminar_servicio(servicio_id):
    """Elimina un servicio. Retorna True si éxito, False si error."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM servicios WHERE id = ?", (servicio_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al eliminar servicio: {e}")
        return False


# ============ PRODUCTOS ============

def get_productos():
    """Retorna lista de todos los productos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

def crear_producto(nombre, precio, stock):
    """Crea un nuevo producto. Retorna True si éxito, False si error."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre, precio, stock)
            VALUES (?, ?, ?)
        """, (nombre, precio, stock))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al crear producto: {e}")
        return False
