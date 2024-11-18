from remote_services.amqp_connector import RabbitAMQPConnector
from remote_services.telegram_alers.services import TelegramAlertsPusher


def sync_get_telegram_pusher_service():
    return TelegramAlertsPusher(connector=RabbitAMQPConnector())
