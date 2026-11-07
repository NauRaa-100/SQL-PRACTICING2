

#REVIEW SQL 

#SCHEMA
'''
customers
---------
customer_id       PK
customer_name
email
city
signup_date
created_at

'''
#1. Retrieve all customers from a specific city.

"""
SELECT
    customer_id,
    customer_name,
    city
FROM customers
WHERE city = 'Cairo'
"""
#-------------------------

#SCHEMA
'''
orders
------
order_id          PK
customer_id       FK
employee_id       FK
order_date
completed_at
status

'''
#2. Display all completed orders 
# sorted by order date, newest first.


"""
SELECT 
      order_id,
      order_date,
      status
FROM orders 
WHERE status = 'Completed'
ORDER BY order_date DESC
"""
#----------------------------

#SCHEMA

'''
customers
---------
customer_id
customer_name
city
'''
#3. Find all distinct cities 
# where customers are located.

"""
SELECT DISTINCT
    city
FROM customers;
"""

#-----------------------------

#SCHEMA

'''
products
--------
product_id        PK
product_name
category_id       FK
selling_price
cost_price
is_active
'''
#4. Find products 
# with a selling price greater than 500.

"""
SELECT
      product_id ,
      product_name,
      selling_price
FROM products
WHERE selling_price > 500

"""
#--------------------------------

#SCHEMA 
'''
orders
------
order_id
customer_id
order_date
completed_at
status

'''
#5. Find orders created between two specific dates.
# U DIDNT MENTION THOSE SPECIFICS DATES !!

"""
SELECT
    order_id,
    order_date
FROM orders
WHERE order_date >= TIMESTAMP '2026-01-01 00:00:00'
  AND order_date < TIMESTAMP '2026-02-01 00:00:00'
"""
#---------------------------------

#SCHEMA

'''
customers
---------
customer_id       PK
customer_name
email
city

'''
#6. Count the total number of customers.

"""
SELECT DISTINCT
     
     COUNT(*) AS num_of_customers
    
FROM customers 


"""
#----------------------------------

#SCHEMA
'''
orders
------
order_id          PK
status

order_items
-----------
order_item_id     PK
order_id          FK
product_id        FK
quantity
unit_price
discount_pct
'''
#7. Calculate the 
# total revenue generated from completed orders.

"""
SELECT
    SUM(
        oi.quantity * oi.unit_price *
        (1 - COALESCE(oi.discount_pct, 0) / 100.0)
    ) AS total_revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.status = 'Completed';
"""

#--------------------------------

#SCHEMA 

'''
products
--------
product_id
product_name
selling_price

'''
#8. Calculate the average 
# selling price of all products.

"""
WITH A AS(
SELECT 
     SUM(selling_price) AS total_price,
     COUNT(DISTINCT product_id) AS num_of_products,
     product_id,
     product_name
FROM products
GROUP BY product_id , product_name
) 
SELECT 
      SUM(total_price) / SUM(num_of_products) AS avg_selling_price
FROM A
"""
#------------------------------------

#SCHEMA

'''
products
--------
product_id
product_name
selling_price
'''
#9. Find the minimum 
# and maximum product selling prices.

"""
SELECT 
     DISTINCT product_id ,
     product_name,
     MIN(selling_price) AS miniumum_product_price,
     MAX(selling_price) AS maximum_product_price
FROM products 
"""
#-------------------------------------

#SCHEMA 

'''
orders
------
order_id          PK
status
order_date
'''

#10. Count the number of orders for each status.

"""
SELECT 
     COUNT(DISTINCT order_id) AS num_of_orders,
     status
FROM orders
GROUP BY status 
"""

#---------------------------------------

#SCHEMA
'''
customers
---------
customer_id       PK
customer_name

orders
------
order_id          PK
customer_id       FK
order_date
status
'''

#11. Find the total number of
# orders placed by each customer.

"""
SELECT 
     c.customer_id,
     c.customer_name,
     COUNT(DISTINCT o.order_id ) AS num_of_orders
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id
GROUP BY c.customer_id , c.customer_name
"""

