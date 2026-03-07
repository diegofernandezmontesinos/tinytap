from fastapi import APIRouter
from app.services.progress_service import get_user_progress

router = APIRouter()


@router.get("/user/progress/{user_id}")
async def user_progress(user_id: str):
    return await get_user_progress(user_id)
