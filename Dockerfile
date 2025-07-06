# ---------- builder ----------
FROM python:3.13-slim AS builder
WORKDIR /srv

# Install Poetry and create a venv INSIDE the project (./.venv)
ENV POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1
RUN python -m venv .venv \
 && . .venv/bin/activate \
 && pip install --upgrade pip \
 && pip install poetry

COPY pyproject.toml poetry.lock ./
RUN . .venv/bin/activate && \
    poetry lock && \
    poetry install --no-root

COPY app/ ./app

# ---------- runtime -----------
FROM python:3.13-slim AS runtime
WORKDIR /srv

COPY --from=builder /srv /srv

ENV PATH="/srv/.venv/bin:$PATH"

# *Production* default; can be overridden by compose-dev
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]