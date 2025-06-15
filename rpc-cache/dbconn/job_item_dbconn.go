package dbconn

import (
	"fmt"
	"log"

	"database/sql"
	_ "github.com/lib/pq"

	"cache/core"
	"cache/models"
	"cache/util"
)

type JobItemDatabaseConnection struct {
	Host         string
	Port         uint16
	Username     string
	Password     string
	DatabaseName string
	SslMode      string
	Conn         *sql.DB
}

func JobItemDbConnFactory(config *core.AppConfig) *JobItemDatabaseConnection {
	newConnection := JobItemDatabaseConnection{}

	newConnection.Username = config.PostgresCredentials.Username
	newConnection.Password = config.PostgresCredentials.Password

	newConnection.Host = config.PostgresConfig.HostName
	newConnection.Port = config.PostgresConfig.Port
	newConnection.DatabaseName = config.PostgresConfig.DatabaseName
	newConnection.SslMode = config.PostgresConfig.SslMode

	return &newConnection
}

func (dbConn *JobItemDatabaseConnection) Connect() error {
	connectionUrl := fmt.Sprintf(
		"postgres://%s:%s@%s:%d/%s?sslmode=%s",
		dbConn.Username, dbConn.Password,
		dbConn.Host, dbConn.Port,
		dbConn.DatabaseName, dbConn.SslMode,
	)

	db, err := sql.Open("postgres", connectionUrl)
	if err != nil {
		return util.WrapError("Db:Connect", err)
	}

	healthcheckErr := db.Ping()
	if healthcheckErr != nil {
		return util.WrapError("Db:Connect:Ping()", healthcheckErr)
	}

	db.SetConnMaxLifetime(0)
	db.SetMaxIdleConns(32)
	db.SetMaxOpenConns(32)

	dbConn.Conn = db
	return nil
}

func (dbConn *JobItemDatabaseConnection) Close() {
	dbConn.Conn.Close()
}

func (dbConn *JobItemDatabaseConnection) GetJobByUuid(uuid string) ([]models.JobItem, error) {
	rows, err := dbConn.Conn.Query("SELECT * FROM jobs WHERE jobs.id = $1;", uuid)
	if err != nil {
		return nil, util.WrapError("Db:GetJobByUuid", err)
	}
	defer rows.Close()

	var results []models.JobItem

	for rows.Next() {
		var job models.JobItem
		if err := rows.Scan(
			&job.Uuid,
			&job.Title,
			&job.Company,
			&job.URL,
			&job.SourceId,
			&job.Location,
			&job.DatePosted,
		); err != nil {
			return nil, err
		}
		results = append(results, job)
	}

	if err := rows.Err(); err != nil {
		return nil, util.WrapError("Db:GetJobByUuid", err)
	}

	log.Printf("%v\n", results)

	return results, nil
}

func (dbConn *JobItemDatabaseConnection) InsertNewJob(job *models.JobItem) error {
	_, err := dbConn.Conn.Exec(`
INSERT INTO jobs (id, title, company, url, source_id, location, date_posted)
VALUES ($1, $2, $3, $4, $5, $6, $7)
	`, job.Uuid, job.Title, job.Company, job.URL, job.SourceId, job.Location, job.DatePosted)
	if err != nil {
		return util.WrapError("Db:InsertNewJob", err)
	}

	return nil
}
