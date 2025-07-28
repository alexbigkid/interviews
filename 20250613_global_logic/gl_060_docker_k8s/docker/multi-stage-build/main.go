package main

import (
    "encoding/json"
    "log"
    "net/http"
    "os"
)

type Response struct {
    Message string `json:"message"`
    Version string `json:"version"`
}

func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        response := Response{
            Message: "Hello from Go in Docker!",
            Version: "1.0",
        }
        json.NewEncoder(w).Encode(response)
    })

    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }

    log.Printf("Server starting on port %s", port)
    log.Fatal(http.ListenAndServe(":"+port, nil))
}