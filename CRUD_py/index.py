import sqlite3
from typing import Union, List, Tuple

# Conexión a la base de datos
def conectar_db(db_name: str = "database.db"):
    """Establece una conexión con la base de datos."""
    conn = sqlite3.connect(db_name)
    return conn, conn.cursor()

# Crear tabla si no existe
def inicializar_tabla():
    """Crea la tabla de usuarios si no existe."""
    conn, cursor = conectar_db()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Crear usuario -> C
def crear_usuario(nombre: str, email: str) -> str:
    """Crea un nuevo usuario en la base de datos."""
    try:
        conn, cursor = conectar_db()
        cursor.execute("INSERT INTO usuarios (nombre, email) VALUES (?, ?)", (nombre, email))
        conn.commit()
        cursor.close()
        conn.close()
        return "Usuario agregado correctamente."
    except sqlite3.IntegrityError:
        return "Error: El email ya está registrado."
    except Exception as e:
        return f"Error al agregar usuario: {e}"

# Obtener todos los registros -> R
def obtener_registros() -> List[Tuple[int, str, str]]:
    """Obtiene todos los registros de usuarios."""
    conn, cursor = conectar_db()
    cursor.execute("SELECT id, nombre, email FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return usuarios

# Actualizar usuario por ID -> U
def actualizar_usuario(id: int, nombre: str, email: str) -> str:
    """Actualiza un usuario por su ID."""
    conn, cursor = conectar_db()
    cursor.execute("SELECT id FROM usuarios WHERE id = ?", (id,))
    if cursor.fetchone():
        cursor.execute("UPDATE usuarios SET nombre = ?, email = ? WHERE id = ?", (nombre, email, id))
        conn.commit()
        mensaje = "Usuario actualizado correctamente."
    else:
        mensaje = "Error: Usuario no encontrado."
    cursor.close()
    conn.close()
    return mensaje

# Eliminar usuario por ID -> D
def eliminar_usuario(id: int) -> str:
    """Elimina un usuario por su ID."""
    conn, cursor = conectar_db()
    cursor.execute("SELECT id FROM usuarios WHERE id = ?", (id,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
        conn.commit()
        mensaje = "Usuario eliminado correctamente."
    else:
        mensaje = "Error: Usuario no encontrado."
    cursor.close()
    conn.close()
    return mensaje

# Obtener usuario por ID
def obtener_usuario(id: int) -> Union[Tuple[int, str, str], str]:
    """Obtiene un usuario por su ID."""
    conn, cursor = conectar_db()
    cursor.execute("SELECT id, nombre, email FROM usuarios WHERE id = ?", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario if usuario else "Usuario no encontrado."

# Inicialización y pruebas
if __name__ == "__main__":
    inicializar_tabla()
    print(crear_usuario("Jorge", "jorge@example.com"))
    print(crear_usuario("Jcva", "jcva@example.com"))
    print(crear_usuario("Joselito", "jose@example.com"))

    print("Usuarios registrados:")
    for usuario in obtener_registros():
        print(usuario)

    print(actualizar_usuario(2, "Juan Carlos", "juancarlos@example.com"))
    print(eliminar_usuario(3))
    print(obtener_usuario(1))
