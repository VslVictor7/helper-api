FROM golang:1.25.6-alpine AS app-builder

RUN apk add --no-cache tzdata

WORKDIR /app
COPY . .

RUN go mod download

ENV CGO_ENABLED=0
ENV GOOS=linux
ENV GOARCH=amd64

RUN go build -ldflags="-s -w" -o helper-api ./cmd/api


FROM scratch

COPY --from=app-builder /usr/share/zoneinfo /usr/share/zoneinfo
COPY --from=app-builder /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime

COPY --from=app-builder /app/helper-api /helper-api
COPY --from=app-builder /app/media /media

ENV TZ=America/Sao_Paulo

ENTRYPOINT ["/helper-api"]
