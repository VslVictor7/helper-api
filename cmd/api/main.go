package main

import (
	"helper-api/internal/handlers"
	"log"
	"net/http"
)

// --------------------
// Middleware (BaseAPIView)
// --------------------
func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Printf("Request: %s %s", r.Method, r.URL.Path)
		next.ServeHTTP(w, r)
	})
}

// --------------------
// main
// --------------------
func main() {
	mux := http.NewServeMux()

	mux.HandleFunc("/images/png/", handlers.ImagePNGHandler)
	mux.HandleFunc("/images/", handlers.ImageByNameHandler)
	mux.HandleFunc("/images", handlers.ImagesHandler)
	mux.HandleFunc("/mobs", handlers.MobsHandler)
	mux.HandleFunc("/deaths", handlers.DeathsHandler)

	server := http.Server{
		Addr:    ":8000",
		Handler: loggingMiddleware(mux),
	}

	log.Printf("Server running on %s", server.Addr)

	log.Fatal(server.ListenAndServe())
}
