-- Sample Data for Employee Management System
USE employee_db;

-- Insert departments
INSERT INTO departments (name, description, budget, location) VALUES
('Information Technology', 'Software development and IT infrastructure', 2500000.00, 'Building A, Floor 3'),
('Human Resources', 'Employee relations and talent management', 800000.00, 'Building B, Floor 1'),
('Finance', 'Financial planning and accounting', 1200000.00, 'Building B, Floor 2'),
('Marketing', 'Brand management and customer acquisition', 1500000.00, 'Building A, Floor 2'),
('Sales', 'Revenue generation and client relations', 2000000.00, 'Building C, Floor 1'),
('Operations', 'Business operations and process management', 1800000.00, 'Building C, Floor 2');

-- Insert positions
INSERT INTO positions (title, description, min_salary, max_salary, department_id, level_rank) VALUES
-- IT positions
('Software Engineer I', 'Entry-level software development', 65000, 85000, 1, 1),
('Software Engineer II', 'Mid-level software development', 85000, 110000, 1, 2),
('Senior Software Engineer', 'Senior-level software development', 110000, 140000, 1, 3),
('Technical Lead', 'Technical leadership and architecture', 130000, 165000, 1, 4),
('Engineering Manager', 'Engineering team management', 150000, 190000, 1, 5),
('DevOps Engineer', 'Infrastructure and deployment automation', 90000, 130000, 1, 3),
('QA Engineer', 'Quality assurance and testing', 70000, 95000, 1, 2),

-- HR positions
('HR Coordinator', 'HR administrative support', 45000, 60000, 2, 1),
('HR Business Partner', 'Strategic HR support', 75000, 95000, 2, 3),
('HR Director', 'HR department leadership', 120000, 150000, 2, 5),

-- Finance positions
('Financial Analyst', 'Financial analysis and reporting', 60000, 80000, 3, 2),
('Senior Financial Analyst', 'Advanced financial analysis', 80000, 100000, 3, 3),
('Finance Manager', 'Finance team management', 100000, 130000, 3, 4),
('CFO', 'Chief Financial Officer', 180000, 250000, 3, 5),

-- Marketing positions
('Marketing Coordinator', 'Marketing campaign support', 45000, 60000, 4, 1),
('Marketing Specialist', 'Campaign development and execution', 65000, 85000, 4, 2),
('Marketing Manager', 'Marketing team leadership', 90000, 120000, 4, 4),

-- Sales positions
('Sales Representative', 'Client relationship and sales', 50000, 75000, 5, 1),
('Senior Sales Representative', 'Advanced sales and key accounts', 75000, 100000, 5, 2),
('Sales Manager', 'Sales team management', 100000, 140000, 5, 4),

-- Operations positions
('Operations Analyst', 'Process analysis and improvement', 55000, 75000, 6, 2),
('Operations Manager', 'Operations team leadership', 85000, 115000, 6, 4);

-- Insert employees (starting with managers and then their reports)
INSERT INTO employees (employee_number, first_name, last_name, email, phone, date_of_birth, hire_date, position_id, department_id, manager_id, salary, employment_status, employment_type, address) VALUES
-- Senior leadership (no managers initially)
('EMP001', 'Sarah', 'Johnson', 'sarah.johnson@company.com', '+1-555-0101', '1975-03-15', '2018-01-15', 5, 1, NULL, 175000, 'active', 'full_time', '123 Tech Ave, San Francisco, CA'),
('EMP002', 'Michael', 'Chen', 'michael.chen@company.com', '+1-555-0102', '1972-08-22', '2017-05-10', 10, 2, NULL, 135000, 'active', 'full_time', '456 HR Blvd, San Francisco, CA'),
('EMP003', 'Lisa', 'Anderson', 'lisa.anderson@company.com', '+1-555-0103', '1978-11-03', '2019-03-20', 13, 3, NULL, 200000, 'active', 'full_time', '789 Finance St, San Francisco, CA'),
('EMP004', 'David', 'Rodriguez', 'david.rodriguez@company.com', '+1-555-0104', '1980-06-18', '2020-02-01', 16, 4, NULL, 105000, 'active', 'full_time', '321 Marketing Dr, San Francisco, CA'),
('EMP005', 'Jennifer', 'Wilson', 'jennifer.wilson@company.com', '+1-555-0105', '1976-09-30', '2018-08-15', 18, 5, NULL, 125000, 'active', 'full_time', '654 Sales Plaza, San Francisco, CA'),
('EMP006', 'Robert', 'Taylor', 'robert.taylor@company.com', '+1-555-0106', '1974-12-01', '2019-06-10', 20, 6, NULL, 100000, 'active', 'full_time', '987 Operations Ct, San Francisco, CA'),

