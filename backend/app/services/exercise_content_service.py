from app.repositories.exercise_repository import ExerciseRepository


async def get_all_exercises():

    exercises = await ExerciseRepository.get_all()

    return exercises
