package queue

type Queue interface {
	Send(msg []byte) error
	Receive() ([]byte, error)
	Close() error
}
