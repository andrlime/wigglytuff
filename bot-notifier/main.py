"""
Producer server for fetching jobs from job boards that streams into RabbitMQ
"""

from concurrent import futures

import grpc

import threading
import time

from notifier.core.config import AppConfig
from notifier.core.logger import create_logger
from notifier.consumers import consumers
from notifier.consumers.orchestrator import ConsumerOrchestrator
from notifier.buffer.shared_queue import SharedQueue
import notifier.servicers as servicers
import notifier.models.job_pb2_grpc as job_pb2_grpc

logger = create_logger()


if __name__ == "__main__":
    config = AppConfig()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    buffer = SharedQueue()
    job_pb2_grpc.add_JobPushServiceServicer_to_server(
        servicers.JobPushServiceServicer(buffer), server
    )

    rpc_port = config.get_grpc_variable("port")
    logger.info("Starting RPC service on %s:%s", __name__, rpc_port)
    server.add_insecure_port(f"[::]:{rpc_port}")
    server.start()

    consumer_orchestrator = ConsumerOrchestrator(consumers, buffer)
    logger.info("Starting orchestration service...")
    threading.Thread(target=consumer_orchestrator.worker).start()

    server.wait_for_termination()
