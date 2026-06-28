"""
## 1) Top Customers by Total Spending

### Schema

```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(50)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2)
);
```

### Question

Write a SQL query to find the top 3 customers who spent the highest total amount in 2025.

Return:

* customer_id
* customer_name
* total_spent

Order the result by total_spent descending.

ANSWER A /

WITH TOP_CUST AS(
SELECT c.customer_id , c.customer_name , DATE_TRUNC('year',o.order_date) AS year ,
SUM(o.total_amount) AS total_spent , ROW_NUMBER() OVER(
ORDER BY o.total_amount DESC) AS TOP_THREE
FROM customers c
LEFT JOIN orders o 
ON c.customer_id = o.customer_id 
WHERE DATE_TRUNC(year,o.order_date) = '2025'
)
SELECT customer_id , customer_name , total_spent
FROM TOP_CUST
WHERE TOP_THREE <=3

--------

ANSWER B /

WITH TOP_CUSTOMERS AS(
SELECT c.customer_id , c.customer_name , DATE_TRUNC('year',o.order_date) AS year,
SUM(o.total_amount) AS total_spent
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id 
WHERE DATE_TRUNC(year,o.order_date) = '2025'
), T AS ( SELECT customer_id , customer_name , total_spent ,
ROW_NUMBER() OVER(ORDER BY total_spent DESC) AS top_three
FROM TOP_CUSTOMERS )
SELECT * FROM T
WHERE top_three <=3

--------
ANSWER C/
SELECT c.customer_id , c.customer_name , SUM(o.total_amount) AS total_spent , 
DATE_TRUNC('year',o.order_date) AS year
FROM customers c
LEFT JOIN orders o 
ON c.customer_id = o.customer_id 
WHERE DATE_TRUNC('year',o.order_date) = ' 2025'
ORDER BY total_spent DESC
LIMIT 3
#انا بحتار اوى امتى اجمع الفلوس وامتى اسيبها زى ماهى ومش عارفة انهى اجابة صح وهل لازم اعمل جروب باى على التاريخ ولا الشرط كدا وخلاص

#===============================
#===============================

## 2) Second Highest Salary

### Schema

```sql
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100),
    department VARCHAR(50),
    salary INT
);
```

### Question

Write a query to find the second highest salary from the employees table.

Return:

* second_highest_salary

ANSWER /

WITH SEC_SALARY AS(
SELECT
emp_id , emp_name , salary ,
ROW_NUMBER() OVER(ORDER BY salary DESC) AS sec_highest_salary
FROM employees 
)
SELECT sec_highest_salary FROM SEC_SALARY
WHERE sec_highest_salary = 2
---
#=========================
#=========================

## 3) Customers Who Never Ordered
 
### Schema

```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE
);
```

### Question

Write a SQL query to find all customers who never placed any orders.

Return:

* customer_id
* customer_name

ANSWER /

SELECT c.customer_id , c.customer_name 
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id 
WHERE o.order_id IS NULL

---
#================================
#================================

## 4) Monthly Sales Report

### Schema

```sql
CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    product_id INT,
    sale_date DATE,
    amount DECIMAL(10,2)
);
```

### Question

Write a query to calculate total sales amount for each month in 2025.

Return:

* month
* total_sales

Sort by month ascending.

---
ANSWER / 
SELECT DATE_TRUNC('month',sale_date) AS month , SUM(amount) AS total_sales
FROM sales 
WHERE DATE_TRUNC('year',sale_date) = '2025'
GROUP BY month
ORDER BY month ASC

#===============================
#===============================
## 5) Highest Paid Employee in Each Department

### Schema

```sql
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100),
    department VARCHAR(50),
    salary INT
);
```

### Question

Write a query to find the employee(s) with the highest salary in each department.

Return:

* department
* emp_name
* salary

ANSWER /

WITH HIGHEST_SAL AS (
SELECT emp_id , emp_name , salary , department 
FROM employees 
GROUP BY department
) , t AS( SELECT 
department , emp_name , salary ,
ROW_NUMBER() OVER(
PARTITION BY department 
ORDER BY salary DESC) AS highest_salary
FROM HIGHEST_SAL
)
SELECT department , emp_name , salary
WHERE highest_salary = 1

#==================================
#==================================

## 6) Duplicate Emails

### Schema

```sql
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    email VARCHAR(255)
);
```

### Question

Write a SQL query to find all duplicate email addresses.

Return:

* email
* duplicate_count

---

ANSWER /
SELECT email 
FROM users 
GROUP BY email
HAVING email > 1

#==============================
#==============================

## 7) Product Revenue Analysis

### Schema

```sql
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50)
);

CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2)
);
```
### Question

Write a query to calculate total revenue generated by each product category.

Revenue = quantity * price

Return:

* category
* total_revenue

Order by total_revenue descending.

ANSWER /
SELECT p.category , SUM(o.price) AS total_revenue
FROM products p 
LEFT JOIN order_items o
ON p.product_id , o.product_id
GROUP BY p.category 
ORDER BY total_revenue DESC

#==================================
#==================================


## 8) Employees Earning Above Department Average

### Schema

```sql
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100),
    department VARCHAR(50),
    salary INT
);
```

### Question

Write a SQL query to find employees whose salary is greater than the average
salary of their department.

Return:

* emp_id
* emp_name
* department
* salary

ANSWER /

SELECT emp_id , emp_name , department ,salary
FROM employees
GROUP BY emp_id , emp_name 
HAVING salary > (SELECT AVG(salary) FROM employees
                GROUP BY department)

#=========================
#=========================


## 9) Daily Active Users

### Schema

```sql
CREATE TABLE logins (
    login_id INT PRIMARY KEY,
    user_id INT,
    login_date DATE
);
```

### Question

Write a query to count the number of unique active users for each day.

Return:

* login_date
* active_users

Sort by login_date ascending.

ANSWER /

SELECT COUNT(DISTINCT user_id) AS active_users , DATE_TRUNC('day',login_date) AS day
FROM logins
GROUP BY day
ORDER BY day ASC 

#==============================
#==============================

## 10) Consecutive Login Days

### Schema

```sql
CREATE TABLE user_logins (
    user_id INT,
    login_date DATE 
);
```

### Question

Write a SQL query to find users who logged in for at least 3 consecutive days.

Return:

* user_id



"""

