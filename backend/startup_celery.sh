#!/bin/bash
celery -A celery_config:celery worker --beat --loglevel=info
