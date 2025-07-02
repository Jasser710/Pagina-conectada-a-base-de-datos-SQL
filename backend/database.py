import mysql.connector
from mysql.connector import Error

def create_db_and_tables():
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="J7102006"
        )
        cursor = conn.cursor()
        
        # Crear base de datos si no existe
        cursor.execute("CREATE DATABASE IF NOT EXISTS datagrow")
        print("Base de datos 'datagrow' creada/verificada")
        
        # Usar la base de datos
        cursor.execute("USE datagrow")
        
        # Crear tabla
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS actividades (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cultivo VARCHAR(100) NOT NULL,
                tarea VARCHAR(100) NOT NULL,
                fecha DATE NOT NULL,
                estado VARCHAR(20) NOT NULL,
                descripcion TEXT
            )
        """)
        print("Tabla 'actividades' creada/verificada")
        
        conn.commit()
        return True
        
    except Error as e:
        print(f"Error en la creación de DB/tablas: {e}")
        return False
        
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()
            print("Conexión cerrada")