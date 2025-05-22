FROM python:latest
COPY --from=ghcr.io/astral-sh/uv:0.7.7 /uv /uvx /bin/

WORKDIR /app
ENV PYTHONPATH=/app/src
COPY uv.lock .
COPY pyproject.toml .
RUN uv venv
RUN uv sync

# Copy the project into the image
ADD . /app

CMD ["uv", "run", "uvicorn", "src.routes:app", "--host", "0.0.0.0", "--port", "8000"]