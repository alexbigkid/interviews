-- Library Management System SQL Queries

-- 1. Find all available books with author information
SELECT 
    b.title,
    CONCAT(a.first_name, ' ', a.last_name) as author_name,
    c.name as category,
    p.name as publisher,
    COUNT(bc.copy_id) as available_copies
FROM books b
JOIN book_authors ba ON b.book_id = ba.book_id
JOIN authors a ON ba.author_id = a.author_id
JOIN categories c ON b.category_id = c.category_id
JOIN publishers p ON b.publisher_id = p.publisher_id
JOIN book_copies bc ON b.book_id = bc.book_id
WHERE bc.is_available = TRUE AND ba.author_role = 'primary'
GROUP BY b.book_id, b.title, a.first_name, a.last_name, c.name, p.name
ORDER BY b.title;

-- 2. Current borrowings with member details
SELECT 
    CONCAT(m.first_name, ' ', m.last_name) as member_name,
    m.membership_number,
    b.title,
    bc.copy_number,
    br.borrowed_date,
    br.due_date,
    DATEDIFF(CURDATE(), br.due_date) as days_overdue,
    br.renewal_count,
    CASE 
        WHEN br.due_date < CURDATE() THEN 'OVERDUE'
        WHEN DATEDIFF(br.due_date, CURDATE()) <= 3 THEN 'DUE SOON'
        ELSE 'ACTIVE'
    END as status_alert
FROM borrowings br
JOIN members m ON br.member_id = m.member_id
JOIN book_copies bc ON br.copy_id = bc.copy_id
JOIN books b ON bc.book_id = b.book_id
WHERE br.status = 'active' OR br.status = 'overdue'
ORDER BY br.due_date;

-- 3. Overdue books and fines
SELECT 
    CONCAT(m.first_name, ' ', m.last_name) as member_name,
    m.email,
    b.title,
    br.due_date,
    DATEDIFF(CURDATE(), br.due_date) as days_overdue,
    COALESCE(SUM(f.amount), 0) as total_fines,
    COUNT(f.fine_id) as fine_count
FROM borrowings br
JOIN members m ON br.member_id = m.member_id
JOIN book_copies bc ON br.copy_id = bc.copy_id
JOIN books b ON bc.book_id = b.book_id
LEFT JOIN fines f ON br.borrowing_id = f.borrowing_id AND f.status = 'unpaid'
WHERE br.status = 'overdue' OR br.due_date < CURDATE()
GROUP BY br.borrowing_id, m.member_id, m.first_name, m.last_name, m.email, b.title, br.due_date
ORDER BY days_overdue DESC;

-- 4. Popular books (most borrowed)
SELECT 
    b.title,
    CONCAT(a.first_name, ' ', a.last_name) as author_name,
    c.name as category,
    COUNT(br.borrowing_id) as times_borrowed,
    AVG(DATEDIFF(COALESCE(br.returned_date, CURDATE()), br.borrowed_date)) as avg_loan_days
FROM books b
JOIN book_authors ba ON b.book_id = ba.book_id AND ba.author_role = 'primary'
JOIN authors a ON ba.author_id = a.author_id
JOIN categories c ON b.category_id = c.category_id
JOIN book_copies bc ON b.book_id = bc.book_id
LEFT JOIN borrowings br ON bc.copy_id = br.copy_id
GROUP BY b.book_id, b.title, a.first_name, a.last_name, c.name
HAVING times_borrowed > 0
ORDER BY times_borrowed DESC, avg_loan_days ASC
LIMIT 10;

-- 5. Member borrowing statistics
SELECT 
    CONCAT(m.first_name, ' ', m.last_name) as member_name,
    m.membership_type,
    COUNT(CASE WHEN br.status = 'active' THEN 1 END) as current_loans,
    COUNT(CASE WHEN br.status = 'returned' THEN 1 END) as completed_loans,
    COUNT(CASE WHEN br.status = 'overdue' THEN 1 END) as overdue_loans,
    SUM(CASE WHEN f.status = 'unpaid' THEN f.amount ELSE 0 END) as outstanding_fines,
    MAX(br.borrowed_date) as last_borrow_date
FROM members m
LEFT JOIN borrowings br ON m.member_id = br.member_id
LEFT JOIN fines f ON br.borrowing_id = f.borrowing_id
WHERE m.is_active = TRUE
GROUP BY m.member_id, m.first_name, m.last_name, m.membership_type
ORDER BY current_loans DESC, outstanding_fines DESC;

-- 6. Book availability and reservation queue
SELECT 
    b.title,
    CONCAT(a.first_name, ' ', a.last_name) as author_name,
    COUNT(bc.copy_id) as total_copies,
    COUNT(CASE WHEN bc.is_available = TRUE THEN 1 END) as available_copies,
    COUNT(CASE WHEN bc.is_available = FALSE THEN 1 END) as borrowed_copies,
    COUNT(r.reservation_id) as reservations_pending,
    MIN(r.reservation_date) as earliest_reservation
FROM books b
JOIN book_authors ba ON b.book_id = ba.book_id AND ba.author_role = 'primary'
JOIN authors a ON ba.author_id = a.author_id
JOIN book_copies bc ON b.book_id = bc.book_id
LEFT JOIN reservations r ON b.book_id = r.book_id AND r.status = 'active'
GROUP BY b.book_id, b.title, a.first_name, a.last_name
HAVING reservations_pending > 0 OR available_copies = 0
ORDER BY reservations_pending DESC, available_copies ASC;

