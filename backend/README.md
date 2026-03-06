# TinyTap Backend

Mini app educativa inspirada en Duolingo para niños (~2 años). Este repositorio contiene el backend del proyecto.

## Stack

* Python
* FastAPI
* MongoDB
* Docker
* Motor (driver async para Mongo)

## Objetivo MVP

1. Backend que almacene:

   * score
   * XP
   * respuestas correctas
2. API simple para el frontend
3. Base de datos MongoDB

---

# 1. Crear proyecto

```bash
mkdir tinytap
cd tinytap
mkdir backend
cd backend
```

---

# 2. Crear entorno virtual

```bash
python3 -m venv venv
```

Activar:

```bash
source venv/bin/activate
```

Motivo:

El entorno virtual aísla las dependencias del proyecto para evitar conflictos con otros proyectos de Python.

---

# 3. Inicializar git

```bash
git init
```

Crear `.gitignore`:

```
venv/
__pycache__/
.env
.pytest_cache/
```

---

# 4. MongoDB con Docker

Crear `docker-compose.yml` en la raíz del proyecto:

```yaml
services:
  mongo:
    image: mongo:6
    container_name: tinytap_mongo
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

Levantar contenedor:

```bash
docker compose up -d
```

Ver contenedores:

```bash
docker ps
```

Motivo:

Docker nos permite ejecutar MongoDB sin instalarlo directamente en el sistema.

---

# 5. Probar conexión Mongo con Python

Instalar driver:

```bash
pip install pymongo
```

Archivo `test_mongo.py`:

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["tinytap"]
collection = db["test"]

result = collection.insert_one({"message": "Mongo connected successfully 🚀"})

print("Inserted document id:", result.inserted_id)

for doc in collection.find():
    print(doc)
```

Ejecutar:

```bash
python3 test_mongo.py
```

Motivo:

Confirmar que Python puede comunicarse correctamente con MongoDB.

---

# 6. Instalar FastAPI

```bash
pip install fastapi uvicorn
```

Motivo:

* FastAPI: framework web para construir APIs
* Uvicorn: servidor ASGI que ejecuta FastAPI

Arquitectura:

Client -> Uvicorn -> FastAPI -> MongoDB

---

# 7. Crear API básica

Archivo `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "TinyTap API running 🚀"}
```

Ejecutar servidor:

```bash
uvicorn main:app --reload
```

Abrir en navegador:

```
http://localhost:8000
```

Docs automáticas:

```
http://localhost:8000/docs
```

Motivo:

FastAPI genera documentación automática y facilita probar endpoints sin frontend.

---

# Estado actual

✔ Mongo funcionando en Docker
✔ Conexión Python → Mongo
✔ API FastAPI funcionando
✔ Documentación Swagger disponible

---

# Próximos pasos

1. Conectar MongoDB dentro de FastAPI
2. Crear modelos de datos
3. Endpoint para guardar resultados de ejercicios
4. Endpoint para obtener progreso del usuario
5. Preparar API para frontend React
