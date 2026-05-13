

#top 5 Employees

#Solution 1 by row_number window function 
'''
WITH TOP_EMPLOYEES AS(
SELECT emplyee_id , amount ,
ROW_NUMBER() OVER(
ORDER BY amount DESC ) AS top_five_employees
FROM Sales 
)
SELECT * FROM TOP_EMPLOYEES
WHERE top_five_employees <=5
'''

#----------------------------

#Solution 2 by DENSE_RANK window function 

'''
WITH TOP_EMPS AS(

SELECT employee_id , amount ,
DENSE_RANK() OVER( 
ORDER BY amount DESC) AS rnk
FROM Sales 
)
SELECT * FROM TOP_EMPS 
WHERE rnk <= 5
'''

#------------------------------
#------------------------------

#2. Monthly Trends (Date Functions)

'''
SELECT DATE_TRUNC('month' , order_date) AS month ,
YEAR(order_date) AS year , total_price 
FROM Orders 
WHERE year = '2025'
GROUP BY month 
ORDER BY total_price DESC 
'''

#------------------------------
#------------------------------

#3. Filtering with Aggregation (HAVING)

'''
SELECT customer_id , COUNT(order_id) AS num_orders 
FROM Orders 
GROUP BY customer_id
HAVING COUNT(order_id) > 10

'''

#------------------------------
#------------------------------

#4. Joins and NULLs

'''
SELECT e.employee_id , d.department_name 
FROM Employees e
LEFT JOIN Departments d
ON e.employee_id = d.employee_id

'''

#------------------------------
#------------------------------

#5. Distinct Counts

'''
SELECT visitor_id ,COUNT(DISTINCT visitor_id) AS unique_visitors
FROM Web_Visits
'''


#6
'''
SELECT product_id , category , price , 
CASE 
WHEN price > 100 THEN 'Premium
ELSE 'Economy' END AS Price_Category
FROM Products 
'''
#-----------------------------

#7 , 8 , 9 , 10 without schema

#===============================
#===============================

"""
Schema:

Users (user_id, username, email, signup_date)

Products (product_id, product_name, price, category)

Orders (order_id, user_id, product_id, order_date, amount)
"""

#6
'''
SELECT product_id ,price, 
CASE 
WHEN price > 100 THEN ' Premium 
WHEN price BETWEEN 50 AND 100 THEN 'Mid-Range'
ELSE 'Otherwise Budget' 
END
FROM Products 
'''

#--------------------------
#7
'''
SELECT u.user_id , u.username , SUM(o.amount) AS user_spending 
FROM Users u
LEFT JOIN Orders o 
ON u.user_id = o.user_id 
GROUP BY u.user_id 
HAVING SUM(o.amount) > (SELECT AVG(amount) AS avg_spending 
FROM Orders )

'''
#-------------------------

#8
#Users (user_id, username, email, signup_date)

'''
SELECT email, COUNT(email) AS num_of_emails
FROM Users 
GROUP BY email
HAVING COUNT(email) > 1
'''

#-------------------------

#9
#Products (product_id, product_name, price, category)
#Orders (order_id, user_id, product_id, order_date, amount)

'''
SELECT p.product_id , p.product_name , 
o.order_date
FROM Products p
JOIN Orders o
ON p.product_id = o.product_id
WHERE p.product_name LIKE '%Smart'
AND o.order_date >= DATE_SUB(CURDATE() - INTERVAL 30 DAY)
'''
#==================================
#==================================
#==================================

#Schema
'''
Customers: (customer_id, first_name, country, join_date)

Products: (product_id, product_name, category, price)

Orders: (order_id, customer_id, order_date, total_amount)

Order_Items: (order_id, product_id, quantity)
'''

#1. The Customer Lifetime Value (Aggregation)
'''
SELECT c.customer_id , c.first_name , SUM(o.total_amount) AS all_spending
FROM Customers c 
LEFT JOIN Orders o
ON c.customer_id = o.customer_id 
GROUP BY c.customer_id 
'''

#----------------------------

