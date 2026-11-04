from pyspark.sql import SparkSession, functions as F
spark = SparkSession.builder.appName("EcommerceCustomerSalesAnalytics").getOrCreate()
df = spark.read.option("header",True).option("inferSchema",True).csv("data/online_retail_full.csv")
df = (df.withColumn("InvoiceDate",F.to_timestamp("InvoiceDate"))
        .withColumn("Quantity",F.col("Quantity").cast("double"))
        .withColumn("UnitPrice",F.col("UnitPrice").cast("double"))
        .withColumn("Revenue",F.col("Quantity")*F.col("UnitPrice")))
sales = df.filter((~F.upper(F.col("InvoiceNo")).startswith("C")) &
                  (F.col("Quantity")>0) & (F.col("UnitPrice")>0) &
                  F.col("CustomerID").isNotNull())
sales.write.mode("overwrite").parquet("warehouse/clean_sales")
(sales.groupBy("Country").agg(F.sum("Revenue").alias("TotalRevenue"),
                              F.countDistinct("InvoiceNo").alias("Orders"))
      .orderBy(F.desc("TotalRevenue"))
      .write.mode("overwrite").option("header",True).csv("output/country_sales"))
(sales.groupBy(F.date_format("InvoiceDate","yyyy-MM").alias("YearMonth"))
      .agg(F.sum("Revenue").alias("Revenue"))
      .orderBy("YearMonth")
      .write.mode("overwrite").option("header",True).csv("output/monthly_sales"))
spark.stop()
