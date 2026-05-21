# =========================
# EXPLORATION QUERIES
# =========================


PREVIEW_DATA = """
SELECT *
FROM retail
LIMIT 5;
"""


TOTAL_ROWS = """
SELECT COUNT(*) AS TotalRows
FROM retail;
"""


TABLE_SCHEMA = """
PRAGMA table_info(retail);
"""


UNIQUE_COUNTRIES = """
SELECT DISTINCT Country
FROM retail
ORDER BY Country;
"""

# =========================
# KPI QUERIES
# =========================


TOTAL_REVENUE = """
SELECT
    ROUND(SUM(Revenue), 2) AS TotalRevenue
FROM retail;
"""


TOTAL_ORDERS = """
SELECT
    COUNT(DISTINCT InvoiceNo) AS TotalOrders
FROM retail;
"""


TOTAL_CUSTOMERS = """
SELECT
    COUNT(DISTINCT CustomerID) AS TotalCustomers
FROM retail
WHERE CustomerID IS NOT NULL;
"""


AVERAGE_ORDER_VALUE = """
SELECT
    ROUND(
        SUM(Revenue) / COUNT(DISTINCT InvoiceNo),
        2
    ) AS AverageOrderValue
FROM retail;
"""

AVERAGE_REVENUE_PER_CUSTOMER = """
SELECT
    ROUND(
        SUM(Revenue) / COUNT(DISTINCT CustomerID),
        2
    ) AS AverageRevenuePerCustomer
FROM retail
WHERE CustomerID IS NOT NULL;
"""


# =========================
# REVENUE ANALYTICS
# =========================


REVENUE_BY_COUNTRY = """
SELECT
    Country,
    ROUND(SUM(Revenue), 2) AS TotalRevenue
FROM retail
GROUP BY Country
ORDER BY TotalRevenue DESC
LIMIT 10;
"""


MONTHLY_REVENUE = """
SELECT
    Year,
    Month,
    ROUND(SUM(Revenue), 2) AS MonthlyRevenue
FROM retail
GROUP BY Year, Month
ORDER BY Year, Month;
"""


REVENUE_BY_WEEKDAY = """
SELECT
    Weekday,
    ROUND(SUM(Revenue), 2) AS TotalRevenue
FROM retail
GROUP BY Weekday
ORDER BY TotalRevenue DESC;
"""


TOP_REVENUE_INVOICES = """
SELECT
    InvoiceNo,
    ROUND(SUM(Revenue), 2) AS InvoiceRevenue
FROM retail
GROUP BY InvoiceNo
ORDER BY InvoiceRevenue DESC
LIMIT 10;
"""


# =========================
# PRODUCT ANALYTICS
# =========================


TOP_PRODUCTS_BY_QUANTITY = """
SELECT
    Description,
    SUM(Quantity) AS TotalQuantitySold
FROM retail
WHERE Quantity > 0
GROUP BY Description
ORDER BY TotalQuantitySold DESC
LIMIT 10;
"""


TOP_PRODUCTS_BY_REVENUE = """
SELECT
    Description,
    ROUND(SUM(Revenue), 2) AS TotalRevenue
FROM retail
GROUP BY Description
ORDER BY TotalRevenue DESC
LIMIT 10;
"""


MOST_FREQUENTLY_PURCHASED_PRODUCTS = """
SELECT
    Description,
    COUNT(DISTINCT InvoiceNo) AS PurchaseFrequency
FROM retail
GROUP BY Description
ORDER BY PurchaseFrequency DESC
LIMIT 10;
"""


AVERAGE_PRODUCT_PRICE = """
SELECT
    Description,
    ROUND(AVG(UnitPrice), 2) AS AveragePrice
FROM retail
WHERE UnitPrice > 0
GROUP BY Description
ORDER BY AveragePrice DESC
LIMIT 10;
"""


# =========================
# CUSTOMER ANALYTICS
# =========================


TOP_CUSTOMERS_BY_REVENUE = """
SELECT
    CustomerID,
    ROUND(SUM(Revenue), 2) AS TotalSpent
FROM retail
WHERE CustomerID IS NOT NULL
GROUP BY CustomerID
ORDER BY TotalSpent DESC
LIMIT 10;
"""


MOST_FREQUENT_CUSTOMERS = """
SELECT
    CustomerID,
    COUNT(DISTINCT InvoiceNo) AS TotalOrders
FROM retail
WHERE CustomerID IS NOT NULL
GROUP BY CustomerID
ORDER BY TotalOrders DESC
LIMIT 10;
"""


AVERAGE_CUSTOMER_SPEND = """
SELECT
    CustomerID,
    ROUND(AVG(Revenue), 2) AS AverageSpend
FROM retail
WHERE CustomerID IS NOT NULL
GROUP BY CustomerID
ORDER BY AverageSpend DESC
LIMIT 10;
"""


CUSTOMER_COUNTRY_DISTRIBUTION = """
SELECT
    Country,
    COUNT(DISTINCT CustomerID) AS TotalCustomers
FROM retail
WHERE CustomerID IS NOT NULL
GROUP BY Country
ORDER BY TotalCustomers DESC;
"""







MONTHLY_ORDER_VOLUME = """
SELECT
    Year,
    Month,
    COUNT(DISTINCT InvoiceNo) AS TotalOrders
FROM retail
GROUP BY Year, Month
ORDER BY Year, Month;
"""

TOP_COUNTRIES_BY_CUSTOMERS = """
SELECT
    Country,
    COUNT(DISTINCT CustomerID) AS TotalCustomers
FROM retail
WHERE CustomerID IS NOT NULL
GROUP BY Country
ORDER BY TotalCustomers DESC
LIMIT 10;
"""


