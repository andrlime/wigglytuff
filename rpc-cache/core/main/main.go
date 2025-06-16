package main

import (
	"log"
	"os"
	"time"

	"cache/core"
	"cache/dbconn"
	"cache/queue"
	"cache/receiver"
	"cache/rpc"
	"cache/util"
)

func RabbitMqWorker(config *core.AppConfig) error {
	log.Println("Starting RabbitMqWorker")
	queue := queue.RabbitQueueFactory(config)
	defer queue.Close()

	log.Println("Creating new DbConn pool")
	dbconn := dbconn.JobItemDbConnFactory(config)
	connectErr := dbconn.Connect()
	if connectErr != nil {
		return util.WrapError("RabbitMqWorker, failed to create db", connectErr)
	}
	defer dbconn.Close()

	log.Println("Starting message listener")
	err := queue.Receive(receiver.JobItemReceiver{
		DbConnection: dbconn,
	})
	return err
}

func RpcServerWorker(config *core.AppConfig) error {
	log.Println("Starting RpcServerWorker")

	err := rpc.StartRpcServer(config)

	return err
}

func main() {
	config := core.ParseConfig()
	log.Printf("Finished reading AppConfig %v\n", config)

	log.Println("Sleeping 3 seconds until RabbitMQ and Postgres start...")
	time.Sleep(5 * time.Second)

	errChan := make(chan error, 2)
	go func() {
		errChan <- RabbitMqWorker(config)
	}()
	go func() {
		errChan <- RpcServerWorker(config)
	}()

	log.Println("Listening for worker errors on main thread")
	err := <-errChan
	log.Printf("Worker failed, error: %v\n", err)
	os.Exit(1)
}
