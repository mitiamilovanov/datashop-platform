import great_expectations as gx
import pandas as pd

DATA = "/home/giga/datashop-platform/lab-10/transactions_with_errors.csv"

# 1. Context — entry point to everything in GX (ephemeral, in-memory)
context = gx.get_context()

# 2. Data Source -> Data Asset -> Batch Definition
data_source = context.data_sources.add_pandas(name="datashop")
data_asset = data_source.add_dataframe_asset(name="transactions")
batch_definition = data_asset.add_batch_definition_whole_dataframe("full_batch")

# 3. Load the flawed CSV and get a batch
df = pd.read_csv(DATA)
batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

print(f"Context type: {type(context).__name__}")
print(f"Batch ready: {len(df)} rows, {len(df.columns)} columns")
print(batch.head())
