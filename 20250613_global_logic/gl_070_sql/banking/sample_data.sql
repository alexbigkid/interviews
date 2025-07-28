-- Sample Data for Banking System
USE banking_db;

-- Insert branches
INSERT INTO branches (branch_code, name, address, city, state, postal_code, phone, manager_name, established_date, is_active) VALUES
('MAIN001', 'Downtown Main Branch', '100 Financial Plaza', 'New York', 'NY', '10001', '+1-212-555-0100', 'Sarah Johnson', '1985-03-15', TRUE),
('WEST002', 'West Side Branch', '2500 Broadway', 'New York', 'NY', '10025', '+1-212-555-0200', 'Michael Chen', '1992-07-20', TRUE),
('EAST003', 'East Village Branch', '350 East 14th Street', 'New York', 'NY', '10003', '+1-212-555-0300', 'Lisa Rodriguez', '1998-11-10', TRUE),
('BKLN004', 'Brooklyn Heights Branch', '185 Montague Street', 'Brooklyn', 'NY', '11201', '+1-718-555-0400', 'David Kim', '2001-05-12', TRUE),
('QUEE005', 'Queens Plaza Branch', '4102 Northern Blvd', 'Queens', 'NY', '11101', '+1-718-555-0500', 'Maria Gonzalez', '2005-09-01', TRUE);

-- Insert account types
INSERT INTO account_types (type_name, description, interest_rate, minimum_balance, monthly_fee, transaction_limit, is_active) VALUES
('Checking', 'Standard checking account', 0.0100, 100.00, 5.00, 0, TRUE),
('Premium Checking', 'High-yield checking with no fees', 0.0250, 2500.00, 0.00, 0, TRUE),
('Savings', 'Regular savings account', 0.0350, 300.00, 3.00, 6, TRUE),
('High-Yield Savings', 'High-interest savings account', 0.0450, 10000.00, 0.00, 6, TRUE),
('Money Market', 'Money market account with check writing', 0.0400, 5000.00, 10.00, 3, TRUE),
('CD 12-Month', '12-month certificate of deposit', 0.0500, 1000.00, 0.00, 0, TRUE),
('Business Checking', 'Business checking account', 0.0150, 500.00, 15.00, 0, TRUE);

-- Insert transaction types
INSERT INTO transaction_types (type_name, description, is_credit, fee_amount) VALUES
('Deposit', 'Cash or check deposit', TRUE, 0.00),
('Withdrawal', 'Cash withdrawal', FALSE, 0.00),
('ATM Withdrawal', 'ATM cash withdrawal', FALSE, 2.50),
('Transfer In', 'Incoming transfer', TRUE, 0.00),
('Transfer Out', 'Outgoing transfer', FALSE, 3.00),
('Check Payment', 'Check written on account', FALSE, 0.00),
('Direct Deposit', 'Payroll or benefit deposit', TRUE, 0.00),
('ACH Debit', 'Automated payment', FALSE, 0.00),
('Wire Transfer In', 'Incoming wire transfer', TRUE, 0.00),
('Wire Transfer Out', 'Outgoing wire transfer', FALSE, 25.00),
('Interest Payment', 'Interest credited', TRUE, 0.00),
('Monthly Fee', 'Account maintenance fee', FALSE, 0.00),
('Overdraft Fee', 'Insufficient funds fee', FALSE, 35.00),
('Card Purchase', 'Debit card purchase', FALSE, 0.00),
('Online Bill Pay', 'Online bill payment', FALSE, 0.00);

