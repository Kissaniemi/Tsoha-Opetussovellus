CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    teacher BOOLEAN
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    teacher_id INTEGER REFERENCES users,
    description TEXT
);

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    course_id INTEGER REFERENCES courses
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    name TEXT,
    question TEXT,
    course_id INTEGER REFERENCES courses
);

CREATE TABLE points (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES users,
    task_id INTEGER REFERENCES tasks,
    points INTEGER
);
