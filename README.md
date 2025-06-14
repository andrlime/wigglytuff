# Job Board Producer, Discord Bot Consumer

Using Docker Compose,

1. Runs a Flask layer which consists of a series of bots that scrape job boards every X minutes, default 15
2. Those jobs are pipelined through into RabbitMQ which feeds them into a cache layer
3. The cache layer deduplicates jobs using Redis and stores all existing jobs into a Postgres database
4. Jobs that are new are buffered and fed into a Discord bot every X minutes, default 15
5. Important jobs can trigger a phone call using Twilio's API
6. The Discord and Twilio bots are contained with a Flask interface through HTTP POST requests.

The use case here is to stream internship posts from job boards, but this can be used for any producer consumer problem. It's honestly just a wrapper of RabbitMQ. All interprocess communication is done using gRPC calls and protobuf. Health check endpoints exist on every layer. Health check status can be streamed to Discord using the `/health` command.
