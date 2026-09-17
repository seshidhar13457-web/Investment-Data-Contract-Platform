from pathlib import Path
import argparse
import yaml


BASE_DIR = Path(__file__).resolve().parent
MAPPING_FILE = BASE_DIR / "producer_consumer_map.yaml"


def load_mapping():
    with open(MAPPING_FILE, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def analyze_field_change(field_name):
    mapping = load_mapping()

    dataset_name = mapping["dataset"]["name"]
    producer_name = mapping["producer"]["name"]
    consumers = mapping["consumers"]

    impacted_consumers = []

    for consumer in consumers:
        required_fields = consumer.get("required_fields", [])

        if field_name in required_fields:
            impacted_consumers.append(
                {
                    "name": consumer["name"],
                    "type": consumer["type"],
                }
            )

    print("=" * 70)
    print("DATA CONTRACT CHANGE IMPACT ANALYSIS")
    print("=" * 70)

    print(f"Dataset          : {dataset_name}")
    print(f"Producer         : {producer_name}")
    print(f"Proposed change  : Remove or modify '{field_name}'")
    print()

    if impacted_consumers:
        print("BREAKING CHANGE DETECTED")
        print()
        print(f"Impacted consumers: {len(impacted_consumers)}")

        for consumer in impacted_consumers:
            print(
                f" - {consumer['name']} "
                f"({consumer['type']})"
            )

        print()
        print("Decision: BLOCK CHANGE")
        return 1

    print("No registered consumer requires this field.")
    print()
    print("Decision: NO CONSUMER IMPACT DETECTED")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Analyze downstream impact of a proposed data contract change."
    )

    parser.add_argument(
        "--field",
        required=True,
        help="Field that the producer proposes to remove or modify.",
    )

    args = parser.parse_args()

    exit_code = analyze_field_change(args.field)

    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()