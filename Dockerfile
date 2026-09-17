FROM python:3.13

WORKDIR /app

COPY app ./app
COPY pyproject.toml uv.lock ./
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN uv sync

CMD ["uv", "run", "uvicorn", "app.main:app",  "--host", "0.0.0.0", "--port", "8000"]