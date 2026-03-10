from app.db import mongo


class ExerciseRepository:

    @staticmethod
    async def get_all():

        cursor = mongo.db.exercises.find()

        exercises = [doc async for doc in cursor]

        return exercises


    @staticmethod
    async def get_random():

        cursor = mongo.db.exercises.aggregate([
            {"$sample": {"size": 1}}
        ])

        result = [doc async for doc in cursor]

        return result[0] if result else None
