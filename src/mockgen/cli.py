from __future__ import annotations

import argparse
from pathlib import Path

from .core import (
    ensure_config_file,
    load_user_config,
    build_indexed_records,
    build_output_payload,
    write_output_file,
    load_master_template,
    merge_brd_with_master,
    generate_model_outputs,
    generate_multiple_model_outputs,
    write_enhanced_output_file,
    generate_model_records,
    write_model_output_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate mock output JSONs using inputs from user_input.json and master template. "
            "Supports both legacy Edit_X format and new Model_X format."
        )
    )
    parser.add_argument(
        "--config",
        type=str,
        default="user_input.json",
        help="Path to the input JSON file containing required fields.",
    )
    parser.add_argument(
        "--master",
        type=str,
        default="master.json",
        help="Path to the master template JSON file.",
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help=(
            "Create/overwrite a template input JSON at --config and exit. "
            "Edit it and rerun."
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
            "Generate output for the specified model (e.g., Model_1, Model_1_Positive). "
            "Works with both Edit_X and Model_X formats."
        ),
    )
    parser.add_argument(
        "--enhanced",
        action="store_true",
        help="Use enhanced mode: merge master template with user input requirements.",
    )
    parser.add_argument(
        "--models",
        type=str,
        nargs="+",
        help="Specific models to generate output for (e.g., Model_1 Model_1_Positive).",
    )
    parser.add_argument(
        "--output-format",
        type=str,
        choices=["single", "multiple", "split"],
        default="single",
        help="Output format: single file, multiple records in one file, or split files.",
    )
    parser.add_argument(
        "--legacy",
        action="store_true",
        help="Force legacy mode for backward compatibility with Edit_X format.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config_path = Path(args.config)
    master_path = Path(args.master)

    if args.init:
        ensure_config_file(config_path, overwrite=True)
        print(f"Wrote template to '{config_path}'. Edit it, then rerun.")
        return

    # Enhanced mode: use master template + user input requirements
    if args.enhanced:
        if not master_path.exists():
            raise SystemExit(f"Master template file '{master_path}' not found.")
        
        if not config_path.exists():
            raise SystemExit(f"User input file '{config_path}' not found.")
        
        # Load master template and user input
        master_data = load_master_template(master_path)
        user_data = load_user_config(config_path)
        
        print(f"Loaded master template from '{master_path}'")
        print(f"Loaded user input from '{config_path}' with {len(user_data)} models")
        
        # Merge master template with user input
        merged_config = merge_brd_with_master(master_data, user_data)
        print("Merged master template with user input requirements")
        
        # Determine which models to process
        if args.models:
            selected_models = args.models
            print(f"Selected models: {', '.join(selected_models)}")
        else:
            selected_models = [key for key in merged_config.keys() if not key.startswith("user_profile")]
            print(f"Processing all models: {', '.join(selected_models)}")
        
        # Generate outputs based on format
        if args.output_format == "split":
            # Generate separate files for each model
            for model in selected_models:
                if model in merged_config:
                    output = generate_model_outputs(merged_config, [model])
                    outfile = write_enhanced_output_file(output, file_tag=f"_{model}")
                    print(f"Generated: {outfile}")
        elif args.output_format == "multiple":
            # Generate multiple records in one file
            outputs = generate_multiple_model_outputs(merged_config, selected_models, args.count)
            for i, output in enumerate(outputs, start=1):
                outfile = write_enhanced_output_file(output, file_tag=f"_batch_{i}")
                print(f"Generated: {outfile}")
        else:
            # Single output file
            output = generate_model_outputs(merged_config, selected_models)
            outfile = write_enhanced_output_file(output)
            print(f"Generated: {outfile}")
        
        return

    # Legacy mode or standard mode
    if not config_path.exists():
        ensure_config_file(config_path, overwrite=False)
        raise SystemExit(
            f"Created '{config_path}'. Please fill in the required fields and rerun."
        )

    user_data = load_user_config(config_path)
    print(f"Loaded {len(user_data)} sections: {', '.join(user_data.keys())}")

    # Handle specific model request
    if args.model:
        if args.model not in user_data:
            available = ", ".join(user_data.keys())
            raise SystemExit(
                f"Model '{args.model}' not found in '{config_path}'. Available models: {available}"
            )
        
        # Check if it's a Model_X format (has list values)
        model_data = user_data[args.model]
        if any(isinstance(v, list) for v in model_data.values()):
            # Model_X format - generate multiple records
            records = generate_model_records(model_data, args.count)
            for i, record in enumerate(records, start=1):
                payload = {f"{args.model}_record_{i}": record}
                outfile = write_model_output_file(payload, args.model, file_tag=f"_record_{i}")
                print(f"Generated: {outfile}")
        else:
            # Edit_X format - use legacy indexed records
            records = build_indexed_records(model_data)
            if not records:
                raise SystemExit(
                    f"No records could be built for model '{args.model}'. Ensure all required fields have values."
                )
            for i, record in enumerate(records, start=1):
                payload = {f"{args.model}_output_{i}": record}
                outfile = write_output_file(payload, file_tag=f"_{i}")
                print(f"Generated: {outfile}")
        return

    # Handle multiple outputs
    if args.count > 1 and args.split:
        for i in range(1, args.count + 1):
            # Simple random selection per output file
            if args.models:
                # Use only specified models
                selected_data = {k: v for k, v in user_data.items() if k in args.models}
                payload = build_output_payload(selected_data, count=1)
            else:
                payload = build_output_payload(user_data, count=1)
            outfile = write_output_file(payload, file_tag=f"_{i}")
            print(f"Generated: {outfile}")
    else:
        if args.models:
            # Use only specified models
            selected_data = {k: v for k, v in user_data.items() if k in args.models}
            payload = build_output_payload(selected_data, count=args.count)
        else:
            payload = build_output_payload(user_data, count=args.count)
        outfile = write_output_file(payload)
        print(f"Generated: {outfile}")


if __name__ == "__main__":
    main()


