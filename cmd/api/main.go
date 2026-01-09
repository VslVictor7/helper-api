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

	mux.HandleFunc("GET /images/png/", handlers.ImagePNGHandler)
	mux.HandleFunc("GET /images/", handlers.ImageByNameHandler)
	mux.HandleFunc("GET /images", handlers.ImagesHandler)
	mux.HandleFunc("GET /mobs", handlers.MobsHandler)
	mux.HandleFunc("GET /deaths", handlers.DeathsHandler)

	server := http.Server{
		Addr:    ":8000",
		Handler: loggingMiddleware(mux),
	}

	log.Printf("Server running on %s", server.Addr)

	log.Fatal(server.ListenAndServe())
}
