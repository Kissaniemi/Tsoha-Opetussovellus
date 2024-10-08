CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    teacher BOOLEAN DEFAULT FALSE
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    teacher_id INTEGER REFERENCES users,
    description TEXT
);

CREATE TABLE materials (
    id SERIAL PRIMARY KEY,
    name TEXT,
    material TEXT,
    course_id INTEGER REFERENCES courses
);

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    course_id INTEGER REFERENCES courses
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    question TEXT,
    course_id INTEGER REFERENCES courses,
    task_type TEXT
);

CREATE TABLE choices (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks,
    choice TEXT,
    answer BOOLEAN DEFAULT FALSE
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES users,
    task_id INTEGER REFERENCES tasks,
    correct BOOLEAN DEFAULT FALSE
);
