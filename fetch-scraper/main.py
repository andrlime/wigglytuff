"""
Producer server for fetching jobs from job boards that streams into RabbitMQ
"""

import threading
import time

from scraper.core.config import AppConfig
from scraper.core.logger import create_logger
from scraper.rabbitmq.rabbit_queue import RabbitQueue, start_receiver
from scraper.producers import Producer, producers

logger = create_logger()


def health_check():
    with open("/tmp/healthy", "w", encoding="utf-8") as f:
        f.write(str(time.time()))


def producer_thread_worker(producer: Producer, queue: RabbitQueue):
    data = producer.consume()
    logger.info("[-] Produced data %s", data)
    for item in data:
        queue.send_message(producer.serialise(item))


if __name__ == "__main__":
    logger.info("Waiting 5 seconds for RabbitMQ to start...")
    time.sleep(5)

    delay_interval = AppConfig().get_config_variable("interval")
    queue_name = AppConfig().get_rmq_variable("queue_name")
    producer_queues = [RabbitQueue(queue_name) for _ in producers]

    debug_mode = AppConfig().get_rmq_variable("debug_mode")
    if debug_mode:
        receiver_queue = RabbitQueue(queue_name)

    try:
        if debug_mode:
            start_receiver(receiver_queue)
        while True:
            logger.info("Beginning producer cycle...")
            threads = []

            for producer_, queue_ in zip(producers, producer_queues):
                t = threading.Thread(
                    target=producer_thread_worker,
                    args=(
                        producer_,
                        queue_,
                    ),
                )
                t.start()
                threads.append(t)
                health_check()

            for t in threads:
                t.join()

            time.sleep(delay_interval)
    finally:
        for queue_ in producer_queues:
            queue_.close()
        if debug_mode:
            receiver_queue.close()
