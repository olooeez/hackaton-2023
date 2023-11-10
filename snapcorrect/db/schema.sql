DROP TABLE IF EXISTS professor;
DROP TABLE IF EXISTS test;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS student_correction;

CREATE TABLE professor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE test (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    professor_id INTEGER REFERENCES professor(id),
    title TEXT NOT NULL,
    date DATE,
    template BLOB
);

CREATE TABLE student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    professor_id INTEGER REFERENCES professor(id)
);

CREATE TABLE student_correction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER REFERENCES test(id),
    student_id INTEGER REFERENCES student(id),
    score INTEGER,
    corrected_test BLOB
);
