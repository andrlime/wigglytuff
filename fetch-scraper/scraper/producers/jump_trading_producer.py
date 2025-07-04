"""
A producer that produces Jump Trading internship jobs.
"""

import uuid
import random
import time

from selenium.webdriver.common.by import By

from scraper.core.logger import create_logger
from scraper.models.job_pb2 import JobItem

from .job_producer import JobProducer

logger = create_logger()


class JumpTradingProducer(JobProducer):
    """
    Generates and produces job listings from Jump's career page
    """

    def __init__(self, company_name: str, source_id: str, chrome_driver) -> None:
        super().__init__()
        self.company_name = company_name
        self.source_id = source_id
        self.root_url = "https://www.jumptrading.com"
        self.driver = chrome_driver

    def produce(self) -> list[JobItem]:
        self.driver.get("https://www.jumptrading.com/careers/?titleSearch=campus+intern")
        time.sleep(3)
        
        new_job_list = []

        section = self.driver.find_element(By.ID, "styled-scrollbar")
        children = section.find_elements(By.XPATH, "//a[@role = 'listitem']")

        for job in children:
            href = job.get_attribute("href")
            if not href:
                continue
            
            uuid = href.rstrip("/").split("/")[-1]
            title_elem = job.find_element(By.TAG_NAME, "p")
            full_title = title_elem.text.strip()

            new_job_list.append(JobItem(
                uuid=f"{self.source_id}-{uuid}",
                title=full_title,
                company=self.company_name,
                url=href,
                source_id=self.source_id
            ))

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
