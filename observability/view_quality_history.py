from pathlib import Path

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

    connection = duckdb.connect(
        str(DATABASE_FILE)
    )

    results = connection.execute(
        """
        SELECT
            run_timestamp,
            dataset_name,
            total_records,
            valid_records,
            quarantined_records,
            ROUND(
                quality_score,
                4
            ) AS quality_score,
            pipeline_status

        FROM data_quality_observability

        ORDER BY run_timestamp DESC
        """
    ).fetchall()

    print(
        "\nDATA QUALITY OBSERVABILITY HISTORY\n"
    )

    for row in results:

        print(
            row
        )

    connection.close()


if __name__ == "__main__":
    main()