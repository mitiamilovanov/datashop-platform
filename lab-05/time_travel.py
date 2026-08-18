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

SNAPSHOT_1 = 3684520702465380532  # January-only state

# The table as it exists NOW
current = spark.table("local.datashop.transactions")
print(f"Current state:  {current.count()} rows")

# The table as it existed at Snapshot 1 — time travel by snapshot ID
jan_state = spark.sql(f"""
    SELECT count(*) AS cnt, round(sum(amount), 2) AS revenue
    FROM local.datashop.transactions VERSION AS OF {SNAPSHOT_1}
""")
print("State at Snapshot 1 (January only):")
jan_state.show()

# Time travel by timestamp — "show me the table as of 16:23"
ts_state = spark.sql("""
    SELECT count(*) AS cnt
    FROM local.datashop.transactions TIMESTAMP AS OF '2026-08-07 16:23:00'
""")
print("State as of 2026-08-07 16:23:00:")
ts_state.show()
