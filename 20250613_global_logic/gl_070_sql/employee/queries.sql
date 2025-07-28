-- Employee Management System SQL Queries

-- 1. Employee directory with manager information
SELECT 
    e.employee_number,
    CONCAT(e.first_name, ' ', e.last_name) as employee_name,
    p.title as position,
    d.name as department,
    CONCAT(m.first_name, ' ', m.last_name) as manager_name,
    e.email,
    e.hire_date,
    e.employment_status
FROM employees e
JOIN positions p ON e.position_id = p.position_id
JOIN departments d ON e.department_id = d.department_id
LEFT JOIN employees m ON e.manager_id = m.employee_id
WHERE e.employment_status = 'active'
ORDER BY d.name, p.level_rank DESC, e.last_name;

-- 2. Department headcount and salary analysis
SELECT 
    d.name as department,
    COUNT(e.employee_id) as headcount,
    AVG(e.salary) as avg_salary,
    MIN(e.salary) as min_salary,
    MAX(e.salary) as max_salary,
    SUM(e.salary) as total_salary_cost,
    CONCAT(dm.first_name, ' ', dm.last_name) as department_manager
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id AND e.employment_status = 'active'
LEFT JOIN employees dm ON d.manager_id = dm.employee_id
GROUP BY d.department_id, d.name, dm.first_name, dm.last_name
ORDER BY total_salary_cost DESC;

-- 3. Salary ranges by position
SELECT 
    p.title,
    d.name as department,
    p.level_rank,
    COUNT(e.employee_id) as employee_count,
    p.min_salary as position_min,
    p.max_salary as position_max,
    COALESCE(AVG(e.salary), 0) as actual_avg_salary,
    COALESCE(MIN(e.salary), 0) as actual_min_salary,
    COALESCE(MAX(e.salary), 0) as actual_max_salary
FROM positions p
JOIN departments d ON p.department_id = d.department_id
LEFT JOIN employees e ON p.position_id = e.position_id AND e.employment_status = 'active'
GROUP BY p.position_id, p.title, d.name, p.level_rank, p.min_salary, p.max_salary
ORDER BY d.name, p.level_rank;

-- 4. Employee performance ratings distribution
SELECT 
    pr.overall_rating,
    COUNT(*) as employee_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM performance_reviews WHERE status = 'final'), 2) as percentage,
    AVG(pr.goals_achievement_score) as avg_goals_score,
    AVG(pr.technical_skills_score) as avg_technical_score,
    AVG(pr.communication_score) as avg_communication_score
FROM performance_reviews pr
WHERE pr.status = 'final' 
    AND pr.review_period_end = '2023-12-31'
GROUP BY pr.overall_rating
ORDER BY FIELD(pr.overall_rating, 'exceeds', 'meets', 'partially_meets', 'does_not_meet');

-- 5. Employees due for performance reviews
SELECT 
    CONCAT(e.first_name, ' ', e.last_name) as employee_name,
    e.employee_number,
    p.title,
    d.name as department,
    CONCAT(m.first_name, ' ', m.last_name) as manager_name,
    COALESCE(MAX(pr.review_date), 'Never') as last_review_date,
    DATEDIFF(CURDATE(), COALESCE(MAX(pr.review_date), e.hire_date)) as days_since_last_review
FROM employees e
JOIN positions p ON e.position_id = p.position_id
JOIN departments d ON e.department_id = d.department_id
LEFT JOIN employees m ON e.manager_id = m.employee_id
LEFT JOIN performance_reviews pr ON e.employee_id = pr.employee_id AND pr.status = 'final'
WHERE e.employment_status = 'active'
GROUP BY e.employee_id, e.first_name, e.last_name, e.employee_number, p.title, d.name, m.first_name, m.last_name, e.hire_date
HAVING days_since_last_review > 365 OR MAX(pr.review_date) IS NULL
ORDER BY days_since_last_review DESC;

