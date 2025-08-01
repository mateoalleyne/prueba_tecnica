CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    plot TEXT,
    image TEXT,
    embedding VECTOR(1536)
);