FROM golang:1.24-alpine AS builder

WORKDIR /app

COPY go.mod ./
COPY go.sum ./
RUN go mod download

COPY . ./
RUN go build -o ./main ./core/main/main.go

FROM alpine:latest AS dev
WORKDIR /app
COPY --from=builder /app/main .
COPY --from=builder /app/config.yaml .
CMD ["./main"]

FROM alpine:latest AS prod
WORKDIR /app
COPY --from=builder /app/main .
COPY --from=builder /app/config.yaml .
CMD ["./main", "-config=config.yaml"]
