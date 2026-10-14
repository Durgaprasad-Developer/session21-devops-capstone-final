# ── Build stage ────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Runtime stage ──────────────────────────────────────────────────────────────
FROM python:3.12-slim

# Apply OS security updates
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Non-root user
RUN addgroup --system bookease && adduser --system --ingroup bookease bookease

# Copy installed packages
COPY --from=builder /install /usr/local

# Copy application code, migrations, tests, and entrypoint
COPY alembic/ ./alembic/
COPY alembic.ini .
COPY app/ ./app/
COPY tests/ ./tests/
COPY pytest.ini .
COPY entrypoint.sh .

# Set ownership and execute permissions
RUN chmod +x /app/entrypoint.sh && chown -R bookease:bookease /app

USER bookease

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

