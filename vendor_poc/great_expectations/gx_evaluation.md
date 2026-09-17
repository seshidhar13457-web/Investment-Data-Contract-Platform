# Great Expectations Evaluation POC

## Project

Enterprise Investment Data Contract, Data Quality & Observability Platform

## Objective

Evaluate Great Expectations as an expectation-based data testing framework
for the investment trades dataset.

The POC uses the same trade data and business rules already validated by the
custom Python contract framework and Soda.

---

## Dataset

Dataset:

data/trades.csv

Baseline record count:

100,000 trade records

Important fields include:

- trade_id
- portfolio_id
- investor_id
- investor_name
- symbol
- exchange
- transaction_type
- order_type
- trade_status
- quantity
- price
- trade_value
- trade_timestamp

---

## Expectations Implemented

The POC validates:

1. trade_id must not be null
2. trade_id must be unique
3. investor_id must not be null
4. exchange must be NYSE or NASDAQ
5. transaction_type must be BUY or SELL
6. order_type must be MARKET or LIMIT
7. trade_status must contain an approved value
8. quantity must be greater than or equal to 1
9. price must be greater than or equal to 0.01
10. trade_value must be greater than or equal to 0.01

---

## Clean Dataset Test

The clean trades dataset was used as the baseline validation scenario.

Expected result:

10 expectations passed
0 expectations failed

This demonstrates that the baseline dataset satisfies the configured
Great Expectations rules.

---

## Negative Testing

The same validation framework was evaluated against intentionally corrupted
datasets.

### Duplicate Trade ID

Dataset:

trades_duplicate_test.csv

Expected detection:

trade_id uniqueness violation

### Invalid Transaction Type

Dataset:

trades_bad_status_test.csv

Injected value:

PURCHASE

Expected detection:

transaction_type allowed-value violation

### Negative Quantity

Dataset:

trades_negative_quantity_test.csv

Injected value:

quantity = -50

Expected detection:

quantity minimum-value violation

### Missing Investor ID

Dataset:

trades_missing_investor_test.csv

Expected detection:

investor_id null-value violation

---

## Comparison with Custom Python Validation

The custom Python validator provides flexible business-specific contract
logic.

Examples include:

- Cross-field trade_value validation
- Contract-specific schema evolution
- Freshness handling
- Custom error messages
- Business-specific validation behavior

Great Expectations provides a reusable expectation-based testing framework
for standard data quality validation.

---

## Comparison with Soda

Both Soda and Great Expectations can validate data quality rules.

In this project, Soda is currently integrated directly into the GitHub
Actions quality gate.

Great Expectations is being evaluated as an additional data testing
framework rather than being added automatically as another required CI gate.

This avoids adding duplicate validation stages without a clear engineering
reason.

---

## Comparison with Gable-Style POC

The Gable-style POC focuses primarily on producer-consumer contract
relationships and change impact.

Example:

A producer proposes changing investor_id.

The impact analyzer determines whether downstream consumers depend on that
field.

Great Expectations focuses on validating the actual dataset against
configured expectations.

Therefore these capabilities address different parts of the overall data
reliability architecture.

---

## Current Evaluation Outcome

Great Expectations successfully demonstrates expectation-based validation
for the investment trades use case.

The POC demonstrates:

- Clean-data validation
- Negative testing
- Schema and field-level expectations
- Reusable automated validation
- Pipeline-compatible exit codes

Further enterprise evaluation would consider scalability, integrations,
operational support, security, governance, maintenance effort, and cost.