from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, count, round as spark_round

spark = SparkSession.builder \
    .appName("DataShop-Revenue-Analysis") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
transactions = spark.read.parquet("/home/giga/datashop-platform/data/parquet/datashop_transactions.parquet")

# Всегда инспектируй данные при первой загрузке
transactions.printSchema()
transactions.show(5, truncate=False)
print(f"Total rows: {transactions.count()}")

result = transactions \
    .filter(col("status") == "completed") \
    .groupBy("category", "country") \
    .agg(
        spark_round(spark_sum("amount"), 2).alias("total_revenue"),
        count("*").alias("order_count")
    ) \
    .orderBy(col("total_revenue").desc())

result.show(25, truncate=False)

result.write \
    .mode("overwrite") \
    .parquet("/home/giga/datashop-platform/data/parquet/category_country_summary.parquet")

print("Wrote category_country_summary.parquet")
print(f"Rows written: {result.count()}")
