# FAQ Chatbot

AI-powered FAQ chatbot with FastAPI backend and Streamlit frontend.

## Setup

1. Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```
   - Set `GROQ_API_KEY` for Groq mode
   - Set `USE_MOCK=true` for mock mode (no API key needed)
   - Set `BUSINESS_NAME` to customize the business name in the assistant's instructions

2. Run the application:
   ```bash
   uv run python run.py
   ```

   Or run separately:
   ```bash
   # Terminal 1 - Backend
   uv run uvicorn backend.main:app --reload --reload-include=.* --port 8000
   
   # Terminal 2 - Frontend
   uv run streamlit run frontend/app.py --server.port 8501
   ```

Both the backend and frontend load all values from `.env` at startup, with `.env` values taking precedence over inherited process environment variables. Restart the affected server after changing `.env` for the changes to take effect.

## Usage

- Open http://localhost:8501 for the chat interface
- API docs at http://localhost:8000/docs
- Health check at http://localhost:8000/health

## API Endpoints

- `POST /chat` - Send a message, get FAQ response
- `GET /health` - Check service status

## Modes

- **Mock** (`USE_MOCK=true`): Uses built-in FAQ responses
- **Groq** (`USE_MOCK=false`): Uses Groq LLM API (requires API key)