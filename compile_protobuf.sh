#!/bin/sh
# Compiles proto file in ./protobuf to the correct destinations

protoc \
    --python_out=./fetch-scraper/scraper \
    ./protobuf/job.proto

protoc \
    --python_out=./bot-notifier/notifier \
    ./protobuf/job.proto

protoc \
    --go_out=./rpc-cache \
    ./protobuf/job.proto

protoc \
    --go-grpc_out=./rpc-cache \
    ./protobuf/job.proto

poetry run \
    python -m grpc_tools.protoc \
    -I./protobuf \
    --python_out=./fetch-scraper/scraper/models \
    --pyi_out=./fetch-scraper/scraper/models \
    --grpc_python_out=./fetch-scraper/scraper/models \
    ./protobuf/job.proto

poetry run \
    python -m grpc_tools.protoc \
    -I./protobuf \
    --python_out=./bot-notifier/notifier/models \
    --pyi_out=./bot-notifier/notifier/models \
    --grpc_python_out=./bot-notifier/notifier/models \
    ./protobuf/job.proto

sed "s/import job_pb2/import scraper.models.job_pb2/g" \
    fetch-scraper/scraper/models/job_pb2_grpc.py > temp.py \
    && mv temp.py fetch-scraper/scraper/models/job_pb2_grpc.py

sed "s/import job_pb2/import notifier.models.job_pb2/g" \
    bot-notifier/notifier/models/job_pb2_grpc.py > temp.py \
    && mv temp.py bot-notifier/notifier/models/job_pb2_grpc.py
