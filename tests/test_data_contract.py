from pathlib import Path

from validation.data_contract_validator import (
    validate_dataset,
)


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


DATA_DIR = (
    PROJECT_ROOT
    / "data"
)


def run_validation(
    filename,
    skip_freshness=True
):

    dataset = (
        DATA_DIR
        / filename
    )

    return validate_dataset(
        dataset,
        skip_freshness=skip_freshness
    )


def test_schema_breaking_change():

    passed, errors = run_validation(
        "trades_schema_test.csv"
    )

    assert passed is False

    assert any(
        "Missing columns"
        in error
        for error in errors
    )


def test_invalid_transaction_type():

    passed, errors = run_validation(
        "trades_bad_status_test.csv"
    )

    assert passed is False

    assert any(
        "Invalid value for "
        "transaction_type"
        in error
        for error in errors
    )


def test_negative_quantity():

    passed, errors = run_validation(
        "trades_negative_quantity_test.csv"
    )

    assert passed is False

    assert any(
        "quantity must be"
        in error
        for error in errors
    )


def test_duplicate_trade_id():

    passed, errors = run_validation(
        "trades_duplicate_test.csv"
    )

    assert passed is False

    assert any(
        "Duplicate trade_id"
        in error
        for error in errors
    )


def test_missing_investor():

    passed, errors = run_validation(
        "trades_missing_investor_test.csv"
    )

    assert passed is False

    assert any(
        "investor_id is required"
        in error
        for error in errors
    )


def test_negative_price():

    passed, errors = run_validation(
        "trades_negative_price_test.csv"
    )

    assert passed is False

    assert any(
        "price must be"
        in error
        for error in errors
    )


def test_trade_value_mismatch():

    passed, errors = run_validation(
        "trades_value_mismatch_test.csv"
    )

    assert passed is False

    assert any(
        "trade_value mismatch"
        in error
        for error in errors
    )


def test_optional_new_column():

    passed, errors = run_validation(
        "trades_extra_column_test.csv"
    )

    assert passed is True

    assert errors == []


def test_stale_dataset():

    passed, errors = run_validation(
        "trades_stale_test.csv",
        skip_freshness=False
    )

    assert passed is False

    assert any(
        "Freshness violation"
        in error
        for error in errors
    )