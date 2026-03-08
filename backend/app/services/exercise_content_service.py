from app.db import mongo

async def get_all_exercises():
    cursor = mongo.db.exercises.find()
    exercises = await cursor.to_list(length=100)

    for ex in exercises:
        ex["_id"] = str(ex["_id"])

    return exercises
