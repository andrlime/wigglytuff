"""
A Consumer registry that avoids long imports in main.py
"""

from .consumer import Consumer as Consumer
from .discord_consumer import DiscordConsumer as DiscordConsumer
from .slack_consumer import SlackConsumer as SlackConsumer

consumers = [DiscordConsumer(), SlackConsumer()]
