"""
An abstract producer that produces anything of any type
"""

import threading
import time

from .producer import Producer
from scraper.core.config import AppConfig
from scraper.core.logger import create_logger
from scraper.rabbitmq.rabbit_queue import start_receiver, RabbitQueue

logger = create_logger()


class ProducerOrchestrator:
    """
    A container of producers
    """

    def __init__(self, producers: list[Producer]):
        self.producers = producers
        self.delay_interval = AppConfig().get_config_variable("interval")
        self.queue_name = AppConfig().get_rmq_variable("queue_name")

        self.debug_mode = AppConfig().get_rmq_variable("debug_mode")
        if self.debug_mode:
            self.receiver_queue = RabbitQueue(self.queue_name)

    def health_check(self):
        with open("/tmp/healthy", "w", encoding="utf-8") as f:
            f.write(str(time.time()))

    def thread_worker(self, producer: Producer, queue: RabbitQueue):
        data = producer.produce()
        if len(data) == 0:  # Heartbeat to prevent queues from being auto closed
            queue.send_message("NO NEW JOBS")
        for item in data:
            queue.send_message(producer.serialise(item))

    def worker(self):
        if self.debug_mode:
            start_receiver(self.receiver_queue)
        while True:
            logger.info("Beginning producer cycle...")
            threads = []
            queues = [RabbitQueue(self.queue_name) for _ in self.producers]

            for producer_, queue_ in zip(self.producers, queues):
                t = threading.Thread(
                    target=self.thread_worker,
                    args=(
                        producer_,
                        queue_,
                    ),
                )
                t.start()
                threads.append(t)
                self.health_check()

            for t in threads:
                t.join()

            for q in queues:
                q.close()

            logger.info("Now sleeping %s seconds", self.delay_interval)
            time.sleep(self.delay_interval)

    def close(self):
        if self.debug_mode:
            self.receiver_queue.close()
