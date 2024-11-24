import os
import logging
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

# TG credentials:
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "some_token")

# API credentials:
API_KEY: str = os.getenv("API_KEY", "some_token")
ALGORITHM: str = os.getenv("ALGORITHM", "some_token")
ACCESS_TOKEN_LIFETIME = timedelta(minutes=30)

# Backend service:
BACKEND_DOMEN: str = os.getenv("BACKEND_DOMEN", "localhost")
BACKEND_PORT: str = os.getenv("BACKEND_PORT", "8000")
BACKEND_URI: str = f"http://{BACKEND_DOMEN}:{BACKEND_PORT}/api"


# AMQP settings:
RABBITMQ_DEFAULT_USER: str = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
RABBITMQ_DEFAULT_PASS: str = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")
AMQP_HOST: str = os.getenv("AMQP_HOST", "localhost")
AMQP_PORT: str = os.getenv("AMQP_PORT", "5672")
AMQP_URL: str = f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{AMQP_HOST}:{AMQP_PORT}//"
REMINDER_ROUTING_KEY: str = os.getenv("REMINDER_ROUTING_KEY", "reminder_queue")


# Redis cache settings:
REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB: str = "1"


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)-8s: %(message)s",
    )
