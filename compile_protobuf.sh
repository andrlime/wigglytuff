#!/bin/sh
# Compiles proto file in ./protobuf to the correct destinations

protoc \
    --python_out=./fetch-scraper/scraper \
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
