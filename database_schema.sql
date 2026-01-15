-- Database Creation
CREATE DATABASE IF NOT EXISTS enrollment_db;
USE enrollment_db;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'student',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Courses Table
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    link VARCHAR(255),
    credits INT NOT NULL,
    seats INT NOT NULL DEFAULT 30,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. Student Details Table
CREATE TABLE IF NOT EXISTS student_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    enrollment_no VARCHAR(50) UNIQUE,
    phone VARCHAR(20),
    address TEXT,
    dob DATE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. Enrollments Table
CREATE TABLE IF NOT EXISTS enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    date_enrolled DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'enrolled',
    FOREIGN KEY (student_id) REFERENCES student_details(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE KEY _student_course_uc (student_id, course_id)
);

-- Optional: Insert Default Admin (Password: admin123)
-- Note: In a real scenario, you should use the programmed hash, this is just a placeholder example or you'd need to generate the hash manually.
-- INSERT INTO users (name, email, password_hash, role) VALUES ('Admin User', 'admin@university.com', 'scrypt:32768:8:1$PWD_HASH_HERE', 'admin');
