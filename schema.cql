CREATE KEYSPACE IF NOT EXISTS ecommerce
WITH replication = {'class':'SimpleStrategy','replication_factor':1};
USE ecommerce;

CREATE TABLE IF NOT EXISTS customer_orders (
  customer_id text,
  invoice_date timestamp,
  invoice_no text,
  stock_code text,
  description text,
  quantity int,
  unit_price double,
  revenue double,
  country text,
  PRIMARY KEY ((customer_id), invoice_date, invoice_no, stock_code)
) WITH CLUSTERING ORDER BY (invoice_date DESC);
