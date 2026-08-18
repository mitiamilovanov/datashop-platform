import pandas as pd
import os

raw = os.path.expanduser("~/datashop-platform/data/raw")
pq = os.path.expanduser("~/datashop-platform/data/parquet")

csv_df = pd.read_csv(f"{raw}/datashop_transactions.csv")
parquet_df = pd.read_parquet(f"{pq}/datashop_transactions.parquet")

print(f"CSV rows:     {len(csv_df)}")
print(f"Parquet rows: {len(parquet_df)}")
print(f"Match: {len(csv_df) == len(parquet_df)}")
print("\nParquet dtypes:")
print(parquet_df.dtypes)
