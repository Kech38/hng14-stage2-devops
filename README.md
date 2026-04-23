# hng14-stage2-devops
# HNG Stage 2 - Containerized Microservices Application

A job processing system made up of four services, containerized with Docker and deployed with a full CI/CD pipeline.

## Services
- **Frontend** (Node.js/Express) — where users submit and track jobs
- **API** (Python/FastAPI) — creates jobs and serves status updates
- **Worker** (Python) — picks up and processes jobs from the queue
- **Redis** — shared message queue between API and worker

## Prerequisites
- Docker Desktop installed and running
- Docker Compose v2+
- Git

## How to Run Locally

### 1. Clone the repository
git clone https://github.com/Kech38/hng14-stage2-devops.git

cd hng14-stage2-devops

### 2. Set up environment variables
cp .env.example .env

Edit `.env` and fill in your values.

### 3. Start the stack
docker compose up --build

### 4. What a successful startup looks like
You should see all four services start in order:
- Redis starts first and becomes healthy
- API and Worker start after Redis is healthy
- Frontend starts after API is healthy

All services will show as running:
✔ Container redis     healthy
✔ Container api       healthy
✔ Container worker    running
✔ Container frontend  healthy
Visit `http://localhost:3000` in your browser to use the application.

### 5. Stop the stack
docker compose down

## API Endpoints

### GET /
Returns API status.
{"message": "API is running"}

### GET /health
Returns health status.
{"message": "healthy"}

### POST /jobs
Creates a new job.
{"job_id": "uuid-here"}

### GET /jobs/{job_id}
Returns job status.
{"job_id": "uuid-here", "status": "completed"}

## Live Deployment URL
https://hngdevops.chickenkiller.com

## CI/CD Pipeline
The GitHub Actions pipeline runs these stages in order:
1. **Lint** — Python (flake8), JavaScript (eslint), Dockerfiles (hadolint)
2. **Test** — pytest with Redis mocked, coverage report uploaded as artifact
3. **Build** — builds all images, tags with git SHA and latest, pushes to registry
4. **Security** — Trivy scan, fails on CRITICAL findings, uploads SARIF artifact
5. **Integration** — brings full stack up, submits a job, verifies completion
6. **Deploy** — rolling update to server on pushes to main only

