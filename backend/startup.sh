#!/bin/bash
alembic upgrade head
# gunicorn main:app \
#     --workers 4 \
#     --worker-class uvicorn.workers.UvicornWorker \
#     --bind 0.0.0.0:8000 \
#     --access-logfile '-' \
#     --error-logfile '-' \
#     --log-level 'info'

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
