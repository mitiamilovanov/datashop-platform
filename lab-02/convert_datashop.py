# convert_datashop.py
import pandas as pd
import os

raw_dir = os.path.expanduser("~/datashop-platform/data/raw")
parquet_dir = os.path.expanduser("~/datashop-platform/data/parquet")

print("Converting DataShop CSV files to Parquet..")

# Явная схема: типы задаём сами, а не доверяем выводу pandas
df = pd.read_csv(
    f"{raw_dir}/datashop_transactions.csv",
    dtype={
        "transaction_id": "string",
        "customer_id": "string",
        "product_id": "string",
        "category": "string",
        "amount": "float64",
        "quantity": "int32",
        "status": "string",
        "country": "string",
        "payment_method": "string",
    },
    parse_dates=["timestamp"],
)

df_cust = pd.read_csv(
    f"{raw_dir}/datashop_customers.csv",
    dtype={
        "customer_id": "string",
        "name": "string",
        "email": "string",
        "country": "string",
    },
    parse_dates=["signup_date"],
)

df_prod = pd.read_csv(
    f"{raw_dir}/datashop_products.csv",
    dtype={
        "product_id": "string",
        "product_name": "string",
        "category": "string",
        "price": "float64",
    },
)

df.to_parquet(f"{parquet_dir}/datashop_transactions.parquet",
              compression="zstd", index=False)
print(f"  datashop_transactions.parquet  ({len(df):,} rows)")

df_cust.to_parquet(f"{parquet_dir}/datashop_customers.parquet",
                   compression="zstd", index=False)
print(f"  datashop_customers.parquet     ({len(df_cust):,} rows)")

df_prod.to_parquet(f"{parquet_dir}/datashop_products.parquet",
                   compression="zstd", index=False)
print(f"  datashop_products.parquet      ({len(df_prod):,} rows)")

print("\nDataShop datasets converted to Parquet -> data/parquet/")
