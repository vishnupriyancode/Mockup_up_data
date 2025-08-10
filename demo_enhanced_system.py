#!/usr/bin/env python3
"""
Demonstration script for the enhanced mock generation system.
This script shows how to use master.json as a default template and 
user_input.json as BRD requirements to generate output JSON for selected models.
"""

import json
from pathlib import Path
from src.mockgen.core import (
    load_master_template,
    load_user_config,
    merge_brd_with_master,
    generate_model_outputs,
    generate_multiple_model_outputs,
    write_enhanced_output_file
)


def main():
    print("=== Enhanced Mock Generation System Demo ===\n")
    
    # Load master template
    print("1. Loading master template from master.json...")
    try:
        master_data = load_master_template(Path("master.json"))
        print(f"   ✓ Loaded master template with {len(master_data)} sections")
        print(f"   ✓ Available sections: {', '.join(master_data.keys())}")
    except Exception as e:
        print(f"   ✗ Error loading master template: {e}")
        return
    
    # Load BRD requirements
    print("\n2. Loading BRD requirements from user_input.json...")
    try:
        brd_data = load_user_config(Path("user_input.json"))
        print(f"   ✓ Loaded BRD requirements with {len(brd_data)} models")
        print(f"   ✓ Available models: {', '.join(brd_data.keys())}")
    except Exception as e:
        print(f"   ✗ Error loading BRD requirements: {e}")
        return
    
    # Merge master template with BRD requirements
    print("\n3. Merging master template with BRD requirements...")
    merged_config = merge_brd_with_master(master_data, brd_data)
    print("   ✓ Successfully merged configurations")
    
    # Show available models for selection
    available_models = [key for key in merged_config.keys() if not key.startswith("user_profile")]
    print(f"\n4. Available models for output generation:")
    for i, model in enumerate(available_models, 1):
        print(f"   {i}. {model}")
    
    # Generate outputs for different scenarios
    print("\n5. Generating outputs for different scenarios...")
    
    # Scenario 1: Single output for all models
    print("\n   Scenario 1: Single output for all models")
    all_models_output = generate_model_outputs(merged_config)
    outfile1 = write_enhanced_output_file(all_models_output, "_all_models")
    print(f"   ✓ Generated: {outfile1}")
    
    # Scenario 2: Output for specific models
    print("\n   Scenario 2: Output for specific models (Model_1, Model_2)")
    specific_models_output = generate_model_outputs(merged_config, ["Model_1", "Model_2"])
    outfile2 = write_enhanced_output_file(specific_models_output, "_specific_models")
    print(f"   ✓ Generated: {outfile2}")
    
    # Scenario 3: Multiple outputs for testing
    print("\n   Scenario 3: Multiple outputs for testing (3 iterations)")
    multiple_outputs = generate_multiple_model_outputs(merged_config, ["Model_1"], 3)
    for i, output in enumerate(multiple_outputs, 1):
        outfile = write_enhanced_output_file(output, f"_test_iteration_{i}")
        print(f"   ✓ Generated: {outfile}")
    
    # Show sample output structure
    print("\n6. Sample output structure:")
    print(json.dumps(all_models_output, indent=2))
    
    print("\n=== Demo completed successfully! ===")
    print("Check the 'mock_outputs' directory for generated files.")


if __name__ == "__main__":
    main()
