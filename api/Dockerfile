# Stage 1: Install dependencies
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production image
FROM python:3.11-slim AS production
WORKDIR /app

# Create non-root user
RUN addgroup --system appgroup && adduser --system --group appuser

# Copy installed packages and app files
COPY --from=builder /root/.local /home/appuser/.local
COPY . .

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set correct ownership
RUN chown -R appuser:appgroup /app
USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=10s --start-period=40s --retries=5 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]