from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

# Importas tu inicializador de base de datos
from Backend.database import create_db_and_tables

# Ejecutar creación de BD y tabla
create_db_and_tables()

#  Crear instancia de FastAPI
app = FastAPI()

# Habilitar CORS para frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O restringe si quieres
    allow_methods=["*"],
    allow_headers=["*"],
)

# Función para abrir conexión
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", #DEBE COLOCAR LA CONTRASEÑA QUE LE PUSO A SU SQL
        database="datagrow"
    )

# Pydantic Model para validar datos
class Actividad(BaseModel):
    cultivo: str
    tarea: str
    fecha: str  # Puedes usar datetime si quieres
    estado: str
    descripcion: str

# GET all actividades
@app.get("/actividades", response_model=List[dict])
def get_actividades():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM actividades")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# 📥 GET actividad by ID
@app.get("/actividades/{actividad_id}")
def get_actividad(actividad_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM actividades WHERE id = %s", (actividad_id,))
    act = cursor.fetchone()
    cursor.close()
    conn.close()
    if not act:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return act

# POST crear actividad
@app.post("/actividades")
def create_actividad(act: Actividad):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO actividades (cultivo, tarea, fecha, estado, descripcion) VALUES (%s, %s, %s, %s, %s)",
        (act.cultivo, act.tarea, act.fecha, act.estado, act.descripcion)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Actividad creada"}

# PUT actualizar actividad
@app.put("/actividades/{actividad_id}")
def update_actividad(actividad_id: int, act: Actividad):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE actividades SET cultivo=%s, tarea=%s, fecha=%s, estado=%s, descripcion=%s WHERE id=%s",
        (act.cultivo, act.tarea, act.fecha, act.estado, act.descripcion, actividad_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Actividad actualizada"}

# DELETE eliminar actividad
@app.delete("/actividades/{actividad_id}")
def delete_actividad(actividad_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM actividades WHERE id=%s", (actividad_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Actividad eliminada"}