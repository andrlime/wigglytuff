"""
A JobProducer sub ABC that produces whatever string it was given
"""

import grpc

from scraper.core.config import AppConfig
from scraper.models.job_pb2 import JobItem, JobItemList

import scraper.models.job_pb2_grpc as job_pb2_grpc

from .producer import Producer


class JobProducer(Producer[JobItem]):
    """
    Abstract job producer that produces JobItem structs
    """

    def __init__(self):
        host = AppConfig().get_grpc_variable("hostname")
        port = AppConfig().get_grpc_variable("port")
        self.grpc_url = f"{host}:{port}"

    def serialise(self, target: JobItem) -> bytes:
        return target.SerializeToString()

    def check_seen(self, job_item: JobItem) -> bool:
        with grpc.insecure_channel(self.grpc_url) as channel:
            stub = job_pb2_grpc.DeduplicationServiceStub(channel)
            response = stub.CheckSeen(job_item)
            return response.seen

    def check_seen_batch(self, job_items: list[JobItem]) -> list[bool]:
        with grpc.insecure_channel(self.grpc_url) as channel:
            stub = job_pb2_grpc.DeduplicationServiceStub(channel)
            response = stub.CheckSeenBatch(JobItemList(jobs=job_items))
            return [item.seen for item in response.results]

    def get_id(self, item: JobItem) -> str:
        return item.uuid
