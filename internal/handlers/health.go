package handlers

import (
	"helper-api/internal/helpers"
	"net/http"
	"os"
)

func HealthHandler(w http.ResponseWriter, r *http.Request) {
	errors := make(map[string]string)

	if _, err := os.Stat(imageDir); err != nil {
		errors["images"] = err.Error()
	}

	if _, err := os.Stat(mobsFile); err != nil {
		errors["mobs"] = err.Error()
	}

	if _, err := os.Stat(deathsFile); err != nil {
		errors["deaths"] = err.Error()
	}

	if len(errors) > 0 {
		helpers.WriteJSON(w, http.StatusServiceUnavailable, map[string]any{
			"status": "unhealthy",
			"errors": errors,
		})
		return
	}

	helpers.WriteJSON(w, http.StatusOK, map[string]string{
		"status": "ok",
	})
}
