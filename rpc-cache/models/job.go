package models

type JobItem struct {
	Uuid       string `json:"uuid"`
	Title      string `json:"title"`
	Company    string `json:"company"`
	URL        string `json:"url"`
	SourceID   string `json:"source_id"`
	Location   string `json:"location"`
	DatePosted string `json:"date_posted"`
}
