

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



#--------KEEPING SQL----------
#=============================
#-------DATABASE SCHEMA-------
#=============================

'''
customers
---------
customer_id       INT PRIMARY KEY
customer_name     VARCHAR(100)
email             VARCHAR(150)
city              VARCHAR(80)
region            VARCHAR(80)
signup_date       DATE


employees
---------
employee_id       INT PRIMARY KEY
employee_name     VARCHAR(100)
department        VARCHAR(80)
hire_date         DATE


categories
----------
category_id       INT PRIMARY KEY
category_name     VARCHAR(100)


products
--------
product_id        INT PRIMARY KEY
product_name      VARCHAR(150)
category_id       INT FOREIGN KEY


orders
------
order_id          INT PRIMARY KEY
customer_id       INT FOREIGN KEY
employee_id       INT FOREIGN KEY
order_date        DATE
status            VARCHAR(30)


order_items
-----------
order_item_id     INT PRIMARY KEY
order_id          INT FOREIGN KEY
product_id        INT FOREIGN KEY
quantity          INT
unit_price        NUMERIC(12,2)
discount_pct      NUMERIC(5,2)
unit_cost         NUMERIC(12,2)


payments
--------
payment_id        INT PRIMARY KEY
order_id          INT FOREIGN KEY
payment_date      DATE
payment_method    VARCHAR(50)
payment_status    VARCHAR(30)
amount            NUMERIC(12,2)


returns
-------
return_id         INT PRIMARY KEY
order_item_id     INT FOREIGN KEY
return_date       DATE
return_status     VARCHAR(30)
returned_quantity INT
refund_amount     NUMERIC(12,2)

'''
#1

#Retrieve all completed orders with 
#their order ID, order date, and status, 
#sorted from newest to oldest.
'''


orders
------
order_id          INT PRIMARY KEY
customer_id       INT FOREIGN KEY
employee_id       INT FOREIGN KEY
order_date        DATE
status            VARCHAR(30)


'''

"""
SELECT 
      order_id ,
      status,
      order_date
FROM orders 
WHERE status = 'Completed'
ORDER BY order_date DESC
"""
#------------------------------------------------

#2

#Retrieve customers who registered after 1 January 2025 and
#display their names, cities, regions, and registration dates.

'''
customers
---------
customer_id       INT PRIMARY KEY
customer_name     VARCHAR(100)
email             VARCHAR(150)
city              VARCHAR(80)
region            VARCHAR(80)
signup_date       DATE


'''

"""
SELECT 
     customer_id ,
     customer_name,
     city,
     region,
     signup_date 
FROM customers 
WHERE signup_date > '2025-01-01'

"""

#---------------------------------------------------------

#3

#Identify email addresses associated 
#with more than one customer, excluding NULL emails.

"""
customers
---------
customer_id       INT PRIMARY KEY
customer_name     VARCHAR(100)
email             VARCHAR(150)
city              VARCHAR(80)
region            VARCHAR(80)
signup_date       DATE


"""

'''
SELECT
    email,
    COUNT(*) AS customer_count
FROM customers
WHERE email IS NOT NULL
GROUP BY email
HAVING COUNT(*) > 1;
'''

#4
#Find completed orders that do not have any successful payment records.

'''

orders
------
order_id          INT PRIMARY KEY
customer_id       INT FOREIGN KEY
employee_id       INT FOREIGN KEY
order_date        DATE
status            VARCHAR(30)
------
------
payments
--------
payment_id        INT PRIMARY KEY
order_id          INT FOREIGN KEY
payment_date      DATE
payment_method    VARCHAR(50)
payment_status    VARCHAR(30)
amount            NUMERIC(12,2)

'''
"""
SELECT 
     o.order_id 
FROM orders o
ON o.order_id = p.order_id 
WHERE o.status = 'Completed'
WHERE NOT EXISTS (
SELECT 1 FROM payments p 
WHERE o.order_id = p.order_id 
AND p.payment_status = 'Successfull'
) 
"""
#-----------------------------------

#5

#Retrieve customers who have never placed a completed order.

