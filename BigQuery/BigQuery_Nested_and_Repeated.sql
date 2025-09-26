-- ================================================================================
-- BigQuery Nested and Repeated Fields Examples
-- ================================================================================
-- This file demonstrates various patterns for working with nested (STRUCT) and
-- repeated (ARRAY) fields in BigQuery, including table creation, data insertion,
-- and querying techniques.
-- ================================================================================

-- ================================================================================
-- SECTION 1: NESTED FIELDS (STRUCT) EXAMPLES
-- ================================================================================
-- Nested fields allow you to store structured data within a single column
-- using STRUCT data type, similar to JSON objects.

-- Create table with nested STRUCT field for address information
-- Each user has a single address with multiple sub-fields (street, city, country)
CREATE OR REPLACE TABLE `myorg-cloudai-gcp1722.demo_dataset.users` (
  user_id STRING,                  -- Unique identifier for each user
  name STRING,                     -- User's full name
  address STRUCT<
    street STRING,                 -- Street address
    city STRING,                   -- City name
    country STRING                 -- Country name
  >
);

-- Insert sample data into the nested structure table
-- Using STRUCT() function to create nested address objects
INSERT INTO `myorg-cloudai-gcp1722.demo_dataset.users` (user_id, name, address) VALUES
  ('U001', 'John Smith', STRUCT('123 Main St', 'New York', 'USA')),
  ('U002', 'Jane Doe', STRUCT('456 Oak Ave', 'Los Angeles', 'USA')),
  ('U003', 'Mike Johnson', STRUCT('789 Pine Rd', 'Chicago', 'USA')),
  ('U004', 'Sarah Wilson', STRUCT('321 Elm St', 'Houston', 'USA')),
  ('U005', 'Tom Brown', STRUCT('654 Maple Dr', 'Phoenix', 'USA'));

-- Query 1: Basic SELECT - retrieve all columns including nested structure
-- This shows the raw nested data structure as stored in BigQuery
SELECT
  *
FROM
  `myorg-cloudai-gcp1722.demo_dataset.users`;

-- Query 2: Accessing nested fields using dot notation
-- Extract individual fields from the nested address structure
-- This flattens the nested structure into separate columns for easier analysis
SELECT
  user_id,
  name,
  address.street AS street,         -- Access nested field with dot notation
  address.city AS city,             -- Alias for cleaner column names
  address.country AS country
FROM
  `myorg-cloudai-gcp1722.demo_dataset.users`;

-- ================================================================================
-- SECTION 2: REPEATED FIELDS (ARRAY) EXAMPLES
-- ================================================================================
-- Repeated fields allow you to store multiple values of the same type
-- using ARRAY data type, similar to JSON arrays.

-- Create table with repeated ARRAY field for multiple phone numbers
-- Each user can have multiple phone numbers stored as an array
CREATE TABLE `myorg-cloudai-gcp1722.demo_dataset.user` (
  user_id STRING,                  -- Unique identifier for each user
  name STRING,                     -- User's full name
  phone_numbers ARRAY<STRING>      -- Array of phone numbers (repeated field)
);

-- Insert sample data with multiple phone numbers per user
-- Using array literal syntax [value1, value2, ...] to create arrays
INSERT INTO `myorg-cloudai-gcp1722.demo_dataset.user` (user_id, name, phone_numbers) VALUES
  ('U001', 'John Smith', ['+1-555-1234', '+1-555-5678']),                -- 2 phone numbers
  ('U002', 'Jane Doe', ['+1-555-9999', '+1-555-8888', '+1-555-7777']),   -- 3 phone numbers
  ('U003', 'Mike Johnson', ['+1-555-1111']),                             -- 1 phone number
  ('U004', 'Sarah Wilson', ['+1-555-2222', '+1-555-3333']),              -- 2 phone numbers
  ('U005', 'Tom Brown', ['+1-555-4444', '+1-555-5555', '+1-555-6666', '+1-555-0000']); -- 4 phone numbers

-- Query 3: Basic SELECT - retrieve all columns including array data
-- This shows the raw array structure as stored in BigQuery
SELECT
  *
FROM
  `myorg-cloudai-gcp1722.demo_dataset.user`;

-- Query 4: Flatten repeated field using UNNEST()
-- Convert array elements into separate rows for easier analysis
-- Each phone number becomes its own row, duplicating user info
SELECT
  user_id,
  phone                             -- Each phone number from the array
FROM
  `myorg-cloudai-gcp1722.demo_dataset.user`,
  UNNEST(phone_numbers) AS phone;   -- UNNEST expands array into multiple rows

