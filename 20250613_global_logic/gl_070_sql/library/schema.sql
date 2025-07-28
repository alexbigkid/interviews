-- Library Management System Database Schema
-- Demonstrates concepts like: borrowed items tracking, overdue fines, reservations

CREATE DATABASE library_db;
USE library_db;

-- Authors table
CREATE TABLE authors (
    author_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE,
    nationality VARCHAR(50),
    biography TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (last_name, first_name)
);

-- Publishers table
CREATE TABLE publishers (
    publisher_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    address TEXT,
    contact_email VARCHAR(100),
    phone VARCHAR(20),
    website VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Book categories
CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

-- Books table
CREATE TABLE books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    isbn VARCHAR(20) UNIQUE,
    title VARCHAR(200) NOT NULL,
    subtitle VARCHAR(200),
    publication_year YEAR,
    edition VARCHAR(20),
    pages INT,
    language VARCHAR(50) DEFAULT 'English',
    publisher_id INT,
    category_id INT,
    location_code VARCHAR(20), -- Shelf location
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    INDEX idx_title (title),
    INDEX idx_isbn (isbn),
    INDEX idx_publisher (publisher_id),
    INDEX idx_category (category_id)
);

-- Book authors relationship (many-to-many)
CREATE TABLE book_authors (
    book_id INT,
    author_id INT,
    author_role ENUM('primary', 'co-author', 'editor', 'translator') DEFAULT 'primary',
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE
);

-- Book copies (multiple copies of the same book)
CREATE TABLE book_copies (
    copy_id INT PRIMARY KEY AUTO_INCREMENT,
    book_id INT NOT NULL,
    copy_number VARCHAR(20) NOT NULL,
    condition_status ENUM('excellent', 'good', 'fair', 'poor', 'damaged') DEFAULT 'excellent',
    acquisition_date DATE,
    price DECIMAL(8, 2),
    is_available BOOLEAN DEFAULT TRUE,
    notes TEXT,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    UNIQUE KEY unique_book_copy (book_id, copy_number),
    INDEX idx_book (book_id),
    INDEX idx_available (is_available)
);

-- Members table
CREATE TABLE members (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    membership_number VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    address TEXT,
    date_of_birth DATE,
    membership_type ENUM('student', 'adult', 'senior', 'faculty') NOT NULL,
    registration_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_membership_number (membership_number),
    INDEX idx_email (email),
    INDEX idx_name (last_name, first_name)
);

-- Borrowing transactions
CREATE TABLE borrowings (
    borrowing_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT NOT NULL,
    copy_id INT NOT NULL,
    borrowed_date DATE NOT NULL,
    due_date DATE NOT NULL,
    returned_date DATE NULL,
    renewal_count INT DEFAULT 0,
    status ENUM('active', 'returned', 'overdue', 'lost') DEFAULT 'active',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (copy_id) REFERENCES book_copies(copy_id),
    INDEX idx_member (member_id),
    INDEX idx_copy (copy_id),
    INDEX idx_status (status),
    INDEX idx_due_date (due_date)
);

-- Reservations table
CREATE TABLE reservations (
    reservation_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT NOT NULL,
    book_id INT NOT NULL,
    reservation_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    status ENUM('active', 'fulfilled', 'cancelled', 'expired') DEFAULT 'active',
    priority_number INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    INDEX idx_member (member_id),
    INDEX idx_book (book_id),
    INDEX idx_status (status),
    INDEX idx_priority (priority_number)
);

-- Fines table
CREATE TABLE fines (
    fine_id INT PRIMARY KEY AUTO_INCREMENT,
    borrowing_id INT NOT NULL,
    fine_type ENUM('overdue', 'damage', 'lost', 'other') NOT NULL,
    amount DECIMAL(8, 2) NOT NULL,
    description TEXT,
    imposed_date DATE NOT NULL,
    paid_date DATE NULL,
    status ENUM('unpaid', 'paid', 'waived') DEFAULT 'unpaid',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (borrowing_id) REFERENCES borrowings(borrowing_id),
    INDEX idx_borrowing (borrowing_id),
    INDEX idx_status (status),
    INDEX idx_imposed_date (imposed_date)
);

-- Library staff
CREATE TABLE staff (
    staff_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    position VARCHAR(50),
    department VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    hire_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transaction log for audit trail
CREATE TABLE transaction_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_type ENUM('borrow', 'return', 'renew', 'reserve', 'fine_payment') NOT NULL,
    member_id INT,
    copy_id INT,
    staff_id INT,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details JSON,
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (copy_id) REFERENCES book_copies(copy_id),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id),
    INDEX idx_type (transaction_type),
    INDEX idx_date (transaction_date),
    INDEX idx_member (member_id)
);