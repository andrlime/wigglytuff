package rpc

import (
	"context"
	"fmt"
	"log"
	"net"

	"google.golang.org/grpc"

	"cache/core"
	"cache/dbconn"
	pb "cache/protobuf"
	"cache/util"
)

type server struct {
	pb.UnimplementedDeduplicationServiceServer
	DbConnection *dbconn.JobItemDatabaseConnection
}

func (s *server) checkSingleUuid(uuid string) (*pb.CheckSeenResponse, error) {
	log.Printf("Checking UUID %v\n", uuid)
	jobs, err := s.DbConnection.GetJobByUuid(uuid)
	if err != nil {
		return nil, util.WrapError("checkSingleUuid", err)
	}
	return &pb.CheckSeenResponse{Uuid: uuid, Seen: len(jobs) != 0}, nil
}

func (s *server) CheckSeen(ctx context.Context, req *pb.JobItem) (*pb.CheckSeenResponse, error) {
	log.Printf("[RPC] Checking job UUID: %s\n", req.Uuid)
	return s.checkSingleUuid(req.Uuid)
}

func (s *server) CheckSeenBatch(ctx context.Context, req *pb.JobItemList) (*pb.CheckSeenListResponse, error) {
	results := make([]*pb.CheckSeenResponse, 0, len(req.Jobs))
	for _, job := range req.Jobs {
		log.Printf("Checking job UUID: %s\n", job.Uuid)
		checkUuidResult, err := s.checkSingleUuid(job.Uuid)
		if err != nil {
			return nil, err
		}
		results = append(results, checkUuidResult)
	}

	return &pb.CheckSeenListResponse{
		Results: results,
	}, nil
}

func StartRpcServer(config *core.AppConfig) error {
	port := config.RpcConfig.Port
	portString := fmt.Sprintf(":%v", port)
	lis, err := net.Listen("tcp", portString)
	if err != nil {
		return util.WrapError("StartRpcServer:Listen()", err)
	}

	dbconn := dbconn.JobItemDbConnFactory(config)
	connectErr := dbconn.Connect()
	if connectErr != nil {
		return util.WrapError("RabbitMqWorker, failed to create db", connectErr)
	}
	defer dbconn.Close()

	grpcServer := grpc.NewServer()
	pb.RegisterDeduplicationServiceServer(grpcServer, &server{
		DbConnection: dbconn,
	})

	log.Printf("Starting gRPC server on port %v\n", port)
	if err := grpcServer.Serve(lis); err != nil {
		return util.WrapError("StartRpcServer:Serve()", err)
	}

	return nil
}
