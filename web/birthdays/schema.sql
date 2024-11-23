-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS person;

CREATE TABLE person (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    firstname TEXT NOT NULL, 
    birthday TEXT NOT NULL
);