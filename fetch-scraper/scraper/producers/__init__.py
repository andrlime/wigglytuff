"""
A Producer registry that avoids long imports in main.py

"""

from .producer import Producer as Producer
from .hello_world_producer import HelloWorldProducer as HelloWorldProducer
from .sample_job_producer import SampleJobProducer as SampleJobProducer
from .haitou_producer import HaitouProducer as HaitouProducer
from .jump_trading_producer import JumpTradingProducer as JumpTradingProducer
from .jane_street_producer import JaneStreetProducer as JaneStreetProducer
from .capital_one_producer import CapitalOneProducer as CapitalOneProducer

from scraper.driver import driver_factory

producers = [
    # SampleJobProducer("Big Finance Company", "some-quant-company"),
    # SampleJobProducer("Small Finance Company", "some-quant-company"),
    HaitouProducer("haitou"),
    JumpTradingProducer("Jump Trading", "jump-trading-2026", driver_factory()),
    CapitalOneProducer("Capital One", "c1-tech-2026", driver_factory()),
]
