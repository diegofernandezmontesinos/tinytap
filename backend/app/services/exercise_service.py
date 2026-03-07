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

    result = await mongo.db.exercise_results.insert_one(document)


    return {
        "status": "saved",
        "xp": xp,
        "id": str(result.inserted_id)
    }
