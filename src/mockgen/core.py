from __future__ import annotations

import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


CONFIG_FILE = Path("user_input.json")
MASTER_TEMPLATE_FILE = Path("master.json")
OUTPUT_DIR = Path("mock_outputs")
REQUIRED_FIELDS: List[str] = ["PRICNG_ZIP_STATE", "CLM_TYPE", "SRVC_FROM_DT", "HCID", "PAT_BRTH_DT", "PAT_FRST_NME", "PAT_LAST_NME", "ClaimDetails"]


def ensure_config_file(path: Path, overwrite: bool = False) -> None:
    if path.exists() and not overwrite:
        return
    template = {
        "Model_1": {
            "PRICNG_ZIP_STATE": ["TN", "KL", "AP", "KT"],
            "CLM_TYPE": ["P", "C", "D"],
            "SRVC_FROM_DT": ["04/20/2025"],
            "HCID": ["ABCDEFGHI", "ABCDEFGHI", "ABCDE5555", "555DEFGHI"],
            "PAT_BRTH_DT": ["01/01/1990", "01/02/1990", "01/03/1990", "01/04/1990"],
            "PAT_FRST_NME": ["Mohan", "Raj", "Rajesh", "Rajeshwari"],
            "PAT_LAST_NME": ["Kumar", "AJ", "VP", "D"],
            "ClaimDetails": [
                {
                    "SRVC_FROM_DT": ["12/12/2024"],
                    "proc_cd": ["12345", "67890", "12394", "30009"],
                    "BILL_TYPE": ["P"]
                }
            ]
        },
        "Model_1_positive": {
            "PRICNG_ZIP_STATE": ["TN", "KL"],
            "CLM_TYPE": ["P"],
            "SRVC_FROM_DT": ["04/20/2025"],
            "HCID": ["ABCDEFGHI", "ABCDEFGHI"],
            "PAT_BRTH_DT": ["01/01/1990"],
            "PAT_FRST_NME": ["Mohan", "Raj"],
            "PAT_LAST_NME": ["Kumar", "AJ"],
            "ClaimDetails": [
                {
                    "SRVC_FROM_DT": ["12/12/2024"],
                    "proc_cd": ["12345", "67890", "12394", "30009"],
                    "BILL_TYPE": ["P"]
                }
            ]
        },
        "Model_1_negative": {
            "PRICNG_ZIP_STATE": ["AP", "KT"],
            "CLM_TYPE": ["C", "D"],
            "SRVC_FROM_DT": ["04/20/2025"],
            "HCID": ["ABCDE5555", "555DEFGHI"],
            "PAT_BRTH_DT": ["01/03/1990", "01/04/1990"],
            "PAT_FRST_NME": ["Rajesh", "Rajeshwari"],
            "PAT_LAST_NME": ["VP", "D"],
            "ClaimDetails": [
                {
                    "SRVC_FROM_DT": ["12/12/2024"],
                    "proc_cd": ["12345", "67890", "12394", "30009"],
                    "BILL_TYPE": ["P"]
                }
            ]
        },
        "Model_1_exclusion": {
            "PRICNG_ZIP_STATE": ["KT"],
            "CLM_TYPE": ["P", "D"],
            "SRVC_FROM_DT": ["04/20/2025"],
            "HCID": ["555DEFGHI"],
            "PAT_BRTH_DT": ["01/04/1990"],
            "PAT_FRST_NME": ["Rajeshwari"],
            "PAT_LAST_NME": ["AJ"],
            "ClaimDetails": [
                {
                    "SRVC_FROM_DT": ["12/12/2024"],
                    "proc_cd": ["12345", "30009"],
                    "BILL_TYPE": ["P"]
                }
            ]
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
                # Handle nested structures (like ClaimDetails)
                if field == "ClaimDetails" and values and isinstance(values[0], dict):
                    # Process nested ClaimDetails structure
                    processed_claim_details = []
                    for claim_detail in values:
                        processed_claim = {}
                        for nested_field, nested_values in claim_detail.items():
                            if isinstance(nested_values, list) and nested_values:
                                # Randomly select from available values
                                processed_claim[nested_field] = random.choice(nested_values)
                            elif isinstance(nested_values, str):
                                # Single value, use as is
                                processed_claim[nested_field] = nested_values
                            else:
                                # Fallback to empty string if no valid values
                                processed_claim[nested_field] = ""
                        processed_claim_details.append(processed_claim)
                    model_output[field] = processed_claim_details
                else:
                    # Randomly select from available values for flat fields
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
                # Handle nested structures (like ClaimDetails)
                if field == "ClaimDetails" and values and isinstance(values[0], dict):
                    # Process nested ClaimDetails structure
                    processed_claim_details = []
                    for claim_detail in values:
                        processed_claim = {}
                        for nested_field, nested_values in claim_detail.items():
                            if isinstance(nested_values, list) and nested_values:
                                # Randomly select from available values
                                processed_claim[nested_field] = random.choice(nested_values)
                            elif isinstance(nested_values, str):
                                # Single value, use as is
                                processed_claim[nested_field] = nested_values
                            else:
                                # Fallback to empty string if no valid values
                                processed_claim[nested_field] = ""
                        processed_claim_details.append(processed_claim)
                    record[field] = processed_claim_details
                else:
                    # Randomly select from available values for flat fields
                    record[field] = random.choice(values)
            elif isinstance(values, str):
                # Single value, use as is
                record[field] = values
            else:
                # Fallback to empty string if no valid values
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
    record = {}
    for field, values in edit_options.items():
        if isinstance(values, list) and values:
            # Handle nested structures (like ClaimDetails)
            if field == "ClaimDetails" and values and isinstance(values[0], dict):
                # Process nested ClaimDetails structure
                processed_claim_details = []
                for claim_detail in values:
                    processed_claim = {}
                    for nested_field, nested_values in claim_detail.items():
                        if isinstance(nested_values, list) and nested_values:
                            # Randomly select from available values
                            processed_claim[nested_field] = random.choice(nested_values)
                        elif isinstance(nested_values, str):
                            # Single value, use as is
                            processed_claim[nested_field] = nested_values
                        else:
                            # Fallback to empty string if no valid values
                            processed_claim[nested_field] = ""
                    processed_claim_details.append(processed_claim)
                record[field] = processed_claim_details
            else:
                # Randomly select from available values for flat fields
                record[field] = random.choice(values)
        else:
            record[field] = ""
    return record


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
        record = {}
        for field, values in section_options.items():
            if isinstance(values, list) and values:
                # Handle nested structures (like ClaimDetails)
                if field == "ClaimDetails" and values and isinstance(values[0], dict):
                    # Process nested ClaimDetails structure
                    processed_claim_details = []
                    for claim_detail in values:
                        processed_claim = {}
                        for nested_field, nested_values in claim_detail.items():
                            if isinstance(nested_values, list) and nested_values:
                                # Use indexed selection for nested fields
                                nested_idx = idx % len(nested_values)
                                processed_claim[nested_field] = nested_values[nested_idx]
                            elif isinstance(nested_values, str):
                                # Single value, use as is
                                processed_claim[nested_field] = nested_values
                            else:
                                # Fallback to empty string if no valid values
                                processed_claim[nested_field] = ""
                        processed_claim_details.append(processed_claim)
                    record[field] = processed_claim_details
                else:
                    # Use indexed selection for flat fields (original behavior)
                    record[field] = values[idx % len(values)]
            else:
                record[field] = ""
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


