# Library Management System

A comprehensive database schema for managing library operations including book catalog, member management, borrowing/returning, reservations, and fines.

## Schema Overview

```mermaid
erDiagram
    authors ||--o{ book_authors : "writes"
    books ||--o{ book_authors : "written by"
    books ||--o{ book_copies : "has copies"
    books ||--o{ reservations : "reserved"
    publishers ||--o{ books : "publishes"
    categories ||--o{ books : "categorizes"
    
    members ||--o{ borrowings : "borrows"
    members ||--o{ reservations : "makes"
    
    book_copies ||--o{ borrowings : "borrowed as"
    borrowings ||--o{ fines : "incurs"
    
    staff ||--o{ transaction_log : "processes"
    
    authors {
        int author_id PK
        string first_name
        string last_name
        date birth_date
        string nationality
        text biography
    }
    
    publishers {
        int publisher_id PK
        string name
        text address
        string contact_email
        string phone
        string website
    }
    
    categories {
        int category_id PK
        string name
        text description
    }
    
    books {
        int book_id PK
        string isbn
        string title
        string subtitle
        year publication_year
        string edition
        int pages
        string language
        int publisher_id FK
        int category_id FK
        string location_code
    }
    
    book_authors {
        int book_id FK
        int author_id FK
        enum author_role
    }
    
    book_copies {
        int copy_id PK
        int book_id FK
        string copy_number
        enum condition_status
        date acquisition_date
        decimal price
        boolean is_available
        text notes
    }
    
    members {
        int member_id PK
        string membership_number
        string first_name
        string last_name
        string email
        string phone
        text address
        date date_of_birth
        enum membership_type
        date registration_date
        date expiry_date
        boolean is_active
    }
    
    borrowings {
        int borrowing_id PK
        int member_id FK
        int copy_id FK
        date borrowed_date
        date due_date
        date returned_date
        int renewal_count
        enum status
        text notes
    }
    
    reservations {
        int reservation_id PK
        int member_id FK
        int book_id FK
        date reservation_date
        date expiry_date
        enum status
        int priority_number
    }
    
    fines {
        int fine_id PK
        int borrowing_id FK
        enum fine_type
        decimal amount
        text description
        date imposed_date
        date paid_date
        enum status
    }
    
    staff {
        int staff_id PK
        string employee_id
        string first_name
        string last_name
        string position
        string department
        string email
        string phone
        date hire_date
        boolean is_active
    }
    
    transaction_log {
        int log_id PK
        enum transaction_type
        int member_id FK
        int copy_id FK
        int staff_id FK
        timestamp transaction_date
        json details
    }
```

## Key Features

### 1. **Multi-Author Support**
- Many-to-many relationship between books and authors
- Support for different author roles (primary, co-author, editor, translator)

### 2. **Copy Management**
- Multiple copies of the same book
- Individual tracking of condition and availability
- Acquisition date and cost tracking

### 3. **Member Management**
- Different membership types (student, adult, senior, faculty)
- Membership expiration tracking
- Contact information management

### 4. **Borrowing System**
- Due date calculation
- Renewal tracking
- Multiple status states (active, returned, overdue, lost)

### 5. **Reservation System**
- Queue management with priority numbers
- Automatic expiration of reservations
- Status tracking

### 6. **Fine Management**
- Different fine types (overdue, damage, lost)
- Payment tracking
- Fine calculation automation

### 7. **Audit Trail**
- Complete transaction logging
- JSON details for flexible data storage
- Staff activity tracking

## Common Library Operations

### Book Availability Check
```sql
SELECT COUNT(*) as available_copies
FROM book_copies bc
JOIN books b ON bc.book_id = b.book_id
WHERE b.isbn = '978-0-452-28423-4' 
AND bc.is_available = TRUE;
```

### Check Out Process
```sql
-- Update copy availability
UPDATE book_copies SET is_available = FALSE WHERE copy_id = ?;

-- Create borrowing record
INSERT INTO borrowings (member_id, copy_id, borrowed_date, due_date)
VALUES (?, ?, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY));
```

### Calculate Overdue Fines
```sql
SELECT 
    borrowing_id,
    DATEDIFF(CURDATE(), due_date) as days_overdue,
    DATEDIFF(CURDATE(), due_date) * 0.50 as fine_amount
FROM borrowings
WHERE status = 'overdue' AND due_date < CURDATE();
```

## Interview Questions

### Schema Design
1. **Why separate books from book_copies?**
   - Same book can have multiple physical copies
   - Individual tracking of condition and availability
   - Historical lending data per copy

2. **How to handle series of books?**
   - Add series_id and volume_number to books table
   - Create separate series table for metadata

3. **Managing book reservations fairly?**
   - Priority queue with reservation_date ordering
   - Member type priority (faculty > adult > student)
   - First-come-first-served within same priority

### Business Logic
1. **Automatic fine calculation**
2. **Reservation expiration**
3. **Member privilege levels**
4. **Renewal limits**
5. **Lost book handling**

### Performance Considerations
- Index on due_date for overdue queries
- Index on member_id for quick lookup
- Index on isbn for book searches
- Composite index on (book_id, is_available)

## Practice Scenarios

1. **Overdue Management** - Find all overdue books and calculate fines
2. **Popular Books** - Identify most borrowed titles
3. **Member Analytics** - Track reading patterns
4. **Inventory Reports** - Books needing replacement
5. **Staff Performance** - Transaction processing metrics