'''
customers
---------
customer_id       INT PRIMARY KEY
customer_name     VARCHAR(100)
email             VARCHAR(150)
city              VARCHAR(80)
region            VARCHAR(80)
signup_date       DATE
-------

orders
------
order_id          INT PRIMARY KEY
customer_id       INT FOREIGN KEY
employee_id       INT FOREIGN KEY
order_date        DATE
status            VARCHAR(30)

'''

'''
SELECT
    c.customer_id,
    c.customer_name
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
    AND o.status = 'Completed'
WHERE o.order_id IS NULL
'''
#-------------------------------------------------

#6 Calculate total revenue generated from completed orders only.

'''
orders
------
order_id          INT PRIMARY KEY
customer_id       INT FOREIGN KEY
employee_id       INT FOREIGN KEY
order_date        DATE
status            VARCHAR(30)


order_items
-----------
order_item_id     INT PRIMARY KEY
order_id          INT FOREIGN KEY
product_id        INT FOREIGN KEY
quantity          INT
unit_price        NUMERIC(12,2)
discount_pct      NUMERIC(5,2)
unit_cost         NUMERIC(12,2)

'''

"""
SELECT 
     o.order_id ,
     SUM(
     (oi.quantity * oi.unit_price) * (1-COALESCE(oi.discount_pct,0)/100.0)
     ) AS total_revenue
FROM orders o
JOIN order_items oi 
ON o.order_id = oi.order_id
WHERE o.status = 'Completed'
GROUP BY o.order_id
"""
#-------------------------------------------

#7 Calculate monthly revenue and the number of completed orders for each month.

"""
SELECT 
     COUNT(o.order_id) AS num_orders ,
     DATE_TRUNC('month',o.order_date) AS month,
     SUM(
     (oi.quantity * oi.unit_price) * (1-COALESCE(oi.discount_pct,0)/100.0)
     ) AS total_revenue
FROM orders o
JOIN order_items oi 
ON o.order_id = oi.order_id
WHERE o.status = 'Completed'
GROUP BY  DATE_TRUNC('month',o.order_date)

"""

#--------------------------------------------
#8 Find the top 10 products by total revenue. 
# Display product name, category, total units sold, and total revenue.

'''

products
--------
product_id        INT PRIMARY KEY
product_name      VARCHAR(150)
category_id       INT FOREIGN KEY


orders
------
order_id          INT PRIMARY KEY
customer_id       INT FOREIGN KEY
employee_id       INT FOREIGN KEY
order_date        DATE
status            VARCHAR(30)


order_items
-----------
order_item_id     INT PRIMARY KEY
order_id          INT FOREIGN KEY
product_id        INT FOREIGN KEY
quantity          INT
unit_price        NUMERIC(12,2)
discount_pct      NUMERIC(5,2)
unit_cost         NUMERIC(12,2)

'''
## Display product name, category, total units sold, and total revenue.

'''

SELECT 
      p.product_id,
      p.product_name,
      p.category,
      SUM(oi.quantity) AS total_units_sold,
      SUM(
      (oi.quantity * oi.unit_price) * (1- COALESCE(oi.discount_pct,0)/100.0)
      ) AS total_revenue
FROM orders o
JOIN order_items oi 
ON o.order_id = oi.order_id
JOIN products p
ON oi.product_id = p.product_id
WHERE o.status = 'Completed'
ORDER BY total_revenue DESC 
LIMIT 10 

'''

#---------------------------------------------

#9 Calculate total sales revenue for each region.


"""
SELECT 
     c.region,
     o.order_id ,
     SUM(
     (oi.quantity * oi.unit_price) * (1-COALESCE(oi.discount_pct,0)/100.0)
     ) AS total_revenue
FROM customers c 
LEFT JOIN orders o 
    ON c.customer_id = o.customer_id 
LEFT JOIN order_items oi
    ON o.order_id = oi.order_id 
GROUP BY c.region 
"""
#---------------------------------------------

#10 Calculate the total revenue generated by employees in each department.

