import time
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("Lab04-Baseline")
    .master("local[*]")
    .config("spark.sql.adaptive.enabled", "false")
    .config("spark.sql.autoBroadcastJoinThreshold", "-1")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

DATA = "/home/giga/datashop-platform/data/parquet"

transactions = spark.read.parquet(f"{DATA}/datashop_transactions.parquet")
products = spark.read.parquet(f"{DATA}/datashop_products.parquet") \
    .withColumnRenamed("category", "product_category")

start = time.perf_counter()

enriched = transactions.join(products, on="product_id", how="left")

summary = (
    enriched.groupBy("product_name")
    .agg(
        F.count("*").alias("num_sales"),
        F.round(F.sum("amount"), 2).alias("total_revenue"),
    )
    .orderBy(F.desc("total_revenue"))
)

top10 = summary.limit(10).collect()

elapsed = time.perf_counter() - start
print(f"\n=== BASELINE: {elapsed:.2f} seconds ===\n")

for row in top10:
    print(row["product_name"], row["num_sales"], row["total_revenue"])

print("\n=== EXECUTION PLAN ===\n")
summary.explain(mode="formatted")

spark.stop()
