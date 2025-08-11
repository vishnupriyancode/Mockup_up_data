#!/usr/bin/env python3
"""
Probability Output Generator for Mock Data

This script generates JSON outputs for positive, negative, and exclusion probabilities
based on the user_input.json configuration without affecting the existing codebase.

Usage:
    python generate_probability_outputs.py --help
    python generate_probability_outputs.py --all
    python generate_probability_outputs.py --positive
    python generate_probability_outputs.py --negative
    python generate_probability_outputs.py --exclusion
    python generate_probability_outputs.py --model Model_1
    python generate_probability_outputs.py --count 5
"""

import json
import random
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional


class ProbabilityOutputGenerator:
    """Generate probability-based outputs for mock data."""
    
    def __init__(self, config_file: str = "user_input.json", output_dir: str = "mock_outputs"):
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
        """Get base model names (without _Positive, _Negative, _Exclusion suffixes)."""
        base_models = set()
        for key in self.config.keys():
            if "_Positive" in key or "_Negative" in key or "_Exclusion" in key:
                base_name = key.replace("_Positive", "").replace("_Negative", "").replace("_Exclusion", "")
                base_models.add(base_name)
            else:
                base_models.add(key)
        return list(base_models)
    
    def _get_probability_data(self, model_name: str, probability_type: str) -> Optional[Dict[str, List[str]]]:
        """Get data for a specific model and probability type."""
        key = f"{model_name}_{probability_type}"
        return self.config.get(key)
    
    def _generate_single_record(self, data: Dict[str, List[str]]) -> Dict[str, str]:
        """Generate a single record from probability data."""
        record = {}
        for field, values in data.items():
            if isinstance(values, list) and values:
                record[field] = random.choice(values)
            else:
                record[field] = ""
        return record
    
    def _wrap_in_user_profile(self, record: Dict[str, str]) -> Dict[str, Any]:
        """Wrap the record in user_profile structure to match master template format."""
        # Load master template to get the complete structure
        try:
            with open("master.json", "r", encoding="utf-8") as f:
                master_template = json.load(f)
            
            # Start with master template and replace only user_input fields
            output = master_template.copy()
            for field, value in record.items():
                if field in output.get("user_profile", {}):
                    output["user_profile"][field] = value
            
            # Convert array values to single values
            for field, value in output["user_profile"].items():
                if isinstance(value, list) and len(value) == 1:
                    output["user_profile"][field] = value[0]
            
            return output
        except FileNotFoundError:
            # Fallback to simple structure if master.json not found
            return {"user_profile": record}
    
    def _generate_multiple_records(self, data: Dict[str, List[str]], count: int) -> List[Dict[str, str]]:
        """Generate multiple records from probability data."""
        records = []
        for _ in range(count):
            records.append(self._generate_single_record(data))
        return records
    
    def _write_output_file(self, data: Any, filename: str) -> Path:
        """Write output to a JSON file."""
        timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S_%fZ")
        outfile = self.output_dir / f"{filename}_{timestamp}.json"
        
        with outfile.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        
        return outfile
    
    def generate_positive_outputs(self, count: int = 1, model_name: Optional[str] = None) -> List[Path]:
        """Generate positive probability outputs."""
        outputs = []
        models = [model_name] if model_name else self._get_model_names()
        
        for model in models:
            positive_data = self._get_probability_data(model, "Positive")
            if positive_data:
                if count == 1:
                    record = self._generate_single_record(positive_data)
                    wrapped_record = self._wrap_in_user_profile(record)
                    data = {f"{model}_Positive": wrapped_record}
                else:
                    records = self._generate_multiple_records(positive_data, count)
                    wrapped_records = [self._wrap_in_user_profile(record) for record in records]
                    data = {f"{model}_Positive": wrapped_records}
                
                outfile = self._write_output_file(data, f"{model}_Positive")
                outputs.append(outfile)
                print(f"Generated Positive output: {outfile}")
        
        return outputs
    
    def generate_negative_outputs(self, count: int = 1, model_name: Optional[str] = None) -> List[Path]:
        """Generate negative probability outputs."""
        outputs = []
        models = [model_name] if model_name else self._get_model_names()
        
        for model in models:
            negative_data = self._get_probability_data(model, "Negative")
            if negative_data:
                if count == 1:
                    record = self._generate_single_record(negative_data)
                    wrapped_record = self._wrap_in_user_profile(record)
                    data = {f"{model}_Negative": wrapped_record}
                else:
                    records = self._generate_multiple_records(negative_data, count)
                    wrapped_records = [self._wrap_in_user_profile(record) for record in records]
                    data = {f"{model}_Negative": wrapped_records}
                
                outfile = self._write_output_file(data, f"{model}_Negative")
                outputs.append(outfile)
                print(f"Generated Negative output: {outfile}")
        
        return outputs
    
    def generate_exclusion_outputs(self, count: int = 1, model_name: Optional[str] = None) -> List[Path]:
        """Generate exclusion probability outputs."""
        outputs = []
        models = [model_name] if model_name else self._get_model_names()
        
        for model in models:
            exclusion_data = self._get_probability_data(model, "Exclusion")
            if exclusion_data:
                if count == 1:
                    record = self._generate_single_record(exclusion_data)
                    wrapped_record = self._wrap_in_user_profile(record)
                    data = {f"{model}_Exclusion": wrapped_record}
                else:
                    records = self._generate_multiple_records(exclusion_data, count)
                    wrapped_records = [self._wrap_in_user_profile(record) for record in records]
                    data = {f"{model}_Exclusion": wrapped_records}
                
                outfile = self._write_output_file(data, f"{model}_Exclusion")
                outputs.append(outfile)
                print(f"Generated Exclusion output: {outfile}")
        
        return outputs
    
    def generate_all_probabilities(self, count: int = 1, model_name: Optional[str] = None) -> List[Path]:
        """Generate all probability types for specified models."""
        outputs = []
        models = [model_name] if model_name else self._get_model_names()
        
        for model in models:
            model_outputs = {}
            
            # Generate positive
            positive_data = self._get_probability_data(model, "Positive")
            if positive_data:
                if count == 1:
                    model_outputs[f"{model}_Positive"] = self._wrap_in_user_profile(self._generate_single_record(positive_data))
                else:
                    model_outputs[f"{model}_Positive"] = [self._wrap_in_user_profile(record) for record in self._generate_multiple_records(positive_data, count)]
            
            # Generate negative
            negative_data = self._get_probability_data(model, "Negative")
            if negative_data:
                if count == 1:
                    model_outputs[f"{model}_Negative"] = self._wrap_in_user_profile(self._generate_single_record(negative_data))
                else:
                    model_outputs[f"{model}_Negative"] = [self._wrap_in_user_profile(record) for record in self._generate_multiple_records(negative_data, count)]
            
            # Generate exclusion
            exclusion_data = self._get_probability_data(model, "Exclusion")
            if exclusion_data:
                if count == 1:
                    model_outputs[f"{model}_Exclusion"] = self._wrap_in_user_profile(self._generate_single_record(exclusion_data))
                else:
                    model_outputs[f"{model}_Exclusion"] = [self._wrap_in_user_profile(record) for record in self._generate_multiple_records(exclusion_data, count)]
            
            if model_outputs:
                outfile = self._write_output_file(model_outputs, f"{model}_All_Probabilities")
                outputs.append(outfile)
                print(f"Generated All Probabilities output: {outfile}")
        
        return outputs
    
    def list_available_models(self):
        """List all available models and their probability types."""
        print("Available Models and Probability Types:")
        print("=" * 50)
        
        for model in self._get_model_names():
            print(f"\n{model}:")
            positive = "✓" if f"{model}_Positive" in self.config else "✗"
            negative = "✓" if f"{model}_Negative" in self.config else "✗"
            exclusion = "✓" if f"{model}_Exclusion" in self.config else "✗"
            
            print(f"  Positive: {positive}")
            print(f"  Negative: {negative}")
            print(f"  Exclusion: {exclusion}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate probability-based mock data outputs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all probability types for all models
  python generate_probability_outputs.py --all
  
  # Generate only positive probabilities
  python generate_probability_outputs.py --positive
  
  # Generate negative probabilities for specific model
  python generate_probability_outputs.py --negative --model Model_1
  
  # Generate multiple records
  python generate_probability_outputs.py --all --count 5
  
  # List available models
  python generate_probability_outputs.py --list
        """
    )
    
    parser.add_argument(
        "--config",
        default="user_input.json",
        help="Path to configuration file (default: user_input.json)"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        default="mock_outputs",
        help="Output directory for generated files (default: mock_outputs)"
    )
    
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Generate all probability types (positive, negative, exclusion)"
    )
    
    parser.add_argument(
        "--positive", "-p",
        action="store_true",
        help="Generate positive probability outputs"
    )
    
    parser.add_argument(
        "--negative", "-n",
        action="store_true",
        help="Generate negative probability outputs"
    )
    
    parser.add_argument(
        "--exclusion", "-e",
        action="store_true",
        help="Generate exclusion probability outputs"
    )
    
    parser.add_argument(
        "--model", "-m",
        help="Generate outputs for specific model only"
    )
    
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=1,
        help="Number of records to generate per probability type (default: 1)"
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available models and their probability types"
    )
    
    args = parser.parse_args()
    
    try:
        generator = ProbabilityOutputGenerator(args.config, args.output_dir)
        
        if args.list:
            generator.list_available_models()
            return
        
        if not any([args.all, args.positive, args.negative, args.exclusion]):
            print("No probability type specified. Use --help for usage information.")
            return
        
        outputs = []
        
        if args.all:
            outputs.extend(generator.generate_all_probabilities(args.count, args.model))
        else:
            if args.positive:
                outputs.extend(generator.generate_positive_outputs(args.count, args.model))
            if args.negative:
                outputs.extend(generator.generate_negative_outputs(args.count, args.model))
            if args.exclusion:
                outputs.extend(generator.generate_exclusion_outputs(args.count, args.model))
        
        if outputs:
            print(f"\nGenerated {len(outputs)} output file(s) in '{args.output_dir}' directory")
        else:
            print("No outputs generated. Check your configuration and model names.")
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
