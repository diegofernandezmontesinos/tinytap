from fastapi import APIRouter
from app.schemas.exercise import ExerciseResult
from app.services.exercise_service import save_exercise_result

router = APIRouter()


@router.post("/exercise/result")
async def save_result(data: ExerciseResult):
    return await save_exercise_result(data)
