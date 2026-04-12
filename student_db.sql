CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    role VARCHAR(50),
    password VARCHAR(100)
);

select*from users;

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
select *from subjects;
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

select* from student_subjects;
CREATE TABLE marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    subject_id INT,
    marks INT
);

select* from users;
select* from classrooms;

ALTER TABLE marks 
ADD COLUMN internal_marks INT,
ADD COLUMN assignment_marks INT,
ADD COLUMN attendance INT,
ADD COLUMN total_marks INT;

ALTER TABLE marks 
ADD UNIQUE KEY unique_entry (student_id, subject_id);

SELECT email FROM users WHERE role='student';

SELECT id FROM users WHERE email = 'Nayana.ece@skit.org.in';

DELETE FROM marks WHERE id = 8;

DESCRIBE users;

ALTER TABLE classrooms 
ADD FOREIGN KEY (teacher_id) REFERENCES users(id);

ALTER TABLE students 
ADD FOREIGN KEY (user_id) REFERENCES users(id),
ADD FOREIGN KEY (class_id) REFERENCES classrooms(id);

ALTER TABLE subjects 
ADD FOREIGN KEY (class_id) REFERENCES classrooms(id);

ALTER TABLE student_subjects 
ADD FOREIGN KEY (student_id) REFERENCES users(id),
ADD FOREIGN KEY (subject_id) REFERENCES subjects(id);

ALTER TABLE marks 
ADD FOREIGN KEY (student_id) REFERENCES users(id),
ADD FOREIGN KEY (subject_id) REFERENCES subjects(id);


