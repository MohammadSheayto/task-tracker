# Build stage: install dependencies into an isolated virtual environment
FROM python:3.11-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Runtime stage: slim image, only the venv and application code, non-root user
FROM python:3.11-slim

RUN useradd --create-home --shell /usr/sbin/nologin app

WORKDIR /home/app
COPY --from=builder /opt/venv /opt/venv
COPY app/ app/

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000
USER app

# No --reload in containers: reload is a development-only feature
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
