package queue

import (
	"errors"
	"fmt"
	"log"

	amqp "github.com/rabbitmq/amqp091-go"

	"cache/core"
	"cache/receiver"
)

type RabbitQueue struct {
	Connection *amqp.Connection
	Channel    *amqp.Channel
	Queue      amqp.Queue
}

func RabbitQueueFactory(config *core.AppConfig) *RabbitQueue {
	connectionUrl := fmt.Sprintf(
		"amqp://%s:%s@%s:%d/",
		config.RabbitMqCredentials.Username,
		config.RabbitMqCredentials.Password,
		config.RabbitMqConfig.HostName,
		config.RabbitMqConfig.Port,
	)
	log.Printf("Connecting to RabbitMQ URL %v\n", connectionUrl)

	log.Println("Creating RabbitMQ Connection")
	conn, err := amqp.Dial(connectionUrl)
	if err != nil {
		log.Panicf("Failed to connect to RabbitMQ: %e\n", err)
	}
	log.Println("Created RabbitMQ Connection")

	log.Println("Creating RabbitMQ Channel")
	ch, err := conn.Channel()
	if err != nil {
		log.Panicf("Failed to open channel: %e\n", err)
	}
	log.Println("Created RabbitMQ Channel")

	queueName := config.RabbitMqConfig.QueueName
	log.Printf("Creating RabbitMQ Queue object for queue %v\n", queueName)
	q, err := ch.QueueDeclare(
		queueName,
		true,  // durable
		false, // delete when unused
		false, // exclusive
		false, // no-wait
		nil,   // arguments
	)
	if err != nil {
		log.Panicf("Failed to create queue %v: %e", queueName, err)
	}
	log.Println("Successfully created RabbitMQ Queue object")

	return &RabbitQueue{
		Connection: conn,
		Channel:    ch,
		Queue:      q,
	}
}

func (queue *RabbitQueue) Send(msg []byte) error {
	return errors.New("not implemented, this service only receives messages from RabbitMQ")
}

func (queue *RabbitQueue) Receive(receiver receiver.Receiver) error {
	msgs, err := queue.Channel.Consume(
		queue.Queue.Name, // queue
		"",               // consumer
		true,             // auto-ack
		false,            // exclusive
		false,            // no-local
		false,            // no-wait
		nil,              // args
	)
	if err != nil {
		return err
	}
	go func() {
		for d := range msgs {
			log.Printf("[+] Received a message: %s", d.Body)
			receiver.OnReceive(d.Body)
		}
	}()
	select {}
}

func (queue *RabbitQueue) Close() {
	queue.Channel.Close()
	queue.Connection.Close()
}
