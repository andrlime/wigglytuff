"""
A producer that produces Haitou job board jobs.
"""

import requests
import time

from scraper.core.logger import create_logger
from scraper.models.job_pb2 import JobItem

from .job_producer import JobProducer

logger = create_logger()


class HaitouProducer(JobProducer):
    """
    Generates and produces job listings from Haitou job aggregator
    """

    def __init__(self, source_id: str) -> None:
        super().__init__()
        self.source_id = source_id
        self.api_url = "https://haitou.zhitongguigu.com/api/search"

    def parse_job(self, body: dict) -> JobItem:
        return JobItem(
            uuid=f"{body.get("id")}-{self.source_id}",
            title=body.get("title", "JOB TITLE NOT FOUND"),
            company=body.get("company", "JOB COMPANY NOT FOUND"),
            url=body.get("url", "JOB URL NOT FOUND"),
            source_id=self.source_id,
        )

    def produce(self) -> list[JobItem]:
        country = ",".join(["美国"])
        direction = ",".join(["sde", "quant"])
        exp = "intern"
        pageIndex = 0
        pageSize = 64
        system = "US"
        timestamp = int(time.time() * 1000)

        request_body = {
            "country": country,
            "direction": direction,
            "duration": "",
            "education": "",
            "exp": exp,
            "inFavorite": "",
            "methodName": "",
            "pageIndex": pageIndex,
            "pageSize": pageSize,
            "remote": "",
            "sponsor": "",
            "system": system,
            "tag": "",
            "timestamp": timestamp,
        }
        headers = {"Content-Type": "application/json"}

        # Fail silently, we'll try again soon
        resp = requests.post(self.api_url, json=request_body, headers=headers)
        resp_data = resp.json().get("data", None)
        if resp_data is None:
            return
        resp_job_list = resp_data.get("list", None)
        if resp_job_list is None:
            return

        new_job_list = [self.parse_job(job) for job in resp_job_list]

        logger.info(
            "[=] Produced new jobs %s", [job.uuid for job in new_job_list]
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