-- 6. Salary history and increases
SELECT 
    CONCAT(e.first_name, ' ', e.last_name) as employee_name,
    sh.change_date,
    sh.old_salary,
    sh.new_salary,
    sh.new_salary - sh.old_salary as increase_amount,
    ROUND((sh.new_salary - sh.old_salary) / sh.old_salary * 100, 2) as increase_percentage,
    sh.reason,
    CONCAT(a.first_name, ' ', a.last_name) as approved_by
FROM salary_history sh
JOIN employees e ON sh.employee_id = e.employee_id
LEFT JOIN employees a ON sh.approved_by = a.employee_id
ORDER BY sh.change_date DESC, increase_percentage DESC;

-- 7. Time off analysis
SELECT 
    CONCAT(e.first_name, ' ', e.last_name) as employee_name,
    tor.request_type,
    COUNT(*) as request_count,
    SUM(tor.total_days) as total_days_requested,
    AVG(tor.total_days) as avg_days_per_request,
    COUNT(CASE WHEN tor.status = 'approved' THEN 1 END) as approved_requests,
    COUNT(CASE WHEN tor.status = 'denied' THEN 1 END) as denied_requests
FROM employees e
JOIN time_off_requests tor ON e.employee_id = tor.employee_id
WHERE tor.requested_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY e.employee_id, e.first_name, e.last_name, tor.request_type
ORDER BY total_days_requested DESC;

-- 8. Training completion status
SELECT 
    tp.name as training_program,
    tp.category,
    COUNT(et.employee_id) as enrolled_count,
    COUNT(CASE WHEN et.status = 'completed' THEN 1 END) as completed_count,
    COUNT(CASE WHEN et.status = 'in_progress' THEN 1 END) as in_progress_count,
    ROUND(COUNT(CASE WHEN et.status = 'completed' THEN 1 END) * 100.0 / COUNT(et.employee_id), 2) as completion_rate,
    AVG(CASE WHEN et.score IS NOT NULL THEN et.score END) as avg_score
FROM training_programs tp
LEFT JOIN employee_training et ON tp.program_id = et.program_id
GROUP BY tp.program_id, tp.name, tp.category
ORDER BY completion_rate DESC, enrolled_count DESC;

-- 9. Project resource allocation
SELECT 
    p.name as project_name,
    p.status as project_status,
    CONCAT(pm.first_name, ' ', pm.last_name) as project_manager,
    COUNT(pa.employee_id) as team_size,
    SUM(pa.allocation_percentage) as total_allocation,
    AVG(pa.allocation_percentage) as avg_allocation,
    SUM(pa.hourly_rate * pa.allocation_percentage / 100) as estimated_hourly_cost
FROM projects p
LEFT JOIN employees pm ON p.project_manager_id = pm.employee_id
LEFT JOIN project_assignments pa ON p.project_id = pa.project_id AND pa.is_active = TRUE
GROUP BY p.project_id, p.name, p.status, pm.first_name, pm.last_name
ORDER BY total_allocation DESC;

-- 10. Employee utilization across projects
SELECT 
    CONCAT(e.first_name, ' ', e.last_name) as employee_name,
    p.title as position,
    COUNT(pa.project_id) as active_projects,
    SUM(pa.allocation_percentage) as total_allocation,
    GROUP_CONCAT(CONCAT(pr.name, ' (', pa.allocation_percentage, '%)') SEPARATOR ', ') as project_details
FROM employees e
JOIN positions p ON e.position_id = p.position_id
LEFT JOIN project_assignments pa ON e.employee_id = pa.employee_id AND pa.is_active = TRUE
LEFT JOIN projects pr ON pa.project_id = pr.project_id
WHERE e.employment_status = 'active'
GROUP BY e.employee_id, e.first_name, e.last_name, p.title
HAVING total_allocation > 100 OR total_allocation < 50
ORDER BY total_allocation DESC;

