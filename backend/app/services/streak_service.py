from datetime import datetime, timedelta
from app.db import mongo


async def update_streak(user_id: str):

    users = mongo.db.users

    user = await users.find_one({"user_id": user_id})

    today = datetime.utcnow().date()

    if not user:
        await users.insert_one({
            "user_id": user_id,
            "streak": 1,
            "last_active": today.isoformat()
        })
        return 1

    last_active = datetime.fromisoformat(user["last_active"]).date()

    if last_active == today:
        return user["streak"]

    if last_active == today - timedelta(days=1):
        new_streak = user["streak"] + 1
    else:
        new_streak = 1

    await users.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "streak": new_streak,
                "last_active": today.isoformat()
            }
        }
    )

    return new_streak