-- IT Department employees
('EMP007', 'Emma', 'Davis', 'emma.davis@company.com', '+1-555-0107', '1990-04-12', '2021-01-15', 4, 1, 1, 145000, 'active', 'full_time', '111 Code Lane, San Francisco, CA'),
('EMP008', 'James', 'Brown', 'james.brown@company.com', '+1-555-0108', '1988-07-25', '2020-09-01', 3, 1, 1, 125000, 'active', 'full_time', '222 Dev Road, San Francisco, CA'),
('EMP009', 'Maria', 'Garcia', 'maria.garcia@company.com', '+1-555-0109', '1992-01-08', '2022-03-01', 2, 1, 7, 95000, 'active', 'full_time', '333 Software St, San Francisco, CA'),
('EMP010', 'Kevin', 'Lee', 'kevin.lee@company.com', '+1-555-0110', '1993-10-14', '2022-06-15', 1, 1, 7, 75000, 'active', 'full_time', '444 Junior Ave, San Francisco, CA'),
('EMP011', 'Ashley', 'Miller', 'ashley.miller@company.com', '+1-555-0111', '1989-05-03', '2021-04-01', 6, 1, 1, 115000, 'active', 'full_time', '555 DevOps Dr, San Francisco, CA'),
('EMP012', 'Ryan', 'Jones', 'ryan.jones@company.com', '+1-555-0112', '1991-12-20', '2021-08-15', 7, 1, 8, 85000, 'active', 'full_time', '666 QA Street, San Francisco, CA'),

-- HR Department employees  
('EMP013', 'Nicole', 'White', 'nicole.white@company.com', '+1-555-0113', '1987-02-28', '2020-11-01', 9, 2, 2, 85000, 'active', 'full_time', '777 People Place, San Francisco, CA'),
('EMP014', 'Thomas', 'Clark', 'thomas.clark@company.com', '+1-555-0114', '1994-08-15', '2023-01-10', 8, 2, 2, 52000, 'active', 'full_time', '888 Talent Terrace, San Francisco, CA'),

-- Finance Department employees
('EMP015', 'Amanda', 'Lewis', 'amanda.lewis@company.com', '+1-555-0115', '1985-11-11', '2021-02-15', 12, 3, 3, 115000, 'active', 'full_time', '999 Money Manor, San Francisco, CA'),
('EMP016', 'Daniel', 'Hall', 'daniel.hall@company.com', '+1-555-0116', '1990-07-07', '2022-04-01', 11, 3, 15, 85000, 'active', 'full_time', '101 Budget Blvd, San Francisco, CA'),
('EMP017', 'Michelle', 'Young', 'michelle.young@company.com', '+1-555-0117', '1992-03-25', '2023-02-01', 11, 3, 15, 72000, 'active', 'full_time', '202 Fiscal St, San Francisco, CA'),

-- Marketing Department employees
('EMP018', 'Christopher', 'King', 'christopher.king@company.com', '+1-555-0118', '1986-09-12', '2021-07-01', 15, 4, 4, 78000, 'active', 'full_time', '303 Brand Ave, San Francisco, CA'),
('EMP019', 'Jessica', 'Scott', 'jessica.scott@company.com', '+1-555-0119', '1993-01-30', '2022-09-15', 14, 4, 4, 55000, 'active', 'full_time', '404 Campaign Ct, San Francisco, CA'),

-- Sales Department employees
('EMP020', 'Matthew', 'Green', 'matthew.green@company.com', '+1-555-0120', '1988-06-18', '2021-05-01', 17, 5, 5, 92000, 'active', 'full_time', '505 Revenue Rd, San Francisco, CA'),
('EMP021', 'Lauren', 'Adams', 'lauren.adams@company.com', '+1-555-0121', '1991-10-05', '2022-01-15', 16, 5, 20, 68000, 'active', 'full_time', '606 Client Circle, San Francisco, CA'),
('EMP022', 'Brandon', 'Baker', 'brandon.baker@company.com', '+1-555-0122', '1994-04-22', '2023-03-01', 16, 5, 20, 58000, 'active', 'full_time', '707 Deal Drive, San Francisco, CA'),

