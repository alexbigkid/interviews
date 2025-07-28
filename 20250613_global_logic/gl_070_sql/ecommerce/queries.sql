-- Common E-commerce SQL Queries for Interview Practice

-- 1. Basic SELECT queries
-- Find all products in Electronics category
SELECT p.name, p.price, p.stock_quantity
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE c.name = 'Electronics';

-- 2. Customer order history
-- Get complete order history for a specific customer
SELECT 
    o.order_id,
    o.order_date,
    o.order_status,
    o.total_amount,
    GROUP_CONCAT(CONCAT(p.name, ' (', oi.quantity, ')') SEPARATOR ', ') as items
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.customer_id = 1
GROUP BY o.order_id, o.order_date, o.order_status, o.total_amount
ORDER BY o.order_date DESC;

-- 3. Top selling products
-- Find the top 5 best-selling products by quantity
SELECT 
    p.name,
    p.price,
    SUM(oi.quantity) as total_sold,
    SUM(oi.total_price) as total_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status NOT IN ('cancelled')
GROUP BY p.product_id, p.name, p.price
ORDER BY total_sold DESC
LIMIT 5;

-- 4. Monthly sales report
-- Calculate total sales by month
SELECT 
    YEAR(order_date) as year,
    MONTH(order_date) as month,
    MONTHNAME(order_date) as month_name,
    COUNT(order_id) as total_orders,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order_value
FROM orders
WHERE order_status NOT IN ('cancelled')
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY year DESC, month DESC;

-- 5. Customer analysis
-- Find customers with their total spending and order count
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
    c.email,
    COUNT(o.order_id) as total_orders,
    COALESCE(SUM(o.total_amount), 0) as total_spent,
    COALESCE(AVG(o.total_amount), 0) as avg_order_value,
    MAX(o.order_date) as last_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id 
    AND o.order_status NOT IN ('cancelled')
GROUP BY c.customer_id, c.first_name, c.last_name, c.email
ORDER BY total_spent DESC;

-- 6. Inventory management
-- Products with low stock (less than 50 units)
SELECT 
    p.name,
    p.sku,
    p.stock_quantity,
    c.name as category,
    p.price
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE p.stock_quantity < 50 AND p.is_active = TRUE
ORDER BY p.stock_quantity ASC;

-- 7. Cart abandonment analysis
-- Find customers with items in cart but no recent orders
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
    sc.created_at as cart_created,
    COUNT(ci.cart_item_id) as items_in_cart,
    SUM(p.price * ci.quantity) as cart_value,
    MAX(o.order_date) as last_order_date
FROM customers c
JOIN shopping_carts sc ON c.customer_id = sc.customer_id
JOIN cart_items ci ON sc.cart_id = ci.cart_id
JOIN products p ON ci.product_id = p.product_id
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, sc.created_at
HAVING last_order_date IS NULL OR last_order_date < DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY cart_value DESC;

-- 8. Product performance by category
-- Revenue and units sold by category
SELECT 
    c.name as category,
    COUNT(DISTINCT p.product_id) as total_products,
    SUM(oi.quantity) as total_units_sold,
    SUM(oi.total_price) as total_revenue,
    AVG(pr.rating) as avg_rating,
    COUNT(pr.review_id) as total_reviews
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.order_id AND o.order_status NOT IN ('cancelled')
LEFT JOIN product_reviews pr ON p.product_id = pr.product_id
WHERE c.parent_category_id IS NOT NULL  -- Only subcategories
GROUP BY c.category_id, c.name
ORDER BY total_revenue DESC;

-- 9. Window functions example
-- Rank customers by spending within each month
SELECT 
    customer_id,
    YEAR(order_date) as year,
    MONTH(order_date) as month,
    SUM(total_amount) as monthly_spending,
    RANK() OVER (
        PARTITION BY YEAR(order_date), MONTH(order_date) 
        ORDER BY SUM(total_amount) DESC
    ) as spending_rank,
    DENSE_RANK() OVER (
        PARTITION BY YEAR(order_date), MONTH(order_date) 
        ORDER BY SUM(total_amount) DESC
    ) as dense_spending_rank
FROM orders
WHERE order_status NOT IN ('cancelled')
GROUP BY customer_id, YEAR(order_date), MONTH(order_date)
ORDER BY year DESC, month DESC, spending_rank;

-- 10. Complex subquery
-- Find products that have never been ordered
SELECT 
    p.product_id,
    p.name,
    p.price,
    p.stock_quantity,
    c.name as category
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE p.product_id NOT IN (
    SELECT DISTINCT product_id 
    FROM order_items
)
AND p.is_active = TRUE;

-- 11. CTE (Common Table Expression) example
-- Calculate running total of sales
WITH daily_sales AS (
    SELECT 
        DATE(order_date) as sale_date,
        SUM(total_amount) as daily_total
    FROM orders
    WHERE order_status NOT IN ('cancelled')
    GROUP BY DATE(order_date)
),
running_totals AS (
    SELECT 
        sale_date,
        daily_total,
        SUM(daily_total) OVER (
            ORDER BY sale_date 
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) as running_total
    FROM daily_sales
)
SELECT * FROM running_totals ORDER BY sale_date;

-- 12. Performance query - Find customers' favorite categories
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
    cat.name as favorite_category,
    COUNT(*) as orders_in_category,
    SUM(oi.total_price) as spent_in_category
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN categories cat ON p.category_id = cat.category_id
WHERE o.order_status NOT IN ('cancelled')
GROUP BY c.customer_id, c.first_name, c.last_name, cat.category_id, cat.name
HAVING COUNT(*) = (
    -- Subquery to find the category with most orders for this customer
    SELECT MAX(category_order_count)
    FROM (
        SELECT COUNT(*) as category_order_count
        FROM orders o2
        JOIN order_items oi2 ON o2.order_id = oi2.order_id
        JOIN products p2 ON oi2.product_id = p2.product_id
        WHERE o2.customer_id = c.customer_id 
        AND o2.order_status NOT IN ('cancelled')
        GROUP BY p2.category_id
    ) AS customer_categories
)
ORDER BY c.customer_id;

-- 13. Date/Time functions
-- Orders placed in the last 30 days
SELECT 
    DATE(order_date) as order_day,
    COUNT(*) as orders_count,
    SUM(total_amount) as daily_revenue
FROM orders
WHERE order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
    AND order_status NOT IN ('cancelled')
GROUP BY DATE(order_date)
ORDER BY order_day DESC;