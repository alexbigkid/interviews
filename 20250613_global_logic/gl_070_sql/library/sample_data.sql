-- Sample Data for Library Management System
USE library_db;

-- Insert categories
INSERT INTO categories (name, description) VALUES
('Fiction', 'Novels and fictional works'),
('Non-Fiction', 'Factual and educational books'),
('Science', 'Scientific research and studies'),
('History', 'Historical books and biographies'),
('Technology', 'Computer science and technology'),
('Literature', 'Classic and modern literature'),
('Children', 'Books for children and young adults'),
('Reference', 'Dictionaries, encyclopedias, and reference materials');

-- Insert publishers
INSERT INTO publishers (name, address, contact_email, phone, website) VALUES
('Penguin Random House', '1745 Broadway, New York, NY 10019', 'info@penguinrandomhouse.com', '+1-212-366-2000', 'www.penguinrandomhouse.com'),
('HarperCollins', '195 Broadway, New York, NY 10007', 'info@harpercollins.com', '+1-212-207-7000', 'www.harpercollins.com'),
('Simon & Schuster', '1230 Avenue of the Americas, New York, NY 10020', 'info@simonandschuster.com', '+1-212-698-7000', 'www.simonandschuster.com'),
('Oxford University Press', 'Great Clarendon Street, Oxford OX2 6DP, UK', 'enquiry@oup.com', '+44-1865-556767', 'www.oup.com'),
('MIT Press', '55 Hayward Street, Cambridge, MA 02142', 'mitpress-info@mit.edu', '+1-617-253-5255', 'www.mitpress.mit.edu');

-- Insert authors
INSERT INTO authors (first_name, last_name, birth_date, nationality, biography) VALUES
('George', 'Orwell', '1903-06-25', 'British', 'English novelist and essayist, journalist and critic'),
('Harper', 'Lee', '1926-04-28', 'American', 'American novelist widely known for To Kill a Mockingbird'),
('J.K.', 'Rowling', '1965-07-31', 'British', 'British author, best known for the Harry Potter series'),
('Stephen', 'King', '1947-09-21', 'American', 'American author of horror, supernatural fiction, suspense, and fantasy novels'),
('Agatha', 'Christie', '1890-09-15', 'British', 'English writer known for her detective novels'),
('Isaac', 'Asimov', '1920-01-02', 'American', 'American writer and professor of biochemistry, known for science fiction'),
('Jane', 'Austen', '1775-12-16', 'British', 'English novelist known for her social commentary'),
('Mark', 'Twain', '1835-11-30', 'American', 'American writer, humorist, entrepreneur, publisher, and lecturer');

-- Insert books
INSERT INTO books (isbn, title, subtitle, publication_year, edition, pages, language, publisher_id, category_id, location_code) VALUES
('978-0-452-28423-4', '1984', NULL, 1949, '1st', 328, 'English', 1, 1, 'A1-001'),
('978-0-06-112008-4', 'To Kill a Mockingbird', NULL, 1960, '1st', 376, 'English', 2, 1, 'A1-002'),
('978-0-439-70818-8', 'Harry Potter and the Philosopher''s Stone', NULL, 1997, '1st', 223, 'English', 1, 1, 'B2-001'),
('978-0-385-19395-8', 'The Shining', NULL, 1977, '1st', 447, 'English', 3, 1, 'C3-001'),
('978-0-00-712498-0', 'Murder on the Orient Express', NULL, 1934, '1st', 256, 'English', 2, 1, 'D4-001'),
('978-0-553-29337-0', 'Foundation', NULL, 1951, '1st', 244, 'English', 1, 3, 'E5-001'),
('978-0-14-143951-8', 'Pride and Prejudice', NULL, 1813, '1st', 432, 'English', 1, 6, 'F6-001'),
('978-0-486-40077-3', 'The Adventures of Tom Sawyer', NULL, 1876, '1st', 274, 'English', 4, 7, 'G7-001');

-- Insert book authors relationships
INSERT INTO book_authors (book_id, author_id, author_role) VALUES
(1, 1, 'primary'),
(2, 2, 'primary'),
(3, 3, 'primary'),
(4, 4, 'primary'),
(5, 5, 'primary'),
(6, 6, 'primary'),
(7, 7, 'primary'),
(8, 8, 'primary');

-- Insert book copies
INSERT INTO book_copies (book_id, copy_number, condition_status, acquisition_date, price, is_available) VALUES
(1, 'C001', 'excellent', '2023-01-15', 15.99, TRUE),
(1, 'C002', 'good', '2023-01-15', 15.99, FALSE),
(1, 'C003', 'fair', '2022-06-10', 12.99, TRUE),
(2, 'C004', 'excellent', '2023-02-20', 18.99, FALSE),
(2, 'C005', 'good', '2023-02-20', 18.99, TRUE),
(3, 'C006', 'excellent', '2023-03-10', 22.99, FALSE),
(3, 'C007', 'excellent', '2023-03-10', 22.99, TRUE),
(3, 'C008', 'good', '2022-09-15', 19.99, TRUE),
(4, 'C009', 'excellent', '2023-01-25', 16.99, TRUE),
(5, 'C010', 'good', '2022-12-05', 14.99, FALSE),
(6, 'C011', 'excellent', '2023-04-01', 17.99, TRUE),
(7, 'C012', 'excellent', '2023-02-14', 13.99, TRUE),
(8, 'C013', 'good', '2022-11-20', 11.99, TRUE);

