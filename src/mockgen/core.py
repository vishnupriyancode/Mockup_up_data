from __future__ import annotations

import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


CONFIG_FILE = Path("user_input.json")
MASTER_TEMPLATE_FILE = Path("master.json")
OUTPUT_DIR = Path("mock_outputs")
REQUIRED_FIELDS: List[str] = ["name", "mail_id", "address", "city"]


def ensure_config_file(path: Path, overwrite: bool = False) -> None:
    if path.exists() and not overwrite:
        return
    template = {
        "Model_1": {
            "name": ["Vishnu", "Priyan", "Raja", "Raji"],
            "mail_id": ["Vishnupriyannatarajan@gmail.com", "ramdon@gamil.com", "ram@gamil.com"],
            "address": ["123456", "12345", "654321", "123"],
            "city": ["Hyderabad", "Chennai", "Kovai", "Dindigul"]
        },
        "Model_1_Positive": {
            "name": ["Vishnu", "Priyan", "Raja", "Raji"],
            "mail_id": ["Vishnupriyannatarajan@gmail.com", "ramdon@gamil.com", "ram@gamil.com"],
            "address": ["123456", "12345", "654321", "123"],
            "city": ["Hyderabad", "Chennai", "Kovai", "Dindigul"]
        },
        "Model_1_Negative": {
            "name": ["", "123", "@@@"],
            "mail_id": ["invalid-email", "no-at-symbol", "user@invalid_domain"],
            "address": ["", "!@#", "????"],
            "city": ["", "Atlantis", "12345"]
        }
    }
    with path.open("w", encoding="utf-8") as f:
        json.dump(template, f, indent=2, ensure_ascii=False)


def load_master_template(path: Path) -> Dict[str, Any]:
    """Load the master template JSON file."""
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except (json.JSONDecodeError, OSError) as exc:
        raise SystemExit(
            f"Could not read master template from '{path}': {exc}. Ensure the file exists and is valid JSON."
        )


def load_user_config(path: Path) -> Dict[str, Dict[str, List[str]]]:
    """Load user configuration with improved model handling."""
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        raise SystemExit(
            f"Could not read configuration from '{path}': {exc}. Edit the file and rerun."
        )

    # Handle the new model-based structure
    if any(key.startswith("Model_") for key in data.keys()):
        parsed: Dict[str, Dict[str, List[str]]] = {}
        for model_key, model_data in data.items():
            if not isinstance(model_data, dict):
                continue
            parsed[model_key] = {}
            for field, values in model_data.items():
                if isinstance(values, list):
                    parsed[model_key][field] = values
                elif isinstance(values, str):
                    # Convert comma-separated string to list
                    parsed[model_key][field] = [v.strip() for v in values.split(",") if v.strip()]
                else:
                    parsed[model_key][field] = [str(values)]
        return parsed

    # Fallback to old format handling
    if any(key.startswith("Edit_") for key in data.keys()):
        parsed: Dict[str, Dict[str, List[str]]] = {}
        for section_key, section_data in data.items():
            if not section_key.startswith("Edit_"):
                continue
            parsed[section_key] = {}
            missing_or_empty: List[str] = []
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
            raise SystemExit(f"No valid 'Edit_X' sections found in '{path}'.")
        return parsed

    # Handle flat structure
    if all(isinstance(v, dict) for v in data.values()):
        parsed = {}
        for section_key, section_data in data.items():
            if not isinstance(section_data, dict):
                continue
            missing_or_empty: List[str] = []
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

    # Handle single section
    missing_or_empty: List[str] = []
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


def merge_brd_with_master(master_data: Dict[str, Any], brd_data: Dict[str, Any]) -> Dict[str, Any]:
    """Merge BRD requirements with master template to create enhanced configuration."""
    merged = master_data.copy()
    
    # For each model in BRD, merge with master template
    for model_key, model_data in brd_data.items():
        if model_key not in merged:
            merged[model_key] = {}
        
        # Start with master template fields as base
        if "user_profile" in master_data:
            for field, values in master_data["user_profile"].items():
                merged[model_key][field] = values
        
        # Override/add BRD-specific fields
        for field, values in model_data.items():
            merged[model_key][field] = values
    
    return merged


