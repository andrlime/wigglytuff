"""
A JobProducer sub ABC that produces whatever string it was given
"""

import json

from dataclasses import asdict

from scraper.models.job import JobItem

from .producer import Producer


class JobProducer(Producer[JobItem]):
    def serialise(self, target: JobItem) -> bytes:
        return json.dumps(asdict(target)).encode("utf-8")

    def get_id(self, item: JobItem) -> str:
        return item.uuid
