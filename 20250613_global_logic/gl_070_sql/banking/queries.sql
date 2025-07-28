-- Banking System SQL Queries

-- 1. Customer account summary
SELECT 
    c.customer_number,
    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
    c.customer_type,
    COUNT(a.account_id) as total_accounts,
    SUM(a.balance) as total_balance,
    AVG(a.balance) as average_balance,
    MAX(a.balance) as highest_balance,
    b.name as primary_branch
FROM customers c
LEFT JOIN accounts a ON c.customer_id = a.customer_id AND a.status = 'active'
LEFT JOIN branches b ON a.branch_id = b.branch_id
WHERE c.status = 'active'
GROUP BY c.customer_id, c.customer_number, c.first_name, c.last_name, c.customer_type, b.name
ORDER BY total_balance DESC;

-- 2. Account balances and transaction activity
SELECT 
    a.account_number,
    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
    at.type_name as account_type,
    a.balance,
    a.available_balance,
    COUNT(t.transaction_id) as transaction_count_30days,
    SUM(CASE WHEN tt.is_credit THEN t.amount ELSE 0 END) as total_credits_30days,
    SUM(CASE WHEN NOT tt.is_credit THEN t.amount ELSE 0 END) as total_debits_30days,
    MAX(t.transaction_date) as last_transaction_date
FROM accounts a
JOIN customers c ON a.customer_id = c.customer_id
JOIN account_types at ON a.account_type_id = at.account_type_id
LEFT JOIN transactions t ON a.account_id = t.account_id 
    AND t.transaction_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    AND t.status = 'completed'
LEFT JOIN transaction_types tt ON t.transaction_type_id = tt.transaction_type_id
WHERE a.status = 'active'
GROUP BY a.account_id, a.account_number, c.first_name, c.last_name, at.type_name, a.balance, a.available_balance
ORDER BY a.balance DESC;

-- 3. Daily transaction volume and revenue
SELECT 
    DATE(t.transaction_date) as transaction_date,
    COUNT(t.transaction_id) as transaction_count,
    SUM(CASE WHEN tt.is_credit THEN t.amount ELSE 0 END) as total_credits,
    SUM(CASE WHEN NOT tt.is_credit THEN t.amount ELSE 0 END) as total_debits,
    SUM(t.fee_amount) as total_fees_collected,
    COUNT(DISTINCT t.account_id) as unique_accounts,
    AVG(t.amount) as average_transaction_amount
FROM transactions t
JOIN transaction_types tt ON t.transaction_type_id = tt.transaction_type_id
WHERE t.status = 'completed' 
    AND t.transaction_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY DATE(t.transaction_date)
ORDER BY transaction_date DESC;

-- 4. Loan portfolio analysis
SELECT 
    l.loan_type,
    COUNT(l.loan_id) as total_loans,
    SUM(l.principal_amount) as total_principal,
    SUM(l.current_balance) as outstanding_balance,
    AVG(l.interest_rate) as avg_interest_rate,
    AVG(l.current_balance) as avg_loan_balance,
    COUNT(CASE WHEN l.status = 'active' THEN 1 END) as active_loans,
    COUNT(CASE WHEN l.status = 'defaulted' THEN 1 END) as defaulted_loans,
    ROUND(COUNT(CASE WHEN l.status = 'defaulted' THEN 1 END) * 100.0 / COUNT(l.loan_id), 2) as default_rate
FROM loans l
GROUP BY l.loan_type
ORDER BY outstanding_balance DESC;

