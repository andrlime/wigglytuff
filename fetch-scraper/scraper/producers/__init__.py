"""
A Producer registry that avoids long imports in main.py
"""

from .producer import Producer as Producer
from .hello_world_producer import HelloWorldProducer as HelloWorldProducer

producers = [
    HelloWorldProducer("ABC"),
    HelloWorldProducer("DEF"),
    HelloWorldProducer("GHI"),
    HelloWorldProducer("Hello world"),
    HelloWorldProducer("srgfhfgdgf"),
]
