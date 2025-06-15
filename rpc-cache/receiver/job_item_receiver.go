package receiver

import (
	"encoding/json"
	"log"

	"cache/dbconn"
	"cache/models"
)

type JobItemReceiver struct {
	DbConnection *dbconn.JobItemDatabaseConnection
}

func (receiver JobItemReceiver) OnReceive(msg []byte) error {
	newJobItem := models.JobItem{}
	if err := json.Unmarshal(msg, &newJobItem); err != nil {
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
