from app.db import mongo
import random

async def get_next_exercise():

    cursor = mongo.db.exercises.find()
    exercises = await cursor.to_list(length=100)

    if not exercises:
        return None

    exercise = random.choice(exercises)

    exercise["_id"] = str(exercise["_id"])

    return exercise