-- ================================================================================
-- SECTION 3: NESTED + REPEATED FIELDS COMBINED (ARRAY<STRUCT>)
-- ================================================================================
-- The most powerful pattern: combining nested and repeated fields
-- This allows storing arrays of complex objects, similar to JSON arrays of objects.

-- Create table with both nested and repeated fields
-- Each user has multiple orders, and each order contains nested product information
CREATE TABLE `myorg-cloudai-gcp1722.demo_dataset.products` (
  user_id STRING,                  -- Unique identifier for each user
  name STRING,                     -- User's full name
  orders ARRAY<STRUCT<
    order_id STRING,               -- Unique identifier for each order
    product STRUCT<                -- Nested product information within each order
      product_id STRING,           -- Product identifier
      product_name STRING,         -- Product display name
      category STRING              -- Product category
    >,
    price FLOAT64                  -- Order price
  >>
);

-- Insert complex nested + repeated data
-- Each user can have multiple orders, each order has nested product details
INSERT INTO `myorg-cloudai-gcp1722.demo_dataset.products` (user_id, name, orders) VALUES
  -- User 1: 2 orders with different electronics
  ('U001', 'John Smith', [
    STRUCT('O001' AS order_id,
           STRUCT('P001' AS product_id, 'Smartphone' AS product_name, 'Electronics' AS category) AS product,
           699.99 AS price),
    STRUCT('O002' AS order_id,
           STRUCT('P002' AS product_id, 'Wireless Headphones' AS product_name, 'Electronics' AS category) AS product,
           199.99 AS price)
  ]),
  -- User 2: 3 orders - laptop and accessories
  ('U002', 'Jane Doe', [
    STRUCT('O003' AS order_id,
           STRUCT('P003' AS product_id, 'Laptop' AS product_name, 'Electronics' AS category) AS product,
           1299.99 AS price),
    STRUCT('O004' AS order_id,
           STRUCT('P004' AS product_id, 'Mouse' AS product_name, 'Electronics' AS category) AS product,
           29.99 AS price),
    STRUCT('O005' AS order_id,
           STRUCT('P005' AS product_id, 'Keyboard' AS product_name, 'Electronics' AS category) AS product,
           89.99 AS price)
  ]),
  -- User 3: 1 order
  ('U003', 'Mike Johnson', [
    STRUCT('O006' AS order_id,
           STRUCT('P006' AS product_id, 'Tablet' AS product_name, 'Electronics' AS category) AS product,
           399.99 AS price)
  ]);

-- Query 5: Basic SELECT - retrieve all data including complex nested arrays
-- Shows the raw complex data structure as stored in BigQuery
SELECT
  user_id,
  name,
  orders                             -- Shows entire orders array with nested structures
FROM
  `myorg-cloudai-gcp1722.demo_dataset.products`
ORDER BY
  user_id;

-- Query 6: Flatten nested + repeated data using UNNEST()
-- Extract and flatten all order details into separate rows
-- Each order becomes its own row with access to nested product fields
SELECT
  user_id,
  name,
  orders.order_id,                   -- Access order ID from flattened array
  orders.product.product_id,         -- Access nested product ID using dot notation
  orders.product.product_name,       -- Access nested product name
  orders.product.category,           -- Access nested product category
  orders.price                       -- Access order price
FROM
  `myorg-cloudai-gcp1722.demo_dataset.products`,
  UNNEST(orders) AS orders           -- Flatten orders array into separate rows
ORDER BY
  user_id,
  orders.order_id;

-- Query 7: Advanced analytics - aggregations on nested + repeated data
-- Calculate order statistics and insights for each user
-- Demonstrates complex aggregations within nested structures
SELECT
  user_id,
  name,
  ARRAY_LENGTH(orders) AS total_orders,  -- Count total number of orders per user
  -- Calculate total spending using subquery with UNNEST
  (SELECT SUM(orders.price)
     FROM UNNEST(orders) AS orders) AS total_spent,
  -- Calculate average order value using subquery with UNNEST
  (SELECT AVG(orders.price)
     FROM UNNEST(orders) AS orders) AS avg_order_value,
  -- Count unique product categories purchased using DISTINCT within subquery
  (SELECT COUNT(DISTINCT orders.product.category)
     FROM UNNEST(orders) AS orders) AS unique_categories_purchased
FROM
  `myorg-cloudai-gcp1722.demo_dataset.products`
WHERE
  ARRAY_LENGTH(orders) > 0           -- Filter out users with no orders
ORDER BY
  total_spent DESC;                  -- Order by highest spending users first

-- ================================================================================
-- END OF FILE
-- ================================================================================
-- These examples demonstrate the full spectrum of BigQuery's nested and repeated
-- field capabilities, from basic STRUCT usage to complex ARRAY<STRUCT> patterns
-- commonly used in modern data warehousing and analytics applications.
-- ================================================================================
