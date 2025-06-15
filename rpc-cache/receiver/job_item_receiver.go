package receiver

import (
	"encoding/json"
	"log"

	"cache/models"
)

type JobItemReceiver struct {}

func (JobItemReceiver) OnReceive(msg []byte) error {
	newJobItem := models.JobItem{}
	if err := json.Unmarshal(msg, &newJobItem); err != nil {
		return err
	}

	log.Printf("[+] Received uuid %v\n", newJobItem.Uuid)

	return nil
}
