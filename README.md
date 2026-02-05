# Lumina 🧠✨ (MVP)

**Lumina** es un prototipo de plataforma educativa impulsada por IA.  
En esta fase inicial (MVP), el sistema toma documentación técnica en formato **PDF** y utiliza la inteligencia artificial de **Google Gemini** para transformarla automáticamente en módulos de aprendizaje estructurados y fáciles de digerir.

Actualmente, el proyecto se encuentra en una fase **experimental**, enfocada en validar la generación automática de contenido educativo a partir de documentación técnica.

---

## 🚀 Funcionalidades Actuales

- **Ingestión de documentación**  
  Procesa archivos PDF de documentación técnica (configuración local).

- **Generación con IA**  
  Utiliza modelos avanzados (Gemini 2.0 / 1.5) para crear:
  - Lecciones
  - Quizzes
  - Resúmenes

- **Cálculo de costos**  
  Estima el costo de tokens de entrada y salida por cada lección generada.

- **Stack moderno**  
  Backend en FastAPI (Python) y frontend con React Router v7.

---

## 🛠️ Tech Stack

### Backend
- Python 3.10+
- FastAPI
- `uv` (gestor de paquetes)
- PyMuPDF (lectura de PDFs)

### IA
- Google Gemini (vía adaptador OpenAI)

### Frontend
- React 19
- React Router v7
- Tailwind CSS v4
- Vite

---

## 📋 Prerrequisitos

- Python 3.10 o superior
- Node.js v20+
- API Key de **Google Gemini**
- Gestor de paquetes `uv` (opcional, pero recomendado)

---

## ⚙️ Instalación y Configuración

Sigue estos pasos para levantar el entorno de desarrollo.

---

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/lumina.git
cd lumina
````

---

### 2. Configurar el Backend

El backend gestiona la lógica de la IA y la lectura de archivos PDF.

```bash
cd backend
```

#### Opción A: Usando `uv` (recomendado)

```bash
uv sync
```

#### Opción B: Usando `pip` tradicional

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e .
```

---

### Variables de entorno

Crea un archivo `.env` en la carpeta `backend` basado en el ejemplo:

```bash
cp .env.example .env
```

Edita el archivo `.env` y agrega tu API Key:

```env
GEMINI_API_KEY=tu_api_key_aqui
AI_MODEL=gemini-2.0-flash  # o gemini-1.5-flash
DEBUG=true
```

---

### ⚠️ Importante (Fase MVP)

Actualmente, el sistema **no cuenta con un botón de subida de archivos** en la interfaz.

Debes colocar manualmente tu archivo PDF de documentación en la ruta que espera el servicio.
Por defecto, revisa:

* `backend/assets`
* o la raíz del proyecto

(depende de la configuración en `pdf_service.py`).

---

### 3. Configurar el Frontend

```bash
cd ../frontend
npm install
```

---

## ▶️ Ejecución

Necesitarás **dos terminales** abiertas para correr el proyecto completo.

---

### Terminal 1: Backend (API)

```bash
cd backend

# Con uv
uv run fastapi dev app/main.py

# Con pip
fastapi dev app/main.py
```

El backend estará disponible en:

```
http://localhost:8000
```

---

### Terminal 2: Frontend (UI)

```bash
cd frontend
npm run dev
```

---

## 🧪 Estado del Proyecto

Este proyecto se encuentra en fase **MVP / experimental**.
El objetivo principal es validar el flujo de:

**PDF técnico → IA → contenido educativo estructurado**.

---

## 📌 Próximos pasos (ideas)

* Subida de archivos desde la UI
* Persistencia de cursos y lecciones
* Autenticación de usuarios
* Exportación de contenido
* Métricas de aprendizaje
