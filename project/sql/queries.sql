-- ============================================================================
-- SQL PRACTICE QUERIES — Customer Orders, Revenue & Product Performance
-- Database: data/sales_data.db  (SQLite)
-- Schema:
--   customers(CustomerID, CustomerName, Region)
--   products(ProductID, Product, Category)
--   orders(OrderID, CustomerID, ProductID, OrderDate, ShipDate, ShipMode,
--          Quantity, UnitPrice, Discount, Sales, Profit, ShippingDays, ProfitMargin)
-- ============================================================================


-- ----------------------------------------------------------------------------
-- 1. SELECT / WHERE — basic filtering
-- All orders shipped by "Same Day" with Sales over $500
-- ----------------------------------------------------------------------------
SELECT OrderID, CustomerID, OrderDate, ShipMode, Sales
FROM orders
WHERE ShipMode = 'Same Day' AND Sales > 500
ORDER BY Sales DESC;


-- ----------------------------------------------------------------------------
-- 2. ORDER BY — top 10 highest-value orders
-- ----------------------------------------------------------------------------
SELECT OrderID, CustomerID, OrderDate, Sales, Profit
FROM orders
ORDER BY Sales DESC
LIMIT 10;


-- ----------------------------------------------------------------------------
-- 3. GROUP BY + Aggregate Functions — revenue and profit by region
-- ----------------------------------------------------------------------------
SELECT
    c.Region,
    COUNT(o.OrderID)          AS total_orders,
    SUM(o.Quantity)           AS total_units,
    ROUND(SUM(o.Sales), 2)    AS total_revenue,
    ROUND(SUM(o.Profit), 2)   AS total_profit,
    ROUND(AVG(o.Sales), 2)    AS avg_order_value
FROM orders o
JOIN customers c ON o.CustomerID = c.CustomerID
GROUP BY c.Region
ORDER BY total_revenue DESC;


-- ----------------------------------------------------------------------------
-- 4. GROUP BY + HAVING — product categories that generate over $500,000 revenue
-- ----------------------------------------------------------------------------
SELECT
    p.Category,
    ROUND(SUM(o.Sales), 2)  AS total_revenue,
    ROUND(SUM(o.Profit), 2) AS total_profit,
    COUNT(*)                AS orders_count
FROM orders o
JOIN products p ON o.ProductID = p.ProductID
GROUP BY p.Category
HAVING SUM(o.Sales) > 500000
ORDER BY total_revenue DESC;


-- ----------------------------------------------------------------------------
-- 5. INNER JOIN — orders with customer name and product name together
-- ----------------------------------------------------------------------------
SELECT
    o.OrderID,
    c.CustomerName,
    p.Product,
    p.Category,
    o.OrderDate,
    o.Sales
FROM orders o
INNER JOIN customers c ON o.CustomerID = c.CustomerID
INNER JOIN products  p ON o.ProductID  = p.ProductID
ORDER BY o.OrderDate DESC
LIMIT 20;


-- ----------------------------------------------------------------------------
-- 6. LEFT JOIN — every customer with their total spend (customers with
--    zero orders would still appear, shown as NULL/0)
-- ----------------------------------------------------------------------------
SELECT
    c.CustomerID,
    c.CustomerName,
    c.Region,
    COUNT(o.OrderID)              AS num_orders,
    COALESCE(SUM(o.Sales), 0)     AS lifetime_revenue
FROM customers c
LEFT JOIN orders o ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID, c.CustomerName, c.Region
ORDER BY lifetime_revenue DESC;


-- ----------------------------------------------------------------------------
-- 7. Product performance — best-selling products by revenue and margin
-- ----------------------------------------------------------------------------
SELECT
    p.Product,
    p.Category,
    SUM(o.Quantity)                                   AS units_sold,
    ROUND(SUM(o.Sales), 2)                            AS revenue,
    ROUND(SUM(o.Profit), 2)                           AS profit,
    ROUND(100.0 * SUM(o.Profit) / NULLIF(SUM(o.Sales), 0), 2) AS profit_margin_pct
FROM orders o
JOIN products p ON o.ProductID = p.ProductID
GROUP BY p.Product, p.Category
ORDER BY revenue DESC;


