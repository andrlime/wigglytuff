"""
Job struct for JobProducer
"""

from dataclasses import dataclass


@dataclass
class JobItem:
    uuid: str
    title: str
    company: str
    url: str
    source_id: str
    location: str = ""
    date_posted: str = ""
