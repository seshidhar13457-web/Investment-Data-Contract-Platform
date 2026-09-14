from pathlib import Path
import argparse

import duckdb


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

DATABASE_FILE = (
    PROJECT_ROOT
    / "data"
    / "investment.duckdb"
)


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Load a regression dataset "
            "into the Soda contract test table."
        )
    )

    parser.add_argument(
        "--dataset",
        required=True,
        help=(
            "Dataset filename inside "
            "the data folder"
        )
    )

    args = parser.parse_args()

    dataset_file = (
        PROJECT_ROOT
        / "data"
        / args.dataset
    )

    if not dataset_file.exists():

        print(
            f"❌ Dataset not found: "
            f"{dataset_file}"
        )

        return

    connection = duckdb.connect(
        str(DATABASE_FILE)
    )

    connection.execute(
        """
        CREATE OR REPLACE TABLE
        trades_contract_test AS
        SELECT *
        FROM read_csv_auto(?)
        """,
        [str(dataset_file)]
    )

    row_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM trades_contract_test
        """
    ).fetchone()[0]

    connection.close()

    print(
        "\nTEST DATASET LOAD COMPLETE"
    )

    print(
        f"✅ Source: {args.dataset}"
    )

    print(
        f"✅ Target: trades_contract_test"
    )

    print(
        f"✅ Rows: {row_count:,}"
    )


if __name__ == "__main__":
    main()