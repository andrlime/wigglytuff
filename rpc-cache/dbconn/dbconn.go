package dbconn

import "database/sql"

type Rows = *sql.Rows
type Result = sql.Result

type DatabaseConnection interface {
	Connect() error
	Close()
}