#2 Monthly Sales Trends (Date Functions)
#Orders: (order_id, customer_id, order_date, total_amount)

'''
SELECT SUM(total_amount) AS total_revenue , DATE_TRUNC('month',order_date) AS month ,
DATE_TRUNC('year',order_date) AS year 
FROM Orders 
GROUP BY month , year 
'''
#----------------------------
#3 Top Spenders (Top N / Sorting)
#Orders: (order_id, customer_id, order_date, total_amount)
#Customers: (customer_id, first_name, country, join_date)

'''
WITH TOP_CUSTOMERS AS (

SELECT c.customer_id , c.first_name , SUM(o.total_amount) AS total_revenue , 
DATE_TRUNC('year',o.order_date) AS year 
FROM Customers c 
JOIN Orders o
ON c.customers_id = o.customers_id 
WHERE DATE_TRUNC('year',o.order_date) = '2025'
GROUP BY year 

) ,
t AS(
SELECT DENSE_RANK() OVER (ORDER BY total_revenue DESC) AS TOP_THREE_CUSTOMERS
FROM TOP_CUSTOMERS 
)

SELECT TOP_THREE_CUSTOMERS 
FROM t 
WHERE TOP_THREE_CUSTOMERS <= 3

'''
#----------------------------
#4 The Non-Matching Records (Left Join & NULL)
#Customers: (customer_id, first_name, country, join_date)
#Orders: (order_id, customer_id, order_date, total_amount)

'''
SELECT c.customers_id , c.first_name , o.order_id 
FROM Customers c
LEFT JOIN Orders o 
ON c.customer_id = o.customer_id 
WHERE o.order_id IS NULL 
'''
#----------------------------
#5 Categorizing Data (CASE WHEN)
#Orders: (order_id, customer_id, order_date, total_amount)
#لما يقولى كريت اكولمن المفروض دى كدا وندو فانكشن صح !!
'''
SELECT total_amount , CASE
WHEN total_amount > 500 THEN 'High_Value' 
WHEN total_amount BETWEEN 200 AND 500 THEN 'Medium_Value'
ELSE 'Low_Value' END AS Order_Category 
FROM Orders 
'''

#-------------------------------
#6 Aggregating Across Tables (JOIN & GROUP BY)
#Order_Items: (order_id, product_id, quantity)
#Products: (product_id, product_name, category, price)

'''
SELECT p.category, COUNT(DISTINCT o.quantity) AS total_sold_quantities 
FROM Products p
RIGHT JOIN Order_Items o
ON o.product_id = p.product_id
GROUP BY p.category
'''
#--------------------------------
#7
#Orders: (order_id, customer_id, order_date, total_amount)
'''
SELECT order_id , total_amount , customer_id ,order_date
FROM Orders 
GROUP BY order_id 
HAVING total_amount > (SELECT order_id ,AVG(total_amount) AS AVG_ALL FROM Orders )
'''
#--------------------------------
#8
#Orders: (order_id, customer_id, order_date, total_amount)
'''
SELECT customer_id , COUNT(DISTINCT order_id) AS num_orders 
FROM Orders 
GROUP BY customer_id 
HAVING COUNT(order_id) > 5
'''
#--------------------------------
#9
#Products: (product_id, product_name, category, price)

'''
SELECT product_id , product_name , category 
FROM Products 
WHERE category = 'Electonics'
AND product_name LIKE 'S%'
'''
#---------------------------------
#10
#Orders: (order_id, customer_id, order_date, total_amount)
'''
SELECT customer_id , COUNT(order_id) , order_date
FROM Orders 
GROUP BY order_date 
HAVING COUNT(order_id) > 1
'''
#====================================
#====================================
#====================================
#====================================
#====================================
#====================================

"""
--- SCHEMA ---
Departments: (department_id, department_name, location) 
Employees: (employee_id, first_name, last_name, department_id, salary, hire_date) 
Projects: (project_id, project_name, budget)
Employee_Projects: (employee_id, project_id, hours_worked)

"""
#1 Department Highest Salary (Window Functions)
#Employees: (employee_id, first_name, last_name, department_id, salary, hire_date)

