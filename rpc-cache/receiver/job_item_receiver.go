package receiver

import (
	"log"

	"google.golang.org/protobuf/proto"

	"cache/dbconn"
	"cache/protobuf"
)

type JobItemReceiver struct {
	DbConnection *dbconn.JobItemDatabaseConnection
}

func (receiver JobItemReceiver) OnReceive(msg []byte) error {
	newJobItem := protobuf.JobItem{}
	if err := proto.Unmarshal(msg, &newJobItem); err != nil {
		return err
	}

	log.Printf("[+] Received uuid %v\n", newJobItem.Uuid)

	log.Printf("[<] Writing job %v to db\n", newJobItem.Uuid)
	receiver.DbConnection.InsertNewJob(&newJobItem)
	log.Printf("[>] Successfully wrote job\n")

	// log.Printf("[<] Sending %v via RPC to notifier receiver\n", newJobItem.Uuid)
	// log.Printf("[>] Successfully sent via RPC\n")

	return nil
}