-- Insert customers
INSERT INTO customers (customer_number, first_name, last_name, date_of_birth, ssn, email, phone, address, city, state, postal_code, customer_type, risk_level, registration_date, status) VALUES
('CUST000001', 'John', 'Smith', '1985-03-15', '123-45-6789', 'john.smith@email.com', '+1-555-0101', '456 Park Avenue', 'New York', 'NY', '10016', 'individual', 'low', '2020-01-15', 'active'),
('CUST000002', 'Sarah', 'Johnson', '1990-07-22', '234-56-7890', 'sarah.johnson@email.com', '+1-555-0102', '789 Madison Avenue', 'New York', 'NY', '10021', 'individual', 'low', '2020-03-10', 'active'),
('CUST000003', 'Michael', 'Davis', '1978-11-08', '345-67-8901', 'michael.davis@email.com', '+1-555-0103', '321 5th Avenue', 'New York', 'NY', '10001', 'individual', 'medium', '2019-08-20', 'active'),
('CUST000004', 'Emily', 'Wilson', '1992-04-18', '456-78-9012', 'emily.wilson@email.com', '+1-555-0104', '654 Lexington Avenue', 'New York', 'NY', '10022', 'individual', 'low', '2021-06-05', 'active'),
('CUST000005', 'Robert', 'Brown', '1975-12-03', '567-89-0123', 'robert.brown@email.com', '+1-555-0105', '987 Wall Street', 'New York', 'NY', '10005', 'individual', 'high', '2018-11-12', 'active'),
('CUST000006', 'Tech Solutions LLC', '', '2010-01-01', '12-3456789', 'info@techsolutions.com', '+1-555-0106', '111 Broadway', 'New York', 'NY', '10006', 'business', 'medium', '2020-09-15', 'active'),
('CUST000007', 'Jennifer', 'Garcia', '1988-09-14', '678-90-1234', 'jennifer.garcia@email.com', '+1-555-0107', '222 Columbus Circle', 'New York', 'NY', '10019', 'individual', 'low', '2021-02-28', 'active'),
('CUST000008', 'David', 'Lee', '1983-06-25', '789-01-2345', 'david.lee@email.com', '+1-555-0108', '333 Central Park West', 'New York', 'NY', '10025', 'individual', 'low', '2022-01-10', 'active');

-- Insert accounts
INSERT INTO accounts (account_number, customer_id, account_type_id, branch_id, balance, available_balance, opened_date, status, overdraft_limit, interest_rate) VALUES
('CHK4001234567', 1, 1, 1, 5250.75, 5250.75, '2020-01-20', 'active', 500.00, 0.0100),
('SAV4001234568', 1, 3, 1, 15750.25, 15750.25, '2020-01-20', 'active', 0.00, 0.0350),
('CHK4002345678', 2, 2, 2, 8500.00, 8200.00, '2020-03-15', 'active', 1000.00, 0.0250),
('SAV4002345679', 2, 4, 2, 45000.00, 45000.00, '2020-03-15', 'active', 0.00, 0.0450),
('CHK4003456789', 3, 1, 1, 2875.50, 2375.50, '2019-08-25', 'active', 300.00, 0.0100),
('MMT4003456790', 3, 5, 1, 12000.00, 12000.00, '2019-09-01', 'active', 0.00, 0.0400),
('CHK4004567890', 4, 1, 3, 3250.00, 3250.00, '2021-06-10', 'active', 200.00, 0.0100),
('SAV4004567891', 4, 3, 3, 8500.00, 8500.00, '2021-06-10', 'active', 0.00, 0.0350),
('CHK4005678901', 5, 2, 1, 25000.00, 24000.00, '2018-11-20', 'active', 2000.00, 0.0250),
('BUS4006789012', 6, 7, 4, 85000.00, 85000.00, '2020-09-20', 'active', 5000.00, 0.0150),
('CHK4007890123', 7, 1, 2, 1850.00, 1850.00, '2021-03-05', 'active', 100.00, 0.0100),
('CHK4008901234', 8, 1, 3, 4200.00, 4200.00, '2022-01-15', 'active', 250.00, 0.0100);

-- Insert some transactions (recent activity)
INSERT INTO transactions (transaction_number, account_id, transaction_type_id, amount, balance_after, description, transaction_date, processing_date, status, location, created_by) VALUES
-- John Smith's checking account
('TXN202401150001', 1, 7, 3500.00, 5250.75, 'Salary Direct Deposit', '2024-01-15 08:00:00', '2024-01-15', 'completed', 'ACH Network', 'system'),
('TXN202401160001', 1, 14, -45.00, 5205.75, 'Grocery Store Purchase', '2024-01-16 14:30:00', '2024-01-16', 'completed', 'Local Merchant', 'customer'),
('TXN202401170001', 1, 5, -500.00, 4705.75, 'Transfer to Savings', '2024-01-17 10:15:00', '2024-01-17', 'completed', 'Online Banking', 'customer'),

