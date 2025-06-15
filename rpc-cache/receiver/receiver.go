package receiver

type Receiver interface {
	OnReceive(msg []byte) error
}
