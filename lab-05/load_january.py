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

# Read all transactions, filter to January 2025
transactions = spark.read.parquet(
    "/home/giga/datashop-platform/data/parquet/datashop_transactions.parquet")

jan_df = transactions.filter(
    (year(col("timestamp")) == 2025) & (month(col("timestamp")) == 1))

# Create the Iceberg table with January data — Snapshot 1
jan_df.writeTo("local.datashop.transactions").create()

print(f"January rows loaded: {jan_df.count()}")

# Inspect the snapshot history
print("\n=== Snapshot history ===")
spark.sql("""
    SELECT snapshot_id, committed_at, operation
    FROM local.datashop.transactions.snapshots
    ORDER BY committed_at
""").show(truncate=False)
