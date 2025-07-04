package receiver

import (
	"context"
	"log"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/protobuf/proto"

	"cache/dbconn"
	pb "cache/protobuf"
	"cache/util"
)

type JobItemReceiver struct {
	DbConnection          *dbconn.JobItemDatabaseConnection
	NotifierRpcConnection *grpc.ClientConn
	NotifierRpcClient     pb.JobPushServiceClient
}

func (receiver JobItemReceiver) OnReceive(msg []byte) error {
	newJobItem := pb.JobItem{}
	if err := proto.Unmarshal(msg, &newJobItem); err != nil {
		return util.WrapError("Unmarshal protobuf data", err)
	}

	log.Printf("[+] Received uuid %v\n", newJobItem.Uuid)

	log.Printf("[<] Writing job %v to db\n", newJobItem.Uuid)
	receiver.DbConnection.InsertNewJob(&newJobItem)
	log.Printf("[>] Successfully wrote job\n")

	log.Printf("[<] Sending %v via RPC to notifier receiver\n", newJobItem.Uuid)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	_, err := receiver.NotifierRpcClient.SendJobs(ctx, &pb.JobItemList{
		Jobs: []*pb.JobItem{&newJobItem},
	})
	if err != nil {
		return util.WrapError("Send jobs via RPC to notifier", err)
	}
	log.Printf("[>] Successfully sent via RPC\n")

	return nil
}
