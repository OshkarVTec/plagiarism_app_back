FROM python:3.10
COPY --from=ghcr.io/astral-sh/uv:0.7.7 /uv /uvx /bin/

WORKDIR /app
ENV PYTHONPATH=/app/src
COPY uv.lock .
COPY pyproject.toml .
RUN uv venv
RUN uv sync

# Copy the project into the image
ADD . /app

CMD ["uv", "run", "uvicorn", "main:app","--reload", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]
