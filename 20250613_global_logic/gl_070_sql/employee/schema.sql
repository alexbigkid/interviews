-- Employee Management System Database Schema
-- Demonstrates HR concepts: departments, roles, salaries, performance reviews

CREATE DATABASE employee_db;
USE employee_db;

-- Departments table
CREATE TABLE departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    budget DECIMAL(12, 2),
    location VARCHAR(100),
    manager_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_manager (manager_id)
);

-- Job titles/positions
CREATE TABLE positions (
    position_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    min_salary DECIMAL(10, 2),
    max_salary DECIMAL(10, 2),
    department_id INT,
    level_rank INT, -- 1 = entry level, 5 = senior
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    INDEX idx_department (department_id),
    INDEX idx_level (level_rank)
);

-- Employees table
CREATE TABLE employees (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_number VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    date_of_birth DATE,
    hire_date DATE NOT NULL,
    termination_date DATE NULL,
    position_id INT,
    department_id INT,
    manager_id INT,
    salary DECIMAL(10, 2),
    employment_status ENUM('active', 'inactive', 'terminated', 'on_leave') DEFAULT 'active',
    employment_type ENUM('full_time', 'part_time', 'contract', 'intern') DEFAULT 'full_time',
    address TEXT,
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (position_id) REFERENCES positions(position_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (manager_id) REFERENCES employees(employee_id),
    INDEX idx_employee_number (employee_number),
    INDEX idx_email (email),
    INDEX idx_name (last_name, first_name),
    INDEX idx_department (department_id),
    INDEX idx_manager (manager_id),
    INDEX idx_hire_date (hire_date),
    INDEX idx_status (employment_status)
);

-- Add foreign key for department manager after employees table is created
ALTER TABLE departments 
ADD FOREIGN KEY (manager_id) REFERENCES employees(employee_id);

-- Salary history table
CREATE TABLE salary_history (
    salary_history_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    old_salary DECIMAL(10, 2),
    new_salary DECIMAL(10, 2) NOT NULL,
    change_date DATE NOT NULL,
    reason VARCHAR(200),
    approved_by INT,
    notes TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (approved_by) REFERENCES employees(employee_id),
    INDEX idx_employee (employee_id),
    INDEX idx_change_date (change_date)
);

-- Performance reviews table
CREATE TABLE performance_reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    reviewer_id INT NOT NULL,
    review_period_start DATE NOT NULL,
    review_period_end DATE NOT NULL,
    overall_rating ENUM('exceeds', 'meets', 'partially_meets', 'does_not_meet') NOT NULL,
    goals_achievement_score INT CHECK (goals_achievement_score BETWEEN 1 AND 10),
    technical_skills_score INT CHECK (technical_skills_score BETWEEN 1 AND 10),
    communication_score INT CHECK (communication_score BETWEEN 1 AND 10),
    leadership_score INT CHECK (leadership_score BETWEEN 1 AND 10),
    teamwork_score INT CHECK (teamwork_score BETWEEN 1 AND 10),
    strengths TEXT,
    areas_for_improvement TEXT,
    goals_next_period TEXT,
    review_date DATE NOT NULL,
    status ENUM('draft', 'submitted', 'approved', 'final') DEFAULT 'draft',
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (reviewer_id) REFERENCES employees(employee_id),
    INDEX idx_employee (employee_id),
    INDEX idx_reviewer (reviewer_id),
    INDEX idx_review_date (review_date),
    INDEX idx_rating (overall_rating)
);

-- Employee benefits table
CREATE TABLE benefits (
    benefit_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    benefit_type ENUM('health', 'dental', 'vision', 'life_insurance', 'retirement', 'vacation', 'other') NOT NULL,
    cost_employee DECIMAL(8, 2) DEFAULT 0,
    cost_employer DECIMAL(8, 2) DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

-- Employee benefits enrollment
CREATE TABLE employee_benefits (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    benefit_id INT NOT NULL,
    enrollment_date DATE NOT NULL,
    termination_date DATE NULL,
    status ENUM('active', 'terminated', 'suspended') DEFAULT 'active',
    monthly_cost DECIMAL(8, 2),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (benefit_id) REFERENCES benefits(benefit_id),
    INDEX idx_employee (employee_id),
    INDEX idx_benefit (benefit_id),
    INDEX idx_status (status)
);

-- Time off requests
CREATE TABLE time_off_requests (
    request_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    request_type ENUM('vacation', 'sick', 'personal', 'bereavement', 'maternity', 'paternity') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_days DECIMAL(3, 1) NOT NULL,
    reason TEXT,
    status ENUM('pending', 'approved', 'denied', 'cancelled') DEFAULT 'pending',
    requested_date DATE NOT NULL,
    approved_by INT,
    approved_date DATE,
    comments TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (approved_by) REFERENCES employees(employee_id),
    INDEX idx_employee (employee_id),
    INDEX idx_status (status),
    INDEX idx_dates (start_date, end_date)
);

-- Training programs
CREATE TABLE training_programs (
    program_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    provider VARCHAR(100),
    duration_hours INT,
    cost DECIMAL(8, 2),
    category VARCHAR(50),
    is_mandatory BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Employee training records
CREATE TABLE employee_training (
    training_record_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    program_id INT NOT NULL,
    enrollment_date DATE NOT NULL,
    completion_date DATE,
    score DECIMAL(5, 2),
    status ENUM('enrolled', 'in_progress', 'completed', 'failed', 'cancelled') DEFAULT 'enrolled',
    certificate_issued BOOLEAN DEFAULT FALSE,
    notes TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (program_id) REFERENCES training_programs(program_id),
    INDEX idx_employee (employee_id),
    INDEX idx_program (program_id),
    INDEX idx_status (status)
);

-- Employee attendance tracking
CREATE TABLE attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    work_date DATE NOT NULL,
    clock_in_time TIME,
    clock_out_time TIME,
    break_duration_minutes INT DEFAULT 0,
    total_hours DECIMAL(4, 2),
    overtime_hours DECIMAL(4, 2) DEFAULT 0,
    status ENUM('present', 'absent', 'late', 'half_day', 'remote') DEFAULT 'present',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    UNIQUE KEY unique_employee_date (employee_id, work_date),
    INDEX idx_employee (employee_id),
    INDEX idx_date (work_date),
    INDEX idx_status (status)
);

-- Projects table
CREATE TABLE projects (
    project_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    budget DECIMAL(12, 2),
    status ENUM('planning', 'active', 'on_hold', 'completed', 'cancelled') DEFAULT 'planning',
    project_manager_id INT,
    department_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_manager_id) REFERENCES employees(employee_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    INDEX idx_manager (project_manager_id),
    INDEX idx_department (department_id),
    INDEX idx_status (status)
);

-- Project assignments
CREATE TABLE project_assignments (
    assignment_id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    employee_id INT NOT NULL,
    role VARCHAR(100),
    allocation_percentage INT DEFAULT 100 CHECK (allocation_percentage BETWEEN 1 AND 100),
    start_date DATE NOT NULL,
    end_date DATE,
    hourly_rate DECIMAL(8, 2),
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    INDEX idx_project (project_id),
    INDEX idx_employee (employee_id),
    INDEX idx_active (is_active)
);