import sqlite3
import pandas as pd

conn = sqlite3.connect('data.sqlite')

# =========================
# STEP 1: Join + Filter
# =========================
df_boston = pd.read_sql("""
SELECT c.contactFirstName AS firstName,
       c.contactLastName AS lastName
FROM customers c
JOIN employees e
ON c.salesRepEmployeeNumber = e.employeeNumber
WHERE c.city = 'Boston'
""", conn)

df_zero_emp = pd.read_sql("""
SELECT e.*
FROM employees e
LEFT JOIN customers c
ON e.employeeNumber = c.salesRepEmployeeNumber
WHERE c.customerNumber IS NULL
""", conn)


# =========================
# STEP 2: Type of Join
# =========================
df_employee = pd.read_sql("""
SELECT e.firstName,
       e.lastName,
       e.jobTitle,
       o.city
FROM employees e
JOIN offices o
ON e.officeCode = o.officeCode
""", conn)

df_contacts = pd.read_sql("""
SELECT customerName,
       contactFirstName,
       contactLastName,
       phone
FROM customers
""", conn)


# =========================
# STEP 3: Built-in Function
# =========================
df_payment = pd.read_sql("""
SELECT c.customerName,
       c.contactFirstName,
       p.paymentDate,
       CAST(p.amount AS REAL) AS amount
FROM payments p
JOIN customers c
ON p.customerNumber = c.customerNumber
""", conn)


# =========================
# STEP 4: Joining + Grouping
# =========================
df_credit = pd.read_sql("""
SELECT e.firstName,
       e.lastName,
       c.creditLimit
FROM customers c
JOIN employees e
ON c.salesRepEmployeeNumber = e.employeeNumber
WHERE c.creditLimit > 100000
""", conn)


df_product_sold = pd.read_sql("""
SELECT p.productCode,
       p.productName,
       SUM(od.quantityOrdered) AS totalunits
FROM products p
JOIN orderdetails od
ON p.productCode = od.productCode
GROUP BY p.productCode, p.productName
""", conn)


# =========================
# STEP 5: Multiple Joins
# =========================
df_total_customers = pd.read_sql("""
SELECT e.firstName,
       e.lastName,
       COUNT(c.customerNumber) AS numpurchasers
FROM employees e
LEFT JOIN customers c
ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber
""", conn)


df_customers = pd.read_sql("""
SELECT e.firstName,
       COUNT(c.customerNumber) AS n_customers
FROM employees e
LEFT JOIN customers c
ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber
""", conn)


# =========================
# STEP 6: Subquery
# =========================
df_under_20 = pd.read_sql("""
SELECT c.contactFirstName AS firstName,
       c.contactLastName AS lastName,
       c.creditLimit,
       COUNT(p.checkNumber) AS num_payments,
       SUM(p.amount) AS total_spent
FROM customers c
JOIN payments p
ON c.customerNumber = p.customerNumber
GROUP BY c.customerNumber
HAVING SUM(p.amount) < 20000
""", conn)

conn.close()