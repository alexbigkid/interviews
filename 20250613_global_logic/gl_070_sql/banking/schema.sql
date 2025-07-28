-- Banking System Database Schema
-- Demonstrates financial concepts: accounts, transactions, loans, fraud detection

CREATE DATABASE banking_db;
USE banking_db;

-- Bank branches
CREATE TABLE branches (
    branch_id INT PRIMARY KEY AUTO_INCREMENT,
    branch_code VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    phone VARCHAR(20),
    manager_name VARCHAR(100),
    established_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_branch_code (branch_code),
    INDEX idx_city (city)
);

-- Customer information
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_number VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    ssn VARCHAR(11), -- Format: XXX-XX-XXXX
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(50) DEFAULT 'USA',
    customer_type ENUM('individual', 'business') DEFAULT 'individual',
    risk_level ENUM('low', 'medium', 'high') DEFAULT 'low',
    registration_date DATE NOT NULL,
    last_login TIMESTAMP,
    status ENUM('active', 'inactive', 'suspended', 'closed') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_customer_number (customer_number),
    INDEX idx_email (email),
    INDEX idx_ssn (ssn),
    INDEX idx_name (last_name, first_name),
    INDEX idx_status (status)
);

-- Account types
CREATE TABLE account_types (
    account_type_id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    interest_rate DECIMAL(5, 4) DEFAULT 0, -- Annual interest rate
    minimum_balance DECIMAL(12, 2) DEFAULT 0,
    monthly_fee DECIMAL(8, 2) DEFAULT 0,
    transaction_limit INT DEFAULT 0, -- 0 = unlimited
    is_active BOOLEAN DEFAULT TRUE
);

-- Bank accounts
CREATE TABLE accounts (
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    customer_id INT NOT NULL,
    account_type_id INT NOT NULL,
    branch_id INT NOT NULL,
    balance DECIMAL(15, 2) DEFAULT 0.00,
    available_balance DECIMAL(15, 2) DEFAULT 0.00, -- Balance minus holds
    currency VARCHAR(3) DEFAULT 'USD',
    opened_date DATE NOT NULL,
    closed_date DATE,
    status ENUM('active', 'inactive', 'frozen', 'closed') DEFAULT 'active',
    overdraft_limit DECIMAL(10, 2) DEFAULT 0.00,
    last_statement_date DATE,
    interest_rate DECIMAL(5, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (account_type_id) REFERENCES account_types(account_type_id),
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id),
    INDEX idx_account_number (account_number),
    INDEX idx_customer (customer_id),
    INDEX idx_status (status),
    INDEX idx_branch (branch_id)
);

-- Transaction types
CREATE TABLE transaction_types (
    transaction_type_id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    is_credit BOOLEAN NOT NULL, -- TRUE for credits, FALSE for debits
    fee_amount DECIMAL(8, 2) DEFAULT 0
);

-- Transactions
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_number VARCHAR(30) UNIQUE NOT NULL,
    account_id INT NOT NULL,
    transaction_type_id INT NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    balance_after DECIMAL(15, 2) NOT NULL,
    description TEXT,
    reference_number VARCHAR(50),
    related_account_id INT, -- For transfers
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_date DATE,
    status ENUM('pending', 'completed', 'failed', 'reversed') DEFAULT 'pending',
    fee_amount DECIMAL(8, 2) DEFAULT 0,
    location VARCHAR(100), -- ATM location, branch, online, etc.
    created_by VARCHAR(50), -- system, customer, teller, etc.
    notes TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (transaction_type_id) REFERENCES transaction_types(transaction_type_id),
    FOREIGN KEY (related_account_id) REFERENCES accounts(account_id),
    INDEX idx_transaction_number (transaction_number),
    INDEX idx_account (account_id),
    INDEX idx_date (transaction_date),
    INDEX idx_status (status),
    INDEX idx_amount (amount),
    INDEX idx_processing_date (processing_date)
);

-- Loans
CREATE TABLE loans (
    loan_id INT PRIMARY KEY AUTO_INCREMENT,
    loan_number VARCHAR(20) UNIQUE NOT NULL,
    customer_id INT NOT NULL,
    account_id INT, -- Account for disbursement and payments
    loan_type ENUM('personal', 'mortgage', 'auto', 'business', 'student') NOT NULL,
    principal_amount DECIMAL(15, 2) NOT NULL,
    current_balance DECIMAL(15, 2) NOT NULL,
    interest_rate DECIMAL(5, 4) NOT NULL,
    term_months INT NOT NULL,
    monthly_payment DECIMAL(10, 2) NOT NULL,
    origination_date DATE NOT NULL,
    maturity_date DATE NOT NULL,
    next_payment_date DATE,
    last_payment_date DATE,
    status ENUM('active', 'paid_off', 'defaulted', 'suspended') DEFAULT 'active',
    collateral_description TEXT,
    purpose TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    INDEX idx_loan_number (loan_number),
    INDEX idx_customer (customer_id),
    INDEX idx_status (status),
    INDEX idx_next_payment (next_payment_date)
);