-- 7. Monthly borrowing trends
SELECT 
    YEAR(borrowed_date) as year,
    MONTH(borrowed_date) as month,
    MONTHNAME(borrowed_date) as month_name,
    COUNT(*) as total_loans,
    COUNT(DISTINCT member_id) as unique_borrowers,
    COUNT(DISTINCT bc.book_id) as unique_books,
    AVG(DATEDIFF(COALESCE(returned_date, CURDATE()), borrowed_date)) as avg_loan_duration
FROM borrowings br
JOIN book_copies bc ON br.copy_id = bc.copy_id
WHERE borrowed_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY YEAR(borrowed_date), MONTH(borrowed_date)
ORDER BY year DESC, month DESC;

-- 8. Books that need replacement (poor condition or lost)
SELECT 
    b.title,
    bc.copy_number,
    bc.condition_status,
    COUNT(CASE WHEN br.status = 'lost' THEN 1 END) as lost_count,
    MAX(br.borrowed_date) as last_borrowed,
    DATEDIFF(CURDATE(), bc.acquisition_date) as age_in_days
FROM books b
JOIN book_copies bc ON b.book_id = bc.book_id
LEFT JOIN borrowings br ON bc.copy_id = br.copy_id
WHERE bc.condition_status IN ('poor', 'damaged') 
   OR bc.copy_id IN (SELECT copy_id FROM borrowings WHERE status = 'lost')
GROUP BY b.book_id, b.title, bc.copy_id, bc.copy_number, bc.condition_status, bc.acquisition_date
ORDER BY lost_count DESC, bc.condition_status, age_in_days DESC;

-- 9. Staff performance metrics
SELECT 
    CONCAT(s.first_name, ' ', s.last_name) as staff_name,
    s.position,
    COUNT(CASE WHEN tl.transaction_type = 'borrow' THEN 1 END) as checkouts_processed,
    COUNT(CASE WHEN tl.transaction_type = 'return' THEN 1 END) as returns_processed,
    COUNT(CASE WHEN tl.transaction_type = 'fine_payment' THEN 1 END) as fine_payments,
    COUNT(*) as total_transactions,
    MIN(tl.transaction_date) as first_transaction,
    MAX(tl.transaction_date) as last_transaction
FROM staff s
LEFT JOIN transaction_log tl ON s.staff_id = tl.staff_id
WHERE s.is_active = TRUE
  AND tl.transaction_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY s.staff_id, s.first_name, s.last_name, s.position
ORDER BY total_transactions DESC;

-- 10. Revenue from fines
SELECT 
    DATE_FORMAT(imposed_date, '%Y-%m') as month,
    COUNT(*) as total_fines,
    SUM(amount) as total_amount,
    SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END) as collected_amount,
    SUM(CASE WHEN status = 'unpaid' THEN amount ELSE 0 END) as outstanding_amount,
    AVG(amount) as avg_fine_amount
FROM fines
WHERE imposed_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY DATE_FORMAT(imposed_date, '%Y-%m')
ORDER BY month DESC;

-- 11. Advanced: Find members who should be contacted for overdue books
WITH overdue_members AS (
    SELECT 
        m.member_id,
        CONCAT(m.first_name, ' ', m.last_name) as member_name,
        m.email,
        m.phone,
        COUNT(br.borrowing_id) as overdue_count,
        SUM(DATEDIFF(CURDATE(), br.due_date)) as total_overdue_days,
        MAX(DATEDIFF(CURDATE(), br.due_date)) as max_overdue_days,
        SUM(COALESCE(f.amount, 0)) as total_fines
    FROM members m
    JOIN borrowings br ON m.member_id = br.member_id
    LEFT JOIN fines f ON br.borrowing_id = f.borrowing_id AND f.status = 'unpaid'
    WHERE br.status = 'overdue' AND m.is_active = TRUE
    GROUP BY m.member_id, m.first_name, m.last_name, m.email, m.phone
)
SELECT 
    *,
    CASE 
        WHEN max_overdue_days > 30 THEN 'URGENT'
        WHEN max_overdue_days > 14 THEN 'HIGH'
        WHEN max_overdue_days > 7 THEN 'MEDIUM'
        ELSE 'LOW'
    END as priority_level
FROM overdue_members
ORDER BY max_overdue_days DESC, total_fines DESC;

-- 12. Book collection analysis by category
SELECT 
    c.name as category,
    COUNT(DISTINCT b.book_id) as unique_titles,
    COUNT(bc.copy_id) as total_copies,
    COUNT(CASE WHEN bc.is_available = TRUE THEN 1 END) as available_copies,
    ROUND(COUNT(CASE WHEN bc.is_available = TRUE THEN 1 END) * 100.0 / COUNT(bc.copy_id), 2) as availability_percentage,
    COUNT(br.borrowing_id) as total_borrows_all_time,
    AVG(b.pages) as avg_pages
FROM categories c
LEFT JOIN books b ON c.category_id = b.category_id
LEFT JOIN book_copies bc ON b.book_id = bc.book_id
LEFT JOIN borrowings br ON bc.copy_id = br.copy_id
GROUP BY c.category_id, c.name
ORDER BY total_borrows_all_time DESC;