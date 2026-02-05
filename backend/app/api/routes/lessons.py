from fastapi import APIRouter, Depends
from app.config import get_settings, Settings
from app.models.lessons import LessonRequest, LessonResponse
from app.services.ai_service import generate_lesson_module

router = APIRouter()

@router.post("/generate", response_model=LessonResponse)
async def generate_lesson(request: LessonRequest, settings: Settings = Depends(get_settings)):
    """
    Genera un módulo de aprendizaje basado en documentación técnica.
    """
    result = await generate_lesson_module(request.lesson_prompt, settings)
    return result
