FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY backend backend
COPY frontend frontend
COPY data data
COPY knowledge_base knowledge_base
COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev

WORKDIR /app/frontend

CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