'''

employees
---------
employee_id       INT PRIMARY KEY
employee_name     VARCHAR(100)
department        VARCHAR(80)
hire_date         DATE


orders
------
order_id          INT PRIMARY KEY
customer_id       INT FOREIGN KEY
employee_id       INT FOREIGN KEY
order_date        DATE
status            VARCHAR(30)


order_items
-----------
order_item_id     INT PRIMARY KEY
order_id          INT FOREIGN KEY
product_id        INT FOREIGN KEY
quantity          INT
unit_price        NUMERIC(12,2)
discount_pct      NUMERIC(5,2)
unit_cost         NUMERIC(12,2)

'''
#10 Calculate the total revenue generated by employees in each department.

"""
SELECT 
     e.employee_id,
     e.employee_name,
     e.department,
     SUM(
     (oi.quantity * oi.unit_price) * (1-COALESCE(oi.discount_pct,0)/100.0)
     ) AS total_revenue
FROM employees e
LEFT JOIN orders o
ON o.employee_id = e.employee_id 
LEFT JOIN order_items oi
ON oi.order_id = o.order_id 
GROUP BY e.employee_id ,
         e.employee_name,
         e.department
"""

#--------------------------------------------

#11 Find employees whose total completed sales exceed AED 100,000.

"""
SELECT 
     e.employee_id,
     e.employee_name,
     SUM(
     (oi.quantity * oi.unit_price) * (1-COALESCE(oi.discount_pct,0)/100.0)
     ) AS total_completed_sales
FROM employees e
JOIN orders o
ON o.employee_id = e.employee_id 
JOIN order_items oi
ON oi.order_id = o.order_id 
WHERE o.status ='Completed'
GROUP BY e.employee_id ,
         e.employee_name
HAVING  SUM(
     (oi.quantity * oi.unit_price) * (1-COALESCE(oi.discount_pct,0)/100.0)
     ) > 100,000
"""
#------------------------------------------

#12 Calculate the average order value for each region.
'''
WITH T AS(
SELECT DISTINCT
     c.region,
     COUNT(o.order_id) AS num_of_orders,
     SUM(
     (oi.quantity * oi.unit_price) * (1-COALESCE(oi.discount_pct,0)/100.0)
     ) AS total_sales,

FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id
AND o.status = 'Completed'
LEFT JOIN oder_items oi
ON o.order_id = oi.order_id
GROUP BY c.region 
)
SELECT 
      region ,
      total_sales,
      (total_sales / num_of_orders ) AS AOV 
FROM T 
'''
#----------------------------------------------
#13 Calculate total revenue and total units sold for each product category.

"""
products
--------
product_id        INT PRIMARY KEY
product_name      VARCHAR(150)
category_id       INT FOREIGN KEY


orders
------
order_id          INT PRIMARY KEY
customer_id       INT FOREIGN KEY
employee_id       INT FOREIGN KEY
order_date        DATE
status            VARCHAR(30)


order_items
-----------
order_item_id     INT PRIMARY KEY
order_id          INT FOREIGN KEY
product_id        INT FOREIGN KEY
quantity          INT
unit_price        NUMERIC(12,2)
discount_pct      NUMERIC(5,2)
unit_cost         NUMERIC(12,2)

"""

'''
SELECT  
      p.product_id ,
      p.product_name,
      p.category_id,
      SUM(
      (oi.quantity * oi.unit_price) * (1-COALESCE(oi.discount_pct,0)/100.0)
      ) AS total_revenue,
      SUM(oi.quantity) AS total_units_sold
FROM products p
LEFT JOIN order_items oi 
ON oi.product_id = p.product_id 
LEFT JOIN orders o 
ON o.order_id = oi.order_id 
AND o.status = 'Completed'
GROUP BY p.product_id ,
         p.product_name,
         p.category_id 

'''
#-------------------------------------------------------
#14 Calculate total revenue, total cost, and gross profit for each product.

'''
WITH T AS(
SELECT  
      p.product_id ,
      p.product_name,
      SUM(oi.quantity * oi.unit_price) AS gross_revenue,
      SUM(oi.quantity * oi.unit_cost) AS total_cost,
FROM products p
LEFT JOIN order_items oi 
ON oi.product_id = p.product_id 
LEFT JOIN orders o 
ON o.order_id = oi.order_id 
AND o.status = 'Completed'
GROUP BY p.product_id ,
         p.product_name
)
SELECT
     product_id ,
     product_name,
     gross_revenue,
     total_cost,
     (gross_revenue - total_cost ) AS gross_profit
FROM T 
'''
#-------------------------------------------------------
#15 Find completed orders whose total value is 
# higher than the average completed order value.