-- Loan payments
CREATE TABLE loan_payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    loan_id INT NOT NULL,
    payment_number INT NOT NULL,
    payment_date DATE NOT NULL,
    amount_due DECIMAL(10, 2) NOT NULL,
    amount_paid DECIMAL(10, 2) DEFAULT 0,
    principal_paid DECIMAL(10, 2) DEFAULT 0,
    interest_paid DECIMAL(10, 2) DEFAULT 0,
    fees_paid DECIMAL(10, 2) DEFAULT 0,
    balance_after DECIMAL(15, 2),
    status ENUM('scheduled', 'paid', 'partial', 'late', 'missed') DEFAULT 'scheduled',
    payment_method ENUM('ach', 'check', 'cash', 'card', 'transfer') DEFAULT 'ach',
    transaction_id INT,
    late_fee DECIMAL(8, 2) DEFAULT 0,
    due_date DATE NOT NULL,
    paid_date DATE,
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
    INDEX idx_loan (loan_id),
    INDEX idx_due_date (due_date),
    INDEX idx_status (status)
);

-- Credit cards
CREATE TABLE credit_cards (
    card_id INT PRIMARY KEY AUTO_INCREMENT,
    card_number VARCHAR(20) UNIQUE NOT NULL, -- Encrypted/masked
    customer_id INT NOT NULL,
    account_id INT, -- Connected checking account
    card_type ENUM('credit', 'debit') NOT NULL,
    credit_limit DECIMAL(12, 2),
    current_balance DECIMAL(12, 2) DEFAULT 0,
    available_credit DECIMAL(12, 2),
    annual_fee DECIMAL(8, 2) DEFAULT 0,
    interest_rate DECIMAL(5, 4),
    cash_advance_limit DECIMAL(10, 2),
    issue_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    status ENUM('active', 'inactive', 'blocked', 'expired') DEFAULT 'active',
    last_used TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    INDEX idx_card_number (card_number),
    INDEX idx_customer (customer_id),
    INDEX idx_status (status)
);

-- ATM machines
CREATE TABLE atms (
    atm_id INT PRIMARY KEY AUTO_INCREMENT,
    atm_code VARCHAR(10) UNIQUE NOT NULL,
    location_name VARCHAR(100),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    branch_id INT,
    cash_available DECIMAL(10, 2) DEFAULT 0,
    status ENUM('active', 'inactive', 'out_of_service', 'maintenance') DEFAULT 'active',
    last_maintenance DATE,
    installed_date DATE,
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id),
    INDEX idx_atm_code (atm_code),
    INDEX idx_status (status),
    INDEX idx_city (city)
);

-- Fraud detection alerts
CREATE TABLE fraud_alerts (
    alert_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    account_id INT,
    transaction_id INT,
    card_id INT,
    alert_type ENUM('unusual_location', 'large_amount', 'frequent_transactions', 'velocity_check', 'pattern_analysis') NOT NULL,
    risk_score INT CHECK (risk_score BETWEEN 1 AND 100),
    description TEXT,
    triggered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('open', 'investigating', 'false_positive', 'confirmed_fraud', 'resolved') DEFAULT 'open',
    reviewed_by VARCHAR(50),
    reviewed_date TIMESTAMP,
    actions_taken TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
    FOREIGN KEY (card_id) REFERENCES credit_cards(card_id),
    INDEX idx_customer (customer_id),
    INDEX idx_account (account_id),
    INDEX idx_status (status),
    INDEX idx_risk_score (risk_score),
    INDEX idx_triggered_date (triggered_date)
);

-- Account holds/freezes
CREATE TABLE account_holds (
    hold_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT NOT NULL,
    hold_amount DECIMAL(15, 2) NOT NULL,
    hold_type ENUM('pending_transaction', 'legal_order', 'fraud_investigation', 'overdraft_protection', 'maintenance') NOT NULL,
    reason TEXT,
    placed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    release_date TIMESTAMP,
    status ENUM('active', 'released', 'expired') DEFAULT 'active',
    placed_by VARCHAR(50),
    released_by VARCHAR(50),
    reference_number VARCHAR(50),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    INDEX idx_account (account_id),
    INDEX idx_status (status),
    INDEX idx_placed_date (placed_date)
);

-- Interest calculations and postings
CREATE TABLE interest_postings (
    posting_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT NOT NULL,
    posting_date DATE NOT NULL,
    calculation_period_start DATE NOT NULL,
    calculation_period_end DATE NOT NULL,
    average_balance DECIMAL(15, 2),
    interest_rate DECIMAL(5, 4),
    interest_earned DECIMAL(10, 2),
    transaction_id INT,
    posted_by VARCHAR(50) DEFAULT 'SYSTEM',
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
    INDEX idx_account (account_id),
    INDEX idx_posting_date (posting_date)
);