'''
WITH TOP_EMPLOYEES AS(

SELECT employee_id , first_name , last_name , department_id , salary ,
ROW_NUMBER() OVER(PARTITION BY department_id 
ORDER BY salary DESC) AS TOP_EMP
FROM Employees 
)
SELECT * FROM TOP_EMPLOYEES
WHERE TOP_EMP = 1
'''

#-------------------------------
#2. Employees Hired in the Last Year (Date Functions)
#Employees: (employee_id, first_name, last_name, department_id, salary, hire_date)

'''
SELECT employee_id , first_name , last_name , hire_date
FROM Employees 
WHERE EXTRACT(YEAR FROM hire_date) >= '2025'
'''
#------------------------------
#3. Departments with High Headcount (Filtering with Aggregation)
#Departments: (department_id, department_name, location) 
#Employees: (employee_id, first_name, last_name, department_id, salary, hire_date)

'''
SELECT d.department_id , d.department_name , COUNT(e.employee_id) AS num_emp
FROM Departments d
LEFT JOIN Employees e
ON d.department_id = e.department_id 
GROUP BY d.department_id , d.department_name
HAVING COUNT(e.employee_id) > 10
'''
#------------------------------
#4. The Non-Matching Records (Anti-Join)
#Employees: (employee_id, first_name, last_name, department_id, salary, hire_date)
#Employee_Projects: (employee_id, project_id, hours_worked)

'''
SELECT e.employee_id , e.first_name , e.last_name , p.project_id
FROM Employees e
LEFT JOIN Employee_Projects p
ON e.employee_id = p.employee_id
WHERE p.project_id IS NULL 
'''

#------------------------------
#5. Total Salary Expense (Aggregation Across Tables)
#Departments: (department_id, department_name, location) 
#Employees: (employee_id, first_name, last_name, department_id, salary, hire_date)

'''
SELECT d.department_id , d.department_name , SUM(e.salary) AS total_salaries
FROM Departments d
LEFT JOIN Employees e
ON d.department_id = e.department_id
GROUP BY d.department_id , d.department_name 
'''
#-------------------------------
# 6. Nth Highest Salary (Subquery/Window Function)
#Employees: (employee_id, first_name, last_name, department_id, salary, hire_date) 

'''
WITH TOP_SECOND_SALARY AS(

SELECT 
    SUM(salary) AS total_salaries ,
    ROW_NUMBER() OVER(ORDER BY salary DESC) AS highest_sec_salary
FROM Employees

)

SELECT * FROM TOP_SECOND_SALARY
WHERE highest_sec_salary = 2
'''
#-------------------------------
#7. Categorizing Salary (CASE WHEN)
#Employees: (employee_id, first_name, last_name, department_id, salary, hire_date) 

'''
SELECT 
    employee_id , first_name , last_name , salary ,
    CASE 
        WHEN salary > 100000 THEN 'Senior' 
        WHEN salary BETWEEN 50000 AND 100000 THEN 'Mid-Level'
        ELSE 'Junior' 
    END AS Salary_Level 
FROM Employees 
'''
#--------------------------------
#8.Employees Earning More Than the Department Average (Correlated Subquery)
#Employees: (employee_id, first_name, last_name, department_id, salary, hire_date) 

'''
SELECT employee_id , first_name , last_name , salary
FROM Employees 
GROUP BY employee_id , first_name , last_name
HAVING salary > (SELECT AVG(salary) FROM Employees)

'''
#--------------------------------
#9. String Manipulation (Pattern Matching)
#Employees: (employee_id, first_name, last_name, department_id, salary, hire_date) 

'''
SELECT employee_id , first_name , last_name , salary 
FROM Employees 
WHERE first_name LIKE 'A%' 
AND salary > 60000 

'''
#--------------------------------
#10. Finding Duplicates (Group By / Having)
#Employees: (employee_id, first_name, last_name, department_id, salary, hire_date) 

