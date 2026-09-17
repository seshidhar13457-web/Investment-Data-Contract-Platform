from pathlib import Path
import argparse

import great_expectations as gx
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


# ============================================================
# COMMAND-LINE ARGUMENTS
# ============================================================

parser = argparse.ArgumentParser(
    description="Validate an investment trade CSV using Great Expectations."
)

parser.add_argument(
    "--dataset",
    required=True,
    help="CSV filename located inside the data directory.",
)

args = parser.parse_args()

DATA_FILE = DATA_DIR / args.dataset


# ============================================================
# VERIFY DATASET EXISTS
# ============================================================

if not DATA_FILE.exists():
    print(f"ERROR: Dataset not found: {DATA_FILE}")
    raise SystemExit(1)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("GREAT EXPECTATIONS TEST DATASET VALIDATION")
print("=" * 70)

print(f"Dataset: {DATA_FILE}")

df = pd.read_csv(DATA_FILE)

print(f"Records loaded: {len(df):,}")


# ============================================================
# CREATE GX CONTEXT
# ============================================================

context = gx.get_context(mode="ephemeral")


# ============================================================
# CREATE PANDAS DATA SOURCE
# ============================================================

data_source = context.data_sources.add_pandas(
    name="investment_test_source"
)


# ============================================================
# CREATE DATAFRAME ASSET
# ============================================================

data_asset = data_source.add_dataframe_asset(
    name="trades_test_asset"
)


# ============================================================
# CREATE BATCH
# ============================================================

batch_definition = data_asset.add_batch_definition_whole_dataframe(
    "trades_test_batch"
)

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
# RUN EXPECTATIONS
# ============================================================

passed = 0
failed = 0

print()
print("=" * 70)
print("EXPECTATION RESULTS")
print("=" * 70)


for expectation in expectations:

    result = batch.validate(expectation)

    expectation_name = expectation.__class__.__name__

    if result.success:

        print(f"PASS: {expectation_name}")
        passed += 1

    else:

        print(f"FAIL: {expectation_name}")
        failed += 1


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 70)
print("VALIDATION SUMMARY")
print("=" * 70)

print(f"Dataset            : {args.dataset}")
print(f"Total expectations : {len(expectations)}")
print(f"Passed             : {passed}")
print(f"Failed             : {failed}")


# ============================================================
# PIPELINE DECISION
# ============================================================

if failed > 0:

    print()
    print("GX VALIDATION FAILED")
    print("Dataset contains quality violations.")

    raise SystemExit(1)


print()
print("GX VALIDATION PASSED")
print("Dataset satisfies all configured expectations.")