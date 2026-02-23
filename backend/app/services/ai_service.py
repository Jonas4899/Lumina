from openai import AsyncOpenAI
from app.config import Settings
from app.services.cost_calculator import calculate_cost
from app.services.retrieval_service import retrieve_relevant_chunks, format_chunks_as_context
from app.prompts.system_prompt import LESSON_GENERATOR_PROMPT

async def generate_lesson_module(user_query: str, settings: Settings):
    """
    Genera un modulo de aprendizaje usando Gemini.
    """

    client = AsyncOpenAI(
        api_key = settings.gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    chunks = await retrieve_relevant_chunks(user_query, settings)
    documentation = format_chunks_as_context(chunks)

    system_prompt = LESSON_GENERATOR_PROMPT.format(documentation=documentation)

    response = await client.chat.completions.create(
        model=settings.ai_model,
        messages=[
            {   "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )

    cost_info = calculate_cost(response, settings)

    return {
        "lesson": response.choices[0].message.content,
        "cost_info": cost_info
    }