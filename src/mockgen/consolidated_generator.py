#!/usr/bin/env python3
"""
Consolidated Mock Data Generator
Combines all functionality from multiple scripts into a single, comprehensive tool.

This script replaces:
- generate_wgs_format.py
- generate_separate_jsons.py  
- generate_output_json.py
- create_project_report.py

Usage:
    python consolidated_generator.py --help
    python consolidated_generator.py --positive --model Model_1
    python consolidated_generator.py --negative
    python consolidated_generator.py --exclusion
    python consolidated_generator.py --report
"""

import json
import random
import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import os

class ConsolidatedGenerator:
    """Unified generator for all mock data scenarios."""
    
    def __init__(self, config_file: str = "user_input.json", output_dir: str = "generated_outputs"):
        self.config_file = Path(config_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load the configuration file."""
        try:
            with self.config_file.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as exc:
            raise SystemExit(f"Could not read configuration from '{self.config_file}': {exc}")
    
    def _get_model_names(self) -> List[str]:
        """Get base model names without probability type suffixes."""
        base_models = set()
        for key in self.config.keys():
            if any(suffix in key.lower() for suffix in ["_positive", "_negative", "_exclusion"]):
                base_name = key.lower().replace("_positive", "").replace("_negative", "").replace("_exclusion", "")
                base_models.add(base_name)
            else:
                base_models.add(key)
        return list(base_models)
    
    def _get_probability_data(self, model_name: str, probability_type: str) -> Optional[Dict[str, List[str]]]:
        """Get data for a specific model and probability type."""
        suffixes = [f"_{probability_type}", f"_{probability_type.lower()}"]
        
        for suffix in suffixes:
            key = f"{model_name}{suffix}"
            if key in self.config:
                return self.config[key]
            
            # Try with capitalized model name
            key_cap = f"{model_name.capitalize()}{suffix}"
            if key_cap in self.config:
                return self.config[key_cap]
        
        return None
    
    def generate_wgs_format(self, data: Dict[str, List[str]], probability_type: str) -> Dict[str, Any]:
        """Generate output in WGS format matching the exact template structure."""
        key_name = f"WGS_csbd_medicaid_{probability_type.lower()}"
        
        output = {}
        
        # Add all the template fields in the exact order from the reference template
        template_fields = [
            "first_proc_cd", "last_proc_cd", "email", "phone", "date_of_birth",
            "street_address", "proc_cd", "mail_id", "address", "city", "state",
            "zip_code", "country", "PRICNG_ZIP_STATE", "CLM_TYPE", "SRVC_FROM_DT",
            "HCID", "PAT_BRTH_DT", "PAT_FRST_NME", "PAT_LAST_NME", "ClaimDetails"
        ]
        
        # Initialize output with empty values - will be populated from user_input.json
        for field in template_fields:
            output[field] = []
        
        # Add probability-specific data from user_input.json
        for field, values in data.items():
            if field == "ClaimDetails":
                # Handle ClaimDetails specially - ensure it uses the structure from user_input.json
                if isinstance(values, list) and len(values) > 0:
                    claim_detail = values[0]  # Take the first claim detail
                    if isinstance(claim_detail, dict):
                        # Ensure each field in ClaimDetails uses values from user_input.json
                        processed_claim = {}
                        for claim_field, claim_values in claim_detail.items():
                            if isinstance(claim_values, list) and len(claim_values) > 0:
                                # For all scenarios, randomly select one value to ensure variety
                                processed_claim[claim_field] = random.choice(claim_values)
                            else:
                                processed_claim[claim_field] = claim_values
                        output[field] = [processed_claim]
                    else:
                        output[field] = values
                else:
                    output[field] = values
            else:
                # For other fields, use values from user_input.json
                if isinstance(values, list) and len(values) > 0:
                    # For all scenarios, randomly select one value to ensure variety
                    output[field] = [random.choice(values)]
                else:
                    output[field] = values
        
        # Ensure all template fields have values (use random value from user input if available)
        for field in template_fields:
            if not output[field] or len(output[field]) == 0:
                # If field is empty, try to get a default value from the data
                if field in data and isinstance(data[field], list) and len(data[field]) > 0:
                    output[field] = [random.choice(data[field])]  # Randomly select one value
                else:
                    # Provide a fallback default value
                    output[field] = ["Default Value"]
        
        return {key_name: output}
    
    def generate_standard_format(self, data: Dict[str, List[str]], probability_type: str) -> Dict[str, Any]:
        """Generate output in standard format."""
        # For all scenarios, randomly select one value for each field to ensure variety
        processed_data = {}
        for field, values in data.items():
            if field == "ClaimDetails":
                # Handle ClaimDetails specially
                if isinstance(values, list) and len(values) > 0:
                    claim_detail = values[0]
                    if isinstance(claim_detail, dict):
                        processed_claim = {}
                        for claim_field, claim_values in claim_detail.items():
                            if isinstance(claim_values, list) and len(claim_values) > 0:
                                processed_claim[claim_field] = random.choice(claim_values)
                            else:
                                processed_claim[claim_field] = claim_values
                        processed_data[field] = [processed_claim]
                    else:
                        processed_data[field] = values
                else:
                    processed_data[field] = values
            else:
                if isinstance(values, list) and len(values) > 0:
                    processed_data[field] = [random.choice(values)]
                else:
                    processed_data[field] = values
        return {f"{probability_type.lower()}_data": processed_data}
    
    def generate_scenarios(self, scenario_type: str, model: Optional[str] = None, 
                          count: int = 1, split: bool = False, wgs_format: bool = False):
        """Generate scenarios for specified type and model(s)."""
        models = [model] if model else self._get_model_names()
        
        for model_name in models:
            data = self._get_probability_data(model_name, scenario_type)
            if not data:
                print(f"Warning: No {scenario_type} data found for {model_name}")
                continue
            
            if wgs_format:
                output = self.generate_wgs_format(data, scenario_type)
            else:
                output = self.generate_standard_format(data, scenario_type)
            
            if split:
                # Generate separate files for each record
                for i in range(count):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{model_name}_{scenario_type}_{timestamp}_{i+1:06d}Z.json"
                    filepath = self.output_dir / filename
                    
                    # Regenerate output for each record to get different random values
                    if wgs_format:
                        record_output = self.generate_wgs_format(data, scenario_type)
                    else:
                        record_output = self.generate_standard_format(data, scenario_type)
                    
                    with filepath.open("w", encoding="utf-8") as f:
                        json.dump(record_output, f, indent=2, ensure_ascii=False)
                    print(f"Generated: {filepath}")
            else:
                # Generate single file with multiple records
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{model_name}_{scenario_type}_{timestamp}.json"
                filepath = self.output_dir / filename
                
                # If count > 1, create array of outputs with different random values for each
                if count > 1:
                    final_output = []
                    for i in range(count):
                        # Regenerate the output for each record to get different random values
                        if wgs_format:
                            record_output = self.generate_wgs_format(data, scenario_type)
                        else:
                            record_output = self.generate_standard_format(data, scenario_type)
                        final_output.append(record_output)
                else:
                    final_output = output
                
                with filepath.open("w", encoding="utf-8") as f:
                    json.dump(final_output, f, indent=2, ensure_ascii=False)
                print(f"Generated: {filepath}")
    
    def generate_all_scenarios(self, wgs_format: bool = False, count: int = 1, split: bool = False):
        """Generate all scenario types for all models."""
        for scenario_type in ["positive", "negative", "exclusion"]:
            print(f"\nGenerating {scenario_type} scenarios...")
            self.generate_scenarios(scenario_type, count=count, split=split, wgs_format=wgs_format)
    
    def generate_combined_output(self, wgs_format: bool = False):
        """Generate a single combined output file with all scenarios."""
        combined = {}
        
        for model_name in self._get_model_names():
            model_data = {}
            for scenario_type in ["positive", "negative", "exclusion"]:
                data = self._get_probability_data(model_name, scenario_type)
                if data:
                    if wgs_format:
                        model_data[scenario_type] = self.generate_wgs_format(data, scenario_type)
                    else:
                        model_data[scenario_type] = self.generate_standard_format(data, scenario_type)
            
            if model_data:
                combined[model_name] = model_data
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"combined_all_scenarios_{timestamp}.json"
        filepath = self.output_dir / filename
        
        with filepath.open("w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)
        print(f"Generated combined output: {filepath}")
    
    def list_models(self):
        """List available models and their scenario types."""
        print("Available Models and Scenarios:")
        print("=" * 50)
        
        for model_name in self._get_model_names():
            print(f"\n{model_name}:")
            for scenario_type in ["positive", "negative", "exclusion"]:
                data = self._get_probability_data(model_name, scenario_type)
                status = "✓" if data else "✗"
                print(f"  {scenario_type}: {status}")
    
    def generate_project_report(self):
        """Generate a comprehensive project report."""
        report = {
            "generation_timestamp": datetime.now().isoformat(),
            "config_file": str(self.config_file),
            "output_directory": str(self.output_dir),
            "models": {},
            "statistics": {
                "total_models": len(self._get_model_names()),
                "total_scenarios": 0
            }
        }
        
        for model_name in self._get_model_names():
            model_info = {"scenarios": {}}
            for scenario_type in ["positive", "negative", "exclusion"]:
                data = self._get_probability_data(model_name, scenario_type)
                if data:
                    model_info["scenarios"][scenario_type] = {
                        "fields_count": len(data),
                        "has_claim_details": "ClaimDetails" in data
                    }
                    report["statistics"]["total_scenarios"] += 1
            
            report["models"][model_name] = model_info
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"project_report_{timestamp}.json"
        filepath = self.output_dir / filename
        
        with filepath.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"Generated project report: {filepath}")
        
        # Also print summary
        print(f"\nProject Summary:")
        print(f"Total Models: {report['statistics']['total_models']}")
        print(f"Total Scenarios: {report['statistics']['total_scenarios']}")

def main():
    parser = argparse.ArgumentParser(
        description="Consolidated Mock Data Generator - All-in-one tool for generating mock scenarios",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Generate positive scenarios for specific model
    python consolidated_generator.py --positive --model Model_1
    
    # Generate negative scenarios
    python consolidated_generator.py --negative
    
    # Generate exclusion scenarios
    python consolidated_generator.py --exclusion
    
    # Generate combined output
    python consolidated_generator.py --combined
    
    # Generate all scenario types (requires --wgs)
    python consolidated_generator.py --all --wgs --count 32 --split
    
    # Generate project report
    python consolidated_generator.py --report
    
    # List available models
    python consolidated_generator.py --list
    

        """
    )
    
    # Scenario type options
    scenario_group = parser.add_mutually_exclusive_group()
    scenario_group.add_argument("--all", action="store_true", help="Generate all scenario types (requires --wgs flag)")
    scenario_group.add_argument("--positive", action="store_true", help="Generate positive scenarios")
    scenario_group.add_argument("--negative", action="store_true", help="Generate negative scenarios")
    scenario_group.add_argument("--exclusion", action="store_true", help="Generate exclusion scenarios")
    scenario_group.add_argument("--combined", action="store_true", help="Generate combined output file")
    scenario_group.add_argument("--list", action="store_true", help="List available models and scenarios")
    scenario_group.add_argument("--report", action="store_true", help="Generate project report")
    
    # Other options
    parser.add_argument("--model", type=str, help="Generate output for specific model")
    parser.add_argument("--count", type=int, default=1, help="Number of records to generate (default: 1, max: 100)")
    parser.add_argument("--split", action="store_true", help="Generate separate files for each record")
    parser.add_argument("--wgs", action="store_true", help="Use WGS format for output")
    parser.add_argument("--config", type=str, default="user_input.json", help="Path to config file")
    parser.add_argument("--output-dir", type=str, default="generated_outputs", help="Output directory")
    
    args = parser.parse_args()
    
    # Validate that --all requires --wgs
    if args.all and not args.wgs:
        parser.error("--all requires --wgs flag to be specified")
    
    if not any([args.positive, args.negative, args.exclusion, 
                args.combined, args.list, args.report, args.all]):
        parser.print_help()
        return
    
    try:
        generator = ConsolidatedGenerator(args.config, args.output_dir)
        
        if args.list:
            generator.list_models()
        elif args.report:
            generator.generate_project_report()
        elif args.all:
            # Generate all scenario types with WGS format
            generator.generate_scenarios("positive", args.model, args.count, args.split, True)
            generator.generate_scenarios("negative", args.model, args.count, args.split, True)
            generator.generate_scenarios("exclusion", args.model, args.count, args.split, True)
        elif args.combined:
            generator.generate_combined_output(wgs_format=args.wgs)
        else:
            # Single scenario type
            if args.positive:
                generator.generate_scenarios("positive", args.model, args.count, args.split, args.wgs)
            elif args.negative:
                generator.generate_scenarios("negative", args.model, args.count, args.split, args.wgs)
            elif args.exclusion:
                generator.generate_scenarios("exclusion", args.model, args.count, args.split, args.wgs)
        
        print("\nGeneration completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
