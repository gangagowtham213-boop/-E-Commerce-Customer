"""
Download the full UCI Online Retail dataset (541,909 rows).
Run: pip install ucimlrepo pandas openpyxl
     python download_dataset.py
"""
from ucimlrepo import fetch_ucirepo
import pandas as pd
from pathlib import Path

out = Path("data")
out.mkdir(exist_ok=True)
dataset = fetch_ucirepo(id=352)
df = dataset.data.features.copy()
# UCI feature columns: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country
if "CustomerID" in df.columns:
    df["CustomerID"] = df["CustomerID"].astype("Int64")
df.to_csv(out / "online_retail_full.csv", index=False)
print(f"Saved {len(df):,} rows to data/online_retail_full.csv")
