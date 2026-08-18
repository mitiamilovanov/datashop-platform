from pyspark.sql import SparkSession
from pyspark.sql.functions import col, month, year

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

# February — Snapshot 2
feb_df = transactions.filter(
    (year(col("timestamp")) == 2025) & (month(col("timestamp")) == 2))
feb_df.writeTo("local.datashop.transactions").append()
print(f"February rows appended: {feb_df.count()}")

# March — Snapshot 3
mar_df = transactions.filter(
    (year(col("timestamp")) == 2025) & (month(col("timestamp")) == 3))
mar_df.writeTo("local.datashop.transactions").append()
print(f"March rows appended: {mar_df.count()}")

print("\n=== Snapshot history ===")
spark.sql("""
    SELECT snapshot_id, committed_at, operation
    FROM local.datashop.transactions.snapshots
    ORDER BY committed_at
""").show(truncate=False)

total = spark.table("local.datashop.transactions").count()
print(f"Total rows in table: {total}")
