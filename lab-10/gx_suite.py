import great_expectations as gx
import pandas as pd

DATA = "/home/giga/datashop-platform/lab-10/transactions_with_errors.csv"

context = gx.get_context()
data_source = context.data_sources.add_pandas(name="datashop")
data_asset = data_source.add_dataframe_asset(name="transactions")
batch_definition = data_asset.add_batch_definition_whole_dataframe("full_batch")

df = pd.read_csv(DATA)

# --- Expectation Suite: the data contract for DataShop transactions ---
suite = context.suites.add(
    gx.core.ExpectationSuite(name="datashop_transactions_suite")
)

# Uniqueness
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(column="transaction_id")
)

# Not null
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="transaction_id")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="customer_id")
)

# Positive amounts (strict: 0 is not a valid sale either)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="amount",
        min_value=0,
        strict_min=True,
    )
)

# Valid countries
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="country",
        value_set={"USA", "UK", "Germany", "Canada", "France"},
    )
)

# Valid categories
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="category",
        value_set={"Books", "Clothing", "Electronics", "Home & Garden", "Sports"},
    )
)

# Valid statuses
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="status",
        value_set={"completed", "pending", "refunded", "failed"},
    )
)

# Row count sanity check
suite.add_expectation(
    gx.expectations.ExpectTableRowCountToBeBetween(min_value=100, max_value=200000)
)

print(f"Suite defined with {len(suite.expectations)} expectations")
