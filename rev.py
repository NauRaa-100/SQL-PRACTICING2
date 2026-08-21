"""


### 1. Second Highest Salary

>  Write a SQL query to get the second highest salary from the `employee` table.
 If there is no second highest salary, then the query should return `null`.

> **Schema & Data:**
> ```sql
> CREATE TABLE employee (
>     id INT PRIMARY KEY,
>     salary INT
> );
> 
> INSERT INTO employee (id, salary) VALUES (1, 100), (2, 200), (3, 300);
> 
> ```

WITH T AS(
SELECT 
     id,
     salary,
     ROW_NUMBER() OVER(ORDER BY salary DESC) AS highest_sec
FROM Employee

)
SELECT * FROM T
WHERE CASE WHEN highest_sec = 2 THEN salary ELSE 'null' END

--------------------------------------------------------------------

### 2. Duplicate Emails

> Write a SQL query to find all duplicate emails in a table named `person`.

> **Schema & Data:**
> ```sql
> CREATE TABLE person (
>     id INT PRIMARY KEY,
>     email VARCHAR(255)
> );
> 
> INSERT INTO person (id, email) VALUES 
> (1, 'a@b.com'), 
> (2, 'c@d.com'), 
> (3, 'a@b.com');
> 
> ```

SELECT 
     id,
     email
FROM person 
GROUP BY email
HAVING COUNT(email)>1

------------------------------------------------------------------

### 3. Department Highest Salary

> Write a SQL query to find employees who have the highest salary
 in each of the departments.

> **Schema & Data:**
> ```sql
> CREATE TABLE department (
>     id INT PRIMARY KEY,
>     name VARCHAR(50)
> );
> 
> CREATE TABLE employee (
>     id INT PRIMARY KEY,
>     name VARCHAR(50),
>     salary INT,
>     department_id INT,
>     FOREIGN KEY (department_id) REFERENCES department(id)
> );

WITH T AS(
SELECT 
     e.id,
     e.name,
     e.salary,
     e.department_id
FROM employee e
JOIN department d
ON e.department_id = d.id
GROUP BY e.department_id     
), R AS(
SELECT 
     id,
     name,
     salary,
     department_id ,
     DENSE_RANK() OVER(PARTITION BY department_id ORDER BY salary DESC) AS highest_salary
FROM T 
)
SELECT * FROM R 
WHERE highest_salary =1

------------------------------------------------------------------

### 4. Who Has No Orders?

> Write a SQL query to report all customers who never order anything.

> **Schema & Data:**
> ```sql
> CREATE TABLE customers (
>     customer_id INT PRIMARY KEY,
>     name VARCHAR(50)
> );
> 
> CREATE TABLE orders (
>     order_id INT PRIMARY KEY,
>     customer_id INT,
>     FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
> );


SELECT 
     c.customer_id ,
     c.name
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id 
WHERE o.order_id IS NULL

-----------------------------------------------------------------

### 5. Cumulative Sum (Running Total)

> Write a SQL query to calculate a running total or cumulative sum of the `amount` 
column ordered by `sale_date`.

> **Schema & Data:**
> ```sql
> CREATE TABLE sales (
>     sale_date DATE,
>     amount INT
> );
> 
> INSERT INTO sales (sale_date, amount) VALUES 
> ('2026-01-01', 100), 
> ('2026-01-02', 150), 
> ('2026-01-03', 200);
> 
> ```

SELECT 
     sale_date,
     SUM(amount) OVER(ORDER BY sale_date ASC) AS runing_total
FROM sales


--------------------------------------------------------------

### 6. Consecutive Numbers

> Write a SQL query to find all numbers that appear 
at least three times consecutively in the `logs` table.

> **Schema & Data:**
> ```sql
> CREATE TABLE logs (
>     id INT PRIMARY KEY,
>     num INT
> );
> 
> INSERT INTO logs (id, num) VALUES 
> (1, 1), (2, 1), (3, 1), (4, 2), (5, 1), (6, 2), (7, 2);
> 
> ```
WITH T AS (
    SELECT
        id,
        num,
        LAG(num, 1) OVER (ORDER BY id) AS prev_1,
        LAG(num, 2) OVER (ORDER BY id) AS prev_2
    FROM logs
)
SELECT DISTINCT num
FROM T
WHERE num = prev_1
AND num = prev_2;

------------------------------------------------------------

### 7. Monthly Active Users (MAU)

> Write a SQL query to find the Monthly Active Users (MAU) for each month based on user logins.

> **Schema & Data:**
> ```sql
> CREATE TABLE user_logins (
>     user_id INT,
>     login_date DATE
> );
> 
> INSERT INTO user_logins (user_id, login_date) VALUES 
> (1, '2026-01-10'), 
> (1, '2026-01-15'), 
> (2, '2026-01-20'), 
> (1, '2026-02-05');
> 
> ```

SELECT 
     user_id ,
     DATE_FORMAT(login_date,'%m') AS month
FROM user_logins
GROUP BY DATE_FORMAT(login_date,'%m') 
HAVING  COUNT(DISTINCT user_id) > 1

-----------------------------------------------------------

### 8. Rank Scores

> Write a SQL query to rank scores. If there is a tie between two scores,
both should have the same ranking. Note that after a tie,
 the next ranking number should be the next consecutive integer value (Dense Rank).

> **Schema & Data:**
> ```sql
> CREATE TABLE scores (
>     id INT PRIMARY KEY,
>     score DECIMAL(3,2)
> );
> 
> INSERT INTO scores (id, score) VALUES 
> (1, 3.50), 
> (2, 3.65), 
> (3, 4.00), 
> (4, 3.85), 
> (5, 4.00), 
> (6, 3.65);
> 
> ```
WITH T AS(
SELECT 
     id,
     CAST(score AS INT) AS int_score,
FROM scores
),D AS(
SELECT 
     id ,
     int_score,
     DENSE_RANK()OVER(ORDER BY int_score DESC) AS rn
FROM T )
SELECT * FROM D

-------------------------------------------------------------

### 10. Self Join (Managers and Employees)

> Write a SQL query to find the employees who earn more than their managers.

> **Schema & Data:**
> ```sql
> CREATE TABLE employee (
>     id INT PRIMARY KEY,
>     name VARCHAR(50),
>     salary INT,
>     manager_id INT
> );
> 
> INSERT INTO employee (id, name, salary, manager_id) VALUES 
> (1, 'Joe', 70000, 3), 
> (2, 'Henry', 80000, 4), 
> (3, 'Sam', 60000, NULL), 
> (4, 'Max', 90000, NULL);
> 
> ```
> 
> 

SELECT 
     e.name,
     e.salary,
     e.manager_id AS employee_id,
     m.id,
     m.name,
     m.salary
FROM employee e
JOIN employee m
ON e.manager_id = m.id
WHERE e.salary > m.salary
"""
