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

print("Spark version:", spark.version)
print("Iceberg catalog 'local' configured")
