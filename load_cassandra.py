import pandas as pd
from cassandra.cluster import Cluster
df = pd.read_csv("data/clean_sales.csv", dtype={"CustomerID":"string","InvoiceNo":"string","StockCode":"string"})
cluster=Cluster(["127.0.0.1"]); session=cluster.connect("ecommerce")
stmt=session.prepare("""INSERT INTO customer_orders
(customer_id,invoice_date,invoice_no,stock_code,description,quantity,unit_price,revenue,country)
VALUES (?,?,?,?,?,?,?,?,?)""")
for r in df.itertuples(index=False):
    cid=str(getattr(r,"CustomerID"))
    if not cid or cid=="<NA>": continue
    dt=pd.to_datetime(getattr(r,"InvoiceDate")).to_pydatetime()
    session.execute(stmt,(cid,dt,str(getattr(r,"InvoiceNo")),str(getattr(r,"StockCode")),
      str(getattr(r,"Description")),int(getattr(r,"Quantity")),float(getattr(r,"UnitPrice")),
      float(getattr(r,"Revenue")),str(getattr(r,"Country"))))
cluster.shutdown()
