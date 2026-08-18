from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import broadcast

spark = (
    SparkSession.builder
    .appName("Lab04-PartitionedWrite")
    .master("local[*]")
    .config("spark.sql.adaptive.enabled", "true")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

DATA = "/home/giga/datashop-platform/data/parquet"
OUT = f"{DATA}/enriched_transactions"

transactions = spark.read.parquet(f"{DATA}/datashop_transactions.parquet")
products_slim = (
    spark.read.parquet(f"{DATA}/datashop_products.parquet")
    .select("product_id", "product_name", "price")
)

enriched = (
    transactions
    .join(broadcast(products_slim), on="product_id", how="left")
    .withColumn("sale_date", F.to_date("timestamp"))
)

enriched.write \
    .partitionBy("sale_date") \
    .mode("overwrite") \
    .parquet(OUT)

print(f"\nЗаписано в {OUT}")
spark.stop()