'''
orders
------
order_id          INT PRIMARY KEY
customer_id       INT FOREIGN KEY
employee_id       INT FOREIGN KEY
order_date        DATE
status            VARCHAR(30)


order_items
-----------
order_item_id     INT PRIMARY KEY
order_id          INT FOREIGN KEY
product_id        INT FOREIGN KEY
quantity          INT
unit_price        NUMERIC(12,2)
discount_pct      NUMERIC(5,2)
unit_cost         NUMERIC(12,2)

'''

'''
WITH T AS(
SELECT DISTINCT
     o.order_id ,
     COUNT(order_id) AS nums_of_orders,
     SUM(
     (oi.quantity * oi.unit_price) * (1 - COALESCE(oi.discount_pct)/100.0)
     ) AS total_revenue ,
     (
     SUM(
     (oi.quantity * oi.unit_price) * (1 - COALESCE(oi.discount_pct)/100.0)
     )/  COUNT(order_id)
     ) AS AOV
FROM orders o 
JOIN order_items oi 
ON o.order_id = oi.order_id 
WHERE o.status = 'Completed'
GROUP BY o.order_id 
)
SELECT 
      order_id ,
      total_revenue,
      AOV
FROM T 
WHERE total_revenue  >  AOV

'''

#-----------------------------------------------------------
#16 Find customers whose total completed-order 
# spending is higher than the average customer spending.

'''
customers
---------
customer_id       INT PRIMARY KEY
customer_name     VARCHAR(100)
email             VARCHAR(150)
city              VARCHAR(80)
region            VARCHAR(80)
signup_date       DATE

orders
------
order_id          INT PRIMARY KEY
customer_id       INT FOREIGN KEY
employee_id       INT FOREIGN KEY
order_date        DATE
status            VARCHAR(30)


order_items
-----------
order_item_id     INT PRIMARY KEY
order_id          INT FOREIGN KEY
product_id        INT FOREIGN KEY
quantity          INT
unit_price        NUMERIC(12,2)
discount_pct      NUMERIC(5,2)
unit_cost         NUMERIC(12,2)

'''

"""
WITH T AS(
SELECT 
     c.customer_id,
     c.customer_name,
     SUM(
     (oi.quantity * oi.unit_price) * (1 - COALESCE(oi.discount_pct,0)/100.0)
     ) AS total_spending,
     AVG(
     (oi.quantity * oi.unit_price) * (1 - COALESCE(oi.discount_pct,0)/100.0)
     ) AS avg_spending
FROM customer c
LEFT JOIN orders o 
ON c.customer_id = o.customer_id
AND o.status = 'Completed' 
LEFT JOIN order_items oi
ON o.order_id = oi.order_id
GROUP BY c.customer_id ,
         c.customer_name 
)
SELECT 
      customer_id ,
      customer_name ,
      total_spending,
      avg_spending
FROM T 
WHERE total_spending > avg_spending
"""

#----------------------------------------------
#17 Identify products that have never been included in any completed order.

'''
products
--------
product_id        INT PRIMARY KEY
product_name      VARCHAR(150)
category_id       INT FOREIGN KEY


orders
------
order_id          INT PRIMARY KEY
customer_id       INT FOREIGN KEY
employee_id       INT FOREIGN KEY
order_date        DATE
status            VARCHAR(30)

'''

'''
SELECT  
      p.product_id ,
      p.product_name
FROM products p

WHERE NOT EXISTS (
SELECT 1 FROM orders o
WHERE o.status = 'Completed'
)
'''
#----------------------------------------------
#18 Find employees who have never generated a completed order.