-- 5. Loan payment status and delinquency
SELECT 
    l.loan_number,
    CONCAT(c.first_name, ' ', c.last_name) as borrower_name,
    l.loan_type,
    l.current_balance,
    l.monthly_payment,
    l.next_payment_date,
    DATEDIFF(CURDATE(), l.next_payment_date) as days_past_due,
    COUNT(lp.payment_id) as total_payments,
    COUNT(CASE WHEN lp.status = 'late' THEN 1 END) as late_payments,
    COUNT(CASE WHEN lp.status = 'missed' THEN 1 END) as missed_payments,
    SUM(CASE WHEN lp.status IN ('late', 'missed') THEN lp.late_fee ELSE 0 END) as total_late_fees,
    CASE 
        WHEN DATEDIFF(CURDATE(), l.next_payment_date) > 90 THEN 'Seriously Delinquent'
        WHEN DATEDIFF(CURDATE(), l.next_payment_date) > 30 THEN 'Delinquent'
        WHEN DATEDIFF(CURDATE(), l.next_payment_date) > 0 THEN 'Past Due'
        ELSE 'Current'
    END as payment_status
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
LEFT JOIN loan_payments lp ON l.loan_id = lp.loan_id
WHERE l.status = 'active'
GROUP BY l.loan_id, l.loan_number, c.first_name, c.last_name, l.loan_type, l.current_balance, l.monthly_payment, l.next_payment_date
ORDER BY days_past_due DESC, l.current_balance DESC;

-- 6. Credit card utilization and risk analysis
SELECT 
    cc.card_number,
    CONCAT(c.first_name, ' ', c.last_name) as cardholder_name,
    cc.credit_limit,
    cc.current_balance,
    cc.available_credit,
    ROUND(cc.current_balance / cc.credit_limit * 100, 2) as utilization_percentage,
    DATEDIFF(CURDATE(), cc.last_used) as days_since_last_use,
    CASE 
        WHEN cc.current_balance / cc.credit_limit > 0.9 THEN 'High Risk'
        WHEN cc.current_balance / cc.credit_limit > 0.7 THEN 'Medium Risk'
        WHEN cc.current_balance / cc.credit_limit > 0.3 THEN 'Low Risk'
        ELSE 'Very Low Risk'
    END as risk_category
FROM credit_cards cc
JOIN customers c ON cc.customer_id = c.customer_id
WHERE cc.status = 'active' AND cc.card_type = 'credit'
ORDER BY utilization_percentage DESC;

-- 7. Fraud detection and security alerts
SELECT 
    fa.alert_id,
    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
    a.account_number,
    fa.alert_type,
    fa.risk_score,
    fa.description,
    fa.triggered_date,
    fa.status,
    DATEDIFF(CURDATE(), DATE(fa.triggered_date)) as days_open,
    fa.reviewed_by,
    fa.actions_taken
FROM fraud_alerts fa
LEFT JOIN customers c ON fa.customer_id = c.customer_id
LEFT JOIN accounts a ON fa.account_id = a.account_id
WHERE fa.status IN ('open', 'investigating')
ORDER BY fa.risk_score DESC, fa.triggered_date DESC;

-- 8. Branch performance metrics
SELECT 
    b.branch_code,
    b.name as branch_name,
    b.city,
    b.manager_name,
    COUNT(DISTINCT a.account_id) as total_accounts,
    SUM(a.balance) as total_deposits,
    AVG(a.balance) as average_account_balance,
    COUNT(DISTINCT a.customer_id) as unique_customers,
    COUNT(DISTINCT CASE WHEN a.opened_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN a.account_id END) as new_accounts_30days,
    SUM(CASE WHEN a.opened_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN a.balance ELSE 0 END) as new_deposits_30days
FROM branches b
LEFT JOIN accounts a ON b.branch_id = a.branch_id AND a.status = 'active'
GROUP BY b.branch_id, b.branch_code, b.name, b.city, b.manager_name
ORDER BY total_deposits DESC;

