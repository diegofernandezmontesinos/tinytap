from pydantic import BaseModel


class ExerciseResult(BaseModel):
    user_id: str
    exercise_id: str
    correct: bool
    response_time_ms: int
