#!/usr/bin/env python3
"""
Scenario Combinations Calculator
Calculates all possible combinations for specified fields from user_input.json
Includes separate calculations for positive, negative, and exclusion scenarios
No overlapping between scenario types
"""

import json
import itertools
from datetime import datetime
from typing import Dict, List, Any

def load_user_input(file_path: str = "user_input.json") -> Dict[str, Any]:
    """Load the user input JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {file_path}")
        return {}

def calculate_combinations(fields_data: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
    """Calculate all possible combinations of field values"""
    # Get all field names and their values
    field_names = list(fields_data.keys())
    field_values = list(fields_data.values())
    
    # Filter out empty fields
    valid_fields = [(name, values) for name, values in zip(field_names, field_values) if values]
    if not valid_fields:
        return []
    
    field_names, field_values = zip(*valid_fields)
    
    # Generate all combinations
    combinations = []
    for combo in itertools.product(*field_values):
        combination_dict = dict(zip(field_names, combo))
        combinations.append(combination_dict)
    
    return combinations

def extract_scenario_fields(model_data: Dict[str, Any]) -> Dict[str, List[Any]]:
    """Extract only the specific target fields from a model section"""
    target_fields = {
        "PRICNG_ZIP_STATE": [],
        "CLM_TYPE": [],
        "SRVC_FROM_DT": [],
        "HCID": [],
        "PAT_BRTH_DT": [],
        "PAT_FRST_NME": [],
        "PAT_LAST_NME": [],
        "ClaimDetails_SRVC_FROM_DT": [],
        "ClaimDetails_proc_cd": [],
        "ClaimDetails_BILL_TYPE": []
    }
    
    # Extract main fields
    for field in ["PRICNG_ZIP_STATE", "CLM_TYPE", "SRVC_FROM_DT", "HCID", 
                 "PAT_BRTH_DT", "PAT_FRST_NME", "PAT_LAST_NME"]:
        if field in model_data:
            target_fields[field] = model_data[field]
    
    # Extract ClaimDetails fields
    if "ClaimDetails" in model_data and model_data["ClaimDetails"]:
        claim_details = model_data["ClaimDetails"][0]  # Take first claim detail
        
        if "SRVC_FROM_DT" in claim_details:
            target_fields["ClaimDetails_SRVC_FROM_DT"] = claim_details["SRVC_FROM_DT"]
        if "proc_cd" in claim_details:
            target_fields["ClaimDetails_proc_cd"] = claim_details["proc_cd"]
        if "BILL_TYPE" in claim_details:
            target_fields["ClaimDetails_BILL_TYPE"] = claim_details["BILL_TYPE"]
    
    return target_fields

def generate_tabular_report(scenarios_data: Dict[str, Dict], all_combinations: Dict[str, List]) -> str:
    """Generate a tabular report for all scenario types"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = []
    report.append("=" * 100)
    report.append("SCENARIO COMBINATIONS REPORT - TABULAR FORMAT")
    report.append("=" * 100)
    report.append(f"Generated on: {timestamp}")
    report.append("")
    
    # Summary table
    report.append("-" * 100)
    report.append("SCENARIO SUMMARY TABLE")
    report.append("-" * 100)
    report.append(f"{'Scenario Type':<20} | {'Fields':<10} | {'Combinations':<15} | {'Description':<50}")
    report.append("-" * 100)
    
    total_combinations = 0
    for scenario_type, combinations in all_combinations.items():
        field_count = len([f for f in scenarios_data[scenario_type].values() if f])
        total_combinations += len(combinations)
        description = {
            "positive": "Valid data combinations for positive testing",
            "negative": "Invalid data combinations for negative testing", 
            "exclusion": "Edge case combinations for exclusion testing"
        }.get(scenario_type, "Data combinations")
        
        report.append(f"{scenario_type:<20} | {field_count:<10} | {len(combinations):<15} | {description}")
    
    report.append("-" * 100)
    report.append(f"{'TOTAL':<20} | {'':<10} | {total_combinations:<15} | All scenario combinations")
    report.append("")
    
    # Field values breakdown table
    report.append("-" * 100)
    report.append("FIELD VALUES BREAKDOWN BY SCENARIO TYPE")
    report.append("-" * 100)
    
    # Get all unique field names
    all_fields = set()
    for fields_data in scenarios_data.values():
        all_fields.update(fields_data.keys())
    
    all_fields = sorted(list(all_fields))
    
    # Header row
    header = f"{'Field Name':<25} | {'Positive':<15} | {'Negative':<15} | {'Exclusion':<15} | {'Total Values'}"
    report.append(header)
    report.append("-" * len(header))
    
    # Data rows
    for field in all_fields:
        positive_count = len(scenarios_data.get("positive", {}).get(field, []))
        negative_count = len(scenarios_data.get("negative", {}).get(field, []))
        exclusion_count = len(scenarios_data.get("exclusion", {}).get(field, []))
        total_values = positive_count + negative_count + exclusion_count
        
        row = f"{field:<25} | {positive_count:<15} | {negative_count:<15} | {exclusion_count:<15} | {total_values}"
        report.append(row)
    
    report.append("")
    
    # Mathematical breakdown table
    report.append("-" * 100)
    report.append("MATHEMATICAL BREAKDOWN BY SCENARIO TYPE")
    report.append("-" * 100)
    
    for scenario_type in ["positive", "negative", "exclusion"]:
        if scenario_type in scenarios_data and scenario_type in all_combinations:
            report.append(f"\n{scenario_type.upper()} SCENARIO:")
            report.append("-" * 50)
            
            field_counts = []
            field_formula = []
            
            for field_name, values in scenarios_data[scenario_type].items():
                if values:
                    field_counts.append(len(values))
                    field_formula.append(f"{field_name}({len(values)})")
                    report.append(f"  {field_name:<25} : {len(values)} values")
            
            if field_counts:
                total = 1
                for count in field_counts:
                    total *= count
                report.append(f"  {'Total Combinations':<25} : {total}")
                report.append(f"  {'Formula':<25} : {' × '.join(field_formula)} = {total}")
    
    report.append("")
    report.append("=" * 100)
    report.append("END OF REPORT")
    report.append("=" * 100)
    
    return "\n".join(report)

