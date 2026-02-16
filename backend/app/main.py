from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import docs, lessons

app = FastAPI(
    title="Lumina API",
    description="AI-Powered learning modules",
    version="0.1.0"
)

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(lessons.router, prefix="/api/lessons", tags=["lessons"])
app.include_router(docs.router, prefix="/api/docs", tags=["docs"])
