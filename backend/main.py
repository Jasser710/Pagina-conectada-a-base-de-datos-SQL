from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
from datetime import date
import uvicorn

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Actividad(BaseModel):
    cultivo: str
    tarea: str
    fecha: date
    estado: str
    descripcion: str = None

# Función para crear la base de datos y tablas
def create_db_and_tables():
    conn = None
    cursor = None
    try:
        # Conectar sin especificar base de datos
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""  # Tu contraseña aquí si la tienes
        )
        cursor = conn.cursor()
        
        # Crear base de datos si no existe
        cursor.execute("CREATE DATABASE IF NOT EXISTS datagrow")
        print("Base de datos 'datagrow' creada/verificada")
        
        # Usar la base de datos
        cursor.execute("USE datagrow")
        
        # Crear tabla de actividades
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

# Función para obtener conexión a la base de datos
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Tu contraseña aquí si la tienes
            database="datagrow"
        )
        return conn
    except Error as e:
        print(f"Error de conexión: {e}")
        return None

# Crear DB y tablas al iniciar la aplicación
@app.on_event("startup")
def startup_event():
    if not create_db_and_tables():
        raise RuntimeError("No se pudo crear la base de datos o tablas")

# Endpoint para obtener todas las actividades
@app.get("/actividades")
def get_actividades():
    conn = create_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM actividades")
        actividades = cursor.fetchall()
        return actividades
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Endpoint para obtener una actividad por ID
@app.get("/actividades/{id}")
def get_actividad(id: int):
    conn = create_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM actividades WHERE id = %s", (id,))
        actividad = cursor.fetchone()
        if not actividad:
            raise HTTPException(status_code=404, detail="Actividad no encontrada")
        return actividad
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Endpoint para crear una nueva actividad
@app.post("/actividades")
def create_actividad(actividad: Actividad):
    conn = create_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO actividades (cultivo, tarea, fecha, estado, descripcion)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (actividad.cultivo, actividad.tarea, actividad.fecha, 
             actividad.estado, actividad.descripcion)
        )
        conn.commit()
        return {"message": "Actividad creada exitosamente"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Endpoint para actualizar una actividad
@app.put("/actividades/{id}")
def update_actividad(id: int, actividad: Actividad):
    conn = create_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE actividades
            SET cultivo = %s, tarea = %s, fecha = %s, 
                estado = %s, descripcion = %s
            WHERE id = %s
            """,
            (actividad.cultivo, actividad.tarea, actividad.fecha, 
             actividad.estado, actividad.descripcion, id)
        )
        conn.commit()
        return {"message": "Actividad actualizada exitosamente"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Endpoint para eliminar una actividad
@app.delete("/actividades/{id}")
def delete_actividad(id: int):
    conn = create_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM actividades WHERE id = %s", (id,))
        conn.commit()
        return {"message": "Actividad eliminada exitosamente"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Para ejecutar directamente con Python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)