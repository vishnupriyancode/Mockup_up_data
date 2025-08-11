#!/usr/bin/env python3
"""
Demonstration script for the enhanced mock generation system.
This script shows how to use the system to generate JSON outputs from user_input.json
using the master template structure.
"""

import json
from pathlib import Path
from src.mockgen.core import (
    load_master_template,
    load_user_config,
    merge_brd_with_master,
    generate_model_outputs,
    generate_multiple_model_outputs,
    write_enhanced_output_file,
    generate_model_records,
    write_model_output_file
)


def demo_basic_usage():
    """Demonstrate basic usage of the enhanced system."""
    print("=== Enhanced Mock Generation System Demo ===\n")
    
    # Load master template and user input
    try:
        master_data = load_master_template(Path("master.json"))
        print("✓ Loaded master template")
        print(f"  Template fields: {list(master_data.get('user_profile', {}).keys())}")
        
        user_data = load_user_config(Path("user_input.json"))
        print(f"✓ Loaded user input with {len(user_data)} models")
        print(f"  Available models: {list(user_data.keys())}")
        
    except Exception as e:
        print(f"✗ Error loading files: {e}")
        return
    
    # Merge master template with user input
    try:
        merged_config = merge_brd_with_master(master_data, user_data)
        print("✓ Merged master template with user input")
        
        # Show what models are available after merging
        available_models = [key for key in merged_config.keys() if not key.startswith("user_profile")]
        print(f"  Available models after merging: {available_models}")
        
    except Exception as e:
        print(f"✗ Error merging configurations: {e}")
        return
    
    # Generate outputs for specific models
    print("\n--- Generating Outputs ---")
    
    # Example 1: Generate output for Model_1
    if "Model_1" in merged_config:
        try:
            output = generate_model_outputs(merged_config, ["Model_1"])
            print("✓ Generated output for Model_1:")
            print(f"  {json.dumps(output['Model_1'], indent=2)}")
            
            # Save to file
            outfile = write_enhanced_output_file(output, file_tag="_demo_Model_1")
            print(f"  Saved to: {outfile}")
            
        except Exception as e:
            print(f"✗ Error generating Model_1 output: {e}")
    
    # Example 2: Generate output for Model_1_Positive
    if "Model_1_Positive" in merged_config:
        try:
            output = generate_model_outputs(merged_config, ["Model_1_Positive"])
            print("\n✓ Generated output for Model_1_Positive:")
            print(f"  {json.dumps(output['Model_1_Positive'], indent=2)}")
            
            # Save to file
            outfile = write_enhanced_output_file(output, file_tag="_demo_Model_1_Positive")
            print(f"  Saved to: {outfile}")
            
        except Exception as e:
            print(f"✗ Error generating Model_1_Positive output: {e}")
    
    # Example 3: Generate multiple outputs for all models
    try:
        all_outputs = generate_model_outputs(merged_config)
        print("\n✓ Generated outputs for all models:")
        for model, data in all_outputs.items():
            print(f"  {model}: {json.dumps(data, indent=2)}")
        
        # Save to file
        outfile = write_enhanced_output_file(all_outputs, file_tag="_demo_all_models")
        print(f"  Saved all outputs to: {outfile}")
        
    except Exception as e:
        print(f"✗ Error generating all outputs: {e}")


def demo_model_specific_generation():
    """Demonstrate generating outputs for specific models."""
    print("\n=== Model-Specific Generation Demo ===\n")
    
    try:
        user_data = load_user_config(Path("user_input.json"))
        
        # Generate multiple records for Model_1
        if "Model_1" in user_data:
            print("Generating 3 records for Model_1:")
            records = generate_model_records(user_data["Model_1"], count=3)
            
            for i, record in enumerate(records, 1):
                print(f"  Record {i}: {json.dumps(record, indent=2)}")
                
                # Save individual record
                payload = {f"Model_1_record_{i}": record}
                outfile = write_model_output_file(payload, "Model_1", file_tag=f"_demo_record_{i}")
                print(f"    Saved to: {outfile}")
        
        # Generate multiple records for Model_1_Negative
        if "Model_1_Negative" in user_data:
            print("\nGenerating 2 records for Model_1_Negative:")
            records = generate_model_records(user_data["Model_1_Negative"], count=2)
            
            for i, record in enumerate(records, 1):
                print(f"  Record {i}: {json.dumps(record, indent=2)}")
                
                # Save individual record
                payload = {f"Model_1_Negative_record_{i}": record}
                outfile = write_model_output_file(payload, "Model_1_Negative", file_tag=f"_demo_record_{i}")
                print(f"    Saved to: {outfile}")
                
    except Exception as e:
        print(f"✗ Error in model-specific generation: {e}")


def demo_cli_usage():
    """Show how to use the CLI commands."""
    print("\n=== CLI Usage Examples ===\n")
    
    print("1. Generate enhanced output using master template:")
    print("   python -m src.mockgen.cli --enhanced")
    print()
    
    print("2. Generate output for specific model:")
    print("   python -m src.mockgen.cli --enhanced --model Model_1")
    print()
    
    print("3. Generate outputs for multiple specific models:")
    print("   python -m src.mockgen.cli --enhanced --models Model_1 Model_1_Positive")
    print()
    
    print("4. Generate multiple records for a model:")
    print("   python -m src.mockgen.cli --model Model_1 --count 5")
    print()
    
    print("5. Generate split output files:")
    print("   python -m src.mockgen.cli --enhanced --output-format split")
    print()
    
    print("6. Generate multiple batches:")
    print("   python -m src.mockgen.cli --enhanced --output-format multiple --count 3")


if __name__ == "__main__":
    try:
        demo_basic_usage()
        demo_model_specific_generation()
        demo_cli_usage()
        
        print("\n=== Demo Complete ===")
        print("Check the 'mock_outputs' directory for generated files.")
        
    except Exception as e:
        print(f"\n✗ Demo failed with error: {e}")
        print("Please ensure user_input.json and master.json exist and are valid.")
