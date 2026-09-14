from pathlib import Path

import duckdb


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

CSV_FILE = (
    PROJECT_ROOT
    / "data"
    / "trades.csv"
)

DATABASE_FILE = (
    PROJECT_ROOT
    / "data"
    / "investment.duckdb"
)


def main():

    print(
        "\nDUCKDB LOAD STARTED"
    )

    print(
        f"Source CSV: {CSV_FILE}"
    )

    print(
        f"Database: {DATABASE_FILE}\n"
    )

    connection = duckdb.connect(
        str(DATABASE_FILE)
    )

    connection.execute(
        """
        CREATE OR REPLACE TABLE trades AS
        SELECT *
        FROM read_csv_auto(?)
        """,
        [str(CSV_FILE)]
    )

    row_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM trades
        """
    ).fetchone()[0]

    print(
        "DUCKDB LOAD COMPLETE"
    )

    print(
        f"✅ trades table rows: {row_count:,}"
    )

    connection.close()


if __name__ == "__main__":
    main()