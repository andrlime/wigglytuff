package main

import (
	"log"
	"os"
	"time"

	"cache/core"
	"cache/queue"
	"cache/receiver"
	"cache/util"
)

func RabbitMqWorker(config *core.AppConfig) error {
	log.Println("Sleeping 5 seconds until RabbitMQ starts...")
	time.Sleep(5 * time.Second)

	log.Println("Starting RabbitMqWorker")
	queue := queue.RabbitQueueFactory(config)

	log.Println("Starting message listener")
	err := queue.Receive(receiver.JobItemReceiver{})
	return err
}

func RpcServerWorker(config *core.AppConfig) error {
	log.Println("Starting RpcServerWorker")

	select {}

	return util.CreateError("RpcServerWorker", "not implemented")
}

func main() {
	config := core.ParseConfig()
	log.Printf("Finished reading AppConfig %v\n", config)

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
