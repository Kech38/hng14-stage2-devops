import redis
import time
import os
import signal
import sys

redis_password = os.getenv("REDIS_PASSWORD", None)
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=redis_password if redis_password else None
)


def handle_shutdown(signum, frame):
    print("Shutting down worker gracefully...")
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)


def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")


while True:
    try:
        job = r.brpop("job", timeout=5)
        if job:
            _, job_id = job
            process_job(job_id.decode())
    except Exception as e:
        print(f"Error processing job: {e}")
        time.sleep(1)
        