-- ----------------------------------------------------------------------------
-- 8. Subquery (WHERE) — customers whose total spend is above the average
--    customer's total spend
-- ----------------------------------------------------------------------------
SELECT CustomerID, CustomerName, total_spend
FROM (
    SELECT c.CustomerID, c.CustomerName, SUM(o.Sales) AS total_spend
    FROM customers c
    JOIN orders o ON c.CustomerID = o.CustomerID
    GROUP BY c.CustomerID, c.CustomerName
) customer_totals
WHERE total_spend > (
    SELECT AVG(customer_spend) FROM (
        SELECT SUM(Sales) AS customer_spend
        FROM orders
        GROUP BY CustomerID
    )
)
ORDER BY total_spend DESC;


-- ----------------------------------------------------------------------------
-- 9. Correlated subquery — each order's Sales vs. that customer's average
--    order value (flags orders bigger than the customer's own norm)
-- ----------------------------------------------------------------------------
SELECT
    o.OrderID,
    o.CustomerID,
    o.Sales,
    (SELECT ROUND(AVG(o2.Sales), 2)
     FROM orders o2
     WHERE o2.CustomerID = o.CustomerID) AS customer_avg_sales
FROM orders o
WHERE o.Sales > (
    SELECT AVG(o2.Sales) FROM orders o2 WHERE o2.CustomerID = o.CustomerID
)
ORDER BY o.Sales DESC
LIMIT 15;


-- ----------------------------------------------------------------------------
-- 10. Window Functions — running monthly revenue total + month-over-month change
-- ----------------------------------------------------------------------------
WITH monthly AS (
    SELECT
        strftime('%Y-%m', OrderDate) AS order_month,
        ROUND(SUM(Sales), 2)         AS monthly_revenue
    FROM orders
    GROUP BY order_month
)
SELECT
    order_month,
    monthly_revenue,
    ROUND(SUM(monthly_revenue) OVER (ORDER BY order_month), 2)        AS running_total,
    ROUND(monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY order_month), 2) AS mom_change
FROM monthly
ORDER BY order_month;


-- ----------------------------------------------------------------------------
-- 11. Window Function — rank products within each category by revenue
-- ----------------------------------------------------------------------------
WITH product_revenue AS (
    SELECT
        p.Category,
        p.Product,
        ROUND(SUM(o.Sales), 2) AS revenue
    FROM orders o
    JOIN products p ON o.ProductID = p.ProductID
    GROUP BY p.Category, p.Product
)
SELECT
    Category,
    Product,
    revenue,
    RANK() OVER (PARTITION BY Category ORDER BY revenue DESC) AS rank_in_category
FROM product_revenue
ORDER BY Category, rank_in_category;


-- ----------------------------------------------------------------------------
-- 12. Window Function — each customer's top order using ROW_NUMBER
-- ----------------------------------------------------------------------------
WITH ranked_orders AS (
    SELECT
        o.CustomerID,
        c.CustomerName,
        o.OrderID,
        o.Sales,
        ROW_NUMBER() OVER (PARTITION BY o.CustomerID ORDER BY o.Sales DESC) AS rn
    FROM orders o
    JOIN customers c ON o.CustomerID = c.CustomerID
)
SELECT CustomerID, CustomerName, OrderID, Sales
FROM ranked_orders
WHERE rn = 1
ORDER BY Sales DESC
LIMIT 15;


-- ----------------------------------------------------------------------------
-- 13. Combined analysis — revenue, profit margin & repeat-purchase rate by region
-- ----------------------------------------------------------------------------
SELECT
    c.Region,
    COUNT(DISTINCT o.CustomerID)                                    AS unique_customers,
    COUNT(o.OrderID)                                                AS total_orders,
    ROUND(COUNT(o.OrderID) * 1.0 / COUNT(DISTINCT o.CustomerID), 2) AS orders_per_customer,
    ROUND(SUM(o.Sales), 2)                                          AS revenue,
    ROUND(100.0 * SUM(o.Profit) / SUM(o.Sales), 2)                  AS profit_margin_pct
FROM orders o
JOIN customers c ON o.CustomerID = c.CustomerID
GROUP BY c.Region
ORDER BY revenue DESC;
