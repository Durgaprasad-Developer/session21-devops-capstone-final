# ── Build stage ────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Runtime stage ──────────────────────────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# Non-root user
RUN addgroup --system bookease && adduser --system --ingroup bookease bookease

# Copy installed packages
COPY --from=builder /install /usr/local

# Copy application code and migrations
COPY alembic/ ./alembic/
COPY alembic.ini .
COPY app/ ./app/

# Set ownership
RUN chown -R bookease:bookease /app

USER bookease

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

# Run Alembic migrations then start Uvicorn
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
