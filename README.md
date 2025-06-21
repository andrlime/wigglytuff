# Job Board Producer, Discord Bot Consumer

The purpose of this project is to have real-time notifications of new job postings using web scraping, but processed via a messaging pipeline to be more robust and independently scalable on both the producer side (so more scrapers, or API callers, etc.) and the consumer side (more bots, or webhooks, or some other API call). In general, this project can be used for any schema, but in this case is used to aggregate job board postings into a Discord server.

## Architecture
Using Docker Compose,
1. Runs a producer layer which consists of a series of producers that produce job structs (mainly bots that scrape job boards, or API handlers) every X seconds
2. That producer layer sends job batches to the cache layer via gRPC which deduplicates jobs
3. Different producers can have different logic for how duplicates are handled - one good example is to stop paginating when a dupe is found
4. Non-dupe jobs are messaged through RabbitMQ which feeds them into the cache layer
5. The cache layer writes all jobs to a PostgreSQL database
6. Jobs are fed into a Python consumer (so... bots or webhooks) via gRPC, which can send to Discord, Twilio, etc.

## Running
From the root directory, run `docker compose up`. Before running for the first time, open the compose file and find all the environment variable names. Then, copy into a `.env` file and make their values whatever you want. They do not matter, and as long as you don't use this system in production, don't need to be particularly secure. A example `.env` is below.
```env
POSTGRES_USER=admin
POSTGRES_PASSWORD=whateveryouwant
POSTGRES_DB=db1
RABBITMQ_USERNAME=admin
RABBITMQ_PASSWORD=alsowhateveryouwant
```

## Additional Notes
The `config.yaml` file is intended to be shared across all modules. In local development, it is sym-linked via `ln config.yaml folder/config.yaml` for all services in this repository. It is unclear if that is maintained after pushing to GitHub.
