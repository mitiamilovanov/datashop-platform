import pandas as pd

RAW = "/home/giga/datashop-platform/data/raw/datashop_transactions.csv"
OUT = "/home/giga/datashop-platform/lab-10/transactions_with_errors.csv"

df = pd.read_csv(RAW)
print(f"Loaded {len(df)} rows from {RAW}")

# Error 1: negative amount (impossible for a sale)
df.loc[100, "amount"] = -50.00

# Error 2: NULL customer_id (orphan transaction)
df.loc[200, "customer_id"] = None

# Error 3: country DataShop doesn't operate in
df.loc[300, "country"] = "Brazil"

# Error 4: duplicate transaction_id (copy id from the next row)
df.loc[400, "transaction_id"] = df.loc[401, "transaction_id"]

df.to_csv(OUT, index=False)
print(f"Wrote {len(df)} rows to {OUT}")
print("Injected 4 errors:")
print("  row 100: amount = -50.00")
print("  row 200: customer_id = NULL")
print("  row 300: country = 'Brazil'")
print("  row 400: transaction_id duplicates row 401")