-- Sarah Johnson's accounts
('TXN202401150002', 3, 7, 4200.00, 8500.00, 'Salary Direct Deposit', '2024-01-15 08:00:00', '2024-01-15', 'completed', 'ACH Network', 'system'),
('TXN202401160002', 3, 3, -150.00, 8350.00, 'ATM Withdrawal', '2024-01-16 19:45:00', '2024-01-16', 'completed', 'ATM-MAIN001-01', 'customer'),
('TXN202401180001', 4, 11, 45.00, 45000.00, 'Monthly Interest', '2024-01-18 00:01:00', '2024-01-18', 'completed', 'System', 'system'),

-- Michael Davis's checking
('TXN202401140001', 5, 6, -1200.00, 2875.50, 'Rent Payment Check', '2024-01-14 16:20:00', '2024-01-15', 'completed', 'Check Processing', 'customer'),
('TXN202401190001', 5, 8, -85.00, 2790.50, 'Utility Bill Payment', '2024-01-19 12:00:00', '2024-01-19', 'completed', 'Online Banking', 'customer'),

-- Business account
('TXN202401120001', 10, 9, 15000.00, 85000.00, 'Client Payment Wire', '2024-01-12 11:30:00', '2024-01-12', 'completed', 'Wire Network', 'system'),
('TXN202401160003', 10, 15, -2500.00, 82500.00, 'Vendor Payment', '2024-01-16 13:45:00', '2024-01-17', 'completed', 'Online Banking', 'customer');

-- Insert loans
INSERT INTO loans (loan_number, customer_id, account_id, loan_type, principal_amount, current_balance, interest_rate, term_months, monthly_payment, origination_date, maturity_date, next_payment_date, status, purpose) VALUES
('LOAN000001', 3, 5, 'auto', 25000.00, 18500.00, 0.0485, 60, 468.50, '2022-01-15', '2027-01-15', '2024-02-15', 'active', 'Vehicle purchase'),
('LOAN000002', 5, 9, 'mortgage', 350000.00, 325000.00, 0.0425, 360, 1724.15, '2019-06-01', '2049-06-01', '2024-02-01', 'active', 'Home purchase'),
('LOAN000003', 1, 1, 'personal', 10000.00, 7500.00, 0.0890, 36, 318.00, '2022-08-10', '2025-08-10', '2024-02-10', 'active', 'Home improvement'),
('LOAN000004', 6, 10, 'business', 100000.00, 85000.00, 0.0650, 84, 1389.50, '2021-03-01', '2028-03-01', '2024-02-01', 'active', 'Equipment purchase');

-- Insert credit cards
INSERT INTO credit_cards (card_number, customer_id, account_id, card_type, credit_limit, current_balance, available_credit, annual_fee, interest_rate, issue_date, expiry_date, status) VALUES
('****-****-****-1234', 1, 1, 'credit', 5000.00, 1250.00, 3750.00, 0.00, 0.1899, '2020-02-01', '2025-02-01', 'active'),
('****-****-****-5678', 2, 3, 'credit', 10000.00, 2150.00, 7850.00, 95.00, 0.1699, '2020-04-15', '2025-04-15', 'active'),
('****-****-****-9012', 3, 5, 'debit', 0.00, 0.00, 0.00, 0.00, 0.0000, '2019-09-10', '2024-09-10', 'active'),
('****-****-****-3456', 5, 9, 'credit', 15000.00, 850.00, 14150.00, 450.00, 0.1599, '2019-01-20', '2024-01-20', 'active'),
('****-****-****-7890', 6, 10, 'credit', 25000.00, 5200.00, 19800.00, 0.00, 0.1499, '2020-10-05', '2025-10-05', 'active');

