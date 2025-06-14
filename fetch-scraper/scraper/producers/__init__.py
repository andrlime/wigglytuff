"""
A Producer registry that avoids long imports in main.py
"""

from .producer import Producer as Producer
from .hello_world_producer import HelloWorldProducer as HelloWorldProducer
from .sample_job_producer import SampleJobProducer as SampleJobProducer

producers = [
    HelloWorldProducer("Hello world"),
    SampleJobProducer("Big Finance Company", "some-quant-company"),
    SampleJobProducer("Small Finance Company", "some-quant-company"),
]