'''

employees
---------
employee_id       INT PRIMARY KEY
employee_name     VARCHAR(100)
department        VARCHAR(80)
hire_date         DATE

orders 
'''
"""
SELECT  
     e.employee_id ,
     e.employee_name
FROM employees e
WHERE NOT EXISTS (
SELECT 1 FROM orders o
WHERE o.status = 'Completed'
)
"""
#----------------------------------------------
#19 Find the five customers with the highest total completed-order spending,
#including customer name, number of orders, and total spending.

'''
WITH T AS(
SELECT DISTINCT
     c.customer_id ,
     c.customer_name,
     COUNT(o.order_id) AS num_of_orders ,
     SUM(
     (oi.quantity * oi.unit_price) * (1 - COALESCE(oi.discount_pct,0)/100.0)
     ) AS total_spending
FROM customers c
JOIN orders o 
ON c.customer_id = o.customer_id 
WHERE o.status = 'Completed'
JOIN order_items oi 
ON o.order_id = oi.order_id 
GROUP BY c.customer_id ,
         c.customer_name
)
SELECT 
      customer_name,
      num_of_orders ,
      total_spending
FROM T 
ORDER BY total_spending DESC
LIMIT 5 
      
'''
#-------------------------------------------------
#20 Retrieve the latest completed order for each customer.

'''
customers
---------
customer_id       INT PRIMARY KEY
customer_name     VARCHAR(100)
email             VARCHAR(150)
city              VARCHAR(80)
region            VARCHAR(80)
signup_date       DATE


orders
------
order_id          INT PRIMARY KEY
customer_id       INT FOREIGN KEY
employee_id       INT FOREIGN KEY
order_date        DATE
status            VARCHAR(30)

'''

"""
WITH T AS(

SELECT
      c.customer_id ,
      c.customer_name,
      o.order_id ,
      o.order_date
FROM customers c 
JOIN orders o
ON c.customer_id = o.customer_id 
WHERE o.status ='Completed'
GROUP BY c.customer_id ,
         c.customer_name
     
) , B AS(

SELECT 
     customer_id ,
     customer_name,
     order_id ,
     order_date,
     ROW_NUMBER() OVER(
                       PARTITION BY order_id 
                       ORDER BY order_date ASC) AS latest_order
FROM T 
)
SELECT * FROM B
WHERE latest_order =1
"""
#--------------------------------------------------
#Rank products by revenue within each category and 
# retrieve the top three products from every category.

'''

categories
----------
category_id       INT PRIMARY KEY
category_name     VARCHAR(100)


products
--------
product_id        INT PRIMARY KEY
product_name      VARCHAR(150)
category_id       INT FOREIGN KEY


orders
------
order_id          INT PRIMARY KEY
customer_id       INT FOREIGN KEY
employee_id       INT FOREIGN KEY
order_date        DATE
status            VARCHAR(30)


order_items
-----------
order_item_id     INT PRIMARY KEY
order_id          INT FOREIGN KEY
product_id        INT FOREIGN KEY
quantity          INT
unit_price        NUMERIC(12,2)
discount_pct      NUMERIC(5,2)
unit_cost         NUMERIC(12,2)

'''

#21 Rank products by revenue within each category and 
# retrieve the top three products from every category.

'''
WITH T AS(
SELECT 
     c.category_id,
     c.category_name,
     p.product_id,
     p.product_name,
     SUM(
     (oi.quantity * oi.unit_price) * (1 - COALESCE(oi.discount_pct,0)/100.0)
     ) AS total_revenue
FROM categories c
JOIN products p
ON c.category_id = p.category_id 
JOIN order_items oi
ON p.product_id = oi.product_id 
JOIN orders o
ON o.order_id = oi.order_id 
WHERE o.status = 'Completed'
GROUP BY c.category_id,
         c.category_name,
         p.product_id,
         p.product_name

), B AS(
SELECT 
      DENSE_RANK() OVER(
                        PARTITION BY category_id , product_id
                        ORDER BY total_revenue DESC) AS top_products,
     DENSE_RANK()OVER (
                       PARTITION BY category_id ,product_id
                       ORDER BY total_revenue DESC) AS top_three
FROM T 
)
SELECT * FROM B 
WHERE top_products =1
AND top_three <= 3
'''

#-------------------------------------------------

#22 Calculate monthly revenue and month-over-month 
# revenue change as both an absolute amount and a percentage.


