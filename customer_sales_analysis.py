import pandas as pd
import numpy as np
from pathlib import Path

src = Path("data/online_retail_full.csv")
if not src.exists():
    raise SystemExit("Run: python data/download_dataset.py first")
df = pd.read_csv(src, dtype={"InvoiceNo":"string","StockCode":"string","CustomerID":"string"})
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# Preserve cancellation/return flags; use valid positive sales for customer and sales KPIs.
df["IsCancellation"] = df["InvoiceNo"].str.startswith("C", na=False)
clean = df.dropna(subset=["InvoiceNo","StockCode","InvoiceDate","Quantity","UnitPrice"])
sales = clean[(~clean["IsCancellation"]) & (clean["Quantity"] > 0) & (clean["UnitPrice"] > 0)].copy()
sales = sales.dropna(subset=["CustomerID"])
sales["CustomerID"] = sales["CustomerID"].astype(str).str.replace(r"\.0$","",regex=True)
sales["Revenue"] = sales["Quantity"] * sales["UnitPrice"]

# RFM at customer level
snapshot = sales["InvoiceDate"].max() + pd.Timedelta(days=1)
rfm = sales.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda x: (snapshot-x.max()).days),
    Frequency=("InvoiceNo","nunique"),
    Monetary=("Revenue","sum")
).reset_index()
rfm["R_Score"] = pd.qcut(rfm["Recency"].rank(method="first"),5,labels=[5,4,3,2,1]).astype(int)
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"),5,labels=[1,2,3,4,5]).astype(int)
rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"),5,labels=[1,2,3,4,5]).astype(int)
rfm["RFM_Score"] = rfm[["R_Score","F_Score","M_Score"]].astype(str).agg("".join,axis=1)
rfm["Segment"] = np.select(
    [ (rfm.R_Score>=4)&(rfm.F_Score>=4)&(rfm.M_Score>=4),
      (rfm.R_Score>=3)&(rfm.F_Score>=3),
      (rfm.R_Score<=2)&(rfm.F_Score>=3),
      (rfm.F_Score<=2)&(rfm.R_Score>=3)],
    ["Champions","Loyal Customers","At Risk","New/Promising"], default="Need Attention")

sales["YearMonth"] = sales["InvoiceDate"].dt.to_period("M").astype(str)
sales["OrderDay"] = sales["InvoiceDate"].dt.day_name()
sales.to_csv("data/clean_sales.csv",index=False)
rfm.to_csv("data/customer_rfm_segments.csv",index=False)

monthly = sales.groupby("YearMonth",as_index=False)["Revenue"].sum()
country = sales.groupby("Country",as_index=False).agg(Revenue=("Revenue","sum"),Orders=("InvoiceNo","nunique"))
products = sales.groupby(["StockCode","Description"],as_index=False).agg(Quantity=("Quantity","sum"),Revenue=("Revenue","sum"))
monthly.to_csv("data/monthly_sales.csv",index=False)
country.to_csv("data/country_sales.csv",index=False)
products.to_csv("data/product_sales.csv",index=False)

print("Valid sales rows:",len(sales))
print("Customers:",sales.CustomerID.nunique())
print("Revenue GBP:",round(sales.Revenue.sum(),2))
print("Invoices:",sales.InvoiceNo.nunique())
print("RFM segments:",rfm.Segment.value_counts().to_dict())
