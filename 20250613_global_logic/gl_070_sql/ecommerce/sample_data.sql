-- Sample Data for E-commerce Database
USE ecommerce_db;

-- Insert categories
INSERT INTO categories (name, description, parent_category_id) VALUES
('Electronics', 'Electronic devices and gadgets', NULL),
('Clothing', 'Apparel and fashion items', NULL),
('Books', 'Books and literature', NULL),
('Home & Garden', 'Home improvement and gardening', NULL),
('Laptops', 'Portable computers', 1),
('Smartphones', 'Mobile phones', 1),
('Men''s Clothing', 'Clothing for men', 2),
('Women''s Clothing', 'Clothing for women', 2),
('Fiction', 'Fiction books', 3),
('Non-Fiction', 'Non-fiction books', 3);

-- Insert products
INSERT INTO products (name, description, price, sku, category_id, stock_quantity, weight, is_active) VALUES
('MacBook Pro 16"', 'High-performance laptop for professionals', 2499.99, 'MBP16-001', 5, 25, 2.0, TRUE),
('iPhone 14 Pro', 'Latest smartphone with advanced camera', 999.99, 'IPH14P-001', 6, 150, 0.2, TRUE),
('Samsung Galaxy S23', 'Android smartphone with excellent display', 799.99, 'SGS23-001', 6, 75, 0.2, TRUE),
('Dell XPS 13', 'Ultrabook for everyday computing', 1299.99, 'DXPS13-001', 5, 40, 1.3, TRUE),
('Men''s Cotton T-Shirt', 'Comfortable cotton t-shirt', 29.99, 'MCT-001', 7, 200, 0.2, TRUE),
('Women''s Denim Jeans', 'Classic blue denim jeans', 79.99, 'WDJ-001', 8, 120, 0.5, TRUE),
('The Great Gatsby', 'Classic American novel', 12.99, 'TGG-001', 9, 500, 0.3, TRUE),
('Atomic Habits', 'Self-improvement book', 16.99, 'AH-001', 10, 300, 0.4, TRUE),
('Wireless Headphones', 'Noise-cancelling headphones', 199.99, 'WH-001', 1, 80, 0.3, TRUE),
('Smart Watch', 'Fitness tracking smartwatch', 299.99, 'SW-001', 1, 60, 0.1, TRUE);

-- Insert customers
INSERT INTO customers (first_name, last_name, email, phone, date_of_birth) VALUES
('John', 'Smith', 'john.smith@email.com', '+1-555-0101', '1990-05-15'),
('Sarah', 'Johnson', 'sarah.johnson@email.com', '+1-555-0102', '1988-11-22'),
('Michael', 'Brown', 'michael.brown@email.com', '+1-555-0103', '1992-03-08'),
('Emily', 'Davis', 'emily.davis@email.com', '+1-555-0104', '1985-07-14'),
('David', 'Wilson', 'david.wilson@email.com', '+1-555-0105', '1993-12-01'),
('Lisa', 'Anderson', 'lisa.anderson@email.com', '+1-555-0106', '1987-09-30'),
('Robert', 'Taylor', 'robert.taylor@email.com', '+1-555-0107', '1991-04-18'),
('Jennifer', 'Thomas', 'jennifer.thomas@email.com', '+1-555-0108', '1989-08-25');

-- Insert addresses
INSERT INTO addresses (customer_id, address_type, street_address, city, state_province, postal_code, country, is_default) VALUES
(1, 'shipping', '123 Main St', 'New York', 'NY', '10001', 'USA', TRUE),
(1, 'billing', '123 Main St', 'New York', 'NY', '10001', 'USA', TRUE),
(2, 'shipping', '456 Oak Ave', 'Los Angeles', 'CA', '90210', 'USA', TRUE),
(2, 'billing', '456 Oak Ave', 'Los Angeles', 'CA', '90210', 'USA', TRUE),
(3, 'shipping', '789 Pine Rd', 'Chicago', 'IL', '60601', 'USA', TRUE),
(3, 'billing', '789 Pine Rd', 'Chicago', 'IL', '60601', 'USA', TRUE),
(4, 'shipping', '321 Elm St', 'Houston', 'TX', '77001', 'USA', TRUE),
(4, 'billing', '321 Elm St', 'Houston', 'TX', '77001', 'USA', TRUE);

-- Insert shopping carts
INSERT INTO shopping_carts (customer_id) VALUES
(1), (2), (3), (4), (5);

-- Insert cart items
INSERT INTO cart_items (cart_id, product_id, quantity) VALUES
(1, 1, 1),  -- John has MacBook Pro in cart
(1, 9, 1),  -- John has Wireless Headphones in cart
(2, 2, 1),  -- Sarah has iPhone 14 Pro in cart
(2, 5, 2),  -- Sarah has 2 Men's T-Shirts in cart
(3, 3, 1),  -- Michael has Samsung Galaxy S23 in cart
(4, 6, 1),  -- Emily has Women's Jeans in cart
(4, 7, 3),  -- Emily has 3 Great Gatsby books in cart
(5, 10, 1); -- David has Smart Watch in cart

-- Insert orders
INSERT INTO orders (customer_id, order_status, shipping_address_id, billing_address_id, subtotal, tax_amount, shipping_cost, total_amount, payment_status) VALUES
(1, 'delivered', 1, 2, 1299.99, 104.00, 15.99, 1419.98, 'paid'),
(2, 'shipped', 3, 4, 799.99, 64.00, 12.99, 876.98, 'paid'),
(3, 'processing', 5, 6, 29.99, 2.40, 5.99, 38.38, 'paid'),
(4, 'pending', 7, 8, 199.99, 16.00, 8.99, 224.98, 'pending'),
(1, 'delivered', 1, 2, 2699.98, 216.00, 19.99, 2935.97, 'paid');

-- Insert order items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
(1, 4, 1, 1299.99, 1299.99),  -- Dell XPS 13
(2, 3, 1, 799.99, 799.99),    -- Samsung Galaxy S23
(3, 5, 1, 29.99, 29.99),      -- Men's T-Shirt
(4, 9, 1, 199.99, 199.99),    -- Wireless Headphones
(5, 1, 1, 2499.99, 2499.99),  -- MacBook Pro 16"
(5, 9, 1, 199.99, 199.99);    -- Wireless Headphones

-- Insert product reviews
INSERT INTO product_reviews (product_id, customer_id, rating, title, review_text, is_verified_purchase) VALUES
(4, 1, 5, 'Excellent laptop!', 'Great performance and build quality. Highly recommended for professionals.', TRUE),
(3, 2, 4, 'Good phone', 'Nice display and camera quality. Battery life could be better.', TRUE),
(5, 3, 5, 'Perfect fit', 'Great quality cotton t-shirt. Very comfortable to wear.', TRUE),
(1, 1, 5, 'Amazing performance', 'This MacBook Pro handles everything I throw at it. Worth every penny.', TRUE),
(9, 1, 4, 'Great sound quality', 'Excellent noise cancellation, but could be more comfortable for long use.', TRUE);

-- Insert inventory movements
INSERT INTO inventory_movements (product_id, movement_type, quantity_change, reason, reference_id) VALUES
(1, 'out', -1, 'Order fulfillment', 5),
(3, 'out', -1, 'Order fulfillment', 2),
(4, 'out', -1, 'Order fulfillment', 1),
(5, 'out', -1, 'Order fulfillment', 3),
(9, 'out', -2, 'Order fulfillment', NULL),
(1, 'in', 50, 'New stock arrival', NULL),
(2, 'in', 100, 'New stock arrival', NULL),
(3, 'adjustment', -5, 'Damaged goods', NULL);