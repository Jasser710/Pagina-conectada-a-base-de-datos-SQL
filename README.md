# 🌱 DataGrow - Dashboard Agrícola Sostenible

Este proyecto es una aplicación web para gestionar actividades agrícolas de forma sencilla, conectada a una base de datos **MySQL**.

---

## 🚀 ¿Qué hace?

✅ Permite registrar, consultar, actualizar y eliminar actividades agrícolas.  
✅ Guarda los datos en una base de datos MySQL llamada **`datagrow`**.  
✅ Incluye un **frontend** (`index.html` + `script.js`) y un **backend** (`main.py` con FastAPI).

---

## 📦 Estructura del proyecto

```
📁 Pagina-conectada-a-base-de-datos-SQL/
 ├── 📁 frontend/
 │    ├── index.html
 │    ├── styles.css
 │    └── script.js
 ├── 📁 backend/
 │    ├── main.py
 │    ├── __init__.py
 │    ├── database.py
 ├──requirements.txt
 └── README.md

```

---

## ⚙️ Requisitos

- Python 3.x
- MySQL Server instalado y corriendo
- `mysql-connector-python` (`pip install mysql-connector-python`)
- `fastapi` y `uvicorn` (`pip install fastapi uvicorn`)

---

## 🗂️ Preparación de la base de datos

El proyecto incluye un archivo `database.py` que **crea la base de datos y la tabla automáticamente**.  
No necesitas crear nada manualmente si corres FastAPI con `main.py`.

---

## 🛠️ 🔑 Configuración IMPORTANTE

👉 **Debes configurar tu contraseña de MySQL:**

Abre el archivo `main.py` y busca la función:

```py
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", # ⚠️ DEBE COLOCAR AQUÍ SU CONTRASEÑA DE MySQL
        database="datagrow"
    )
```

➡️ Debes colocar tú contraseña  entre las comillas `password="tu_contraseña"` para entrar a tu servidor MySQL.  
Si no tienes contraseña, deja `""`, pero lo recomendado es tener una.

---

## 🚦 ¿Cómo correrlo?

1️⃣ Instala dependencias:
```bash
pip install fastapi uvicorn mysql-connector-python
```

2️⃣ Ejecuta el backend:
```bash
uvicorn backend.main:app --reload
```

3️⃣ Abre `index.html` en tu navegador.

4️⃣ Usa la web: agrega actividades, edita o elimina.  
La información se guarda en la base de datos **datagrow**.

---

## 🧹 Comandos útiles para gestionar la tabla

Si quieres **borrar todos los registros**:

```sql
DELETE FROM actividades;
ALTER TABLE actividades AUTO_INCREMENT = 1;
```

---

## 📝 Notas finales

- La API REST está disponible en [http://localhost:8000/docs](http://localhost:8000/docs).
- Desde ahí puedes probar todos los endpoints: `GET`, `POST`, `PUT`, `DELETE`.
- El frontend (`index.html`) se comunica con FastAPI vía `fetch` en `script.js`.

---


Participantes 

Jason Barrantes, Jasser Palacios, Junior Ramírez, Melany Ramírez
