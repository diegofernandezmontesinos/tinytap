from fastapi import APIRouter
from app.services.exercise_content_service import get_all_exercises

router = APIRouter()


@router.get("/exercises")
async def list_exercises():

    return await get_all_exercises()
