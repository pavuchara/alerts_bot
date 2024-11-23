import os
import logging
from datetime import timedelta

from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

# Use -> `openssl rand -hex 32`
API_KEY: str = os.getenv("API_KEY", "some_key")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_LIFETIME = timedelta(minutes=30)


# Database:
POSTGRES_DRIVER: str = os.getenv("POSTGRES_DRIVER", "asyncpg")
POSTGRES_DB: str = os.getenv("POSTGRES_DB", "test")
POSTGRES_USER: str = os.getenv("POSTGRES_USER", "test")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "test")
POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
DATABASE_URL: str = f"postgresql+{POSTGRES_DRIVER}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"
SYNC_DATABASE_URL: str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"


# Redis:
REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT: str = os.getenv("REDIS_HOST", "6379")


# Celery:
CELERY_BROCKER: str = f"redis://{REDIS_HOST}:6379/0"
CELERY_BACKEND: str = f"redis://{REDIS_PORT}:6379/0"


# RabbitMQ
RABBITMQ_DEFAULT_USER: str = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
RABBITMQ_DEFAULT_PASS: str = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")
AMQP_HOST: str = os.getenv("AMQP_HOST", "localhost")
AMQP_PORT: str = os.getenv("AMQP_PORT", "5672")

REMINDER_ROUTING_KEY: str = os.getenv("REMINDER_ROUTING_KEY", "reminder_queue")


# Logging
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)-8s: %(message)s",
    )
