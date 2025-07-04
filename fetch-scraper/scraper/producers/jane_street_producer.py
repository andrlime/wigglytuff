"""
A producer that produces Jane Street internship jobs.
"""

import uuid
import random
import time

from selenium.webdriver.common.by import By

from scraper.core.logger import create_logger
from scraper.models.job_pb2 import JobItem

from .job_producer import JobProducer

logger = create_logger()


class JaneStreetProducer(JobProducer):
    """
    Generates and produces job listings from JS's career page
    """

    def __init__(self, company_name: str, source_id: str, chrome_driver) -> None:
        super().__init__()
        self.company_name = company_name
        self.source_id = source_id
        self.root_url = "https://www.janestreet.com"
        self.driver = chrome_driver

    def produce(self) -> list[JobItem]:
        self.driver.get("https://www.janestreet.com/join-jane-street/open-roles/?type=internship&location=all-locations")
        time.sleep(3)
        
        new_job_list = []

        children = self.driver.find_elements(By.CSS_SELECTOR, "div.students-and-new-grads.job.open")
        parents = [el.find_element(By.XPATH, "..") for el in children]

        for job, link in zip(children, parents):
            href = link.get_attribute("href")
            if not href:
                continue
            uuid = href.rstrip("/").split("/")[-1]

            position_name = job.find_element(By.CSS_SELECTOR, "div.position").text.strip()
            position_type = job.find_element(By.CSS_SELECTOR, "div.type").text.strip()
            position_loc = job.find_element(By.CSS_SELECTOR, "div.city").text.strip()
            if not position_name or not position_type or not position_loc:
                continue

            full_title = f"{position_name} - {position_type} - {position_loc}"

            new_job_list.append(JobItem(
                uuid=f"{self.source_id}-{uuid}",
                title=full_title,
                company=self.company_name,
                url=href,
                source_id=self.source_id
            ))
        
        print(new_job_list, len(new_job_list))

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