-- Insert members
INSERT INTO members (membership_number, first_name, last_name, email, phone, address, date_of_birth, membership_type, registration_date, expiry_date, is_active) VALUES
('M001001', 'Alice', 'Johnson', 'alice.johnson@email.com', '+1-555-0101', '123 Elm St, Springfield, IL', '1990-05-15', 'adult', '2023-01-10', '2024-01-10', TRUE),
('M001002', 'Bob', 'Smith', 'bob.smith@email.com', '+1-555-0102', '456 Oak Ave, Springfield, IL', '1985-08-22', 'adult', '2023-02-15', '2024-02-15', TRUE),
('M001003', 'Carol', 'Davis', 'carol.davis@email.com', '+1-555-0103', '789 Pine Rd, Springfield, IL', '2005-12-03', 'student', '2023-03-01', '2024-03-01', TRUE),
('M001004', 'David', 'Wilson', 'david.wilson@email.com', '+1-555-0104', '321 Maple Dr, Springfield, IL', '1945-04-18', 'senior', '2023-01-20', '2024-01-20', TRUE),
('M001005', 'Emma', 'Brown', 'emma.brown@email.com', '+1-555-0105', '654 Cedar Ln, Springfield, IL', '1992-11-30', 'faculty', '2023-02-28', '2024-02-28', TRUE),
('M001006', 'Frank', 'Miller', 'frank.miller@email.com', '+1-555-0106', '987 Birch St, Springfield, IL', '1988-07-14', 'adult', '2023-04-05', '2024-04-05', TRUE);

-- Insert staff
INSERT INTO staff (employee_id, first_name, last_name, position, department, email, phone, hire_date, is_active) VALUES
('EMP001', 'Sarah', 'Thompson', 'Head Librarian', 'Administration', 'sarah.thompson@library.gov', '+1-555-1001', '2020-01-15', TRUE),
('EMP002', 'Michael', 'Roberts', 'Reference Librarian', 'Reference', 'michael.roberts@library.gov', '+1-555-1002', '2021-03-10', TRUE),
('EMP003', 'Lisa', 'Anderson', 'Circulation Assistant', 'Circulation', 'lisa.anderson@library.gov', '+1-555-1003', '2022-06-01', TRUE),
('EMP004', 'James', 'Taylor', 'Technical Services', 'Cataloging', 'james.taylor@library.gov', '+1-555-1004', '2021-09-15', TRUE);

-- Insert borrowings
INSERT INTO borrowings (member_id, copy_id, borrowed_date, due_date, returned_date, renewal_count, status) VALUES
(1, 2, '2024-01-15', '2024-02-15', '2024-02-10', 0, 'returned'),
(2, 4, '2024-01-20', '2024-02-20', NULL, 1, 'active'),
(3, 6, '2024-02-01', '2024-03-01', NULL, 0, 'overdue'),
(1, 10, '2024-02-10', '2024-03-10', NULL, 0, 'active'),
(4, 1, '2024-02-15', '2024-03-15', '2024-03-01', 0, 'returned'),
(5, 5, '2024-03-01', '2024-04-01', NULL, 0, 'active');

-- Insert reservations
INSERT INTO reservations (member_id, book_id, reservation_date, expiry_date, status, priority_number) VALUES
(2, 1, '2024-02-20', '2024-03-20', 'active', 1),
(3, 3, '2024-03-01', '2024-04-01', 'active', 1),
(6, 2, '2024-03-05', '2024-04-05', 'active', 1),
(1, 4, '2024-03-10', '2024-04-10', 'active', 1);

-- Insert fines
INSERT INTO fines (borrowing_id, fine_type, amount, description, imposed_date, paid_date, status) VALUES
(3, 'overdue', 5.00, 'Book returned 5 days late', '2024-03-06', NULL, 'unpaid'),
(1, 'overdue', 2.00, 'Book returned 2 days late', '2024-02-12', '2024-02-15', 'paid');

-- Insert transaction log
INSERT INTO transaction_log (transaction_type, member_id, copy_id, staff_id, transaction_date, details) VALUES
('borrow', 1, 2, 3, '2024-01-15 10:30:00', '{"due_date": "2024-02-15", "staff_notes": "Regular checkout"}'),
('return', 1, 2, 3, '2024-02-10 14:20:00', '{"return_condition": "good", "late_days": 0}'),
('borrow', 2, 4, 3, '2024-01-20 09:15:00', '{"due_date": "2024-02-20", "staff_notes": "Member renewed membership"}'),
('renew', 2, 4, 2, '2024-02-18 11:45:00', '{"new_due_date": "2024-03-20", "renewal_count": 1}'),
('borrow', 3, 6, 3, '2024-02-01 16:00:00', '{"due_date": "2024-03-01", "staff_notes": "Student discount applied"}'),
('fine_payment', 1, NULL, 2, '2024-02-15 13:30:00', '{"fine_id": 2, "amount": 2.00, "payment_method": "cash"}');