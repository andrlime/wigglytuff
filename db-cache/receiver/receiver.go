package receiver

import (
	"log"
)

type Receiver interface {
	OnReceive(msg []byte)
}

type JobItemReceiver struct {}

func (JobItemReceiver) OnReceive(msg []byte) {
	log.Printf("AAAAAAAAHHHHHHHHH: %v", string(msg))
}
