"""
A sample JobProducer producer that produces fake jobs.

Provided as an example. Useless in production.
"""

import uuid
import random

from scraper.models.job import JobItem

from .job_producer import JobProducer


class SampleJobProducer(JobProducer):
    """
    Generates and produces fake job listings
    """

    def __init__(self, company_name: str, source_id: str) -> None:
        self.company_name = company_name
        self.source_id = source_id

    def consume(self) -> list[JobItem]:
        titles = ["Title 1", "Title 2", "Title 3", "Title 4"]

        def generate_fake_job():
            job_uuid = str(uuid.uuid4())
            return JobItem(
                uuid=job_uuid,
                title=random.choice(titles),
                company=self.company_name,
                url=f"https://jobs.example.com/{job_uuid}",
                source_id=self.source_id,
            )

        return [generate_fake_job() for _ in range(random.randint(6, 9))]
