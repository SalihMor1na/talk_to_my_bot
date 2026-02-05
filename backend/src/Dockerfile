FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY backend backend
COPY frontend frontend
COPY knowledge_base knowledge_base
COPY data data
COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev

WORKDIR /app/backend

WORKDIR /app

ENV PYTHONPATH=/app

CMD ["uv","run","uvicorn","backend.src.api:app","--host","0.0.0.0","--port","8000"]