-- 9. ATM usage and cash management
SELECT 
    atm.atm_code,
    atm.location_name,
    atm.city,
    atm.cash_available,
    COUNT(t.transaction_id) as withdrawal_count_30days,
    SUM(CASE WHEN tt.type_name = 'ATM Withdrawal' THEN t.amount ELSE 0 END) as total_withdrawals_30days,
    AVG(CASE WHEN tt.type_name = 'ATM Withdrawal' THEN t.amount END) as avg_withdrawal_amount,
    SUM(t.fee_amount) as fees_collected_30days,
    CASE 
        WHEN atm.cash_available < 10000 THEN 'Low Cash - Refill Needed'
        WHEN atm.cash_available < 25000 THEN 'Medium Cash'
        ELSE 'Adequate Cash'
    END as cash_status
FROM atms atm
LEFT JOIN transactions t ON t.location LIKE CONCAT('%', atm.atm_code, '%')
    AND t.transaction_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    AND t.status = 'completed'
LEFT JOIN transaction_types tt ON t.transaction_type_id = tt.transaction_type_id
WHERE atm.status = 'active'
GROUP BY atm.atm_id, atm.atm_code, atm.location_name, atm.city, atm.cash_available
ORDER BY total_withdrawals_30days DESC;

-- 10. Customer profitability analysis
WITH customer_revenue AS (
    SELECT 
        c.customer_id,
        SUM(t.fee_amount) as transaction_fees,
        SUM(CASE WHEN l.loan_id IS NOT NULL THEN lp.interest_paid ELSE 0 END) as loan_interest,
        SUM(CASE WHEN cc.card_id IS NOT NULL THEN cc.annual_fee / 12 ELSE 0 END) as card_fees,
        SUM(at.monthly_fee) as account_fees
    FROM customers c
    LEFT JOIN accounts a ON c.customer_id = a.customer_id
    LEFT JOIN transactions t ON a.account_id = t.account_id 
        AND t.transaction_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
    LEFT JOIN loans l ON c.customer_id = l.customer_id
    LEFT JOIN loan_payments lp ON l.loan_id = lp.loan_id 
        AND lp.paid_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
    LEFT JOIN credit_cards cc ON c.customer_id = cc.customer_id
    LEFT JOIN account_types at ON a.account_type_id = at.account_type_id
    GROUP BY c.customer_id
)
SELECT 
    c.customer_number,
    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
    c.customer_type,
    COALESCE(cr.transaction_fees, 0) as annual_transaction_fees,
    COALESCE(cr.loan_interest, 0) as annual_loan_interest,
    COALESCE(cr.card_fees, 0) as annual_card_fees,
    COALESCE(cr.account_fees, 0) as annual_account_fees,
    COALESCE(cr.transaction_fees + cr.loan_interest + cr.card_fees + cr.account_fees, 0) as total_annual_revenue,
    SUM(a.balance) as total_deposits,
    COUNT(a.account_id) as account_count
FROM customers c
LEFT JOIN customer_revenue cr ON c.customer_id = cr.customer_id
LEFT JOIN accounts a ON c.customer_id = a.customer_id AND a.status = 'active'
WHERE c.status = 'active'
GROUP BY c.customer_id, c.customer_number, c.first_name, c.last_name, c.customer_type, cr.transaction_fees, cr.loan_interest, cr.card_fees, cr.account_fees
ORDER BY total_annual_revenue DESC;

-- 11. Account holds and frozen funds analysis
SELECT 
    ah.hold_id,
    a.account_number,
    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
    ah.hold_amount,
    ah.hold_type,
    ah.reason,
    ah.placed_date,
    DATEDIFF(CURDATE(), ah.placed_date) as days_held,
    ah.placed_by,
    ah.status,
    CASE 
        WHEN ah.hold_type = 'fraud_investigation' THEN 'High Priority'
        WHEN ah.hold_type = 'legal_order' THEN 'Legal Required'
        WHEN DATEDIFF(CURDATE(), ah.placed_date) > 7 THEN 'Review Required'
        ELSE 'Normal'
    END as priority_level
FROM account_holds ah
JOIN accounts a ON ah.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
WHERE ah.status = 'active'
ORDER BY ah.placed_date DESC, ah.hold_amount DESC;

