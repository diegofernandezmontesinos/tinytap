from app.repositories.exercise_result_repository import ExerciseResultRepository


async def get_user_progress(user_id: str):

    result = await ExerciseResultRepository.get_user_progress(user_id)

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
