"""
An abstract producer that produces anything of any type
"""

from .consumer import Consumer
from typing import override
from notifier.models.job_pb2 import JobItem
from notifier.core.config import AppConfig
from notifier.core.logger import create_logger

from discord_webhook import DiscordWebhook

logger = create_logger()


class DiscordConsumer(Consumer[list[JobItem]]):
    """
    Discord consumer that sends via a Discord bot
    """

    def __init__(self):
        self.webhook_url = AppConfig().get_environment_variable(
            "DISCORD_WEBHOOK_URL"
        )
        logger.info("Created Discord client!")

    def single_job_to_string(self, item: JobItem) -> str:
        return f"[{item.source_id}]\t{item.title} at **{item.company}**\t{item.url}"

    @override
    def consume(self, message: list[JobItem]):
        logger.info("Received message: %s", [job.uuid for job in message])
        if len(message) == 0:
            return

        chunks = []
        job_strings = [self.single_job_to_string(job) for job in message]
    
        current_chunk = ""
        for s in job_strings:
            if len(current_chunk) + len(s) > 1900:
                chunks.append(current_chunk)
                current_chunk = s
            else:
                current_chunk += "\n" + s

        if current_chunk:
            chunks.append(current_chunk)
        
        for c in chunks:
            if "jane-street" in c:
                c = "<@274430419917733888>\n" + c
            response = DiscordWebhook(
                url=self.webhook_url, content=c
            ).execute()

            if response.status_code != 200:
                logger.error("FAILED to send to Discord webhook! %s", response)
            else:
                logger.info("Sent batch of jobs to Discord webhook!")
