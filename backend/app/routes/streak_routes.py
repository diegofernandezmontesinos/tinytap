from fastapi import APIRouter
from app.services.streak_service import update_streak

router = APIRouter()


@router.post("/streak/{user_id}")
async def streak(user_id: str):

    streak = await update_streak(user_id)

    return {
        "user_id": user_id,
        "streak": streak
    }
