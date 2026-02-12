# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Lumina is an AI-powered educational platform (MVP) that transforms technical documentation PDFs into structured learning modules using Google Gemini. Fullstack app with a Python/FastAPI backend and React Router v7 frontend.

## Commands

### Backend (from `backend/`)
```bash
uv sync                           # Install dependencies
uv run fastapi dev app/main.py    # Dev server at http://localhost:8000
```

### Frontend (from `frontend/`)
```bash
npm install                       # Install dependencies
npm run dev                       # Dev server at http://localhost:5173
npm run build                     # Production build
npm run typecheck                 # Type generation + type checking
```

Both servers must run simultaneously for the app to work.

## Architecture

### Backend (`backend/app/`)
- **FastAPI** app with a single endpoint: `POST /api/lessons/generate`
- **Service layer pattern**: `services/ai_service.py` (Gemini integration via OpenAI SDK), `services/pdf_service.py` (PDF-to-markdown with PyMuPDF, cached via `@lru_cache`), `services/cost_calculator.py` (token cost calculation)
- **Pydantic models** in `models/lessons.py` for request/response validation
- **Config** via `pydantic-settings` in `config.py` (reads `.env` file)
- **System prompt** in `prompts/system_prompt.py` — lessons are generated in Spanish with a specific structure
- PDF docs are stored in `backend/docs/` (currently hardcoded to `docs/polars/dataframe_documentation.pdf`)

### Frontend (`frontend/app/`)
- **React Router v7** with SSR enabled, Vite bundler, Tailwind CSS v4
- Single route in `routes/home.tsx` with a server action that calls the backend API
- Uses fetcher-based form submission (no full page reload)
- API client in `services/api.ts` — base URL hardcoded to `http://localhost:8000/api/lessons`
- TypeScript interfaces in `types/index.ts`

### Data Flow
1. User submits a learning prompt via the form
2. Server action calls `POST /api/lessons/generate` with `{ lesson_prompt }`
3. Backend loads cached PDF documentation, constructs system prompt, calls Gemini API
4. Returns generated lesson (markdown) + cost breakdown (tokens, USD)

## Environment Variables (Backend `.env`)
```
GEMINI_API_KEY=<required>
AI_MODEL=gemini-3-flash-preview
PRICE_INPUT=0.50
PRICE_OUTPUT=3.0
DEBUG=true
```

## Commit Convention
Uses gitmoji + conventional commits: `feat: :sparkles:`, `fix: :bug:`, `docs: :memo:`
