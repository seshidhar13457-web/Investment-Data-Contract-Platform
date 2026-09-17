# Gable Vendor Evaluation POC

## Project
Enterprise Investment Data Contract, Data Quality & Observability Platform

## Objective

Evaluate how a data contract platform such as Gable could integrate with our
investment data platform and prevent unsafe producer changes from impacting
downstream consumers.

## Business Scenario

The `trades` dataset is produced by the investment trade pipeline.

Downstream consumers may include:

- Portfolio analytics
- Risk analytics
- Compliance reporting
- Trade dashboards
- Machine learning pipelines

A producer should not be able to introduce a breaking schema or semantic
change without identifying the downstream impact.

## POC Requirements

The vendor evaluation should demonstrate:

1. Data contract definition
2. Schema validation
3. Producer and consumer ownership
4. Breaking-change detection
5. Schema evolution
6. Downstream impact analysis
7. CI/CD integration
8. Data quality integration
9. Observability
10. Contract versioning

## Example Breaking Changes

The following changes should be treated as potentially breaking:

- Remove `trade_id`
- Rename `price`
- Change `quantity` from integer to string
- Remove a valid `trade_status`
- Change the meaning of `trade_value`
- Remove `investor_id`

## Example Non-Breaking Change

Adding a new optional field such as:

broker_code

should be allowed when existing consumers are not required to use it.

## Evaluation Outcome

The POC will compare the vendor-style contract approach with the existing
custom Python validation and Soda implementation.

The goal is to determine how a dedicated data contract platform can provide
additional producer-consumer governance and change-impact visibility.