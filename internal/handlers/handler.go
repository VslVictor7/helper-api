// Tentativa de aprendizado utilizando Go. Yay!

package handlers

import (
	"helper-api/internal/helpers"
	"net/http"
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

// Diretórios (equivalente ao settings.MEDIA_ROOT)
var (
	imageDir   = "media/images"
	mobsFile   = "media/mobs/mobs.json"
	deathsFile = "media/deaths/deaths.json"
)

// --------------------
// /images/
// --------------------
func ImagesHandler(w http.ResponseWriter, r *http.Request) {
	files, err := os.ReadDir(imageDir)
	if err != nil {
		helpers.WriteJSON(w, http.StatusInternalServerError, map[string]string{
			"error": err.Error(),
		})
		return
	}

	re := regexp.MustCompile(`([a-z])([A-Z])`)
	var images []map[string]string

	for _, file := range files {
		name := strings.TrimSuffix(file.Name(), filepath.Ext(file.Name()))
		friendly := re.ReplaceAllString(name, "$1 $2")

		images = append(images, map[string]string{
			"filename": file.Name(),
			"name":     friendly,
		})
	}

	helpers.WriteJSON(w, http.StatusOK, map[string]any{
		"images": images,
	})
}

// --------------------
// /images/png/{filename}/
// --------------------
func ImagePNGHandler(w http.ResponseWriter, r *http.Request) {
	filename := strings.TrimPrefix(r.URL.Path, "/images/png/")
	filename = filepath.Base(filename)

	path := filepath.Join(imageDir, filename)

	if _, err := os.Stat(path); err != nil {
		helpers.WriteJSON(w, http.StatusNotFound, map[string]string{
			"error": "Imagem não encontrada.",
		})
		return
	}

	http.ServeFile(w, r, path)
}

// --------------------
// /images/{name}/
// --------------------
func ImageByNameHandler(w http.ResponseWriter, r *http.Request) {
	name := strings.TrimPrefix(r.URL.Path, "/images/")
	name = strings.ToLower(name)

	files, err := os.ReadDir(imageDir)
	if err != nil {
		helpers.WriteJSON(w, http.StatusInternalServerError, map[string]string{
			"error": err.Error(),
		})
		return
	}

	mapping := make(map[string]string)

	for _, file := range files {
		stem := strings.TrimSuffix(file.Name(), filepath.Ext(file.Name()))
		friendly := strings.ReplaceAll(stem, "_", " ")

		mapping[strings.ToLower(friendly)] = file.Name()
		mapping[strings.ReplaceAll(strings.ToLower(friendly), " ", "")] = file.Name()
	}

	filename := mapping[name]
	if filename == "" {
		helpers.WriteJSON(w, http.StatusNotFound, map[string]string{
			"error": "Imagem não encontrada.",
		})
		return
	}

	base := helpers.BaseURL(r)

	helpers.WriteJSON(w, http.StatusOK, map[string]string{
		"name": strings.TrimSuffix(filename, ".png"),
		"url":  base + "/images/png/" + filename,
	})
}

// --------------------
// /mobs/
// --------------------
func MobsHandler(w http.ResponseWriter, r *http.Request) {
	data, err := os.ReadFile(mobsFile)
	if err != nil {
		helpers.WriteJSON(w, http.StatusNotFound, map[string]string{
			"error": "Arquivo JSON de mobs não encontrado.",
		})
		return
	}

	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.Write(data)
}

// --------------------
// /deaths/
// --------------------
func DeathsHandler(w http.ResponseWriter, r *http.Request) {
	data, err := os.ReadFile(deathsFile)
	if err != nil {
		helpers.WriteJSON(w, http.StatusNotFound, map[string]string{
			"error": "Arquivo JSON de deaths não encontrado.",
		})
		return
	}

	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.Write(data)
}
