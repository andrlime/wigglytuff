"""
A sample JobProducer producer that produces fake jobs.

Provided as an example. Useless in production.
"""

import uuid
import random

from scraper.core.logger import create_logger
from scraper.models.job_pb2 import JobItem

from .job_producer import JobProducer

logger = create_logger()


class SampleJobProducer(JobProducer):
    """
    Generates and produces fake job listings
    """

    def __init__(self, company_name: str, source_id: str) -> None:
        super().__init__()
        self.company_name = company_name
        self.source_id = source_id

    def produce(self) -> list[JobItem]:
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

        new_job_list = [
            generate_fake_job() for _ in range(random.randint(6, 9))
        ]
        logger.info(
            "[=] Created new jobs %s", [job.uuid for job in new_job_list]
        )
        seen_list = self.check_seen_batch(new_job_list)
        logger.info("[=] Seen booleans %s", seen_list)

        seen_jobs = [job for job, seen in zip(new_job_list, seen_list) if seen]
        for job in seen_jobs:
            logger.info("[-] Seen %s", job.uuid)

        not_seen_jobs = [
            job for job, seen in zip(new_job_list, seen_list) if not seen
        ]
        for job in not_seen_jobs:
            logger.info("[+] New %s", job.uuid)

        return not_seen_jobs
