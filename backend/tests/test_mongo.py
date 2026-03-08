from pymongo import MongoClient

# Conectamos a Mongo que corre en Docker
client = MongoClient("mongodb://localhost:27017")

# Crear / acceder base de datos
db = client["tinytap_test"]

# Crear colección
collection = db["connection_test"]

# Documento de prueba
doc = {
    "message": "Mongo connected successfully 🚀"
}

# Insertar documento
result = collection.insert_one(doc)

print("Inserted document id:", result.inserted_id)

# Leer documentos
documents = list(collection.find())

print("Documents inside collection:")
for d in documents:
    print(d)