-- Operations Department employees
('EMP023', 'Stephanie', 'Nelson', 'stephanie.nelson@company.com', '+1-555-0123', '1989-12-15', '2021-10-01', 19, 6, 6, 68000, 'active', 'full_time', '808 Process Place, San Francisco, CA');

-- Update departments with manager_id
UPDATE departments SET manager_id = 1 WHERE department_id = 1; -- IT
UPDATE departments SET manager_id = 2 WHERE department_id = 2; -- HR  
UPDATE departments SET manager_id = 3 WHERE department_id = 3; -- Finance
UPDATE departments SET manager_id = 4 WHERE department_id = 4; -- Marketing
UPDATE departments SET manager_id = 5 WHERE department_id = 5; -- Sales
UPDATE departments SET manager_id = 6 WHERE department_id = 6; -- Operations

-- Insert salary history
INSERT INTO salary_history (employee_id, old_salary, new_salary, change_date, reason, approved_by) VALUES
(9, 85000, 95000, '2023-01-01', 'Annual performance increase', 7),
(10, 70000, 75000, '2023-01-01', 'Annual performance increase', 7),
(12, 80000, 85000, '2023-01-01', 'Annual performance increase', 8),
(16, 75000, 85000, '2023-06-01', 'Promotion to Senior Analyst', 15),
(21, 62000, 68000, '2023-01-01', 'Annual performance increase', 20),
(22, 55000, 58000, '2023-06-01', 'Performance increase', 20);

-- Insert benefits
INSERT INTO benefits (name, description, benefit_type, cost_employee, cost_employer) VALUES
('Health Insurance Premium', 'Comprehensive health coverage', 'health', 150.00, 450.00),
('Dental Insurance', 'Dental and orthodontic coverage', 'dental', 25.00, 75.00),
('Vision Insurance', 'Eye care and vision correction', 'vision', 15.00, 35.00),
('Life Insurance', 'Basic life insurance coverage', 'life_insurance', 0.00, 50.00),
('401k Match', 'Company 401k matching up to 6%', 'retirement', 0.00, 0.00),
('Paid Time Off', '20 days PTO annually', 'vacation', 0.00, 0.00);

-- Insert employee benefits (assuming all active employees have basic benefits)
INSERT INTO employee_benefits (employee_id, benefit_id, enrollment_date, status, monthly_cost) 
SELECT 
    e.employee_id, 
    b.benefit_id, 
    e.hire_date,
    'active',
    b.cost_employee
FROM employees e
CROSS JOIN benefits b
WHERE e.employment_status = 'active' AND b.benefit_id IN (1, 2, 3, 4, 5, 6);

-- Insert training programs
INSERT INTO training_programs (name, description, provider, duration_hours, cost, category, is_mandatory) VALUES
('New Employee Orientation', 'Company overview and policies', 'Internal HR', 8, 0, 'Onboarding', TRUE),
('Safety Training', 'Workplace safety protocols', 'Safety Corp', 4, 200, 'Safety', TRUE),
('Leadership Development', 'Management and leadership skills', 'Leadership Institute', 40, 2500, 'Leadership', FALSE),
('Technical Skills - Python', 'Python programming fundamentals', 'Tech Academy', 80, 1500, 'Technical', FALSE),
('Project Management', 'PMP certification preparation', 'PM Institute', 60, 3000, 'Management', FALSE),
('Communication Skills', 'Effective workplace communication', 'Comm Experts', 16, 800, 'Soft Skills', FALSE);

-- Insert performance reviews
INSERT INTO performance_reviews (employee_id, reviewer_id, review_period_start, review_period_end, overall_rating, goals_achievement_score, technical_skills_score, communication_score, leadership_score, teamwork_score, strengths, areas_for_improvement, goals_next_period, review_date, status) VALUES
(9, 7, '2023-01-01', '2023-12-31', 'meets', 8, 9, 7, 6, 8, 'Strong technical skills, reliable delivery', 'Communication with stakeholders, leadership presence', 'Lead a major project, improve presentation skills', '2024-01-15', 'final'),
(10, 7, '2023-01-01', '2023-12-31', 'exceeds', 9, 8, 8, 7, 9, 'Fast learner, great team player', 'Take on more complex challenges', 'Senior engineer promotion track', '2024-01-15', 'final'),
(12, 8, '2023-01-01', '2023-12-31', 'meets', 7, 8, 9, 5, 8, 'Excellent attention to detail', 'Automation and tool development', 'Implement test automation framework', '2024-01-15', 'final'),
(16, 15, '2023-01-01', '2023-12-31', 'exceeds', 9, 9, 8, 7, 8, 'Outstanding analytical skills', 'Strategic thinking development', 'Lead financial planning initiatives', '2024-01-15', 'final');

