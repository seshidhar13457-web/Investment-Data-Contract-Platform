from pathlib import Path
from datetime import datetime

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

QUARANTINE_DIR = (
    PROJECT_ROOT
    / "quarantine"
)

REPORTS_DIR = (
    PROJECT_ROOT
    / "reports"
)

QUARANTINE_FILE = (
    QUARANTINE_DIR
    / "trades_quarantine.csv"
)

VALID_FILE = (
    PROJECT_ROOT
    / "data"
    / "trades_validated.csv"
)

QUALITY_REPORT_FILE = (
    REPORTS_DIR
    / "data_quality_report.csv"
)


def main():

    QUARANTINE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = duckdb.connect(
        str(DATABASE_FILE)
    )

    print(
        "\nDATA QUALITY + OBSERVABILITY PROCESS STARTED\n"
    )

    connection.execute(
        """
        CREATE OR REPLACE TABLE
        trades_quality_results AS

        WITH duplicate_check AS (

            SELECT
                *,
                COUNT(*) OVER (
                    PARTITION BY trade_id
                ) AS trade_id_count

            FROM trades_contract_test
        )

        SELECT
            *,

            CASE

                WHEN trade_id_count > 1
                    THEN 'DUPLICATE_TRADE_ID'

                WHEN transaction_type
                     NOT IN ('BUY', 'SELL')
                    THEN 'INVALID_TRANSACTION_TYPE'

                WHEN quantity < 1
                    THEN 'INVALID_QUANTITY'

                WHEN price < 0.01
                    THEN 'INVALID_PRICE'

                WHEN investor_id IS NULL
                     OR TRIM(investor_id) = ''
                    THEN 'MISSING_INVESTOR_ID'

                ELSE NULL

            END AS failure_reason

        FROM duplicate_check
        """
    )

    connection.execute(
        """
        CREATE OR REPLACE TABLE
        trades_quarantine AS

        SELECT *
        FROM trades_quality_results
        WHERE failure_reason IS NOT NULL
        """
    )

    connection.execute(
        """
        CREATE OR REPLACE TABLE
        trades_validated AS

        SELECT *
        FROM trades_quality_results
        WHERE failure_reason IS NULL
        """
    )

    total_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM trades_quality_results
        """
    ).fetchone()[0]

    quarantine_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM trades_quarantine
        """
    ).fetchone()[0]

    valid_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM trades_validated
        """
    ).fetchone()[0]

    if total_count > 0:

        quality_score = (
            valid_count
            / total_count
        ) * 100

    else:

        quality_score = 0

    pipeline_status = (
        "PASSED"
        if quarantine_count == 0
        else "FAILED"
    )

    run_timestamp = datetime.now()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS
        data_quality_observability
        (
            run_timestamp TIMESTAMP,
            dataset_name VARCHAR,
            total_records BIGINT,
            valid_records BIGINT,
            quarantined_records BIGINT,
            quality_score DOUBLE,
            pipeline_status VARCHAR
        )
        """
    )

    connection.execute(
        """
        INSERT INTO
        data_quality_observability
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            run_timestamp,
            "trades_contract_test",
            total_count,
            valid_count,
            quarantine_count,
            quality_score,
            pipeline_status,
        ]
    )

    connection.execute(
        f"""
        COPY trades_quarantine
        TO '{QUARANTINE_FILE.as_posix()}'
        (
            HEADER,
            DELIMITER ','
        )
        """
    )

    connection.execute(
        f"""
        COPY trades_validated
        TO '{VALID_FILE.as_posix()}'
        (
            HEADER,
            DELIMITER ','
        )
        """
    )

    connection.execute(
        f"""
        COPY (
            SELECT
                failure_reason,
                COUNT(*) AS failed_records
            FROM trades_quarantine
            GROUP BY failure_reason
            ORDER BY failed_records DESC
        )
        TO '{QUALITY_REPORT_FILE.as_posix()}'
        (
            HEADER,
            DELIMITER ','
        )
        """
    )

    print(
        f"Total records: "
        f"{total_count:,}"
    )

    print(
        f"✅ Valid records: "
        f"{valid_count:,}"
    )

    print(
        f"🚫 Quarantined records: "
        f"{quarantine_count:,}"
    )

    print(
        f"📊 Quality score: "
        f"{quality_score:.4f}%"
    )

    print(
        f"Pipeline status: "
        f"{pipeline_status}"
    )

    print(
        "\nFailure reasons:"
    )

    failure_results = connection.execute(
        """
        SELECT
            failure_reason,
            COUNT(*) AS failed_records

        FROM trades_quarantine

        GROUP BY failure_reason

        ORDER BY failed_records DESC
        """
    ).fetchall()

    if failure_results:

        for (
            failure_reason,
            failed_records
        ) in failure_results:

            print(
                f"  {failure_reason}: "
                f"{failed_records}"
            )

    else:

        print(
            "  No quality failures"
        )

    print(
        "\n✅ Observability record saved"
    )

    print(
        f"✅ Report: "
        f"{QUALITY_REPORT_FILE}"
    )

    connection.close()


if __name__ == "__main__":
    main()