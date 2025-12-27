package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/gofiber/fiber/v2"
	_ "github.com/go-sql-driver/mysql"
	"github.com/google/uuid"
)

type AppContext struct {
	DB *sql.DB
}

func main() {
	// Connect to MySQL
    // user:password@tcp(host:port)/dbname
	dsn := os.Getenv("DATABASE_URL")
	if dsn == "" {
		dsn = "root:root@tcp(localhost:3306)/roadsense?parseTime=true"
	}

	db, err := sql.Open("mysql", dsn)
	if err != nil {
		log.Fatalf("Error opening database: %v", err)
	}
	defer db.Close()

	if err := db.Ping(); err != nil {
		log.Fatalf("Error connecting to database: %v", err)
	}

	appCtx := &AppContext{DB: db}
	app := fiber.New()

	app.Post("/video/upload", appCtx.UploadVideo)
	app.Get("/health", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{"status": "ok"})
	})

	log.Println("IngestionVideo microservice running on port 8080")
	log.Fatal(app.Listen(":8080"))
}

func (a *AppContext) UploadVideo(c *fiber.Ctx) error {
	file, err := c.FormFile("file")
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "File is required",
		})
	}

	videoID := uuid.New().String()

	// MySQL query with ?
	query := "INSERT INTO videos (id, filename, uploaded_at, source_type) VALUES (?, ?, ?, ?)"
	_, err = a.DB.ExecContext(context.Background(), query, videoID, file.Filename, time.Now(), "dashcam")

	if err != nil {
		log.Printf("DB Error: %v", err)
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "DB insert failed",
		})
	}

	return c.JSON(fiber.Map{
		"video_id": videoID,
		"filename": file.Filename,
		"status":   "video registered",
	})
}

