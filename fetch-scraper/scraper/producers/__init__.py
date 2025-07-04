"""
A Producer registry that avoids long imports in main.py

"""

from .producer import Producer as Producer
from .hello_world_producer import HelloWorldProducer as HelloWorldProducer
from .sample_job_producer import SampleJobProducer as SampleJobProducer
from .jump_trading_producer import JumpTradingProducer as JumpTradingProducer
from .jane_street_producer import JaneStreetProducer as JaneStreetProducer

from scraper.driver import driver_factory

producers = [
    # SampleJobProducer("Big Finance Company", "some-quant-company"),
    # SampleJobProducer("Small Finance Company", "some-quant-company"),
    JumpTradingProducer("Jump Trading", "jump-trading-2026", driver_factory()),
    JaneStreetProducer("Jane Street", "jane-street-2026", driver_factory()),
]