#====================================
#====================================
#====================================
#====================================

"""
#15/5
# 1) Find Managers With At Least 5 Direct Reports

### Schema

```sql
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    manager_id INT,
    salary INT
);
```

### Question

Write a SQL query to find managers who have at least 5 direct reports.

Return:

* manager_id
* total_reports

ANSWER /

SELECT
    m.employee_id AS manager_id,
    COUNT(e.employee_id) AS total_reports
FROM employees e
JOIN employees m
    ON e.manager_id = m.employee_id
GROUP BY m.employee_id
HAVING COUNT(e.employee_id) >= 5;
#----------------------------------
# Find Employees Who Earn More Than Their Manager

### Schema

```sql id="8y3zke"
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    manager_id INT,
    salary INT
);
```

### Question

Write a SQL query to find employees whose salary is greater than their manager's salary.

Return:

* employee_id
* employee_name
* employee_salary
* manager_name
* manager_salary

ANSWER /

SELECT
    e.employee_id,
    e.employee_name AS employee_name,
    e.salary AS employee_salary,
    m.employee_name AS manager_name,
    m.salary AS manager_salary
FROM employees e
JOIN employees m
    ON m.employee_id = e.manager_id
WHERE e.salary > m.salary;
#---------------------------
# Find Employees Who Have the Same Salary as Their Manager

### Schema

```sql id="z4jw9r"
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    manager_id INT,
    salary INT
);
```

### Question

Write a SQL query to find employees whose salary is exactly the same as their manager's salary.

Return:

* employee_id
* employee_name
* employee_salary
* manager_name
* manager_salary

ANSWER /

SELECT 
    e.employee_id AS employee_id ,
    e.employee_name AS employee_name ,
    e.salary AS employee_salary ,
    m.employee_name AS manager_name ,
    m.salary AS manager_salary
FROM employees e
JOIN employees m
ON m.employee_id = e.manager_id 
WHERE e.salary = m.salary 

#=========================================================
16/5
#=========================================================
#REV
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    manager_id INT,
    salary INT
);
Write a SQL query to find employees whose salary
is less than their manager's salary.

RETURN :
employee_id
employee_name
employee_salary
manager_name
manager_salary

SELECT  e.employee_id , e.employee_name ,
        e.salary AS employee_salary , 
        m.employee_name AS manager_name ,
        m.salary AS manager_salary
FROM employees e
JOIN employees m
ON e.manager_id = m.employee_id 
WHERE e.salary < m.salary

#===================================
#===================================

# 2) Latest Order for Each Customer

### Schema

```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2)
);
```

### Question

Write a query to return the latest order
placed by each customer.

Return:

* customer_id
* customer_name
* order_id
* order_date
* total_amount

ANSWER A /

SELECT c.customer_id , c.customer_name , 
       o.order_id , o.order_date ,
       o.total_amount 
FROM customers c
LEFT JOIN orders o 
ON c.customer_id = o.customer_id 
GROUP BY c.customer_id , c.customer_name 
ORDER BY o.order_date DESC


#-----------
ANSWER B /

WITH LATEST_O AS(
SELECT c.customer_id , c.customer_name , 
       o.order_id , o.order_date ,
       o.total_amount ,
       DENSE_RANK() OVER(
       PARTITION BY c.customer_id , c.customer_name
       ORDER BY o.order_date DESC) AS latest_order
FROM customers c
LEFT JOIN orders o 
ON c.customer_id = o.customer_id 
)
SELECT * FROM LATEST_O
WHERE latest_order = 1

#----------------------------------
# Find Highest Salary Employee in Each Department

### Schema

```sql id="z7x3m1"
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    department VARCHAR(50),
    salary INT
);
```
### Question

Write a SQL query to find the employee(s) who have the highest salary in each department.

Return:

* department
* employee_id
* employee_name
* salary


### Important

If multiple employees have the same highest salary in a department, return all of them.

WITH HIGHEST_S AS(
SELECT  
    department , 
    employee_id , 
    employee_name ,
    salary ,
    DENSE_RANK() OVER(
    PARTITION BY department , department_id
    ORDER BY salary DESC) AS highest_salary

FROM employees 
)
SELECT * FROM HIGHEST_S
WHERE highest_salary =1


#====================================
#====================================
17/5
#====================================
#====================================
#REV
# Find the Lowest Paid Employee(s) in Each Department

### Schema

```sql id="8j4rpn"
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    department VARCHAR(50),
    salary INT
);
```

### Question

Write a SQL query to find the employee(s) who have the lowest salary in each department.

Return:

* department
* employee_id
* employee_name
* salary

---

### Important

If multiple employees have the same lowest salary in a department, return all of them.

ANSWER /

WITH LOWEST_S AS (
SELECT 
    department , 
    employee_id , 
    employee_name , 
    salary , 
    DENSE_RANK() OVER(
    PARTITION BY department 
    ORDER BY salary ASC) AS lowest_salary 
FROM employees 
)
SELECT * FROM LOWEST_S 
WHERE lowest_salary = 1

#==============================
#==============================

# 3) Find Products Never Sold

### Schema

```sql
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50)
);

CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    product_id INT,
    quantity INT,
    sale_date DATE
);
```

### Question

Write a SQL query to find products that were never sold.

Return:

* product_id
* product_name

ANSWER /

SELECT 
    p.product_id ,
    p.product_name 
FROM products p
LEFT JOIN sales s
ON p.product_id = s.product_id 
WHERE s.sale_id IS NULL

#------------------------------------
# Find Customers Who Never Placed an Order in 2025

### Schema

```sql id="5v7kqp"
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2)
);
```

### Question

Write a SQL query to find customers who never placed any orders in 2025.

Return:

* customer_id
* customer_name

ANSWER /

SELECT
    c.customer_id ,
    c.customer_name 
FROM customers c 
LEFT JOIN orders o
ON c.customer_id = o.customer_id
AND DATE_TRUNC('year',o.order_date) = '2025'
WHERE o.order_id IS NULL

#-----------------------------
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100)
);

CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    product_id INT,
    sale_date DATE,
    quantity INT
);

ANSWER /
SELECT 
    p.product_id ,
    p.product_name
FROM products p 
LEFT JOIN sales s
ON p.product_id = s.product_id 
AND sale_date BETWEEN '01-01-2025' AND '31-01-2025'
WHERE s.sale_id IS NULL

#=====================================
#=====================================
18/5
#=====================================
#=====================================
REV
# Find Employees Who Did Not Receive Any Bonus in 2025

### Schema

```sql id="k9w2mf"
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    department VARCHAR(50)
);

CREATE TABLE bonuses (
    bonus_id INT PRIMARY KEY,
    employee_id INT,
    bonus_amount DECIMAL(10,2),
    bonus_date DATE
);
```

### Question

Write a SQL query to find employees who did not receive any bonus in 2025.

Return:

* employee_id
* employee_name

ANSWER /
SELECT 
    e.employee_id , 
    e.employee_name
FROM employees e
LEFT JOIN bonuses b
ON e.employee_id = b.employee_id 
AND DATE_TRUNC('year',bonus_date) = '2025'
WHERE b.bonus_id IS NULL

#-----------------------------
# Find Customers Who Placed Orders in Every Month of 2025

### Schema

```sql id="q6z9af"
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2)
);
```

### Question

Write a SQL query to find customers who placed at least one order in **every month** of 2025.

Return:

* customer_id
* customer_name

---

### Important

* A customer should have orders in:

  * January
  * February
  * March
  * ...
  * December

ANSWER / 

SELECT 
    c.customer_id ,
    c.customer_name 
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id
WHERE EXTRACT(YEAR FROM o.order_date) = 2025
GROUP BY c.customer_id , c.customer_name 
HAVING COUNT(DISTINCT EXTRACT(MONTH FROM o.order_date)) =12


#======================================
#======================================
------------------------------------------------------------------------------
----------------------------- REV THE LAST TRICKY ----------------------------
------------------------------------------------------------------------------

# 1) Customers Who Purchased All Product Categories

### Schema

```sql id="m7x2qa" A
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100)  
);

CREATE TABLE products ( D 'TARGET TABLE'
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50)
);

CREATE TABLE orders ( B
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE
);

CREATE TABLE order_items ( C
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT
);
```

### Question

Write a SQL query to find customers who purchased products from **all categories**.

Return:

* customer_id
* customer_name

SELECT 
    c.customer_id ,
    c.customer_name 
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
JOIN order_items ot
ON o.order_id = ot.order_id
JOIN products p
ON ot.product_id = p.product_id 
GROUP BY c.customer_id , c.customer_name
HAVING COUNT(DISTINCT p.category) = (SELECT COUNT(DISTINCT category) FROM products)


#-------------------------------------------
#-------------------------------------------

# 2) Employees Assigned to All Projects

### Schema

```sql id="j4n8wk"
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100)
);

CREATE TABLE projects (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(100)
);

CREATE TABLE employee_projects (
    employee_id INT,
    project_id INT,
    assigned_date DATE
);
```

### Question

Write a SQL query to find employees who are assigned to **every project**.

Return:

* employee_id
* employee_name

ANSWER /
SELECT 
    e.employee_id ,
    e.employee_name
FROM employees e
JOIN employee_projects ep
ON e.employee_id = ep.employee_id
JOIN projects p
ON ep.project_id = p.project_id
GROUP BY e.employee_id , e.employee_name
HAVING COUNT(DISTINCT p.project_id) = (SELECT COUNT(DISTINCT project_id) FROM projects )


#----------------------------------------
#----------------------------------------
# 3) Users Active Every Day for 7 Consecutive Days

### Schema

```sql id="t2v7pz"
CREATE TABLE user_logins (
    user_id INT,
    login_date DATE
);
```

### Question

Write a SQL query to find users who logged in for at least 7 consecutive days.

Return:

* user_id

ANSWER /

WITH USERS AS(
SELECT 
    user_id 
FROM user_logins
GROUP BY user_id 
), T AS( SELECT user_id,
    LAG(login_date) OVER(ORDER BY login_date ASC) AS f_day ,
    LEAD(login_date) OVER(ORDER BY login_date ASC ) AS n_day
FROM USERS
)
SELECT user_id FROM T
WHERE n_day - f_day = 7



#---------------------------------------
#---------------------------------------

# 4) Find the Second Most Expensive Product in Each Category

### Schema

```sql id="x9m4rq"
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2)
);
```

### Question

Write a SQL query to find the second most expensive product in each category.

Return:

* category
* product_id
* product_name
* price

---

# 5) Find Customers Whose Total Spending Is Above the Average Spending of All Customers

### Schema

```sql id="q8z1lm"
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    total_amount DECIMAL(10,2)
);
```

### Question

Write a SQL query to find customers whose total spending is greater than the average total spending of all customers.

Return:

* customer_id
* customer_name
* total_spending

---

# 6) Find Departments Where the Average Salary Is Higher Than the Company Average Salary

### Schema

```sql id="p6w3kn"
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    department VARCHAR(50),
    salary INT
);
```

### Question

Write a SQL query to find departments whose average salary is greater than the overall average salary of the company.

Return:

* department
* department_avg_salary

---

# 7) Find Customers With More Than 3 Orders in a Single Month

### Schema

```sql id="v5r8xy"
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE
);
```

### Question

Write a SQL query to find customers who placed more than 3 orders within the same month.

Return:

* customer_id
* customer_name
* month
* total_orders

---

# 8) Find Products With Increasing Sales for 3 Consecutive Months

### Schema

```sql id="w1q9ts"
CREATE TABLE monthly_sales (
    product_id INT,
    sales_month DATE,
    total_sales INT
);
```

### Question

Write a SQL query to find products whose sales increased for 3 consecutive months.

Return:

* product_id

---

# 9) Find Employees Who Earn More Than the Average Salary of Their Department

### Schema

```sql id="r2m7yv"
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    department VARCHAR(50),
    salary INT
);
```

### Question

Write a SQL query to find employees whose salary is higher than the average salary of their own department.

Return:

* employee_id
* employee_name
* department
* salary

---

# 10) Find the Top 2 Highest Paid Employees in Each Department

### Schema

```sql id="u8x3kp"
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    department VARCHAR(50),
    salary INT
);
```

### Question

Write a SQL query to find the top 2 highest paid employees in each department.

Return:

* department
* employee_id
* employee_name
* salary
* salary_rank

*************************************************************************
*************************************************************************
*************************************************************************
*************************************************************************
*************************************************************************
*************************************************************************
*************************************************************************
#======================================
#======================================
#======================================
# 4) Running Total of Sales

### Schema

```sql
CREATE TABLE daily_sales (
    sale_date DATE,
    sales_amount DECIMAL(10,2)
);
```
### Question

Write a query to calculate the running total of sales by date.

Return:

* sale_date
* sales_amount
* running_total

Sort by sale_date ascending.

'''
SELECT 
    sales_amount , sale_date ,
    SUM(sales_amount) OVER(
                        ORDER BY sale_date ASC) AS running_total
FROM daily_sales

'''
---

# 5) Find Consecutive Orders

### Schema

```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE
);
```

### Question

Write a SQL query to find customers who placed orders on 3 consecutive days.

Return:
* customer_id

WITH cte AS (
SELECT DISTINCT
    customer_id , order_id , order_date ,
    LAG(order_date,1) OVER(PARTITION BY customer_id ORDER BY order_date) AS prev_1 ,
    LAG(order_date,2) OVER(PARTITION BY customer_id ORDER BY order_date) AS prev_2
FROM orders 
) 
SELECT DISTINCT
    customer_id 
FROM cte
WHERE DATEDIFF(day,prev_1 , order_date) = 1
AND DATEDIFF(day,prev_2 , prev_1) = 1

#===========================================
#===========================================
---

# 6) Department Salary Ranking

### Schema

```sql
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100),
    department VARCHAR(50),
    salary INT
);
```

### Question

Write a query to rank employees within each department based on salary.

Return:

* emp_id
* emp_name
* department
* salary
* salary_rank

Highest salary should get rank 1.


SELECT 
    emp_id , 
    emp_name , 
    department , 
    salary ,
    RANK() OVER (PARTITION BY department
            ORDER BY salary DESC) AS rank
FROM employees
)
---

#===============================
#===============================

# 7) Percentage Contribution to Total Sales

### Schema

```sql
CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    category VARCHAR(50),
    amount DECIMAL(10,2)
);
```

### Question

Write a SQL query to calculate what percentage each category contributes to total sales.

Return:

* category
* total_sales
* percentage_of_total

---

WITH t AS (
SELECT 
    category , 
    sale_id , 
    SUM(amount) AS total_sales,
    
FROM sales
GROUP BY category
) 
SELECT 
    category , 
    total_sales ,
    total_sales * 0.01 / SUM(total_sales) OVER() AS percentage_total 
FROM t  
#============================================
#============================================
# 8
# ) Find Duplicate Records Based on Multiple Columns

### Schema

```sql
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    user_id INT,
    transaction_date DATE,
    amount DECIMAL(10,2)
);
```

### Question

Write a query to find duplicate transactions based on:

* user_id
* transaction_date
* amount

Return:

* user_id
* transaction_date
* amount
* duplicate_count

SELECT DISTINCT
    user_id , 
    transaction_date , 
    amount ,
    COUNT(DISTINCT transaction_id) AS duplicate_count
FROM transactions
GROUP BY user_id , transaction_date , amount

#=================================
#=================================


# 9) Average Time Between Orders

### Schema

```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE
);
```

### Question

Write a SQL query to calculate the average number of days between orders for each customer.

Return:

* customer_id
* avg_days_between_orders


WITH t AS (
    SELECT
        customer_id,
        order_date,
        LAG(order_date) OVER(
            PARTITION BY customer_id
            ORDER BY order_date
        ) AS prev_order_date
    FROM orders
)

SELECT
    customer_id,
    AVG(
        DATEDIFF(day, prev_order_date, order_date)
    ) AS avg_days_between_orders
FROM t
WHERE prev_order_date IS NOT NULL
GROUP BY customer_id  



#======================================
#======================================

# 10) Find Top Selling Product Per Month

### Schema

```sql
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100)
);

CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    product_id INT,
    quantity INT,
    sale_date DATE
);
```

### Question

Write a query to find the top-selling product for each month based on total quantity sold.

Return:

* month
* product_id
* product_name
* total_quantity_sold

SOLUTION A /

WITH T AS(
SELECT DISTINCT
    p.product_id , 
    p.product_name ,
    MONTH(s.sale_date) AS month ,
    COUNT(s.quantity) AS total_quantity_sold ,
FROM product p
JOIN sales s
ON p.product_id = s.product_id 
GROUP BY month , total_quantity_sold
)
SELECT 
    month ,
    product_id ,
    product_name ,
    total_quantity_sold ,
    ROW_NUMBER() OVER(
    PARTITION BY product_id , product_name 
    ORDER BY total_quantity_sold DESC) AS top_selling_product
FROM T
WHERE top_selling_product = 1


SOLUTION B /


SELECT DISTINCT
    p.product_id , 
    p.product_name ,
    MONTH(s.sale_date) AS month ,
    COUNT(s.quantity) AS total_quantity_sold ,
FROM product p
JOIN sales s
ON p.product_id = s.product_id 
GROUP BY month , total_quantity_sold
ORDER BY  COUNT(s.quantity) AS total_quantity_sold DESC
LIMIT 1


#==================================
#==================================
#==================================
#==================================
#==================================
#----------------------------------
--- Rev Of Week ---
#----------------------------------
#==================================
#==================================
#==================================
#==================================
#==================================
# WEEK ONE---

# RANK Problem 1

### Schema

```sql
CREATE TABLE employees (
    emp_id INT,
    emp_name VARCHAR(50),
    department VARCHAR(50),
    salary INT
);
```

### Question

Rank employees within each department based on salary.

Return:

* emp_id
* emp_name
* department
* salary
* salary_rank

Highest salary should get rank 1.

SELECT 
    emp_id ,
    emp_name ,
    department ,
    salary ,
    RANK() OVER(PARTITION BY department ORDER BY salary DESC) AS salary_rank
FROM employees 

#==============================
#==============================

# RANK Problem 2

### Schema

```sql
CREATE TABLE products (
    product_id INT,
    category VARCHAR(50),
    product_name VARCHAR(50),
    revenue INT
);
```

### Question

Find the top 2 highest-revenue products in each category.

Return:

* category
* product_name
* revenue

WITH t AS (
SELECT 
    product_id ,
    category ,
    product_name ,
    revenue ,
    RANK() OVER(PARTITION BY category ORDER BY revenue DESC) AS highest_rank
FROM products 
)
SELECT 
    category ,
    product_name ,
    revenue 
FROM t 
WHERE highest_rank <=2

#===============================
#===============================

---

# RANK Problem 3

### Schema

```sql
CREATE TABLE exam_results (
    student_id INT,
    subject VARCHAR(50),
    score INT
);
```

### Question

For each subject, find the student(s) with the highest score.

Return:

* student_id
* subject
* score

WITH t AS (
SELECT 
    student_id ,
    subject , score ,
    RANK() OVER (PARTITION BY subject ORDER BY score DESC) AS highest_score 
FROM exam_results)

SELECT * 
FROM t
WHERE highest_score = 1

#=====================================
#=====================================
---

# Running Total Problem

### Schema

```sql
CREATE TABLE daily_orders (
    order_date DATE,
    order_amount INT
);
```

### Question

Calculate the cumulative sales amount over time.

Return:

* order_date
* order_amount
* running_total

Sort by order_date ascending.

SELECT 
    order_date ,
    order_amount ,
    SUM(order_amount) OVER(ORDER BY order_date ASC) AS running_total
FROM daily_orders 
ORDER BY order_date ASC 


#===============================
#===============================
---

# Percentage of Total Problem

### Schema

```sql
CREATE TABLE sales (
    sale_id INT,
    category VARCHAR(50),
    amount INT
);
```

### Question

Calculate what percentage each category contributes to total sales.

Return:

* category
* total_sales
* percentage_of_total


WITH t AS(
SELECT 
    category ,
    SUM(amount) AS total_sales
    sale_id 
FROM sales 
GROUP BY category 
)
SELECT 
      category ,
      total_sales ,
      total_sales *100.0 / 
      SUM(total_sales) OVER() AS percentage_of_total

FROM t

#===============================
#===============================

CREATE TABLE users (
    user_id INT,
    email VARCHAR(100)
);

Find duplicated emails.

SELECT 
    email ,
    COUNT(*) AS duplicate_count
FROM users
GROUP BY email
#--------------------------
#--------------------------

Find users who logged in
more than once on the same day.

SELECT
    user_id,
    login_date,
    COUNT(*) AS login_count
FROM users
GROUP BY
    user_id,
    login_date
HAVING COUNT(*) > 1 

#---------------------------
#---------------------------
Find customers who 
purchased the same product more than once.

SELECT 
      customer_id ,
      product_id ,
      COUNT(*) AS purchase_count
FROM orders
GROUP BY customer_id , product_id
HAVING COUNT(*) > 1
-----------------------------------

CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    amount DECIMAL(10,2)
);

SOLUTION A /

SELECT 
    order_id ,
    customer_id ,
    order_date ,
    AVG(amount) AS avg_amount 
FROM orders 
GROUP BY customer_id 

-----

SOLUTION B /

WITH T AS(

SELECT 
    order_id ,
    customer_id ,
    order_date ,
    LAG(order_date) OVER(
    PARTITION BY customer_id 
    ORDER BY order_date) AS prev_1
FROM orders 
)
SELECT 
    customer_id ,
    AVG(DATEDIFF(day,order_date,prev1)) AS avg_orders_per_customer
FROM T
WHERE prev_1 IS NOT NULL
GROUP BY customer_id

#---------------------------------------
#---------------------------------------
#26/6/26

---

# Problem 1 — Running Total

### Schema

```sql
CREATE TABLE payments (
    payment_id INT,
    payment_date DATE,
    amount DECIMAL(10,2)
);
```

### Question

Calculate the cumulative payment amount by payment date.

Return:

* payment_date
* amount
* running_total

Sort by payment_date ascending.

SELECT 
     payment_date ,
     amount ,
     SUM(amount) OVER(ORDER BY payment_date ASC) AS running_total
FROM payments 
ORDER BY payment_date ASC

#----------------------------------------------------


# Problem 2 — Running Average

### Schema

```sql
CREATE TABLE daily_sales (
    sale_date DATE,
    sales_amount DECIMAL(10,2)
);
```

### Question

Calculate the running average of sales over time.

Return:

* sale_date
* sales_amount
* running_avg

SELECT 
    sale_date ,
    sale_amount ,
    AVG(amount) OVER(ORDER BY sale_date ASC) AS running_avg
FROM daily_sales


#-----------------------------------------------------

# Problem 3 — Consecutive Days

### Schema

```sql
CREATE TABLE logins (
    user_id INT,
    login_date DATE
);
```

### Question

Find users who logged in on **4 consecutive days**.

Return:

* user_id
WITH T AS (
SELECT 
    user_id ,
    login_date ,
    LAG(login_date , 1) OVER(PARTITION BY user_id ORDER BY login_date ASC) AS prev_1 ,
    LAG(login_date , 2) OVER(PARTITION BY user_id ORDER BY login_date ASC) AS prev_2 ,
    LAG(login_date , 3) OVER(PARTITION BY user_id ORDER BY login_date ASC) AS prev_3
FROM logins     
)
SELECT 
    user_id 
FROM T 
WHERE DATEDIFF(day, prev_1,login_date) = 1
AND DATEDIFF(day, prev_2,prev_1) = 1
AND DATEDIFF(day, prev_3 , prev_2) = 1
AND prev_1 IS NOT NULL

#-------------------------------------------------------

# Problem 4 — Consecutive Purchases

### Schema

```sql
CREATE TABLE purchases (
    purchase_id INT,
    customer_id INT,
    purchase_date DATE
);
```

### Question

Find customers who made purchases on **at least 3 consecutive days**.

Return:

* customer_id

WITH T AS(
SELECT 
     customer_id ,
     purchase_id ,
     purchase_date ,
     LAG(purchase_date , 1) OVER (PARTITION BY customer_id ORDER BY purchase_date ASC) AS prev1 , 
     LAG(purchase_date , 2) OVER (PARTITION BY customer_id ORDER BY purchase_date ASC) AS prev2 
FROM purchases 
)
SELECT 
    customer_id 
FROM T
WHERE DATEDIFF(day,prev1,purchase_date) = 1
AND DATEDIFF(day,prev2,prev1) = 1
AND prev1 IS NOT NULL
GROUP BY customer_id 

#--------------------------------------------------------------

# Problem 5 — Ranking

### Schema

```sql
CREATE TABLE employees (
    emp_id INT,
    department VARCHAR(50),
    salary INT
);
```

### Question

Find the employee with the **second highest salary** in each department.

Return:

* emp_id
* department
* salary
WITH T AS( 
SELECT 
    emp_id ,
    department ,
    salary ,
    RANK() OVER(PARTITION BY department ORDER BY salary DESC) AS sec_salary
FROM employees
)
SELECT 
    emp_id ,
    department ,
    salary
FROM T 
WHERE sec_salary = 2

#-------------------------------------------------

# Problem 6 — Ranking

### Schema

```sql
CREATE TABLE products (
    product_id INT,
    category VARCHAR(50),
    revenue DECIMAL(10,2)
);
```

### Question

Return the **top 3 products** by revenue within each category.

Return:

* category
* product_id
* revenue

WITH T AS(
SELECT
    product_id ,
    category ,
    revenue ,
    RANK() OVER(PARTITION BY category ORDER BY revenue DESC) AS top3
FROM products     
)
SELECT 
    category ,
    product_id ,
    revenue
FROM T
WHERE top3 <=3
#-------------------------------------------------------

# Problem 7 — Percentage of Total

### Schema

```sql
CREATE TABLE sales (
    category VARCHAR(50),
    amount DECIMAL(10,2)
);
```

### Question

Calculate the percentage contribution of each category to total revenue.

Return:

* category
* total_sales
* percentage_of_total

WITH T AS(
SELECT 
    category ,
    SUM(amount) AS total_sales 
FROM sales 
GROUP BY category  
)
SELECT 
    category ,
    total_sales ,
    total_sales *100.0/ SUM(total_sales)OVER() AS percentage_of_total
FROM T


#------------------------------------------------------------

# Problem 8 — Percentage داخل كل Group

### Schema

```sql
CREATE TABLE sales (
    region VARCHAR(30),
    category VARCHAR(30),
    amount DECIMAL(10,2)
);
```

### Question

Calculate what percentage each category contributes **within its region**.

Return:

* region
* category
* total_sales
* percentage_of_region_sales

WITH T AS (
SELECT 
    region ,
    category ,
    SUM(amount) AS total_sales 
FROM sales 
GROUP BY category , region

)
SELECT 
   region ,
   category ,
   total_sales ,
   total_sales * 100.00  / SUM(total_sales)OVER(PARTITION BY region) AS percentage_of_region_sales
FROM T
GROUP BY category

#-------------------------------------------------------------

# Problem 9 — Top Product Per Month

### Schema

```sql
CREATE TABLE sales (
    product_id INT,
    quantity INT,
    sale_date DATE
);
```

### Question

Find the **top-selling product** for every month.

Return:

* month
* product_id
* total_quantity

WITH T AS(
SELECT 
   product_id ,
   MONTH(sale_date) AS month,
   SUM(quantity) AS total_quantity   
FROM sales 
GROUP BY MONTH(sale_date) ,product_id
), R AS(
SELECT  
   * ,
    ROW_NUMBER() OVER (PARTITION BY month 
                    ORDER BY total_quantity DESC) AS top_product
FROM T
)
SELECT 
   month ,
   product_id ,
   total_quantity
FROM R 
WHERE top_product = 1

#-----------------------------------------------------------------

# Problem 10 — Top 2 Products Per Month

### Schema

```sql
CREATE TABLE sales (
    product_id INT,
    quantity INT,
    sale_date DATE
);
```

### Question

Return the **top two selling products** in every month.

Return:

* month
* product_id
* total_quantity

WITH T AS(
SELECT 
   product_id ,
   MONTH(sale_date) AS month,
   SUM(quantity) AS total_quantity   
FROM sales 
GROUP BY MONTH(sale_date) AS month ,product_id
), R AS(
SELECT  
   * ,
    DENSE_RANK() OVER (PARTITION BY month 
                    ORDER BY total_quantity DESC) AS top_product
FROM T
)
SELECT 
   month ,
   product_id ,
   total_quantity
FROM R 
WHERE top_product <= 2

#-----------------------------------------------------------------

# Problem 11 — Duplicate Records

### Schema

```sql
CREATE TABLE transactions (
    transaction_id INT,
    user_id INT,
    transaction_date D2)
);
```
ATE,
    amount DECIMAL(10,
### Question

Find duplicated transactions based on:

* user_id
* transaction_date
* amount

Return:

* user_id
* transaction_date
* amount
* duplicate_count

SELECT 
    transaction_date ,
    user_id ,
    amount,
    COUNT(*) AS duplicat_count
FROM transactions
GROUP BY user_id , transaction_date ,amount
HAVING COUNT(*) > 1

#========================================

# Problem 12 — Duplicate Emails

### Schema

```sql
CREATE TABLE users (
    user_id INT,
    email VARCHAR(100)
);
```

### Question

Find emails used by more than one user.

Return:

* email
* duplicate_count

SELECT 
    email,
    COUNT(*) AS duplicate_count
FROM users
GROUP BY email 
HAVING COUNT(*) > 1

#=================================== 
# Problem 13 — Average Time Between Orders

### Schema

```sql
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE
);
```

### Question

Calculate the average number of days between consecutive orders for each customer.

Return:

* customer_id
* avg_days_between_orders

WITH T AS(

SELECT 
   order_id ,
   customer_id ,
   order_date ,
   LAG(order_date) OVER(PARTITION BY customer_id 
                        ORDER BY order_date ASC) AS prev1
FROM orders 
)

SELECT 
   customer_id ,
   AVG(DATEDIFF(day,prev1,order_date)) AS avg_days_between_orders
FROM T
WHERE prev1 IS NOT NULL
GROUP BY customer_id

#--------------------------------------------
# Problem 14 — First & Last Order

### Schema

```sql
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE
);
```

### Question

Return each customer's:

* first_order_date
* last_order_date
* days_between_first_and_last_order

WITH T AS(

SELECT 
   order_id ,
   customer_id ,
   order_date ,
   MIN(order_date) AS first_order_date ,
   MAX(order_date) AS last_order_date
FROM orders 
GROUP BY customer_id
)
SELECT 
   first_order_date ,
   last_order_date ,
   DATEDIFF(day, last_order_date , first_order_date) AS days_btw_first_and_last_order
FROM T

#-------------------------------------------
# Problem 15 — Window Aggregate

### Schema

```sql
CREATE TABLE employees (
    emp_id INT,
    department VARCHAR(50),
    salary INT
);
```

### Question $$$$$$$$$$$$$$$$$$$$$$$$$$$

For every employee, show:

* emp_id
* department
* salary
* department_average_salary


WITH T AS(

SELECT 
   emp_id ,
   department ,
   salary ,
   AVG(salary)OVER(PARTITION BY emp_id , department 
                   ORDER BY salary DESC) AS department_avg_salary
FROM employees )
#------------------------------------

# Problem 16 — Above Department Average

### Schema

```sql
CREATE TABLE employees (
    emp_id INT,
    department VARCHAR(50),
    salary INT
);
```

### Question

Return employees whose salary is **greater than the average salary of their department**.

Return:

* emp_id
* department
* salary

SELECT 
    emp_id ,
    department ,
    salary 
FROM employees 
GROUP BY emp_id 
HAVING salary > (
                SELECT 
                    AVG(salary) AS avg_salary
                FROM employees
                GROUP BY department

                ) 

#----------------------------------------

# Problem 17 — Previous Order

### Schema

```sql
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE
);
```

### Question

For every order, return:

* order_id
* customer_id
* order_date
* previous_order_date

WITH T AS (

SELECT 
   order_id ,
   customer_id ,
   order_date,
   LAG(order_date)OVER(PARTITION BY order_id ORDER BY order_date ASC) AS previous_order_date
FROM orders 
GROUP BY customer_id
) 

SELECT 
   order_id,
   customer_id ,
   order_id,
   order_date ,
   previous_order_date
FROM T 

#--------------------------------------

# Problem 18 — Days Since Previous Order

### Schema

```sql
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    order_date DATE
);
```

### Question

For every order, calculate the number of days since the customer's previous order.

Return:

* customer_id
* order_date
* days_since_previous_order

WITH T AS(
SELECT 
    order_id ,
    customer_id ,
    order_date,
    LAG(order_date) OVER(PARTITION BY customer_id ORDER BY order_date ASC) AS prev1
FROM orders
)
SELECT  
   customer_id ,
   order_date ,
   DATEDIFF(day,prev1,order_date) AS days_since_previous_order

FROM T 
WHERE prev1 IS NOT NULL;







| لو شوفتي في السؤال...      | فكري في...                                 |
| -------------------------- | ------------------------------------------ |
| Running total / cumulative | `SUM() OVER(ORDER BY ...)`                 |
| Running average            | `AVG() OVER(ORDER BY ...)`                 |
| Top N per group            | `ROW_NUMBER()` / `RANK()` + `PARTITION BY` |
| Percentage of total        | `SUM() OVER()`                             |
| Percentage داخل كل قسم     | `SUM() OVER(PARTITION BY ...)`             |
| Previous row               | `LAG()`                                    |
| Next row                   | `LEAD()`                                   |
| Consecutive days           | `LAG()` أو Pattern الـ Gaps & Islands      |
| Department average         | `AVG() OVER(PARTITION BY ...)`             |
| Duplicates                 | `GROUP BY` + `HAVING COUNT(*) > 1`         |


"""
