from fastapi import APIRouter
from app.services.session_service import get_next_exercise

router = APIRouter()

@router.get("/session/next")
async def next_exercise():
    return await get_next_exercise()
