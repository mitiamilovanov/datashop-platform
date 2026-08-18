from pyspark.sql import SparkSession

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

# Count data files BEFORE the schema change
files_before = spark.sql(
    "SELECT count(*) AS n FROM local.datashop.transactions.files").first()["n"]

# Add the column — watch how fast this is
spark.sql("""
    ALTER TABLE local.datashop.transactions
    ADD COLUMN discount_pct DOUBLE
""")

# Count data files AFTER
files_after = spark.sql(
    "SELECT count(*) AS n FROM local.datashop.transactions.files").first()["n"]

print(f"Data files before: {files_before}, after: {files_after}")

print("\n=== 5 rows with the new column ===")
spark.sql("""
    SELECT transaction_id, timestamp, amount, discount_pct
    FROM local.datashop.transactions
    LIMIT 5
""").show(truncate=False)