-- 12. Interest earned and paid analysis
SELECT 
    a.account_number,
    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
    at.type_name as account_type,
    a.balance,
    a.interest_rate,
    SUM(ip.interest_earned) as ytd_interest_earned,
    COUNT(ip.posting_id) as interest_postings,
    AVG(ip.average_balance) as avg_monthly_balance,
    ROUND(SUM(ip.interest_earned) / a.balance * 100, 4) as effective_yield
FROM accounts a
JOIN customers c ON a.customer_id = c.customer_id
JOIN account_types at ON a.account_type_id = at.account_type_id
LEFT JOIN interest_postings ip ON a.account_id = ip.account_id 
    AND ip.posting_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
WHERE a.status = 'active' AND at.interest_rate > 0
GROUP BY a.account_id, a.account_number, c.first_name, c.last_name, at.type_name, a.balance, a.interest_rate
HAVING ytd_interest_earned > 0
ORDER BY ytd_interest_earned DESC;

-- 13. Risk assessment by customer
SELECT 
    c.customer_number,
    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
    c.risk_level as assigned_risk_level,
    COUNT(DISTINCT a.account_id) as account_count,
    SUM(a.balance) as total_balance,
    COUNT(DISTINCT l.loan_id) as loan_count,
    SUM(l.current_balance) as total_loan_balance,
    COUNT(fa.alert_id) as fraud_alerts_12months,
    COUNT(ah.hold_id) as active_holds,
    CASE 
        WHEN COUNT(fa.alert_id) > 3 THEN 'High Risk'
        WHEN COUNT(fa.alert_id) > 1 OR COUNT(ah.hold_id) > 0 THEN 'Medium Risk'
        WHEN SUM(a.balance) > 100000 THEN 'High Value'
        ELSE 'Low Risk'
    END as calculated_risk_level
FROM customers c
LEFT JOIN accounts a ON c.customer_id = a.customer_id AND a.status = 'active'
LEFT JOIN loans l ON c.customer_id = l.customer_id AND l.status = 'active'
LEFT JOIN fraud_alerts fa ON c.customer_id = fa.customer_id 
    AND fa.triggered_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
LEFT JOIN account_holds ah ON a.account_id = ah.account_id AND ah.status = 'active'
WHERE c.status = 'active'
GROUP BY c.customer_id, c.customer_number, c.first_name, c.last_name, c.risk_level
ORDER BY fraud_alerts_12months DESC, total_balance DESC;

-- 14. Monthly financial summary
SELECT 
    DATE_FORMAT(t.transaction_date, '%Y-%m') as month,
    COUNT(DISTINCT t.account_id) as active_accounts,
    COUNT(t.transaction_id) as total_transactions,
    SUM(CASE WHEN tt.is_credit THEN t.amount ELSE 0 END) as total_deposits,
    SUM(CASE WHEN NOT tt.is_credit THEN t.amount ELSE 0 END) as total_withdrawals,
    SUM(t.fee_amount) as fee_revenue,
    (SELECT SUM(ip.interest_earned) 
     FROM interest_postings ip 
     WHERE DATE_FORMAT(ip.posting_date, '%Y-%m') = DATE_FORMAT(t.transaction_date, '%Y-%m')) as interest_paid,
    (SELECT COUNT(*) 
     FROM accounts a 
     WHERE DATE_FORMAT(a.opened_date, '%Y-%m') = DATE_FORMAT(t.transaction_date, '%Y-%m')) as new_accounts,
    (SELECT COUNT(*) 
     FROM loans l 
     WHERE DATE_FORMAT(l.origination_date, '%Y-%m') = DATE_FORMAT(t.transaction_date, '%Y-%m')) as new_loans
FROM transactions t
JOIN transaction_types tt ON t.transaction_type_id = tt.transaction_type_id
WHERE t.status = 'completed' 
    AND t.transaction_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY DATE_FORMAT(t.transaction_date, '%Y-%m')
ORDER BY month DESC;