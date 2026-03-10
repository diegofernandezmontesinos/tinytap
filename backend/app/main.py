from fastapi import FastAPI
from app.routes.exercise_routes import router as exercise_router
from app.db.mongo import connect_to_mongo, close_mongo_connection
from app.routes.progress_routes import router as progress_router
from app.routes.exercise_content_routes import router as exercise_content_router
from app.routes.session_routes import router as session_router
from app.routes.streak_routes import router as streak_router



app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()



app.include_router(progress_router)
app.include_router(exercise_router)
app.include_router(exercise_content_router)
app.include_router(session_router)
app.include_router(streak_router)


