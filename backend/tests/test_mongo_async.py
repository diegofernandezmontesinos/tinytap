import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


async def test_connection():
    # Conexión
    client = AsyncIOMotorClient("mongodb://localhost:27017")

    # Base de datos
    db = client["tinytap_async_test"]

    # Colección
    collection = db["connection_test"]

    # Documento
    doc = {
        "message": "Mongo async connected successfully 🚀"
    }

    # Insertar documento
    result = await collection.insert_one(doc)
    print("Inserted document id:", result.inserted_id)

    # Leer documentos
    documents = []
    async for document in collection.find():
        documents.append(document)

    print("Documents inside collection:")
    for d in documents:
        print(d)

    # Cerrar conexión
    client.close()


if __name__ == "__main__":
    asyncio.run(test_connection())
