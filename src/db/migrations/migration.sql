-- Migration: 001_initial_schema.sql

CREATE TABLE IF NOT EXISTS videos (
    UniqueID INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT NOT NULL,
    language TEXT,
    status INTEGER CHECK (status IN (0, 1, 2, 3)) DEFAULT 0
);

-- Index for performance if you often filter by status
CREATE INDEX IF NOT EXISTS idx_video_status ON videos(status);