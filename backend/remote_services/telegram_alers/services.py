import json
import logging
import uuid
from abc import ABC, abstractmethod
from typing import Any

import pika

import config
from remote_services.amqp_connector import RabbitAMQPConnector

log = logging.getLogger(__name__)


class AbstractTelegramAlertsPusher(ABC):

    @abstractmethod
    def push_messages(self, messages: list[dict[str, Any]]) -> None:
        raise NotImplementedError


class TelegramAlertsPusher(AbstractTelegramAlertsPusher):
    __DELIVERY_MOD: int = pika.spec.PERSISTENT_DELIVERY_MODE
    __QUEUE_DURABLE: bool = True

    def __init__(self, connector: RabbitAMQPConnector) -> None:
        self.connector = connector

    def push_messages(self, messages: list[dict[str, Any]]) -> None:
        prepared_messages = self._prepare_messages(messages=messages)

        with self.connector as connector:
            connector.channel.queue_declare(
                queue=config.REMINDER_ROUTING_KEY,
                durable=self.__QUEUE_DURABLE,
            )
            for body, properties in prepared_messages:
                connector.channel.basic_publish(
                    exchange="",
                    routing_key=config.REMINDER_ROUTING_KEY,
                    body=body,
                    properties=properties,
                )
            log.info("RABBIT: send message to queue")

    def _prepare_messages(
        self,
        messages: list[dict[str, Any]],
    ) -> list[tuple[bytes, pika.BasicProperties]]:
        prepared_messages: list[tuple[bytes, pika.BasicProperties]] = []

        for message in messages:
            message_body = json.dumps({
                "tg_id": message["tg_id"],
                "description": message["description"],
            }).encode()

            properties = pika.BasicProperties(
                correlation_id=str(uuid.uuid4()),
                delivery_mode=self.__DELIVERY_MOD,
            )

            prepared_messages.append((message_body, properties))
        return prepared_messages