def generate_model_outputs(merged_config: Dict[str, Any], selected_models: List[str] = None) -> Dict[str, Any]:
    """Generate output JSON for selected models based on merged configuration."""
    if selected_models is None:
        # If no models specified, use all models from BRD
        selected_models = [key for key in merged_config.keys() if not key.startswith("user_profile")]
    
    outputs = {}
    
    for model in selected_models:
        if model not in merged_config:
            continue
            
        model_data = merged_config[model]
        model_output = {}
        
        # Generate records for each field
        for field, values in model_data.items():
            if isinstance(values, list) and values:
                # Randomly select from available values
                model_output[field] = random.choice(values)
            elif isinstance(values, str):
                # Single value, use as is
                model_output[field] = values
            else:
                # Fallback to empty string if no valid values
                model_output[field] = ""
        
        outputs[model] = model_output
    
    return outputs


def generate_multiple_model_outputs(merged_config: Dict[str, Any], selected_models: List[str] = None, count: int = 1) -> List[Dict[str, Any]]:
    """Generate multiple output JSONs for selected models."""
    outputs_list = []
    
    for i in range(count):
        output = generate_model_outputs(merged_config, selected_models)
        outputs_list.append(output)
    
    return outputs_list


def generate_model_records(model_data: Dict[str, List[str]], count: int = 1) -> List[Dict[str, str]]:
    """Generate multiple records for a specific model."""
    records = []
    
    for i in range(count):
        record = {}
        for field, values in model_data.items():
            if isinstance(values, list) and values:
                record[field] = random.choice(values)
            elif isinstance(values, str):
                record[field] = values
            else:
                record[field] = ""
        records.append(record)
    
    return records


def write_enhanced_output_file(payload: Dict[str, Any], file_tag: Optional[str] = None) -> Path:
    """Write enhanced output to file with timestamp."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S_%fZ")
    suffix = file_tag or ""
    outfile = OUTPUT_DIR / f"enhanced_output_{ts}{suffix}.json"
    
    with outfile.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")
    
    return outfile


def write_model_output_file(payload: Dict[str, Any], model_name: str, file_tag: Optional[str] = None) -> Path:
    """Write model-specific output to file with timestamp."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S_%fZ")
    suffix = file_tag or ""
    outfile = OUTPUT_DIR / f"{model_name}_output_{ts}{suffix}.json"
    
    with outfile.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")
    
    return outfile


def _to_choice_list(value: Any) -> List[str]:
    if isinstance(value, list):
        items = [str(v).strip() for v in value]
    elif isinstance(value, str):
        items = [v.strip() for v in value.split(",")]
    else:
        items = [str(value).strip()]
    return [v for v in items if v]


def _select_random_record_from_edit(edit_options: Dict[str, List[str]]) -> Dict[str, str]:
    return {
        "name": random.choice(edit_options["name"]),
        "mail_id": random.choice(edit_options["mail_id"]),
        "address": random.choice(edit_options["address"]),
        "city": random.choice(edit_options["city"]),
    }


def _select_random_edit_and_record(
    edits: Dict[str, Dict[str, List[str]]]
) -> Tuple[str, Dict[str, str]]:
    edit_key = random.choice(list(edits.keys()))
    record = _select_random_record_from_edit(edits[edit_key])
    return edit_key, record


def build_output_payload(
    edits: Dict[str, Dict[str, List[str]]], count: int
) -> Dict[str, Dict[str, str]]:
    payload: Dict[str, Dict[str, str]] = {}
    for i in range(1, max(1, count) + 1):
        edit_key, record = _select_random_edit_and_record(edits)
        payload[f"{edit_key}_output_{i}"] = record
    return payload


def build_indexed_records(section_options: Dict[str, List[str]]) -> List[Dict[str, str]]:
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


