"""
A Consumer registry that avoids long imports in main.py
"""

from .consumer import Consumer as Consumer

consumers = [
    # SampleJobConsumer("Big Finance Company", "some-quant-company"),
    # SampleJobConsumer("Small Finance Company", "some-quant-company"),
]
