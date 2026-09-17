# Enterprise Data Platform Vendor Evaluation

## Project

Investment Data Contract, Data Quality & Observability Platform

## Objective

Evaluate specialized tools that can support data contracts, data quality,
producer-consumer governance, CI/CD enforcement, and data observability.

The evaluation is based on the requirements of the investment trade
data platform.

---

## Current Platform

The project currently contains:

- YAML-based data contracts
- Custom Python contract validation
- Pytest regression testing
- Soda data quality validation
- DuckDB validation environment
- Quarantine processing
- Data quality observability
- GitHub Actions CI/CD
- Protected main branch
- Producer-consumer dependency mapping
- Breaking-change impact analysis

---

## Gable Evaluation Focus

Gable is being evaluated primarily from the data contract and
producer-consumer governance perspective.

POC areas include:

- Contract ownership
- Producer registration
- Consumer dependencies
- Schema evolution
- Breaking-change detection
- Downstream impact analysis
- CI/CD enforcement
- Contract versioning

The project contains a Gable-style POC implementation for demonstrating
these concepts without representing it as a production Gable deployment.

---

## Soda Evaluation Focus

Soda is used directly in the project for data quality validation.

The current implementation validates the trades dataset against defined
quality expectations and executes those checks through GitHub Actions.

The Soda quality gate must pass before protected changes can satisfy the
repository merge requirements.

---

## Great Expectations Evaluation Focus

Great Expectations is included as an evaluation candidate for
expectation-based data validation.

Evaluation areas include:

- Dataset expectations
- Schema validation
- Data quality testing
- Pipeline validation
- Automated regression testing

A dedicated POC may be added after the vendor comparison stage.

---

## Monte Carlo Evaluation Focus

Monte Carlo is included primarily in the observability evaluation.

Evaluation areas include:

- Data reliability monitoring
- Incident detection
- Dataset health
- Lineage
- Operational observability

The existing project observability implementation provides a baseline
against which an enterprise observability product can be evaluated.

---

## Evaluation Approach

The evaluation follows the same business dataset and contract requirements
for each candidate.

The objective is not to declare that one product universally replaces
another.

Different products may address different layers of the data reliability
architecture.

---

## Current Architecture

Trade Producer
    |
    v
Data Contract
    |
    +------------------------+
    |                        |
    v                        v
Custom Contract          Soda Validation
Validation                   |
    |                        |
    +------------+-----------+
                 |
                 v
              CI/CD
                 |
                 v
        Contract Impact Analysis
                 |
                 v
        Protected Main Branch
                 |
                 v
        Validated Trade Data
                 |
          +------+------+
          |             |
          v             v
      Consumers     Observability

---

## POC Outcome

The project demonstrates how data contracts, data quality validation,
producer-consumer impact analysis, CI/CD enforcement, and observability
can work together rather than being treated as isolated capabilities.

Final vendor selection in a real enterprise environment would additionally
consider security, platform compatibility, operational support, licensing,
cost, scalability, vendor support, and organizational requirements.