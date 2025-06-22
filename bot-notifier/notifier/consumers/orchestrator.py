"""
An abstract producer that produces anything of any type
"""

import threading
import time

from .consumer import Consumer
from notifier.buffer.buffer import Buffer
from notifier.core.config import AppConfig
from notifier.core.logger import create_logger

logger = create_logger()


class ConsumerOrchestrator:
    """
    A container of consumers
    """

    def __init__(self, consumers: list[Consumer], buffer: Buffer):
        self.consumers = consumers
        self.buffer = buffer
        self.delay_interval = AppConfig().get_config_variable("interval")

    def worker(self):
        while True:
            logger.info("Beginning consumer cycle...")
            contents = self.buffer.empty()
            logger.info("Contents of buffer: %s", [job.uuid for job in contents])
            threads = []

            for c in self.consumers:
                t = threading.Thread(
                    target=c.consume,
                    args=(contents),
                )
                t.start()
                threads.append(t)

            for t in threads:
                t.join()

            logger.info("Now sleeping %s seconds", self.delay_interval)
            time.sleep(self.delay_interval)
