-- ================= DATABASE =================
CREATE DATABASE student_db;
USE student_db;


-- ================= USERS =================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role ENUM('student','teacher') NOT NULL,
    password VARCHAR(100) NOT NULL
);


-- ================= CLASSROOMS =================
CREATE TABLE classrooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    class_code VARCHAR(10) UNIQUE NOT NULL,
    teacher_id INT,
    FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE CASCADE
);


-- ================= SUBJECTS =================
CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL,
    subject_code VARCHAR(10) UNIQUE NOT NULL,
    class_id INT,
    min_attendance INT DEFAULT 0,
    min_internal_marks INT DEFAULT 0,
    assignment_marks INT DEFAULT 0,
    FOREIGN KEY (class_id) REFERENCES classrooms(id) ON DELETE CASCADE
);


-- ================= STUDENTS (CLASS JOIN) =================
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    class_id INT,
    UNIQUE(user_id, class_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classrooms(id) ON DELETE CASCADE
);


-- ================= STUDENT-SUBJECT MAPPING =================
CREATE TABLE student_subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    subject_id INT,
    UNIQUE(student_id, subject_id),
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);


-- ================= MARKS =================
CREATE TABLE marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    subject_id INT,
    internal_marks INT DEFAULT 0,
    assignment_marks INT DEFAULT 0,
    attendance INT DEFAULT 0,
    total_marks INT DEFAULT 0,

    -- OPTIONAL (safe, not used in app but future-ready)
    test_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(student_id, subject_id),

    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);


-- ================= OPTIONAL CHECK QUERIES =================
SELECT * FROM users;
SELECT * FROM classrooms;
SELECT * FROM subjects;
SELECT * FROM student_subjects;
SELECT * FROM marks;

select * from classrooms;


SELECT id, name, email FROM users WHERE role='teacher';

DELETE FROM users 
WHERE email IN (
    'john@skit.org.in',
    'michael@skit.org.in',
    'sarah@skit.org.in',
    'david@skit.org.in'
);