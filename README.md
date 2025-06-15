# Job Board Producer, Discord Bot Consumer

Using Docker Compose,

1. Runs a producer layer which consists of a series of bots that scrape job boards every X seconds
2. That producer layer sends job batches to the cache layer via gRPC which deduplicates jobs
3. Different producers can have different logic for how duplicates are handled - one good example is to stop paginating when a dupe is found
4. Non-dupe jobs are messaged through RabbitMQ which feeds them into the cache layer
5. The cache layer writes all jobs to a PostgreSQL database
6. Jobs are fed into a Python consumer (so... bots) via gRPC, which can send to Discord, Twilio, etc.

The use case here is to stream internship posts from job boards, but this can be used for any producer consumer problem. It's honestly just a wrapper of RabbitMQ. All interprocess communication is done using gRPC calls and protobuf.
