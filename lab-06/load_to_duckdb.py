"""Lab 06 — Load DataShop raw CSVs into DuckDB warehouse."""
import duckdb
from pathlib import Path

ROOT = Path.home() / "datashop-platform"
DB_PATH = str(ROOT / "lab-06" / "datashop.duckdb")
RAW = str(ROOT / "data" / "raw")

TABLES = {
    "raw_transactions": f"{RAW}/datashop_transactions.csv",
    "raw_customers": f"{RAW}/datashop_customers.csv",
    "raw_products": f"{RAW}/datashop_products.csv",
}

conn = duckdb.connect(DB_PATH)

for table, csv_path in TABLES.items():
    conn.execute(f"DROP TABLE IF EXISTS {table}")
    conn.execute(
        f"CREATE TABLE {table} AS SELECT * FROM read_csv_auto('{csv_path}')"
    )
    count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table}: {count:,} rows loaded")

print(f"\nDone. Warehouse file: {DB_PATH}")
conn.close()