'''
SELECT last_name , COUNT(last_name) AS nums_lastName
FROM Employees
GROUP BY last_name 
HAVING COUNT(last_name) > 1

'''
#=================================
#=================================
#=================================
#=================================
#=================================
#=================================
#1
"""
customers(customer_id, name)
orders(order_id, customer_id, order_date, amount)
Write a query to find the top 3 customers who spent the most money overall.
"""
'''
WITH TOP_CUST AS(
SELECT customer_id , order_id , amount,
ROW_NUMBER() OVER(ORDER BY amount DESC) AS TOP_THREE
FROM orders
)
SELECT * FROM TOP_CUST
WHERE TOP_THREE <=3
'''
#-------------------------------
#2
"""
orders(order_id, order_date, amount)
Return total revenue per month ordered chronologically.
"""
'''
SELECT SUM(amount) AS total_revenue , DATE_TRUNC('month',order_date) AS month
FROM orders 
GROUP BY DATE_TRUNC('month',order_date) 

'''
#-------------------------------
#3
"""
customers(customer_id, name)
orders(order_id, customer_id)
Find all customers who never placed any order.
"""
'''
SELECT c.customer_id , c.name
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id 
WHERE o.order_id IS NULL
'''

#---------------------------------
#4
"""
employees(employee_id, name, salary)
Get the second highest salary in the company.
"""
'''
WITH HIGH_SEC AS (
SELECT employee_id , name , salary ,
DENSE_RANK() OVER(ORDER BY salary DESC) AS top_sec
FROM employees 
)
SELECT * FROM HIGH_SEC
WHERE top_sec = 2
'''

#---------------------------------
#5

"""
logins(user_id, login_date)
Count how many unique users logged in each day.
"""
'''
SELECT COUNT(DISTINCT user_id) AS num_of_users , DATE_TRUNC('day',login_date) AS day
FROM logins 
GROUP BY DATE_TRUNC('day',login_date) 
'''
#--------------------------------
#6
"""
orders(order_id, customer_id)
customers(customer_id)
Find orders that have a customer_id that does not exist in customers table
"""
'''
SELECT o.order_id 
FROM orders o
LEFT JOIN customers c 
ON c.customer_id = o.customer_id 
WHERE o.customer_id NOT EXIST IN customers c

'''

#--------------------------------
#7 
"""
sales(sale_id, sale_date, amount)
Calculate a running total of sales over time ordered by date.
"""
'''
SELECT 
    SUM(amount) OVER(
    ORDER BY sale_date ASC
    ROWS BETWEEN UNBOUNDED PRECEDING CURRENT ROW) AS running_total
FROM sales 
'''
#--------------------------------
#8
"""
order_items(order_id, product_id, quantity)
products(product_id, product_name)
Find the most purchased product by total quantity.
"""
### SOLUTION A
'''
SELECT 
    o.order_id , o.product_id , SUM(o.quantity) AS TOT, p.product_name
FROM order_items o
JOIN products p
    ON o.product_id = p.product_id 
GROUP BY p.product_id , p.product_name 
ORDER BY TOT DESC
LIMIT 1

'''
### SOLUTION B 

'''
WITH TOP_PRODUCT AS(
    SELECT o.order_id , o.product_id , p.product_name , SUM(o.quantity) AS total_quantities 
    FROM order_items o
    JOIN products p
        ON o.product_id = p.product_id
    GROUP BY p.product_id , p.product_name 
 ), T AS(
        SELECT product_id , product_name , total_quantities , 
               ROW_NUMBER() OVER(
                                PARTITION BY product_name 
        ORDER BY total_quantities DESC) AS TOP_ONE
        FROM TOP_PRODUCT)
SELECT * FROM T 
WHERE TOP_ONE = 1
'''
#-----------------------------
#9
"""
users(user_id, email)
Find emails that appear more than once.
"""
'''
SELECT user_id ,email
FROM users
GROUP BY email
HAVING COUNT(DISTINCT email) > 1
'''

#------------------------------
