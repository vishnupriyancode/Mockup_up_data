#!/usr/bin/env python3
"""
MockGen CLI - Command Line Interface for Mock Data Generation
Handles probability scenarios (positive, negative, exclusion) with count support and WGS format
"""

import argparse
import sys
from .core import MockGenCore


def main():
    parser = argparse.ArgumentParser(
        description="MockGen CLI - Generate probability scenarios for mock data (WGS format only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Generate 1 positive scenario for Model_1 with WGS format
    python -m src.mockgen.cli --probability --positive --model Model_1 --wgs
    
    # Generate 2 positive scenarios for Model_1 with WGS format
    python -m src.mockgen.cli --probability --positive --model Model_1 --count 2 --wgs
    
    # Generate 1 negative scenario for Model_1 with WGS format
    python -m src.mockgen.cli --probability --negative --model Model_1 --wgs
    
    # Generate 2 negative scenarios for Model_1 with WGS format
    python -m src.mockgen.cli --probability --negative --model Model_1 --count 2 --wgs
    
    # Generate 1 exclusion scenario for Model_1 with WGS format
    python -m src.mockgen.cli --probability --exclusion --model Model_1 --wgs
    
    # Generate 2 exclusion scenarios for Model_1 with WGS format
    python -m src.mockgen.cli --probability --exclusion --model Model_1 --count 2 --wgs
    
    # Generate all available scenario types for Model_1 with WGS format
    python -m src.mockgen.cli --probability --all --model Model_1 --wgs
    
    # Generate all available scenario types with multiple records for Model_1 in WGS format
    python -m src.mockgen.cli --probability --all --model Model_1 --count 5 --wgs
    
    # List available models
    python -m src.mockgen.cli --list
    
Note: All probability scenario generation now requires --wgs flag
        """
    )
    
    # Required arguments (only for scenario generation)
    parser.add_argument("--probability", action="store_true",
                       help="Generate probability scenarios")
    
    # Scenario type (mutually exclusive)
    scenario_group = parser.add_mutually_exclusive_group(required=True)
    scenario_group.add_argument("--positive", action="store_true", help="Generate positive scenarios")
    scenario_group.add_argument("--negative", action="store_true", help="Generate negative scenarios")
    scenario_group.add_argument("--exclusion", action="store_true", help="Generate exclusion scenarios")
    scenario_group.add_argument("--all", action="store_true", help="Generate all available scenario types")
    scenario_group.add_argument("--list", action="store_true", help="List available models")
    
    # Optional arguments
    parser.add_argument("--model", type=str, help="Model name to generate scenarios for")
    parser.add_argument("--count", type=int, default=1, help="Number of JSON files to generate (default: 1)")
    parser.add_argument("--wgs", action="store_true", help="Use WGS format for output (complete template structure)")
    parser.add_argument("--config", type=str, default="user_input.json", help="Path to config file")
    parser.add_argument("--output-dir", type=str, default="generated_outputs", help="Output directory")
    
    args = parser.parse_args()
    
    try:
        core = MockGenCore(args.config, args.output_dir)
        
        if args.list:
            models = core.list_models()
            if not models:
                print("No models found in configuration.")
                return
            
            print("Available Models:")
            for model in sorted(models.keys()):
                print(f"  {model}:")
                for prob_type in ["positive", "negative", "exclusion"]:
                    status = "✓" if models[model].get(prob_type, False) else "✗"
                    print(f"    {prob_type}: {status}")
        else:
            # Check if probability flag is provided for scenario generation
            if not args.probability:
                print("Error: --probability is required when generating scenarios")
                sys.exit(1)
            
            if not args.model:
                print("Error: --model is required when generating scenarios")
                sys.exit(1)
            
            # Check if WGS flag is provided for scenario generation
            if not args.wgs:
                print("Error: --wgs flag is required for all probability scenario generation")
                print("Please add --wgs flag to your command")
                print("Example: python -m src.mockgen.cli --probability --positive --model Model_1 --wgs")
                sys.exit(1)
            
            if args.positive:
                generated_files = core.generate_probability_scenarios("positive", args.model, args.count, args.wgs)
            elif args.negative:
                generated_files = core.generate_probability_scenarios("negative", args.model, args.count, args.wgs)
            elif args.exclusion:
                generated_files = core.generate_probability_scenarios("exclusion", args.model, args.count, args.wgs)
            elif args.all:
                generated_files = core.generate_all_scenarios(args.model, args.count, args.wgs)
            
            # Print generated files
            for filepath in generated_files:
                print(f"Generated: {filepath}")
            
            if args.all:
                print(f"\nGeneration completed successfully! Generated {len(generated_files)} JSON file(s) across all available scenario types in WGS format.")
            else:
                print(f"\nGeneration completed successfully! Generated {len(generated_files)} JSON file(s) in WGS format.")
                
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
