FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim AS production
WORKDIR /app
RUN addgroup --system appgroup && adduser --system --group appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY . .
RUN chown -R appuser:appgroup /app
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
HEALTHCHECK --interval=15s --timeout=10s --start-period=40s --retries=5 \
    CMD python -c "import redis; import os; r = redis.Redis(host=os.getenv('REDIS_HOST','redis')); r.ping()" || exit 1
CMD ["python", "worker.py"]
