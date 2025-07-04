"""
Producer server for fetching jobs from job boards that streams into RabbitMQ
"""

import threading

from scraper.core.config import AppConfig
from scraper.core.logger import create_logger
from scraper.producers import producers
from scraper.producers.orchestrator import ProducerOrchestrator

logger = create_logger()


if __name__ == "__main__":
    config = AppConfig()

    producer_orchestrator = ProducerOrchestrator(producers)
    logger.info("Starting orchestration service...")
    threading.Thread(target=producer_orchestrator.worker).start()