def main():
    """Main function"""
    print("Loading user input data...")
    user_data = load_user_input()
    
    if not user_data:
        print("Failed to load user input data")
        return
    
    # Define scenario types to analyze (excluding base)
    scenario_types = ["positive", "negative", "exclusion"]
    model_mapping = {
        "positive": "Model_1_positive",
        "negative": "Model_1_negative", 
        "exclusion": "Model_1_exclusion"
    }
    
    scenarios_data = {}
    all_combinations = {}
    
    print("Analyzing different scenario types...")
    
    # Process each scenario type
    for scenario_type in scenario_types:
        model_key = model_mapping[scenario_type]
        
        if model_key in user_data:
            print(f"Processing {scenario_type} scenarios from {model_key}...")
            
            # Extract fields for this scenario type
            fields_data = extract_scenario_fields(user_data[model_key])
            scenarios_data[scenario_type] = fields_data
            
            # Calculate combinations
            combinations = calculate_combinations(fields_data)
            all_combinations[scenario_type] = combinations
            
            print(f"  Found {len(combinations)} combinations for {scenario_type} scenarios")
        else:
            print(f"Warning: {model_key} not found in user input data")
            scenarios_data[scenario_type] = {}
            all_combinations[scenario_type] = []
    
    print("Generating tabular report...")
    report = generate_tabular_report(scenarios_data, all_combinations)
    
    # Save report to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tabular_scenario_combinations_report_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Tabular report generated successfully: {filename}")
    
    # Display summary
    print("\n" + "="*100)
    print("REPORT SUMMARY:")
    print("="*100)
    total_all = sum(len(combos) for combos in all_combinations.values())
    print(f"Total combinations across all scenarios: {total_all}")
    
    for scenario_type, combinations in all_combinations.items():
        print(f"{scenario_type.capitalize()} scenarios: {len(combinations)} combinations")
    
    print(f"\nDetailed tabular report saved to: {filename}")

if __name__ == "__main__":
    main()
