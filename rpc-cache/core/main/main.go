package main

import (
	"fmt"
	"log"
	"os"

	"google.golang.org/grpc"

	"cache/core"
	"cache/dbconn"
	"cache/queue"
	"cache/receiver"
	"cache/rpc"
	"cache/util"
	pb "cache/protobuf"
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

	log.Println("Creating NotifierRPC connection and client")
	notifierRpcUrl := fmt.Sprintf(
		"%v:%v",
		config.RpcConfig.NotifierName,
		config.RpcConfig.Port,
	)
	conn, dialErr := grpc.Dial(notifierRpcUrl, grpc.WithInsecure())
	if dialErr != nil {
		return util.WrapError("Dial NotifierRPC", dialErr)
	}
	defer conn.Close()

	client := pb.NewJobPushServiceClient(conn)

	log.Println("Starting message listener")
	err := queue.Receive(receiver.JobItemReceiver{
		DbConnection: dbconn,
		NotifierRpcConnection: conn,
		NotifierRpcClient: client,
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
