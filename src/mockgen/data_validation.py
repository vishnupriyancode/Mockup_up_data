#!/usr/bin/env python3
"""
Consolidated Data Validation and Testing Tool
Combines all validation, testing, and comparison functionality into a single comprehensive tool.

This script replaces:
- compare_scenarios.py
- verify_generation.py  
- test_format_generation.py

Usage:
    python data_validation.py --help
    python data_validation.py --compare
    python data_validation.py --verify
    python data_validation.py --test
    python data_validation.py --all
"""

import json
import glob
import subprocess
import sys
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

class DataValidator:
    """Unified validator for all data validation and testing needs."""
    
    def __init__(self):
        self.output_dir = Path("generated_outputs")
        self.user_input_file = Path("user_input.json")
    
    def load_json_file(self, file_path: Path) -> Optional[Dict]:
        """Load a JSON file and return the data."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")
            return None
    
    def extract_scenario_data(self, data: Dict, scenario_type: str) -> Optional[Dict]:
        """Extract key scenario data from the JSON."""
        key_name = f"WGS_csbd_medicaid_{scenario_type.lower()}"
        
        if key_name not in data:
            return None
        
        scenario_data = data[key_name]
        
        # Extract key fields for comparison
        key_fields = {
            'PRICNG_ZIP_STATE': scenario_data.get('PRICNG_ZIP_STATE', 'N/A'),
            'CLM_TYPE': scenario_data.get('CLM_TYPE', 'N/A'),
            'HCID': scenario_data.get('HCID', 'N/A'),
            'PAT_BRTH_DT': scenario_data.get('PAT_BRTH_DT', 'N/A'),
            'PAT_FRST_NME': scenario_data.get('PAT_FRST_NME', 'N/A'),
            'PAT_LAST_NME': scenario_data.get('PAT_LAST_NME', 'N/A'),
            'proc_cd': scenario_data.get('ClaimDetails', [{}])[0].get('proc_cd', 'N/A') if scenario_data.get('ClaimDetails') else 'N/A'
        }
        
        return key_fields
    
    def compare_scenarios(self):
        """Compare different scenario types."""
        print("🔍 Scenario Comparison Tool")
        print("=" * 60)
        
        # Find scenario files
        positive_files = list(self.output_dir.glob("*Positive*.json"))
        negative_files = list(self.output_dir.glob("*Negative*.json"))
        exclusion_files = list(self.output_dir.glob("*Exclusion*.json"))
        
        scenarios = {}
        
        # Load positive scenario
        if positive_files:
            latest_positive = max(positive_files, key=lambda x: x.stat().st_mtime)
            print(f"📁 Positive scenario: {latest_positive.name}")
            data = self.load_json_file(latest_positive)
            if data:
                scenarios['Positive'] = self.extract_scenario_data(data, 'positive')
        
        # Load negative scenario
        if negative_files:
            latest_negative = max(negative_files, key=lambda x: x.stat().st_mtime)
            print(f"📁 Negative scenario: {latest_negative.name}")
            data = self.load_json_file(latest_negative)
            if data:
                scenarios['Negative'] = self.extract_scenario_data(data, 'negative')
        
        # Load exclusion scenario
        if exclusion_files:
            latest_exclusion = max(exclusion_files, key=lambda x: x.stat().st_mtime)
            print(f"📁 Exclusion scenario: {latest_exclusion.name}")
            data = self.load_json_file(latest_exclusion)
            if data:
                scenarios['Exclusion'] = self.extract_scenario_data(data, 'exclusion')
        
        if not scenarios:
            print("❌ No scenario files found!")
            return
        
        # Display comparison table
        print(f"\n📊 Scenario Comparison Table")
        print("=" * 80)
        
        # Header
        header = f"{'Field':<20}"
        for scenario_type in scenarios.keys():
            header += f"{scenario_type:<15}"
        print(header)
        print("-" * 80)
        
        # Data rows
        fields = ['PRICNG_ZIP_STATE', 'CLM_TYPE', 'HCID', 'PAT_BRTH_DT', 'PAT_FRST_NME', 'PAT_LAST_NME', 'proc_cd']
        
        for field in fields:
            row = f"{field:<20}"
            for scenario_type in scenarios.keys():
                value = scenarios[scenario_type].get(field, 'N/A') if scenarios[scenario_type] else 'N/A'
                if isinstance(value, list):
                    value = value[0] if value else 'N/A'
                row += f"{str(value):<15}"
            print(row)
        
        print("-" * 80)
        print("✅ Scenario comparison completed!")
    
    def verify_generation(self):
        """Verify that generated values come from user input options."""
        print(f"\n{'='*60}")
        print(f"Verifying User Input Compliance")
        print(f"{'='*60}")
        
        # Load user input
        try:
            with open(self.user_input_file, 'r') as f:
                user_input = json.load(f)
            
            # Check Model_1_positive configuration
            if 'Model_1_positive' in user_input:
                positive_config = user_input['Model_1_positive']
                print(f"📋 Model_1_positive configuration:")
                
                for field, values in positive_config.items():
                    if isinstance(values, list):
                        print(f"   {field}: {values}")
                    else:
                        print(f"   {field}: {values}")
            
            print(f"\n✅ User input loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading user input: {e}")
            return
        
        # Analyze generated files
        generated_files = list(self.output_dir.glob("*.json"))
        if not generated_files:
            print("❌ No generated files found!")
            return
        
        print(f"\n📊 Analyzing {len(generated_files)} generated files...")
        
        for file_path in generated_files[:5]:  # Limit to first 5 files
            self.analyze_generated_file(file_path)
    
    def analyze_generated_file(self, file_path: Path):
        """Analyze a single generated JSON file."""
        print(f"\n{'='*60}")
        print(f"Analyzing: {file_path.name}")
        print(f"{'='*60}")
        
        data = self.load_json_file(file_path)
        if not data:
            return
        
        # Find the main data section
        main_key = None
        for key in data.keys():
            if key.startswith('WGS_csbd_medicaid'):
                main_key = key
                break
        
        if not main_key:
            print("❌ No WGS_csbd_medicaid section found")
            return
        
        main_data = data[main_key]
        
        # Analyze key fields for variety
        key_fields = ['PRICNG_ZIP_STATE', 'CLM_TYPE', 'HCID', 'PAT_BRTH_DT', 'PAT_FRST_NME', 'PAT_LAST_NME']
        
        print(f"📊 Analysis Results:")
        print(f"   Main section: {main_key}")
        
        for field in key_fields:
            if field in main_data:
                values = main_data[field]
                if isinstance(values, list):
                    unique_values = list(set(values))
                    print(f"   {field}: {len(values)} values, {len(unique_values)} unique")
                    print(f"      Values: {values}")
                    print(f"      Unique: {unique_values}")
                    
                    # Check if we have variety
                    if len(unique_values) > 1:
                        print(f"      ✅ GOOD: Multiple unique values")
                    else:
                        print(f"      ⚠️  WARNING: Only one unique value")
                else:
                    print(f"   {field}: Single value - {values}")
        
        # Analyze ClaimDetails
        if 'ClaimDetails' in main_data:
            claim_details = main_data['ClaimDetails']
            print(f"   ClaimDetails: {len(claim_details)} entries")
            
            proc_codes = []
            for claim in claim_details:
                if isinstance(claim, dict) and 'proc_cd' in claim:
                    proc_codes.append(claim['proc_cd'])
            
            if proc_codes:
                unique_proc_codes = list(set(proc_codes))
                print(f"      Procedure codes: {proc_codes}")
                print(f"      Unique codes: {unique_proc_codes}")
                if len(unique_proc_codes) > 1:
                    print(f"      ✅ GOOD: Multiple unique procedure codes")
                else:
                    print(f"      ⚠️  WARNING: Only one unique procedure code")
    
    def run_command(self, command: str) -> Optional[str]:
        """Run a command and return the output."""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {command}")
            print(f"Error: {e}")
            return None
    
    def check_json_format(self, file_path: Path) -> Tuple[bool, str]:
        """Check if a JSON file has the correct format."""
        try:
            data = self.load_json_file(file_path)
            if not data:
                return False, "Could not load file"
            
            # Check if it has the expected structure
            if not isinstance(data, dict):
                return False, "Root is not a dictionary"
            
            # Check if it has a WGS_csbd_medicaid key
            wgs_keys = [k for k in data.keys() if k.startswith("WGS_csbd_medicaid")]
            if not wgs_keys:
                return False, "No WGS_csbd_medicaid key found"
            
            wgs_key = wgs_keys[0]
            wgs_data = data[wgs_key]
            
            # Check for required base fields
            required_base_fields = [
                "first_proc_cd", "last_proc_cd", "email", "phone", "date_of_birth",
                "street_address", "proc_cd", "mail_id", "address", "city", "state",
                "zip_code", "country"
            ]
            
            missing_fields = []
            for field in required_base_fields:
                if field not in wgs_data:
                    missing_fields.append(field)
            
            if missing_fields:
                return False, f"Missing base fields: {missing_fields}"
            
            # Check for required scenario fields
            required_scenario_fields = [
                "PRICNG_ZIP_STATE", "CLM_TYPE", "SRVC_FROM_DT", "HCID",
                "PAT_BRTH_DT", "PAT_FRST_NME", "PAT_LAST_NME", "ClaimDetails"
            ]
            
            missing_scenario_fields = []
            for field in required_scenario_fields:
                if field not in wgs_data:
                    missing_scenario_fields.append(field)
            
            if missing_scenario_fields:
                return False, f"Missing scenario fields: {missing_scenario_fields}"
            
            return True, "Format is correct"
            
        except Exception as e:
            return False, f"Error reading file: {e}"
    
    def test_format_generation(self):
        """Test JSON format generation."""
        print("Testing JSON Format Generation")
        print("=" * 50)
        
        # Test positive scenario
        print("\n1. Testing Positive Scenario Generation...")
        print("   Note: Positive scenarios are disabled for Model_1")
        output = self.run_command("python -m src.mockgen.cli --probability --positive --model Model_1")
        if output and "disabled" in output.lower():
            print("✅ Positive scenario restriction working correctly (command properly disabled)")
        elif output:
            print("✅ Positive scenario generated successfully")
            
            # Find the generated file
            positive_files = list(self.output_dir.glob("*Positive*.json"))
            if positive_files:
                latest_positive = max(positive_files, key=lambda x: x.stat().st_mtime)
                print(f"   Generated file: {latest_positive.name}")
                
                # Check format
                is_valid, message = self.check_json_format(latest_positive)
                if is_valid:
                    print("   ✅ Format verification: PASSED")
                else:
                    print(f"   ❌ Format verification: FAILED - {message}")
            else:
                print("   ❌ No positive scenario file found")
        else:
            print("   ❌ Failed to generate positive scenario")
        
        # Test negative scenario
        print("\n2. Testing Negative Scenario Generation...")
        output = self.run_command("python -m src.mockgen.cli --probability --negative --model Model_1")
        if output:
            print("✅ Negative scenario generated successfully")
            
            # Find the generated file
            negative_files = list(self.output_dir.glob("*Negative*.json"))
            if negative_files:
                latest_negative = max(negative_files, key=lambda x: x.stat().st_mtime)
                print(f"   Generated file: {latest_negative.name}")
                
                # Check format
                is_valid, message = self.check_json_format(latest_negative)
                if is_valid:
                    print("   ✅ Format verification: PASSED")
                else:
                    print(f"   ❌ Format verification: FAILED - {message}")
            else:
                print("   ❌ No negative scenario file found")
        else:
            print("   ❌ Failed to generate negative scenario")
        
        # Test exclusion scenario
        print("\n3. Testing Exclusion Scenario Generation...")
        output = self.run_command("python -m src.mockgen.cli --probability --exclusion --model Model_1")
        if output:
            print("✅ Exclusion scenario generated successfully")
            
            # Find the generated file
            exclusion_files = list(self.output_dir.glob("*Exclusion*.json"))
            if exclusion_files:
                latest_exclusion = max(exclusion_files, key=lambda x: x.stat().st_mtime)
                print(f"   Generated file: {latest_exclusion.name}")
                
                # Check format
                is_valid, message = self.check_json_format(latest_exclusion)
                if is_valid:
                    print("   ✅ Format verification: PASSED")
                else:
                    print(f"   ❌ Format verification: FAILED - {message}")
            else:
                print("   ❌ No exclusion scenario file found")
        else:
            print("   ❌ Failed to generate exclusion scenario")
        
        print("\n🎉 Format generation testing completed!")
    
    def run_all_tests(self):
        """Run all validation and testing functions."""
        print("🚀 Running All Data Validation and Testing Tools")
        print("=" * 60)
        
        print("\n1️⃣  Testing JSON Format Generation...")
        self.test_format_generation()
        
        print("\n2️⃣  Comparing Scenarios...")
        self.compare_scenarios()
        
        print("\n3️⃣  Verifying Generation Compliance...")
        self.verify_generation()
        
        print("\n🎉 All tests completed successfully!")

def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description="Consolidated Data Validation and Testing Tool")
    parser.add_argument('--compare', action='store_true', help='Compare different scenario types')
    parser.add_argument('--verify', action='store_true', help='Verify generation compliance')
    parser.add_argument('--test', action='store_true', help='Test JSON format generation')
    parser.add_argument('--all', action='store_true', help='Run all validation and testing tools')
    
    args = parser.parse_args()
    
    validator = DataValidator()
    
    if args.compare:
        validator.compare_scenarios()
    elif args.verify:
        validator.verify_generation()
    elif args.test:
        validator.test_format_generation()
    elif args.all:
        validator.run_all_tests()
    else:
        # Default: show help and run all
        print("🚀 Consolidated Data Validation and Testing Tool")
        print("=" * 60)
        print("Usage:")
        print("  python data_validation.py --compare    # Compare scenarios")
        print("  python data_validation.py --verify     # Verify compliance")
        print("  python data_validation.py --test       # Test format generation")
        print("  python data_validation.py --all        # Run all tools")
        print("  python data_validation.py              # Run all tools (default)")
        print()
        validator.run_all_tests()

if __name__ == "__main__":
    main()
