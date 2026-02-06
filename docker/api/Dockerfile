FROM python:3.11-slim AS builder 
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==1.8.5 

COPY ./api/pyproject.toml ./api/poetry.lock api/README.md /app/api/
WORKDIR /app/api 

RUN poetry export -f requirements.txt --only main --without-hashes -o /app/requirements.txt

FROM python:3.11-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*


COPY --from=builder /app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt


COPY api/src /app/src


ENV PYTHONPATH=/app/src

EXPOSE 8001

CMD ["python", "-m", "uvicorn", "bank_api.main:app", "--host", "0.0.0.0", "--port", "8001"]