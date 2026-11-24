# Background Worker

Asynchronous Python worker processing order PDFs and email notifications from Redis.

- **Stack:** Python 3.12, Celery, Redis, PostgreSQL
- **Run Worker:** `celery -A worker.app worker --loglevel=info`
- **Depends On:** Redis broker and PostgreSQL (`docker-compose.yml`)
