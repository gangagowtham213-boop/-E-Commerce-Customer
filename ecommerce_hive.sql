-- Create database and external table over cleaned CSV in HDFS.
CREATE DATABASE IF NOT EXISTS ecommerce_analytics;
USE ecommerce_analytics;

CREATE EXTERNAL TABLE IF NOT EXISTS online_retail (
  InvoiceNo STRING, StockCode STRING, Description STRING,
  Quantity INT, InvoiceDate STRING, UnitPrice DOUBLE,
  CustomerID STRING, Country STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES ("separatorChar"=",","quoteChar"="\"")
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/online_retail';

CREATE TABLE IF NOT EXISTS sales_fact STORED AS PARQUET AS
SELECT InvoiceNo, StockCode, Description, Quantity,
       CAST(InvoiceDate AS TIMESTAMP) AS InvoiceDate,
       UnitPrice, CustomerID, Country,
       Quantity * UnitPrice AS Revenue
FROM online_retail
WHERE UPPER(InvoiceNo) NOT LIKE 'C%'
  AND Quantity > 0 AND UnitPrice > 0 AND CustomerID IS NOT NULL;

-- Monthly sales
SELECT date_format(InvoiceDate,'yyyy-MM') AS month,
       ROUND(SUM(Revenue),2) AS revenue
FROM sales_fact GROUP BY date_format(InvoiceDate,'yyyy-MM')
ORDER BY month;

-- Top products
SELECT StockCode, MAX(Description) AS product,
       SUM(Quantity) AS units, ROUND(SUM(Revenue),2) AS revenue
FROM sales_fact GROUP BY StockCode ORDER BY revenue DESC LIMIT 10;

-- Country performance
SELECT Country, ROUND(SUM(Revenue),2) AS revenue,
       COUNT(DISTINCT InvoiceNo) AS orders
FROM sales_fact GROUP BY Country ORDER BY revenue DESC;
