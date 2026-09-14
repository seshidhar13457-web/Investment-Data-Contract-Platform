from pathlib import Path
from datetime import datetime
import argparse
import csv
import sys

import yaml


PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONTRACT_FILE = (
    PROJECT_ROOT
    / "data_contracts"
    / "trades_contract.yaml"
)


def load_contract():

    with open(
        CONTRACT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return yaml.safe_load(file)


def validate_type(
    value,
    expected_type
):

    try:

        if expected_type == "integer":
            int(value)

        elif expected_type == "float":
            float(value)

        elif expected_type == "timestamp":
            datetime.fromisoformat(value)

        elif expected_type == "string":
            str(value)

        return True

    except (ValueError, TypeError):

        return False


def validate_dataset(
    dataset_path,
    skip_freshness=False
):

    contract = load_contract()

    schema = contract["schema"]

    schema_evolution = contract.get(
        "schema_evolution",
        {}
    )

    freshness_config = contract.get(
        "freshness",
        {}
    )

    errors = []

    print(
        "\nDATA CONTRACT VALIDATION STARTED"
    )

    print(
        f"Dataset: {dataset_path}\n"
    )

    with open(
        dataset_path,
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        actual_columns = reader.fieldnames or []

        expected_columns = list(
            schema.keys()
        )

        missing_columns = [
            column
            for column in expected_columns
            if column not in actual_columns
        ]

        if missing_columns:

            errors.append(
                f"Missing columns: {missing_columns}"
            )

        extra_columns = [
            column
            for column in actual_columns
            if column not in expected_columns
        ]

        allow_new_columns = (
            schema_evolution.get(
                "allow_new_optional_columns",
                False
            )
        )

        if (
            extra_columns
            and not allow_new_columns
        ):

            errors.append(
                f"Unexpected columns: {extra_columns}"
            )

        seen_unique_values = {}

        for column, rules in schema.items():

            if rules.get("unique"):

                seen_unique_values[column] = set()

        latest_timestamp = None

        row_number = 1

        for row in reader:

            row_number += 1

            for column, rules in schema.items():

                if column not in row:
                    continue

                value = row[column]

                if rules.get("required"):

                    if (
                        value is None
                        or value.strip() == ""
                    ):

                        errors.append(
                            f"Row {row_number}: "
                            f"{column} is required"
                        )

                        continue

                if (
                    value is None
                    or value.strip() == ""
                ):
                    continue

                expected_type = rules.get(
                    "type"
                )

                if expected_type:

                    if not validate_type(
                        value,
                        expected_type
                    ):

                        errors.append(
                            f"Row {row_number}: "
                            f"{column} expected "
                            f"{expected_type} "
                            f"but received {value}"
                        )

                        continue

                if rules.get("unique"):

                    if (
                        value
                        in seen_unique_values[column]
                    ):

                        errors.append(
                            f"Row {row_number}: "
                            f"Duplicate {column}: "
                            f"{value}"
                        )

                    else:

                        seen_unique_values[
                            column
                        ].add(value)

                allowed_values = rules.get(
                    "allowed_values"
                )

                if allowed_values:

                    if value not in allowed_values:

                        errors.append(
                            f"Row {row_number}: "
                            f"Invalid value for "
                            f"{column}: {value}"
                        )

                minimum = rules.get(
                    "min"
                )

                if minimum is not None:

                    try:

                        if float(value) < minimum:

                            errors.append(
                                f"Row {row_number}: "
                                f"{column} must be "
                                f">= {minimum}"
                            )

                    except ValueError:

                        pass

            required_business_columns = [
                "quantity",
                "price",
                "trade_value"
            ]

            if all(
                column in row
                for column
                in required_business_columns
            ):

                try:

                    quantity = float(
                        row["quantity"]
                    )

                    price = float(
                        row["price"]
                    )

                    trade_value = float(
                        row["trade_value"]
                    )

                    expected_trade_value = (
                        quantity * price
                    )

                    difference = abs(
                        trade_value
                        - expected_trade_value
                    )

                    if difference > 0.02:

                        errors.append(
                            f"Row {row_number}: "
                            f"trade_value mismatch. "
                            f"Expected "
                            f"{expected_trade_value:.2f}, "
                            f"received "
                            f"{trade_value:.2f}"
                        )

                except (
                    ValueError,
                    TypeError
                ):

                    pass

            freshness_column = (
                freshness_config.get(
                    "column"
                )
            )

            if (
                freshness_column
                and freshness_column in row
                and row[freshness_column]
            ):

                try:

                    timestamp = (
                        datetime.fromisoformat(
                            row[
                                freshness_column
                            ]
                        )
                    )

                    if (
                        latest_timestamp is None
                        or timestamp
                        > latest_timestamp
                    ):

                        latest_timestamp = (
                            timestamp
                        )

                except ValueError:

                    pass

    maximum_delay_minutes = (
        freshness_config.get(
            "maximum_delay_minutes"
        )
    )

    if (
        not skip_freshness
        and latest_timestamp
        and maximum_delay_minutes
        is not None
    ):

        current_time = datetime.now()

        delay_minutes = (
            current_time
            - latest_timestamp
        ).total_seconds() / 60

        if (
            delay_minutes
            > maximum_delay_minutes
        ):

            errors.append(
                "Freshness violation: "
                f"latest record is "
                f"{delay_minutes:.0f} "
                f"minutes old. "
                f"Maximum allowed is "
                f"{maximum_delay_minutes} "
                f"minutes."
            )

    if errors:

        print(
            "DATA CONTRACT FAILED\n"
        )

        for error in errors[:20]:

            print(
                f"❌ {error}"
            )

        if len(errors) > 20:

            print(
                f"\n... plus "
                f"{len(errors) - 20} "
                f"more errors"
            )

        print(
            f"\nTotal violations: "
            f"{len(errors)}"
        )

        return False, errors

    print(
        "DATA CONTRACT PASSED"
    )

    print(
        "\n✅ Schema matched"
    )

    print(
        "✅ Required fields passed"
    )

    print(
        "✅ Unique fields passed"
    )

    print(
        "✅ Allowed values passed"
    )

    print(
        "✅ Minimum value rules passed"
    )

    print(
        "✅ Trade value calculation passed"
    )

    if skip_freshness:

        print(
            "⏭️ Freshness skipped"
        )

    else:

        print(
            "✅ Freshness passed"
        )

    return True, []


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Validate investment data "
            "against the trades contract."
        )
    )

    parser.add_argument(
        "--dataset",
        default=None,
        help="CSV dataset to validate"
    )

    parser.add_argument(
        "--skip-freshness",
        action="store_true",
        help=(
            "Skip freshness validation "
            "for historical regression data"
        )
    )

    args = parser.parse_args()

    contract = load_contract()

    if args.dataset:

        dataset_path = (
            PROJECT_ROOT
            / args.dataset
        )

    else:

        dataset_path = (
            PROJECT_ROOT
            / contract[
                "dataset"
            ][
                "source"
            ]
        )

    if not dataset_path.exists():

        print(
            f"Dataset not found: "
            f"{dataset_path}"
        )

        sys.exit(1)

    passed, _ = validate_dataset(
        dataset_path,
        skip_freshness=(
            args.skip_freshness
        )
    )

    if not passed:

        sys.exit(1)


if __name__ == "__main__":
    main()