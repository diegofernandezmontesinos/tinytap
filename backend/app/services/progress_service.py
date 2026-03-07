from app.db import mongo


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

    if not result:
        return {
            "user_id": user_id,
            "exercises_done": 0,
            "accuracy": 0,
            "total_xp": 0,
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
