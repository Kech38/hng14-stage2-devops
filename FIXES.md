# FIXES.md

## Fix 1
- **File:** api/main.py
- **Line:** 8
- **Problem:** Redis host hardcoded as "localhost" — fails inside Docker containers
  because each service has its own network namespace and cannot reach other 
  services via localhost
- **Fix:** Changed to `os.getenv("REDIS_HOST", "redis")`

## Fix 2
- **File:** api/requirements.txt
- **Line:** 1-3
- **Problem:** Package versions unpinned using "^" — can cause unexpected breakage 
  in production when new versions are released automatically
- **Fix:** Pinned exact versions and added missing python-multipart package

## Fix 3
- **File:** worker/worker.py
- **Line:** 14
- **Problem:** signal module imported but never used — no graceful shutdown 
  handling meaning the worker cannot shut down cleanly when Docker stops it.
  Also no error handling around job processing meaning a single failure 
  crashes the entire worker
- **Fix:** Added signal handlers for SIGTERM and SIGINT, wrapped job 
  processing in try/except block

## Fix 4
- **File:** frontend/app.js
- **Line:** 6
- **Problem:** API_URL hardcoded as "http://localhost:8000" — fails inside 
  Docker because the frontend container cannot reach the API container 
  via localhost
- **Fix:** Changed to `process.env.API_URL || "http://api:8000"`

## Fix 5
- **File:** frontend/app.js
- **Line:** 26
- **Problem:** Port hardcoded as 3000 — should be configurable via 
  environment variable for flexibility across environments
- **Fix:** Changed to `process.env.PORT || 3000`

## Fix 6
- **File:** frontend/app.js
- **Line:** 27
- **Problem:** Single quotes used in console.log instead of backticks — 
  causes ${PORT} to print literally as a string instead of the actual 
  port number
- **Fix:** Changed single quotes to backticks for template literal

## Fix 7
- **File:** frontend/package.json
- **Line:** 9-10
- **Problem:** Package versions use "^" caret which allows automatic 
  minor/patch updates — can cause unexpected breakage in production
- **Fix:** Removed caret and pinned exact versions

## Fix 8
- **File:** frontend/package.json
- **Problem:** Missing "engines" field — Node.js version not specified 
  meaning any version could be used causing compatibility issues
- **Fix:** Added engines field specifying Node.js >= 18.0.0

## Fix 9
- **File:** api/main.py
- **Problem:** Missing /health endpoint — required for Docker healthcheck 
  and CI/CD pipeline integration test to verify the service is running
- **Fix:** Added /health endpoint returning {"message": "healthy"}

## Fix 10
- **File:** api/main.py
- **Line:** 28
- **Problem:** get_job returns HTTP 200 with error message in body when 
  job is not found — incorrect HTTP semantics, should return 404
- **Fix:** Changed to raise HTTPException(status_code=404)

## Fix 11
- **File:** api/main.py
- **Problem:** Missing root / endpoint — pipeline integration test 
  expects a root endpoint to verify API is running
- **Fix:** Added root endpoint returning {"message": "API is running"}

## Fix 12
- **File:** worker/requirements.txt
- **Problem:** Package version unpinned — can cause unexpected breakage 
  in production when new versions are released
- **Fix:** Pinned exact version redis==5.0.3

## Fix 13
- **File:** .env
- **Problem:** .env file committed to repository — serious security issue 
  exposing credentials publicly on GitHub
- **Fix:** Added .env to .gitignore and removed from git tracking

## Fix 14
- **File:** (missing)
- **Problem:** No .gitignore file existed — sensitive files like .env 
  could be accidentally committed and pushed to GitHub
- **Fix:** Created .gitignore with essential entries for Python, 
  Node.js and Docker

## Fix 15
- **File:** .env
- **Problem:** Real Redis password committed to repository — critical 
  security vulnerability exposing credentials publicly
- **Fix:** Removed .env from git tracking, created .env.example 
  with placeholder values instead

## Fix 16
- **File:** api/main.py, worker/worker.py
- **Problem:** REDIS_PASSWORD set in .env but never used in Redis 
  connection — Redis running without authentication despite password 
  being configured
- **Fix:** Added password=os.getenv("REDIS_PASSWORD", None) to 
  Redis connection in both files
