FROM golang:1.25.5-alpine AS builder

WORKDIR /build
COPY . .
RUN go mod download
RUN go build -o helper-api ./cmd/api/main.go

FROM scratch

WORKDIR /app

COPY /media /app/media
COPY --from=builder /build/helper-api /helper-api

ENTRYPOINT [ "/helper-api" ]