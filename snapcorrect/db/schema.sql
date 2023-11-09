DROP TABLE IF EXISTS professor;

CREATE TABLE
    professor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
