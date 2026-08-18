from pyspark.sql import SparkSession
import duckdb

# Test PySpark
spark = SparkSession.builder.appName("SanityCheck").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

data = [("Electronics", 100), ("Home", 200), ("Books", 50)]
df = spark.createDataFrame(data, ["category", "amount"])
result = df.groupBy("category").sum("amount").collect()
print("PySpark OK:", len(result), "categories aggregated")
spark.stop()

# Test DuckDB
conn = duckdb.connect()
conn.execute("CREATE TABLE test AS SELECT 1 as id, 'hello' as msg")
row = conn.execute("SELECT * FROM test").fetchone()
print("DuckDB OK:", row)

print("\n✓ Environment ready for Lab 01")
