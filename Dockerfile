FROM golang:1.25.5-alpine AS builder

ENV CGO_ENABLED=0
WORKDIR /build
COPY . .
RUN go mod download
RUN go build -ldflags="-w -s" -o helper-api ./cmd/api/main.go


FROM alpine:3.23

RUN apk add --no-cache curl

WORKDIR /app

COPY media /app/media
COPY --from=builder /build/helper-api /app/helper-api

EXPOSE 8000
ENTRYPOINT [ "/app/helper-api" ]