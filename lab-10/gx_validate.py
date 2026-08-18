import great_expectations as gx
import pandas as pd

DATA = "/home/giga/datashop-platform/lab-10/transactions_with_errors.csv"

context = gx.get_context()
data_source = context.data_sources.add_pandas(name="datashop")
data_asset = data_source.add_dataframe_asset(name="transactions")
batch_definition = data_asset.add_batch_definition_whole_dataframe("full_batch")

df = pd.read_csv(DATA)

suite = context.suites.add(
    gx.core.ExpectationSuite(name="datashop_transactions_suite")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(column="transaction_id")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="transaction_id")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="customer_id")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="amount", min_value=0, strict_min=True
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="country",
        value_set=["USA", "UK", "Germany", "Canada", "France"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="category",
        value_set=["Books", "Clothing", "Electronics", "Home & Garden", "Sports"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="status",
        value_set=["completed", "pending", "refunded", "failed"],
    )
)
suite.add_expectation(
    gx.expectations.ExpectTableRowCountToBeBetween(min_value=100, max_value=200000)
)

# Persist the modified suite back to the context store
suite.save()

# --- Validation: run the suite against the batch ---
validation_definition = context.validation_definitions.add(
    gx.core.ValidationDefinition(
        name="datashop_nightly_validation",
        data=batch_definition,
        suite=suite,
    )
)

results = validation_definition.run(batch_parameters={"dataframe": df})

print("\nValidation Summary:")
print(f"Success: {results.success}")
print(f"Evaluated expectations: {results.statistics['evaluated_expectations']}")
print(f"Successful: {results.statistics['successful_expectations']}")
print(f"Failed: {results.statistics['unsuccessful_expectations']}")

# --- Inspect the failures ---
for result in results.results:
    if not result.success:
        print(f"\nFAILED: {result.expectation_config.type}")
        print(f"  Column: {result.expectation_config.kwargs.get('column', 'N/A')}")
        r = result.result
        print(f"  Unexpected count: {r.get('unexpected_count')}")
        print(f"  Sample unexpected values: {r.get('partial_unexpected_list')}")
