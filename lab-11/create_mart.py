import duckdb

MART_PATH = '/home/giga/datashop-platform/lab-11/datashop_mart.duckdb'
DBT_DB = '/home/giga/datashop-platform/lab-06/datashop.duckdb'

conn = duckdb.connect(MART_PATH)
conn.execute(f"ATTACH '{DBT_DB}' AS src (READ_ONLY)")

conn.execute("DROP TABLE IF EXISTS agg_daily_revenue")
conn.execute("""
    CREATE TABLE agg_daily_revenue AS
    SELECT
        CAST(sale_date AS DATE)          AS sale_date,
        category,
        country,
        SUM(order_count)                 AS order_count,
        ROUND(SUM(total_revenue), 2)     AS total_revenue
    FROM src.fct_daily_revenue
    GROUP BY CAST(sale_date AS DATE), category, country
    ORDER BY sale_date
""")

row_count = conn.execute("SELECT COUNT(*) FROM agg_daily_revenue").fetchone()[0]
date_range = conn.execute(
    "SELECT MIN(sale_date), MAX(sale_date) FROM agg_daily_revenue"
).fetchone()
total = conn.execute(
    "SELECT ROUND(SUM(total_revenue), 2) FROM agg_daily_revenue"
).fetchone()[0]

print(f"Mart created: {row_count} rows")
print(f"Date range: {date_range[0]} .. {date_range[1]}")
print(f"Total revenue: {total}")

conn.close()