-- Insert ATMs
INSERT INTO atms (atm_code, location_name, address, city, state, branch_id, cash_available, status, last_maintenance, installed_date) VALUES
('ATM001', 'Main Branch Lobby', '100 Financial Plaza', 'New York', 'NY', 1, 50000.00, 'active', '2024-01-10', '2020-01-15'),
('ATM002', 'West Side Branch', '2500 Broadway', 'New York', 'NY', 2, 35000.00, 'active', '2024-01-08', '2020-03-20'),
('ATM003', 'Times Square', '1515 Broadway', 'New York', 'NY', NULL, 25000.00, 'active', '2024-01-12', '2021-05-15'),
('ATM004', 'Grand Central Station', '89 E 42nd St', 'New York', 'NY', NULL, 40000.00, 'active', '2024-01-09', '2021-08-10'),
('ATM005', 'Brooklyn Heights Branch', '185 Montague Street', 'Brooklyn', 'NY', 4, 30000.00, 'active', '2024-01-11', '2021-12-05');

-- Insert loan payments (historical)
INSERT INTO loan_payments (loan_id, payment_number, payment_date, amount_due, amount_paid, principal_paid, interest_paid, balance_after, status, payment_method, due_date, paid_date) VALUES
-- Auto loan payments
(1, 1, '2022-02-15', 468.50, 468.50, 368.50, 100.00, 24631.50, 'paid', 'ach', '2022-02-15', '2022-02-15'),
(1, 2, '2022-03-15', 468.50, 468.50, 370.00, 98.50, 24261.50, 'paid', 'ach', '2022-03-15', '2022-03-15'),
(1, 24, '2024-01-15', 468.50, 468.50, 425.00, 43.50, 18500.00, 'paid', 'ach', '2024-01-15', '2024-01-15'),
(1, 25, '2024-02-15', 468.50, 0.00, 0.00, 0.00, 18500.00, 'scheduled', 'ach', '2024-02-15', NULL),

-- Mortgage payments
(2, 1, '2019-07-01', 1724.15, 1724.15, 494.15, 1230.00, 349505.85, 'paid', 'ach', '2019-07-01', '2019-07-01'),
(2, 55, '2024-01-01', 1724.15, 1724.15, 875.00, 849.15, 325000.00, 'paid', 'ach', '2024-01-01', '2024-01-01'),
(2, 56, '2024-02-01', 1724.15, 0.00, 0.00, 0.00, 325000.00, 'scheduled', 'ach', '2024-02-01', NULL);

-- Insert fraud alerts
INSERT INTO fraud_alerts (customer_id, account_id, transaction_id, alert_type, risk_score, description, triggered_date, status) VALUES
(3, 5, NULL, 'unusual_location', 75, 'Transaction attempted from unusual geographic location', '2024-01-18 15:30:00', 'false_positive'),
(5, 9, NULL, 'large_amount', 85, 'Large cash withdrawal amount outside normal pattern', '2024-01-17 20:15:00', 'investigating'),
(1, 1, NULL, 'velocity_check', 65, 'Multiple small transactions in short time frame', '2024-01-16 22:45:00', 'resolved');

-- Insert account holds
INSERT INTO account_holds (account_id, hold_amount, hold_type, reason, placed_date, status, placed_by, reference_number) VALUES
(3, 300.00, 'pending_transaction', 'Large purchase pending authorization', '2024-01-19 14:20:00', 'active', 'fraud_system', 'HOLD20240119001'),
(9, 1000.00, 'fraud_investigation', 'Account under fraud investigation', '2024-01-17 16:45:00', 'active', 'fraud_analyst', 'HOLD20240117002');

-- Insert interest postings
INSERT INTO interest_postings (account_id, posting_date, calculation_period_start, calculation_period_end, average_balance, interest_rate, interest_earned, posted_by) VALUES
(2, '2024-01-31', '2024-01-01', '2024-01-31', 15250.00, 0.0350, 44.57, 'SYSTEM'),
(4, '2024-01-31', '2024-01-01', '2024-01-31', 44800.00, 0.0450, 167.95, 'SYSTEM'),
(6, '2024-01-31', '2024-01-01', '2024-01-31', 11950.00, 0.0400, 39.83, 'SYSTEM'),
(8, '2024-01-31', '2024-01-01', '2024-01-31', 8400.00, 0.0350, 24.50, 'SYSTEM');