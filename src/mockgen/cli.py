from __future__ import annotations

import argparse
from pathlib import Path

from .core import (
    ensure_config_file,
    load_user_config,
    build_indexed_records,
    build_output_payload,
    write_output_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a mock output JSON using inputs sourced from a JSON file "
            "with multiple edits (no interactive prompts)."
        )
    )
    parser.add_argument(
        "--config",
        type=str,
        default="user_input.json",
        help="Path to the input JSON file containing required fields.",
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help=(
            "Create/overwrite a template input JSON at --config and exit. "
            "Edit it and rerun."
        ),
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of random outputs to include in a single JSON file.",
    )
    parser.add_argument(
        "--split",
        action="store_true",
        help=(
            "If set with --count > 1, writes each randomized output to its own JSON file "
            "instead of combining them into one file."
        ),
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help=(
            "Generate one JSON per paired record for the specified section (e.g., Model_1). "
            "Counts are derived from the number of values per field, paired by index."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config_path = Path(args.config)

    if args.init:
        ensure_config_file(config_path, overwrite=True)
        print(f"Wrote template to '{config_path}'. Edit it, then rerun.")
        return

    if not config_path.exists():
        ensure_config_file(config_path, overwrite=False)
        raise SystemExit(
            f"Created '{config_path}'. Please fill in the required fields and rerun."
        )

    edits = load_user_config(config_path)
    print(f"Loaded {len(edits)} sections: {', '.join(edits.keys())}")

    if args.model:
        if args.model not in edits:
            available = ", ".join(edits.keys())
            raise SystemExit(
                f"Section '{args.model}' not found in '{config_path}'. Available sections: {available}"
            )
        records = build_indexed_records(edits[args.model])
        if not records:
            raise SystemExit(
                f"No records could be built for section '{args.model}'. Ensure all required fields have values."
            )
        for i, record in enumerate(records, start=1):
            payload = {f"{args.model}_output_{i}": record}
            outfile = write_output_file(payload, file_tag=f"_{i}")
            print(f"Generated: {outfile}")
        return

    if args.count > 1 and args.split:
        for i in range(1, args.count + 1):
            # Simple random selection per output file
            payload = build_output_payload(edits, count=1)
            outfile = write_output_file(payload, file_tag=f"_{i}")
            print(f"Generated: {outfile}")
    else:
        payload = build_output_payload(edits, count=args.count)
        outfile = write_output_file(payload)
        print(f"Generated: {outfile}")


if __name__ == "__main__":
    main()


