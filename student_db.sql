CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    role VARCHAR(50),
    password VARCHAR(100)
);

CREATE TABLE classrooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(100),
    class_code VARCHAR(10) UNIQUE,
    teacher_id INT
);

CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id VARCHAR(20),
    subject_name VARCHAR(100),
    subject_code VARCHAR(10) UNIQUE,
    class_id INT,
    min_attendance INT,
    min_internal_marks INT,
    assignment_marks INT
);

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    class_id INT,
    UNIQUE(user_id, class_id)
);

CREATE TABLE student_subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    subject_id INT,
    UNIQUE(student_id, subject_id)
);