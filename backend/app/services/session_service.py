from app.repositories.exercise_repository import ExerciseRepository


async def get_next_exercise():

    exercise = await ExerciseRepository.get_random()

    return exercise
