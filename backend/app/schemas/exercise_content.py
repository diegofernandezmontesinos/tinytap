from pydantic import BaseModel
from typing import Optional


class Exercise(BaseModel):
    exercise_id: str
    type: str
    question: str
    image_url: Optional[str]
    correct_answer: str
    difficulty: int
    language: str
