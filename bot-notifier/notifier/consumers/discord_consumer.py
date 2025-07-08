"""
An abstract producer that produces anything of any type
"""

from .consumer import Consumer
from typing import override
from notifier.models.job_pb2 import JobItem
from notifier.core.config import AppConfig
from notifier.core.logger import create_logger

from discord_webhook import DiscordEmbed, DiscordWebhook

logger = create_logger()


class DiscordConsumer(Consumer[list[JobItem]]):
    """
    Discord consumer that sends via a Discord bot
    """

    def __init__(self):
        self.webhook_url = AppConfig().get_environment_variable(
            "DISCORD_WEBHOOK_URL"
        )
        self.colors_map = {
            "haitou": 11316396,
            "jane-street-2026": 1715357,
            "jump-trading-2026": 12004149,
            "c1-2026": 13378599
        }
        logger.info("Created Discord client!")

    def single_job_to_string(self, item: JobItem) -> str:
        return f"[{item.source_id}]\t{item.title} at **{item.company}**\t{item.url}"

    def single_job_to_json(self, item: JobItem) -> str:
        return {
            "color": self.color_map.get(item.source_id, "#CDCDCD"),
            "author": item.company,
            "title": item.title,
            "url": item.url,
        }

    @override
    def consume(self, message: list[JobItem]):
        logger.info("Received message: %s", [job.uuid for job in message])
        if len(message) == 0:
            return

        chunks = []
        this_chunk = []
        for job in message:
            this_chunk.append(job)
            if len(this_chunk) == 10:
                chunks.append(this_chunk)
                this_chunk = []

        if this_chunk:
            chunks.append(this_chunk)

        for c in chunks:
            webhook = DiscordWebhook(url=self.webhook_url)

            for item in c:
                embed = DiscordEmbed(
                    url=item.url,
                    title=item.company,
                    description=f"""
[{item.source_id}] **{item.company}** - {item.title}
{item.url}
                    """,
                    color=self.colors_map.get(item.source_id, "#CDCDCD"),
                )
                webhook.add_embed(embed)

            response = webhook.execute()
            if response.status_code != 200:
                logger.error("FAILED to send to Discord webhook! %s", response)
            else:
                logger.info("Sent batch of jobs to Discord webhook!")
