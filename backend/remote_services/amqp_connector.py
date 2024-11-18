import pika
from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

import config


class RabbitAMQPConnector:

    def __init__(self) -> None:
        self._connection: BlockingConnection | None = None
        self._channel: BlockingChannel | None = None

    @property
    def channel(self) -> BlockingChannel:
        """To get a channel you need to use an context manager."""
        if self._channel is None:
            raise ValueError("Use -> `with instance`")
        return self._channel

    def __enter__(self):
        if self._connection is None:
            credentials = pika.PlainCredentials(
                config.RABBITMQ_DEFAULT_USER,
                config.RABBITMQ_DEFAULT_PASS,
            )
            parameters = pika.ConnectionParameters(
                config.AMQP_HOST,
                config.AMQP_PORT,
                "/",
                credentials,
            )
            self._connection = pika.BlockingConnection(parameters)
        if self._channel is None:
            self._channel = self._connection.channel()
        return self

    def __exit__(self, ext_type, exc, tb) -> None:
        if self._channel is not None and not self._channel.is_closed:
            self._channel.close()
        if self._connection is not None and not self._connection.is_closed:
            self._connection.close()
