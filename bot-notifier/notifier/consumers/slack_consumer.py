"""
An abstract producer that produces anything of any type
"""

from .consumer import Consumer
from typing import override
from notifier.models.job_pb2 import JobItem
from notifier.core.config import AppConfig
from notifier.core.logger import create_logger

import requests

logger = create_logger()


class SlackConsumer(Consumer[list[JobItem]]):
    """
    Slack consumer that sends via a Slack webhook
    """

    def __init__(self):
        self.webhook_url = AppConfig().get_environment_variable(
            "SLACK_WEBHOOK_URL"
        )
        logger.info("Created Slack client!")

    def single_job_to_string(self, item: JobItem) -> str:
        return f"[**{item.company}**]\t{item.title}\t{item.url}"
    
    def text_to_json(self, text: str) -> dict[str, str]:
        return {
            "text": text
        }

    @override
    def consume(self, message: list[JobItem]):
        logger.info("Received message: %s", [job.uuid for job in message])
        if len(message) == 0:
            return
        
        haitou_jobs = [m for m in message if m.source_id == "haitou"]

        chunks = []
        this_chunk = []
        for job in haitou_jobs:
            this_chunk.append(job)
            if len(this_chunk) == 10:
                chunks.append(this_chunk)
                this_chunk = []

        if this_chunk:
            chunks.append(this_chunk)

        for c in chunks:
            url = self.webhook_url
            body = ""

            for item in c:
                body += self.single_job_to_string(item) + "\n"

            response = requests.post(url, json=self.text_to_json(body))
            if response.status_code != 200:
                logger.error("FAILED to send to Slack webhook! %s", response)
            else:
                logger.info("Sent batch of jobs to Slack webhook!")