-- 11. Benefits enrollment analysis
SELECT 
    b.name as benefit_name,
    b.benefit_type,
    COUNT(eb.employee_id) as enrolled_employees,
    SUM(eb.monthly_cost) as total_employee_cost,
    SUM(b.cost_employer) as total_employer_cost,
    ROUND(COUNT(eb.employee_id) * 100.0 / (SELECT COUNT(*) FROM employees WHERE employment_status = 'active'), 2) as enrollment_percentage
FROM benefits b
LEFT JOIN employee_benefits eb ON b.benefit_id = eb.benefit_id AND eb.status = 'active'
GROUP BY b.benefit_id, b.name, b.benefit_type
ORDER BY enrollment_percentage DESC;

-- 12. Attendance patterns and issues
SELECT 
    CONCAT(e.first_name, ' ', e.last_name) as employee_name,
    COUNT(a.attendance_id) as total_days,
    COUNT(CASE WHEN a.status = 'present' THEN 1 END) as present_days,
    COUNT(CASE WHEN a.status = 'absent' THEN 1 END) as absent_days,
    COUNT(CASE WHEN a.status = 'late' THEN 1 END) as late_days,
    ROUND(COUNT(CASE WHEN a.status = 'present' THEN 1 END) * 100.0 / COUNT(a.attendance_id), 2) as attendance_rate,
    AVG(a.total_hours) as avg_daily_hours,
    SUM(a.overtime_hours) as total_overtime_hours
FROM employees e
LEFT JOIN attendance a ON e.employee_id = a.employee_id 
    AND a.work_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
WHERE e.employment_status = 'active'
GROUP BY e.employee_id, e.first_name, e.last_name
HAVING total_days > 0
ORDER BY attendance_rate ASC, late_days DESC;

-- 13. Manager span of control analysis
SELECT 
    CONCAT(m.first_name, ' ', m.last_name) as manager_name,
    p.title as manager_position,
    d.name as department,
    COUNT(e.employee_id) as direct_reports,
    AVG(e.salary) as avg_subordinate_salary,
    SUM(e.salary) as total_team_cost
FROM employees m
JOIN positions p ON m.position_id = p.position_id
JOIN departments d ON m.department_id = d.department_id
LEFT JOIN employees e ON m.employee_id = e.manager_id AND e.employment_status = 'active'
WHERE m.employment_status = 'active'
GROUP BY m.employee_id, m.first_name, m.last_name, p.title, d.name
HAVING direct_reports > 0
ORDER BY direct_reports DESC;

-- 14. Career progression tracking
WITH employee_tenure AS (
    SELECT 
        e.employee_id,
        CONCAT(e.first_name, ' ', e.last_name) as employee_name,
        e.hire_date,
        DATEDIFF(CURDATE(), e.hire_date) / 365.25 as years_of_service,
        e.salary as current_salary,
        p.level_rank as current_level
    FROM employees e
    JOIN positions p ON e.position_id = p.position_id
    WHERE e.employment_status = 'active'
),
salary_progression AS (
    SELECT 
        sh.employee_id,
        COUNT(*) as salary_increases,
        SUM(sh.new_salary - sh.old_salary) as total_increase,
        MIN(sh.old_salary) as starting_salary
    FROM salary_history sh
    GROUP BY sh.employee_id
)
SELECT 
    et.employee_name,
    et.years_of_service,
    et.current_level,
    COALESCE(sp.starting_salary, et.current_salary) as starting_salary,
    et.current_salary,
    et.current_salary - COALESCE(sp.starting_salary, et.current_salary) as total_salary_growth,
    COALESCE(sp.salary_increases, 0) as number_of_raises,
    ROUND((et.current_salary - COALESCE(sp.starting_salary, et.current_salary)) / et.years_of_service, 0) as avg_annual_increase
FROM employee_tenure et
LEFT JOIN salary_progression sp ON et.employee_id = sp.employee_id
WHERE et.years_of_service >= 1
ORDER BY et.years_of_service DESC, total_salary_growth DESC;