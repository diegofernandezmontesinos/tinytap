# TinyTap Backend

Mini app educativa inspirada en Duolingo para niños (~2 años).
Backend completo construido con:

* Python 3.10+
* FastAPI
* MongoDB (async con Motor)
* Docker
* Pydantic
* Uvicorn
* VS Code Mongo Extension

---

# 🎯 Objetivo MVP

El backend debe permitir:

* Guardar resultados de ejercicios
* Calcular progreso automáticamente
* Gestionar ejercicios
* Entregar ejercicios al frontend
* Sistema de streaks
* Analítica básica

Si esto funciona, el frontend puede construirse sin bloqueos.

---

# 🏗 Arquitectura Actual

```
backend
│
├── .env
├── docker-compose.yml
├── requirements.txt
│
└── app
    ├── main.py
    ├── core
    │   └── config.py
    ├── db
    │   └── mongo.py
    ├── schemas
    │   └── exercise.py
    ├── services
    │   ├── exercise_service.py
    │   └── progress_service.py
    └── routes
        ├── exercise_routes.py
        └── progress_routes.py
```

Arquitectura basada en separación de responsabilidades:

* routes → endpoints API
* services → lógica de negocio
* schemas → validación
* db → conexión Mongo
* core → configuración

---

# 🚀 1. Crear Proyecto

```bash
mkdir tinytap
cd tinytap
mkdir backend
cd backend
```

Motivo: separar backend y frontend desde el inicio.

---

# 🔐 2. Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

¿Por qué?

Aísla dependencias del proyecto y evita conflictos globales.

---

# 🧱 3. Git

```bash
git init
```

`.gitignore` recomendado:

```
venv/
__pycache__/
.env
.pytest_cache/
```

---

# 🐳 4. MongoDB con Docker

`docker-compose.yml`

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

Levantar:

```bash
docker compose up -d
docker ps
```

Motivo: ejecutar Mongo sin instalarlo manualmente y con persistencia.

---

# 🗄 5. Configuración .env

```
MONGO_URL=mongodb://localhost:27017
DB_NAME=tinytap
```

`app/core/config.py`

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGO_URL: str
    DB_NAME: str

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
    )

settings = Settings()
```

Motivo: separar configuración sensible y facilitar despliegue.

---

# 🔌 6. Conexión Mongo Async

`app/db/mongo.py`

```python
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client: AsyncIOMotorClient = None
mdb = None

async def connect_to_mongo():
    global client, mdb
    client = AsyncIOMotorClient(settings.MONGO_URL)
    mdb = client[settings.DB_NAME]
    print("✅ Connected to MongoDB")

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("❌ MongoDB connection closed")
```

Importante: usar `mdb` para evitar problemas de referencia.

---

# 📦 7. Sistema de Ejercicios

## Schema

`app/schemas/exercise.py`

```python
from pydantic import BaseModel

class ExerciseResult(BaseModel):
    user_id: str
    exercise_id: str
    correct: bool
    response_time_ms: int
```

Validación automática de requests.

---

## Service

`app/services/exercise_service.py`

```python
from datetime import datetime
from app.db import mongo

async def save_exercise_result(data):

    xp = 10 if data.correct else 0

    document = {
        "user_id": data.user_id,
        "exercise_id": data.exercise_id,
        "correct": data.correct,
        "xp": xp,
        "response_time_ms": data.response_time_ms,
        "timestamp": datetime.utcnow()
    }

    result = await mongo.mdb.exercise_results.insert_one(document)

    return {
        "status": "saved",
        "xp": xp,
        "id": str(result.inserted_id)
    }
```

Motivo: lógica de negocio separada del endpoint.

---

## Route

`app/routes/exercise_routes.py`

```python
from fastapi import APIRouter
from app.schemas.exercise import ExerciseResult
from app.services.exercise_service import save_exercise_result

router = APIRouter()

@router.post("/exercise/result")
async def save_result(data: ExerciseResult):
    return await save_exercise_result(data)
```

---

# 📊 8. Progreso del Usuario (Aggregation Pipeline)

## Service

`app/services/progress_service.py`

```python
from app.db import mongo

async def get_user_progress(user_id: str):

    pipeline = [
        {"$match": {"user_id": user_id}},
        {
            "$group": {
                "_id": "$user_id",
                "exercises_done": {"$sum": 1},
                "total_xp": {"$sum": "$xp"},
                "correct_answers": {
                    "$sum": {"$cond": ["$correct", 1, 0]}
                },
                "avg_response_time": {"$avg": "$response_time_ms"}
            }
        }
    ]

    result = await mongo.mdb.exercise_results.aggregate(pipeline).to_list(1)

    if not result:
        return {
            "user_id": user_id,
            "exercises_done": 0,
            "total_xp": 0,
            "accuracy": 0,
            "avg_response_time": 0
        }

    data = result[0]

    accuracy = data["correct_answers"] / data["exercises_done"]

    return {
        "user_id": user_id,
        "exercises_done": data["exercises_done"],
        "total_xp": data["total_xp"],
        "accuracy": accuracy,
        "avg_response_time": data["avg_response_time"]
    }
```

---

## Route

`app/routes/progress_routes.py`

```python
from fastapi import APIRouter
from app.services.progress_service import get_user_progress

router = APIRouter()

@router.get("/user/progress/{user_id}")
async def user_progress(user_id: str):
    return await get_user_progress(user_id)
```

---

# 🚀 9. Main Application

`app/main.py`

```python
from fastapi import FastAPI
from app.db.mongo import connect_to_mongo, close_mongo_connection
from app.routes.exercise_routes import router as exercise_router
from app.routes.progress_routes import router as progress_router

app = FastAPI()

app.include_router(exercise_router)
app.include_router(progress_router)

@app.on_event("startup")
async def startup_db():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db():
    await close_mongo_connection()
```

---

# 🔎 Cómo Ver los Datos

## Terminal

```bash
docker exec -it tinytap_mongo mongosh
use tinytap
show collections
db.exercise_results.find().pretty()
```

## MongoDB Compass

Connection:

```
mongodb://localhost:27017
```

## VS Code Mongo Extension

Add connection:

```
mongodb://localhost:27017
```

---

# ✅ Estado Actual

✔ Backend funcionando
✔ Mongo async conectado
✔ Guardar resultados
✔ Calcular progreso con agregaciones
✔ Swagger disponible

El backend ya es funcional y preparado para frontend.

---

# 🛣 Próximos Pasos (Orden Correcto)

1. Crear colección `exercises`
2. Endpoint `GET /exercises`
3. Endpoint `GET /session/next`
4. Sistema de streaks
5. Crear índices en Mongo
6. Empezar frontend React

---

# 🔐 PROMPT DE CONTEXTO (Guardar esto)

Si en el futuro necesito recuperar el estado del proyecto, usa este prompt:

> Estamos desarrollando TinyTap, una mini app educativa tipo Duolingo para niños (~2 años).
> Backend actual: FastAPI async + MongoDB Docker + Motor.
> Ya tenemos endpoints:
>
> * POST /exercise/result
> * GET /user/progress/{user_id}
>   Con agregaciones Mongo funcionando.
>   Arquitectura separada en routes/services/schemas/db.
>   Próximo paso: crear colección exercises y sistema de entrega de ejercicios.

---

Proyecto en estado intermedio pero estructuralmente sólido.
