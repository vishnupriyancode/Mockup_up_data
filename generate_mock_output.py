from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
import random
from pathlib import Path
from typing import Dict, List, Any, Optional


CONFIG_FILE = Path("user_input.json")
OUTPUT_DIR = Path("mock_outputs")
REQUIRED_FIELDS: List[str] = ["name", "mail_id", "address", "city"]


def ensure_config_file(path: Path, overwrite: bool = False) -> None:
    if path.exists() and not overwrite:
        return
    # Template with multiple edits
    template = {
        "Edit_1": {
            "name": "Vishnu,Priyan",
            "mail_id": "Vishnupriyannatarajan@gmail.com, ramdon@gamil.com",
            "address": "123456,12345",
            "city": "Hyderabad,Chennai"
        },
        "Edit_2": {
            "name": "Raju,Natarajan",
            "mail_id": "Vishnupriyan@gmail.com, Ran@gmail.com",
            "address": "124596,5748",
            "city": "Chennai,Kovai"
        }
    }
    with path.open("w", encoding="utf-8") as f:
        json.dump(template, f, indent=2, ensure_ascii=False)


def _to_choice_list(value: Any) -> List[str]:
    if isinstance(value, list):
        items = [str(v).strip() for v in value]
    elif isinstance(value, str):
        # Support comma-separated values in strings
        items = [v.strip() for v in value.split(",")]
    else:
        items = [str(value).strip()]
    # Remove empty strings
    return [v for v in items if v]


def load_user_config(path: Path) -> Dict[str, Dict[str, List[str]]]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        raise SystemExit(
            f"Could not read configuration from '{path}': {exc}. Edit the file and rerun."
        )

    # If any explicit edit sections exist, parse only those
    if any(key.startswith("Edit_") for key in data.keys()):
        parsed: Dict[str, Dict[str, List[str]]] = {}
        for section_key, section_data in data.items():
            if not section_key.startswith("Edit_"):
                continue
            parsed[section_key] = {}
            missing_or_empty = []
            for field in REQUIRED_FIELDS:
                if field not in section_data:
                    missing_or_empty.append(field)
                    continue
                choices = _to_choice_list(section_data[field])
                if not choices:
                    missing_or_empty.append(field)
                    continue
                parsed[section_key][field] = choices
            if missing_or_empty:
                raise SystemExit(
                    f"Section '{section_key}' is missing required non-empty fields: "
                    + ", ".join(missing_or_empty)
                    + f". Please edit '{path}' and rerun."
                )
        if not parsed:
            raise SystemExit(
                f"No valid 'Edit_X' sections found in '{path}'."
            )
        return parsed

    # If the top-level object is a mapping of sections (e.g., Model_1, Model_2), parse them generically
    if all(isinstance(v, dict) for v in data.values()):
        parsed: Dict[str, Dict[str, List[str]]] = {}
        for section_key, section_data in data.items():
            # Skip empty or invalid sections
            if not isinstance(section_data, dict):
                continue
            missing_or_empty = []
            normalized_section: Dict[str, List[str]] = {}
            for field in REQUIRED_FIELDS:
                if field not in section_data:
                    missing_or_empty.append(field)
                    continue
                choices = _to_choice_list(section_data[field])
                if not choices:
                    missing_or_empty.append(field)
                    continue
                normalized_section[field] = choices
            if missing_or_empty:
                raise SystemExit(
                    f"Section '{section_key}' is missing required non-empty fields: "
                    + ", ".join(missing_or_empty)
                    + f". Please edit '{path}' and rerun."
                )
            parsed[section_key] = normalized_section
        if not parsed:
            raise SystemExit(f"No valid sections found in '{path}'.")
        return parsed

    # Legacy format - top level contains fields directly
    missing_or_empty = []
    parsed: Dict[str, Dict[str, List[str]]] = {"Edit_1": {}}
    for key in REQUIRED_FIELDS:
        if key not in data:
            missing_or_empty.append(key)
            continue
        choices = _to_choice_list(data[key])
        if not choices:
            missing_or_empty.append(key)
            continue
        parsed["Edit_1"][key] = choices
    if missing_or_empty:
        raise SystemExit(
            "Configuration is missing required non-empty fields: "
            + ", ".join(missing_or_empty)
            + f". Please edit '{path}' and rerun."
        )
    return parsed


def _select_random_record_from_edit(edit_options: Dict[str, List[str]]) -> Dict[str, str]:
    return {
        "name": random.choice(edit_options["name"]),
        "mail_id": random.choice(edit_options["mail_id"]),
        "address": random.choice(edit_options["address"]),
        "city": random.choice(edit_options["city"]),
    }


def _select_random_edit_and_record(edits: Dict[str, Dict[str, List[str]]]) -> tuple[str, Dict[str, str]]:
    # Randomly select an edit
    edit_key = random.choice(list(edits.keys()))
    record = _select_random_record_from_edit(edits[edit_key])
    return edit_key, record


def build_output_payload(edits: Dict[str, Dict[str, List[str]]], count: int) -> Dict[str, Dict[str, str]]:
    payload: Dict[str, Dict[str, str]] = {}
    for i in range(1, max(1, count) + 1):
        edit_key, record = _select_random_edit_and_record(edits)
        payload[f"{edit_key}_output_{i}"] = record
    return payload


def build_indexed_records(section_options: Dict[str, List[str]]) -> List[Dict[str, str]]:
    """Build records by pairing values by index across fields.

    Uses the maximum length across required fields to determine how many
    records to build. Shorter fields are cycled (round-robin) using modulo
    indexing so that adding an extra value in any field increases the number
    of outputs accordingly.
    """
    lengths = [len(section_options[field]) for field in REQUIRED_FIELDS]
    if not lengths:
        return []
    num_records = max(lengths)
    records: List[Dict[str, str]] = []
    for idx in range(num_records):
        record = {
            "name": section_options["name"][idx % len(section_options["name"])],
            "mail_id": section_options["mail_id"][idx % len(section_options["mail_id"])],
            "address": section_options["address"][idx % len(section_options["address"])],
            "city": section_options["city"][idx % len(section_options["city"])],
        }
        records.append(record)
    return records


def write_output_file(payload: Dict[str, Dict[str, str]], file_tag: Optional[str] = None) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S_%fZ")
    suffix = file_tag or ""
    outfile = OUTPUT_DIR / f"output_{ts}{suffix}.json"
    with outfile.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return outfile


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
        default=str(CONFIG_FILE),
        help="Path to the input JSON file containing required fields.",
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help=(
            "Create/overwrite a template input JSON at --config and exit. "
            "Edit it and rerun without --init."
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
            "Generate one JSON per paired record for the specified section name (e.g., Model_1). "
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
    
    # Model/section-specific generation: pair values by index and write one file per record
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
            edit_key, record = _select_random_edit_and_record(edits)
            payload = {f"{edit_key}_output_{i}": record}
            outfile = write_output_file(payload, file_tag=f"_{i}")
            print(f"Generated: {outfile}")
    else:
        payload = build_output_payload(edits, count=args.count)
        outfile = write_output_file(payload)
        print(f"Generated: {outfile}")


if __name__ == "__main__":
    main()