#----------------------------------
#SCHEMA 
'''
customers
---------
customer_id       PK
customer_name

orders
------
order_id          PK
customer_id       FK
'''
#12. Display customers 
# who have placed more than 3 orders.

"""
SELECT 
     c.customer_id ,
     c.customer_name ,
     COUNT(DISTINCT o.order_id ) AS num_of_orders
FROM customers c
JOIN orders o 
ON c.customer_id = o.customer_id 
GROUP BY c.customer_id , c.customer_name 
HAVING COUNT(DISTINCT o.order_id ) > 3

"""
#---------------------------------

#SCHEMA

'''
products
--------
product_id        PK
product_name

order_items
-----------
order_item_id     PK
order_id          FK
product_id        FK
quantity
'''
#13. Find the total quantity sold for each product.

"""
SELECT 
     p.product_id ,
     p.product_name ,
     SUM(oi.quantity) AS total_quantities
FROM products p
LEFT JOIN order_items oi 
ON p.product_id = oi.product_id
GROUP BY p.product_id , p.product_name

"""
#----------------------------------

#SCHEMA

'''
categories
----------
category_id       PK
category_name

products
--------
product_id        PK
product_name
category_id       FK

orders
------
order_id          PK
status

order_items
-----------
order_item_id     PK
order_id          FK
product_id        FK
quantity
unit_price
discount_pct
'''
#14. Calculate total revenue by product category.

"""

SELECT
    c.category_id,
    c.category_name,
    SUM(
        oi.quantity * oi.unit_price *
        (1 - COALESCE(oi.discount_pct, 0) / 100.0)
    ) AS total_revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON p.product_id = oi.product_id
JOIN categories c
    ON p.category_id = c.category_id
WHERE o.status = 'Completed'
GROUP BY
    c.category_id,
    c.category_name
"""

#--------------------------------------

#SCHEMA

'''
categories
----------
category_id       PK
category_name

products
--------
product_id        PK
product_name
category_id       FK

orders
------
order_id          PK
status

order_items
-----------
order_item_id     PK
order_id          FK
product_id        FK
quantity
unit_price
discount_pct
'''

#15. Find categories 
#with total revenue greater than 10,000.

"""
SELECT
    c.category_id,
    c.category_name,
    SUM(
        oi.quantity * oi.unit_price *
        (1 - COALESCE(oi.discount_pct, 0) / 100.0)
    ) AS total_revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON p.product_id = oi.product_id
JOIN categories c
    ON p.category_id = c.category_id
WHERE o.status = 'Completed'
GROUP BY
    c.category_id,
    c.category_name
HAVING SUM(
    oi.quantity * oi.unit_price *
    (1 - COALESCE(oi.discount_pct, 0) / 100.0)
) > 10000
"""

#--------------------------------------

#SCHEMA 

'''
orders
------
order_id          PK
customer_id       FK
order_date
status

customers
---------
customer_id       PK
customer_name

'''
#16. Retrieve each order
# along with the customer's name.

"""
SELECT 
     c.customer_name ,
     o.order_id 
FROM orders o
LEFT JOIN customers c
ON o.customer_id = c.customer_id 
"""
#------------------------------------

#SCHEMA

'''
customers
---------
customer_id       PK
customer_name

orders
------
order_id          PK
customer_id       FK
'''

#17. Display all customers, 
# including those who have never placed an order.

#18. Find customers who have never placed an order.
"""
SELECT 
     c.customer_id,
     c.customer_name ,
     o.order_id 
FROM customers c
LEFT JOIN orders o 
ON c.customer_id = o.customer_id 

"""
#----
"""
SELECT 
     c.customer_id,
     c.customer_name ,
     o.order_id 
FROM customers c
LEFT JOIN orders o 
ON c.customer_id = o.customer_id 
WHERE o.order_id IS NULL 

"""
#-------------------------------

# SCHEMA
'''
products
--------
product_id        PK
product_name

order_items
-----------
order_item_id     PK
product_id        FK
order_id          FK
quantity
'''
#19. Find products that have never been sold.

