from pathlib import Path

import great_expectations as gx
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = PROJECT_ROOT / "data" / "trades.csv"


# ============================================================
# LOAD TRADE DATA
# ============================================================

print("=" * 70)
print("GREAT EXPECTATIONS TRADE VALIDATION")
print("=" * 70)

print(f"Dataset: {DATA_FILE}")

df = pd.read_csv(DATA_FILE)

print(f"Records loaded: {len(df):,}")
print()


# ============================================================
# CREATE GREAT EXPECTATIONS CONTEXT
# ============================================================

context = gx.get_context(mode="ephemeral")

print("Great Expectations context created.")


# ============================================================
# CREATE PANDAS DATA SOURCE
# ============================================================

data_source = context.data_sources.add_pandas(
    name="investment_trades_source"
)


# ============================================================
# CREATE DATA ASSET
# ============================================================

data_asset = data_source.add_dataframe_asset(
    name="trades_asset"
)


# ============================================================
# CREATE BATCH DEFINITION
# ============================================================

batch_definition = data_asset.add_batch_definition_whole_dataframe(
    "trades_batch"
)


# ============================================================
# GET BATCH
# ============================================================

batch = batch_definition.get_batch(
    batch_parameters={
        "dataframe": df
    }
)


# ============================================================
# DEFINE EXPECTATIONS
# ============================================================

expectations = [

    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="trade_id"
    ),

    gx.expectations.ExpectColumnValuesToBeUnique(
        column="trade_id"
    ),

    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="investor_id"
    ),

    gx.expectations.ExpectColumnValuesToBeInSet(
        column="exchange",
        value_set=[
            "NYSE",
            "NASDAQ"
        ]
    ),

    gx.expectations.ExpectColumnValuesToBeInSet(
        column="transaction_type",
        value_set=[
            "BUY",
            "SELL"
        ]
    ),

    gx.expectations.ExpectColumnValuesToBeInSet(
        column="order_type",
        value_set=[
            "MARKET",
            "LIMIT"
        ]
    ),

    gx.expectations.ExpectColumnValuesToBeInSet(
        column="trade_status",
        value_set=[
            "COMPLETED",
            "EXECUTED",
            "PENDING",
            "CANCELLED"
        ]
    ),

    gx.expectations.ExpectColumnValuesToBeBetween(
        column="quantity",
        min_value=1
    ),

    gx.expectations.ExpectColumnValuesToBeBetween(
        column="price",
        min_value=0.01
    ),

    gx.expectations.ExpectColumnValuesToBeBetween(
        column="trade_value",
        min_value=0.01
    )
]


# ============================================================
# RUN VALIDATION
# ============================================================

passed = 0
failed = 0

print()
print("=" * 70)
print("EXPECTATION RESULTS")
print("=" * 70)


for expectation in expectations:

    result = batch.validate(
        expectation
    )

    expectation_name = expectation.__class__.__name__

    if result.success:

        print(f"PASS: {expectation_name}")

        passed += 1

    else:

        print(f"FAIL: {expectation_name}")

        failed += 1


# ============================================================
# VALIDATION SUMMARY
# ============================================================

print()
print("=" * 70)
print("GREAT EXPECTATIONS VALIDATION SUMMARY")
print("=" * 70)

print(f"Total expectations : {len(expectations)}")
print(f"Passed             : {passed}")
print(f"Failed             : {failed}")


# ============================================================
# PIPELINE DECISION
# ============================================================

if failed == 0:

    print()
    print("GX VALIDATION PASSED")
    print("Dataset satisfies all configured expectations.")

else:

    print()
    print("GX VALIDATION FAILED")
    print("Dataset contains one or more quality violations.")

    raise SystemExit(1)