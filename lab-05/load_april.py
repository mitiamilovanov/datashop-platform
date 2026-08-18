from pyspark.sql import SparkSession
from pyspark.sql.functions import col, month, year, rand, round as spark_round

spark = SparkSession.builder \
    .appName("DataShop-Iceberg") \
    .config("spark.jars.packages",
            "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.2") \
    .config("spark.sql.extensions",
            "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.local",
            "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.local.type", "hadoop") \
    .config("spark.sql.catalog.local.warehouse",
            "/home/giga/datashop-platform/data/warehouse") \
    .getOrCreate()

transactions = spark.read.parquet(
    "/home/giga/datashop-platform/data/parquet/datashop_transactions.parquet")

# April — the discount program is live, so new rows carry discount_pct
apr_df = transactions.filter(
    (year(col("timestamp")) == 2025) & (month(col("timestamp")) == 4)) \
    .withColumn("discount_pct", spark_round(rand(seed=42) * 25, 1))

apr_df.writeTo("local.datashop.transactions").append()
print(f"April rows appended: {apr_df.count()}")

print("\n=== Snapshot history ===")
spark.sql("""
    SELECT snapshot_id, committed_at, operation
    FROM local.datashop.transactions.snapshots
    ORDER BY committed_at
""").show(truncate=False)

print("=== Old rows vs new rows ===")
spark.sql("""
    SELECT month(timestamp) AS mon,
           count(*) AS rows,
           count(discount_pct) AS rows_with_discount
    FROM local.datashop.transactions
    GROUP BY month(timestamp)
    ORDER BY mon
""").show()
