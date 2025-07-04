"""
JobPushServiceServicer class
"""

import notifier.models.job_pb2 as job_pb2
import notifier.models.job_pb2_grpc as job_pb2_grpc

from notifier.buffer.buffer import Buffer
from notifier.core.logger import create_logger

logger = create_logger()


class JobPushServiceServicer(job_pb2_grpc.JobPushServiceServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self, buffer: Buffer):
        self.buffer = buffer

    def SendJobs(self, request, context):
        if len(request.jobs) == 0:
            logger.info(f"Received no jobs")
        for job in request.jobs:
            logger.info(f"Received job {job.uuid}")
            self.buffer.push(job)
        return job_pb2.Ack(success=True)
