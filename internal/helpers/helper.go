package helpers

import (
	"encoding/json"
	"net/http"
)

func WriteJSON(w http.ResponseWriter, status int, data any) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(data)
}

func BaseURL(r *http.Request) string {
	scheme := "http"

	if r.TLS != nil {
		scheme = "https"
	}

	if proto := r.Header.Get("X-Forwarded-Proto"); proto != "" {
		scheme = proto
	}

	return scheme + "://" + r.Host
}
