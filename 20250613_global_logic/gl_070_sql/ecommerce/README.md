# E-commerce Database Example

This example demonstrates a comprehensive e-commerce database schema suitable for online retail applications.

## Database Schema Overview

```mermaid
erDiagram
    categories ||--o{ categories : "has subcategories"
    categories ||--o{ products : "contains"
    products ||--o{ cart_items : "added to"
    products ||--o{ order_items : "purchased in"
    products ||--o{ product_reviews : "reviewed"
    products ||--o{ inventory_movements : "tracked"
    
    customers ||--o{ addresses : "has"
    customers ||--o{ shopping_carts : "owns"
    customers ||--o{ orders : "places"
    customers ||--o{ product_reviews : "writes"
    
    shopping_carts ||--o{ cart_items : "contains"
    
    orders ||--o{ order_items : "contains"
    orders }o--|| addresses : "shipping_address"
    orders }o--|| addresses : "billing_address"
    
    categories {
        int category_id PK
        string name
        string description
        int parent_category_id FK
        timestamp created_at
    }
    
    products {
        int product_id PK
        string name
        text description
        decimal price
        string sku
        int category_id FK
        int stock_quantity
        decimal weight
        string dimensions
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }
    
    customers {
        int customer_id PK
        string first_name
        string last_name
        string email
        string phone
        date date_of_birth
        timestamp created_at
        timestamp updated_at
    }
    
    addresses {
        int address_id PK
        int customer_id FK
        enum address_type
        string street_address
        string city
        string state_province
        string postal_code
        string country
        boolean is_default
    }
    
    shopping_carts {
        int cart_id PK
        int customer_id FK
        timestamp created_at
        timestamp updated_at
    }
    
    cart_items {
        int cart_item_id PK
        int cart_id FK
        int product_id FK
        int quantity
        timestamp added_at
    }
    
    orders {
        int order_id PK
        int customer_id FK
        enum order_status
        timestamp order_date
        int shipping_address_id FK
        int billing_address_id FK
        decimal subtotal
        decimal tax_amount
        decimal shipping_cost
        decimal total_amount
        enum payment_status
        timestamp shipped_at
        timestamp delivered_at
    }
    
    order_items {
        int order_item_id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_price
        decimal total_price
    }
    
    product_reviews {
        int review_id PK
        int product_id FK
        int customer_id FK
        int rating
        string title
        text review_text
        boolean is_verified_purchase
        timestamp created_at
    }
    
    inventory_movements {
        int movement_id PK
        int product_id FK
        enum movement_type
        int quantity_change
        string reason
        int reference_id
        timestamp created_at
    }
```

## Key Features

### 1. **Hierarchical Categories**
- Supports nested categories (Electronics > Laptops)
- Self-referencing foreign key design

### 2. **Comprehensive Product Management**
- SKU tracking for inventory
- Stock quantity management
- Product attributes (weight, dimensions)
- Active/inactive status

### 3. **Customer Management**
- Multiple addresses per customer
- Separate billing and shipping addresses
- Customer profile information

### 4. **Shopping Cart Functionality**
- Persistent cart storage
- Multiple items per cart
- Quantity management

### 5. **Order Processing**
- Multiple order statuses
- Payment tracking
- Shipping and delivery timestamps
- Order item details with pricing

### 6. **Review System**
- Star ratings (1-5)
- Verified purchase tracking
- Review text and titles

### 7. **Inventory Tracking**
- Movement logging (in/out/adjustments)
- Reference tracking for audit trail

## Common Interview Questions

### Schema Design
1. **Why separate addresses from customers?**
   - Customers often have multiple addresses
   - Supports both billing and shipping addresses
   - Historical address tracking for orders

2. **Why track unit_price in order_items?**
   - Prices change over time
   - Order history should reflect price at time of purchase
   - Historical accuracy for reporting

3. **How to handle product variants?**
   - Could extend with `product_variants` table
   - Store size, color, etc. as separate products
   - Use parent-child relationships

### Performance Considerations
1. **Indexing Strategy**
   - Primary keys (automatic)
   - Foreign keys for joins
   - Email for customer lookup
   - SKU for product lookup
   - Order status and date for reporting

2. **Query Optimization**
   - Use appropriate JOINs
   - Limit result sets
   - Consider denormalization for reporting

### Business Logic
1. **Cart vs Wishlist**
   - Cart: intended for purchase
   - Wishlist: saved for later
   - Could add `cart_type` enum

2. **Inventory Management**
   - Real-time stock updates
   - Reserved quantities for pending orders
   - Low stock alerts

## Files Included

- `schema.sql` - Complete database schema
- `sample_data.sql` - Test data for practice
- `queries.sql` - Common query patterns
- `README.md` - This documentation

## Practice Scenarios

1. **Find abandoned carts** - Carts with items but no recent orders
2. **Calculate customer lifetime value** - Total spending per customer
3. **Inventory reports** - Low stock alerts, movement tracking
4. **Sales analytics** - Revenue by category, time periods
5. **Product recommendations** - Based on purchase history