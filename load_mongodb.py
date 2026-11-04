import pandas as pd
from pymongo import MongoClient, UpdateOne
df = pd.read_csv("data/clean_sales.csv", dtype={"CustomerID":"string","InvoiceNo":"string"})
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]
orders = db["orders"]
records = df.fillna("").to_dict("records")
if records:
    orders.insert_many(records, ordered=False)
customers = db["customer_summary"]
summary = df.groupby("CustomerID").agg(
    total_spend=("Revenue","sum"),
    total_orders=("InvoiceNo","nunique"),
    last_purchase=("InvoiceDate","max")
).reset_index()
customers.insert_many(summary.fillna("").to_dict("records"), ordered=False)
print("Loaded order and customer summary documents into MongoDB.")
