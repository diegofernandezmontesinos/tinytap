from app.db import mongo


class ExerciseResultRepository:

    @staticmethod
    async def insert_result(document):

        result = await mongo.db.exercise_results.insert_one(document)

        return result


    @staticmethod
    async def get_user_progress(user_id: str):

        pipeline = [
            {
                "$match": {"user_id": user_id}
            },
            {
                "$group": {
                    "_id": "$user_id",
                    "exercises_done": {"$sum": 1},
                    "total_xp": {"$sum": "$xp"},
                    "correct_answers": {
                        "$sum": {
                            "$cond": ["$correct", 1, 0]
                        }
                    },
                    "avg_response_time": {
                        "$avg": "$response_time_ms"
                    }
                }
            }
        ]

        result = await mongo.db.exercise_results.aggregate(pipeline).to_list(1)

        return result
