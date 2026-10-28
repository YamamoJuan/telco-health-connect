"""
Dockerfile for Telco Health Connect Payment Service.
Multi-stage build for production security and image size optimization.
"""

# Stage 1: Build stage
FROM python:3.12-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements files
COPY requirements.txt requirements-dev.txt ./

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt

# Stage 2: Production stage
FROM python:3.12-slim as production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create non-root user
RUN groupadd --gid 1001 appuser && \
    useradd --uid 1001 --gid 1001 --shell /bin/bash --create-home appuser

# Set working directory
WORKDIR /app

# Copy requirements and install minimal dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Set permissions
RUN chown -R appuser:appuser /app/
USER appuser

# Expose port
EXPOSE 8000

# Set environment variables for production
ENV PYTHONPATH="/app"

# Set entrypoint command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]