from pydantic import BaseModel, Field

class LessonRequest(BaseModel):
    lesson_prompt: str = Field(
        ...,
        description="Lo que el usuario quiere aprender",
        example="Quiero aprender a crear DataFrames en Polars"
    )


class CostInfo(BaseModel):
    input_tokens: int
    output_tokens: int
    total_cost_usd: float


class LessonResponse(BaseModel):
    lesson: str
    cost_info: CostInfo