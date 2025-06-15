"""
Wrapper around RabbitMQ to send messages into a queue
"""

import threading

import pika

from scraper.core.config import AppConfig
from scraper.core.logger import create_logger
from scraper.core.exceptions import RabbitMQError

logger = create_logger()


class RabbitQueue:
    """
    A wrapper around RabbitMQ to enqueue (and dequeue if desired) byte messages
    """

    def __init__(self, queue_name: str) -> None:
        try:
            hostname = AppConfig().get_rmq_variable("hostname")
            port = AppConfig().get_rmq_variable("port")
            credentials = pika.PlainCredentials(
                AppConfig().get_environment_variable("RABBITMQ_USERNAME"),
                AppConfig().get_environment_variable("RABBITMQ_PASSWORD"),
            )
            logger.info(
                "Attempting to connect to amqp://****:****@%s:%s",
                hostname,
                port,
            )
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    hostname, port=port, credentials=credentials
                )
            )
        except Exception as e:
            raise RabbitMQError(
                "Unable to connect to RabbitMQ. Did you run `docker compose up`?"
            ) from e

        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue=queue_name, durable=True)

    def send_message(self, message: bytes):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def receive_message(self, ch, method, _, body):
        logger.info("[+] Received: %s", body.decode())
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.receive_message,
            auto_ack=False,
        )

        logger.info("[*] Started message consumer, waiting for messages...")
        self.channel.start_consuming()

    def close(self):
        self.connection.close()


def start_receiver(queue: RabbitQueue):
    """
    Start a receiver thread. Mainly useless except for debugging.
    """
    t = threading.Thread(target=queue.start_consuming)
    t.start()
