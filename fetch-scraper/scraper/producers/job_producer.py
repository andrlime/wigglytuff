"""
A JobProducer sub ABC that produces whatever string it was given
"""

import json

from dataclasses import asdict

from scraper.models.job_pb2 import JobItem

from .producer import Producer


class JobProducer(Producer[JobItem]):
    def serialise(self, target: JobItem) -> bytes:
        return target.SerializeToString()

    def get_id(self, item: JobItem) -> str:
        return item.uuid
