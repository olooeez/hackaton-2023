DROP TABLE IF EXISTS professor;
DROP TABLE IF EXISTS test;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS grade;
DROP TABLE IF EXISTS student_correction;

CREATE TABLE professor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE test (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    professor_id INTEGER REFERENCES professor(id),
    grade_id INTEGER REFERENCES grade(id),
    title TEXT NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    template BLOB
);

CREATE TABLE grade (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    professor_id INTEGER REFERENCES professor(id),
    title TEXT UNIQUE NOT NULL,
    date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    professor_id INTEGER REFERENCES professor(id),
    grade_id INTEGER REFERENCES grade(id)
);

CREATE TABLE student_correction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER REFERENCES test(id),
    student_id INTEGER REFERENCES student(id),
    score INTEGER,
    corrected_test BLOB
);
