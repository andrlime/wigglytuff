CREATE TABLE jobs (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    url TEXT NOT NULL,
    source_id TEXT NOT NULL,
    location TEXT,
    date_posted TEXT
);