"""
SELECT 
      p.product_id ,
      p.product_name,
      o.order_id 

FROM products p
LEFT JOIN order_items o
ON p.product_id = o.product_id 
WHERE o.order_id IS NULL 

"""
#--------------------------------

#SCHEMA
'''
orders
------
order_id          PK
employee_id       FK
order_date
status

employees
---------
employee_id       PK
employee_name
department
'''
#20. Retrieve each order 
# with the employee responsible for it.

"""
SELECT 
     o.order_id ,
     e.employee_id,
     e.employee_name 
FROM orders o 
LEFT JOIN employees e
ON e.employee_id = o.employee_id 

"""
#---------------------------------------
#---------------------------------------


#keep SQL

#SCHEMA

'''
CREATE TABLE orders (
    order_id       INT PRIMARY KEY,
    customer_id    INT,
    employee_id    INT,
    order_date     DATE,
    status         VARCHAR(30),
    payment_method VARCHAR(30),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
#----
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id      INT NOT NULL,
    product_id    INT NOT NULL,
    quantity      INT NOT NULL,
    unit_price    DECIMAL(10,2) NOT NULL,
    discount_pct  DECIMAL(5,2) DEFAULT 0,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

'''

#Calculate the total revenue 
#generated from completed orders only.

"""
SELECT
    SUM(
        oi.quantity * oi.unit_price *
        (1 - COALESCE(oi.discount_pct, 0) / 100.0)
    ) AS total_revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.status = 'Completed'
"""

#--------------------------

#Calculate monthly revenue 
#and the number of completed orders.

"""
SELECT
    DATE_TRUNC('month', o.order_date) AS month,
    COUNT(DISTINCT o.order_id) AS num_of_orders,

    SUM(
        oi.quantity * oi.unit_price *
        (1 - COALESCE(oi.discount_pct, 0) / 100.0)
    ) AS monthly_revenue

FROM orders o

JOIN order_items oi
    ON o.order_id = oi.order_id

WHERE o.status = 'Completed'

GROUP BY DATE_TRUNC('month', o.order_date)

ORDER BY month
"""
#---------------------------

#SCHEMA

'''
CREATE TABLE products (
    product_id   INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category     VARCHAR(80),
    unit_cost    DECIMAL(10,2),
    list_price   DECIMAL(10,2)
);

CREATE TABLE orders (
    order_id       INT PRIMARY KEY,
    customer_id    INT,
    employee_id    INT,
    order_date     DATE,
    status         VARCHAR(30),
    payment_method VARCHAR(30),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id      INT NOT NULL,
    product_id    INT NOT NULL,
    quantity      INT NOT NULL,
    unit_price    DECIMAL(10,2) NOT NULL,
    discount_pct  DECIMAL(5,2) DEFAULT 0,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
'''

#Identify the top 5 products by revenue,
# including product names and categories.

'''
WITH A AS(
SELECT 
     p.product_id ,
     p.product_name,
     p.category,
     SUM(
     (oi.quantity * oi.unit_price) * 1 - (COALESCE(oi.discount_pct,0) / 100.0)
     ) AS total_revenue
FROM products p
JOIN order_items oi
ON p.product_id = oi.product_id 
GROUP BY p.product_id ,
         p.product_name,
         p.category
),B AS(
SELECT 
     total_revenue ,
     DENSE_RANK() OVER(
                      ORDER BY revenue DESC) AS top_five_products
FROM A 
)
SELECT * FROM B 
WHERE top_five_products <= 5

'''

#----------------------------------

#Find customers 
#who have never placed a completed order.

#SCHEMA

'''
CREATE TABLE customers (
    customer_id   INT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email         VARCHAR(150),
    city          VARCHAR(80),
    signup_date   DATE
);


CREATE TABLE orders (
    order_id       INT PRIMARY KEY,
    customer_id    INT,
    employee_id    INT,
    order_date     DATE,
    status         VARCHAR(30),
    payment_method VARCHAR(30),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

'''


"""
SELECT 
     c.customer_id,
     c.customer_name ,
     o.status
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id
AND o.status <> 'Completed'
WHERE o.order_id IS NULL
"""