'''

orders
------
order_id          INT PRIMARY KEY
customer_id       INT FOREIGN KEY
employee_id       INT FOREIGN KEY
order_date        DATE
status            VARCHAR(30)
 
order_items
-----------
order_item_id     INT PRIMARY KEY
order_id          INT FOREIGN KEY
product_id        INT FOREIGN KEY
quantity          INT
unit_price        NUMERIC(12,2)
discount_pct      NUMERIC(5,2)
unit_cost         NUMERIC(12,2)

'''
"""
WITH T AS (
    SELECT
        DATE_TRUNC('month', o.order_date) AS month,
        SUM(
            oi.quantity * oi.unit_price *
            (1 - COALESCE(oi.discount_pct,0)/100.0)
        ) AS monthly_revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.status = 'Completed'
    GROUP BY DATE_TRUNC('month', o.order_date)
),
B AS (
    SELECT
        month,
        monthly_revenue,
        LAG(monthly_revenue) OVER (
            ORDER BY month
        ) AS prev_month
    FROM T
)

SELECT
    month,
    monthly_revenue,
    monthly_revenue - prev_month AS absolute_change,
    (monthly_revenue - prev_month)
        / NULLIF(prev_month, 0) * 100 AS percentage_change
FROM B
WHERE prev_month IS NOT NULL
"""
#-------------------------------------------------

#23 Calculate cumulative monthly revenue from the beginning of the dataset.

'''
WITH T AS (
    SELECT
        DATE_TRUNC('month', o.order_date) AS month,
        SUM(
            oi.quantity * oi.unit_price *
            (1 - COALESCE(oi.discount_pct,0)/100.0)
        ) AS monthly_revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.status = 'Completed'
    GROUP BY DATE_TRUNC('month', o.order_date)
)

SELECT
    month,
    monthly_revenue,
    SUM(monthly_revenue) OVER (
        ORDER BY month
    ) AS cumulative_revenue
FROM T
'''

#-------------------------------------------------
#24 Rank customers by total spending within each city.

'''
WITH T AS (
    SELECT
        c.city,
        c.customer_id,
        c.customer_name,
        COALESCE(
            SUM(
                oi.quantity * oi.unit_price *
                (1 - COALESCE(oi.discount_pct,0)/100.0)
            ), 0
        ) AS total_spending

    FROM customers c
    LEFT JOIN orders o
        ON c.customer_id = o.customer_id
        AND o.status = 'Completed'

    LEFT JOIN order_items oi
        ON o.order_id = oi.order_id

    GROUP BY
        c.city,
        c.customer_id,
        c.customer_name
),
R AS (
    SELECT
        *,
        DENSE_RANK() OVER (
            PARTITION BY city
            ORDER BY total_spending DESC
        ) AS rnk
    FROM T
)

SELECT *
FROM R
ORDER BY city, rnk;
'''
#---------------------------------------------
#25 Calculate monthly revenue for each employee 
#and include their cumulative revenue over time.

'''
WITH T AS(
SELECT 
     e.employee_id ,
     e.employee_name,
     DATE_TRUNC('month',o.order_date) AS month ,
     SUM(
     (oi.quantity * oi.unit_price) * (1 - COALESCE(oi.discount_pct,0)/100.0)
     ) AS monthly_revenue 
FROM employees e
LEFT JOIN orders o 
ON o.employee_id = e.employee_id 
AND o.status = 'Completed'
LEFT JOIN order_items oi 
ON o.order_id = oi.order_id
GROUP BY e.employee_id ,
         e.employee_name,
         DATE_TRUNC('month',o.order_date)

), L AS(
SELECT 
      month,
      employee_id ,
      employee_name,
      monthly_revenue ,
      SUM(monthly_revenue) OVER(PARTITION BY employee_id
                                ORDER BY order_date ASC) AS cumulative_revenue
FROM T
)
SELECT * FROM L

'''
#---------------------------------------------------
#26 Rank each customer's completed orders 
# from highest to lowest by order value.