-- Insert time off requests
INSERT INTO time_off_requests (employee_id, request_type, start_date, end_date, total_days, reason, status, requested_date, approved_by, approved_date) VALUES
(9, 'vacation', '2024-03-15', '2024-03-22', 8, 'Family vacation', 'approved', '2024-02-15', 7, '2024-02-16'),
(10, 'sick', '2024-02-10', '2024-02-10', 1, 'Flu symptoms', 'approved', '2024-02-10', 7, '2024-02-10'),
(16, 'vacation', '2024-04-01', '2024-04-05', 5, 'Spring break', 'pending', '2024-03-15', NULL, NULL),
(21, 'personal', '2024-03-20', '2024-03-20', 1, 'Personal appointment', 'approved', '2024-03-15', 20, '2024-03-16');

-- Insert projects
INSERT INTO projects (name, description, start_date, end_date, budget, status, project_manager_id, department_id) VALUES
('Customer Portal Redesign', 'Modernize customer-facing web portal', '2024-01-15', '2024-06-30', 250000, 'active', 7, 1),
('Sales CRM Implementation', 'Deploy new CRM system for sales team', '2024-02-01', '2024-08-31', 180000, 'active', 8, 1),
('HR Digital Transformation', 'Digitize HR processes and workflows', '2024-03-01', '2024-12-31', 150000, 'planning', 13, 2),
('Financial Reporting Automation', 'Automate monthly financial reports', '2024-01-01', '2024-05-31', 100000, 'active', 15, 3);

-- Insert project assignments
INSERT INTO project_assignments (project_id, employee_id, role, allocation_percentage, start_date, hourly_rate, is_active) VALUES
(1, 7, 'Project Manager', 50, '2024-01-15', 75.00, TRUE),
(1, 8, 'Lead Developer', 80, '2024-01-15', 65.00, TRUE),
(1, 9, 'Frontend Developer', 100, '2024-01-20', 50.00, TRUE),
(1, 12, 'QA Lead', 60, '2024-02-01', 45.00, TRUE),
(2, 8, 'Technical Lead', 20, '2024-02-01', 65.00, TRUE),
(2, 10, 'Developer', 100, '2024-02-15', 40.00, TRUE),
(3, 13, 'Project Manager', 75, '2024-03-01', 45.00, TRUE),
(4, 15, 'Project Manager', 30, '2024-01-01', 60.00, TRUE),
(4, 16, 'Financial Analyst', 50, '2024-01-01', 45.00, TRUE);

-- Insert attendance records for the last month
INSERT INTO attendance (employee_id, work_date, clock_in_time, clock_out_time, break_duration_minutes, total_hours, overtime_hours, status) VALUES
-- Sample attendance for employee 9 (Maria Garcia) for March 2024
(9, '2024-03-01', '09:00:00', '17:30:00', 60, 7.5, 0, 'present'),
(9, '2024-03-04', '09:15:00', '17:30:00', 60, 7.25, 0, 'late'),
(9, '2024-03-05', '08:45:00', '18:00:00', 60, 8.25, 0.75, 'present'),
(9, '2024-03-06', '09:00:00', '17:30:00', 60, 7.5, 0, 'present'),
(9, '2024-03-07', '09:00:00', '17:30:00', 60, 7.5, 0, 'present'),
-- Sample for employee 10 (Kevin Lee)
(10, '2024-03-01', '09:00:00', '17:30:00', 60, 7.5, 0, 'present'),
(10, '2024-03-04', '09:00:00', '17:30:00', 60, 7.5, 0, 'present'),
(10, '2024-03-05', NULL, NULL, 0, 0, 0, 'absent'),
(10, '2024-03-06', '09:00:00', '17:30:00', 60, 7.5, 0, 'present'),
(10, '2024-03-07', '09:00:00', '13:00:00', 30, 3.5, 0, 'half_day');