#هنا يقصد sum(order_id) ! ولا قيمة الاوردر يعنى بالريفينيو العادى 
#بعيدا عن كتابة الكويرى كاملة الفكرة هتبقى 
'''
WITH T AS (
    SELECT
        c.customer_id,
        c.customer_name,
        o.order_id,

        SUM(
            oi.quantity * oi.unit_price *
            (1 - COALESCE(oi.discount_pct,0)/100.0)
        ) AS order_value

    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.status = 'Completed'

    GROUP BY
        c.customer_id,
        c.customer_name,
        o.order_id
)

SELECT
    *,
    DENSE_RANK() OVER (
        PARTITION BY customer_id
        ORDER BY order_value DESC
    ) AS order_rank
FROM T
'''
#----------------------------------------------------
#27 Calculate the return rate for each product based on 
# approved returned quantities compared with completed-order quantities.


'''

returns
-------
return_id         INT PRIMARY KEY
order_item_id     INT FOREIGN KEY
return_date       DATE
return_status     VARCHAR(30)
returned_quantity INT
refund_amount     NUMERIC(12,2)

products
--------
product_id        INT PRIMARY KEY
product_name      VARCHAR(150)
category_id       INT FOREIGN KEY

order_items
-----------
order_item_id     INT PRIMARY KEY
order_id          INT FOREIGN KEY
product_id        INT FOREIGN KEY
quantity          INT
unit_price        NUMERIC(12,2)
discount_pct      NUMERIC(5,2)
unit_cost         NUMERIC(12,2)

orders
------
order_id          INT PRIMARY KEY
customer_id       INT FOREIGN KEY
employee_id       INT FOREIGN KEY
order_date        DATE
status            VARCHAR(30)

'''

#27 Calculate the return rate for each product based on 
# approved returned quantities compared with completed-order quantities.

'''
WITH T AS (
    SELECT
        p.product_id,
        p.product_name,
        SUM(oi.quantity) AS sold_qty
    FROM products p
    JOIN order_items oi
        ON p.product_id = oi.product_id
    JOIN orders o
        ON oi.order_id = o.order_id
    WHERE o.status = 'Completed'
    GROUP BY p.product_id, p.product_name
),
R AS (
    SELECT
        oi.product_id,
        SUM(r.returned_quantity) AS returned_qty
    FROM returns r
    JOIN order_items oi
        ON r.order_item_id = oi.order_item_id
    JOIN orders o
        ON oi.order_id = o.order_id
    WHERE r.return_status = 'Approved'
      AND o.status = 'Completed'
    GROUP BY oi.product_id
)

SELECT
    T.product_id,
    T.product_name,
    T.sold_qty,
    COALESCE(R.returned_qty, 0) AS returned_qty,
    COALESCE(R.returned_qty, 0) * 100.0
        / NULLIF(T.sold_qty, 0) AS return_rate
FROM T
LEFT JOIN R
    ON T.product_id = R.product_id
'''

#---------------------------------------------
#28 Calculate total approved refunds by product category 
# and identify the categories with the highest refund amounts.

'''
categories
----------
category_id       INT PRIMARY KEY
category_name     VARCHAR(100)

products
--------
product_id        INT PRIMARY KEY
product_name      VARCHAR(150)
category_id       INT FOREIGN KEY

order_items
-----------
order_item_id     INT PRIMARY KEY
order_id          INT FOREIGN KEY
product_id        INT FOREIGN KEY
quantity          INT
unit_price        NUMERIC(12,2)
discount_pct      NUMERIC(5,2)
unit_cost         NUMERIC(12,2)

returns
-------
return_id         INT PRIMARY KEY
order_item_id     INT FOREIGN KEY
return_date       DATE
return_status     VARCHAR(30)
returned_quantity INT
refund_amount     NUMERIC(12,2)
'''

'''
WITH T AS (
    SELECT
        c.category_id,
        c.category_name,
        SUM(r.refund_amount) AS total_refunds

    FROM categories c
    JOIN products p
        ON c.category_id = p.category_id

    JOIN order_items oi
        ON p.product_id = oi.product_id

    JOIN returns r
        ON oi.order_item_id = r.order_item_id

    WHERE r.return_status = 'Approved'

    GROUP BY
        c.category_id,
        c.category_name
)

SELECT
    *,
    DENSE_RANK() OVER (
        ORDER BY total_refunds DESC
    ) AS refund_rank
FROM T
ORDER BY total_refunds DESC;
'''
#-------------------------------------------------------

#29 Compare the completed-order value against the total successful 
#payments for each order. Identify orders where the two amounts do not match.

'''

orders
------
order_id          INT PRIMARY KEY
customer_id       INT FOREIGN KEY
employee_id       INT FOREIGN KEY
order_date        DATE
status            VARCHAR(30)


order_items
-----------
order_item_id     INT PRIMARY KEY
order_id          INT FOREIGN KEY
product_id        INT FOREIGN KEY
quantity          INT
unit_price        NUMERIC(12,2)
discount_pct      NUMERIC(5,2)
unit_cost         NUMERIC(12,2)


payments
--------
payment_id        INT PRIMARY KEY
order_id          INT FOREIGN KEY
payment_date      DATE
payment_method    VARCHAR(50)
payment_status    VARCHAR(30)
amount            NUMERIC(12,2)

'''
'''
WITH T AS (
    SELECT
        o.order_id,
        SUM(
            oi.quantity * oi.unit_price *
            (1 - COALESCE(oi.discount_pct,0)/100.0)
        ) AS order_value

    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.status = 'Completed'
    GROUP BY o.order_id
),
P AS (
    SELECT
        order_id,
        SUM(amount) AS total_payments
    FROM payments
    WHERE payment_status = 'Successful'
    GROUP BY order_id
)

SELECT
    T.order_id,
    T.order_value,
    COALESCE(P.total_payments, 0) AS total_payments
FROM T
LEFT JOIN P
    ON T.order_id = P.order_id
WHERE T.order_value <> COALESCE(P.total_payments, 0);
     
'''
#-------------------------------------------------------

#30 Identify customers who placed at least three 
#completed orders and calculate their total spending.


'''
SELECT 
      c.customer_id ,
      c.customer_name,
      SUM(
           (oi.quantity * oi.unit_price) * (1 - COALESCE(oi.discount_pct,0)/100.0)
           ) AS compeleted_revenue,
     COUNT(DISTINCT o.order_id) AS num_of_orders 
FROM customers c 
JOIN orders o 
ON c.customer_id = o.customer_id 
JOIN order_items oi 
ON o.order_id = oi.order_id 
WHERE o.status = 'Completed'
GROUP BY c.customer_id ,
         c.customer_name 
HAVING COUNT(DISTINCT o.order_id) >= 3


'''
#------------------------------------------------------
#31 Calculate the percentage contribution of 
#each product category to total completed-order revenue.

'''
WITH T AS (
    SELECT
        c.category_id,
        c.category_name,

        SUM(
            oi.quantity * oi.unit_price *
            (1 - COALESCE(oi.discount_pct,0)/100.0)
        ) AS category_revenue

    FROM categories c

    JOIN products p
        ON c.category_id = p.category_id

    JOIN order_items oi
        ON p.product_id = oi.product_id

    JOIN orders o
        ON oi.order_id = o.order_id

    WHERE o.status = 'Completed'

    GROUP BY
        c.category_id,
        c.category_name
)

SELECT
    category_id,
    category_name,
    category_revenue,

    category_revenue * 100.0 /
    SUM(category_revenue) OVER () AS contribution_percentage

FROM T
ORDER BY contribution_percentage DESC;
'''
#------------------------------------------------------
#32 Calculate monthly revenue by region and identify the 
# highest-revenue month for each region.

'''
WITH T AS (
    SELECT
        c.region,
        DATE_TRUNC('month', o.order_date) AS month,

        SUM(
            oi.quantity * oi.unit_price *
            (1 - COALESCE(oi.discount_pct,0)/100.0)
        ) AS monthly_revenue

    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.status = 'Completed'

    GROUP BY
        c.region,
        DATE_TRUNC('month', o.order_date)
),
R AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY region
            ORDER BY monthly_revenue DESC
        ) AS rn
    FROM T
)

SELECT *
FROM R
WHERE rn = 1
'''











